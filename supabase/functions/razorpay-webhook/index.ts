// POST /functions/v1/razorpay-webhook  (called by Razorpay; deploy with --no-verify-jwt)
// Verifies X-Razorpay-Signature over the raw body with RAZORPAY_WEBHOOK_SECRET. Handles payment.captured, order.paid,
// payment.failed and refund.processed. Idempotent: replays do nothing.
import { admin, env, markPaid, verifyWebhookSignature } from "../_shared/razorpay.ts";

Deno.serve(async req => {
  if (req.method !== "POST") return new Response("method not allowed", { status: 405 });
  const raw = await req.text();
  try {
    if (!(await verifyWebhookSignature(raw, req.headers.get("X-Razorpay-Signature"), env("RAZORPAY_WEBHOOK_SECRET"))))
      return new Response("bad signature", { status: 401 });
    const ev = JSON.parse(raw), db = admin();
    const pay = ev?.payload?.payment?.entity, ref = ev?.payload?.refund?.entity;
    if ((ev.event === "payment.captured" || ev.event === "order.paid") && pay?.order_id) {
      const { data: row } = await db.from("passes").select("amount_paise").eq("razorpay_order_id", pay.order_id).maybeSingle();
      if (row && row.amount_paise === pay.amount) await markPaid(db, pay.order_id, pay.id);
    } else if (ev.event === "payment.failed" && pay?.order_id) {
      await db.from("passes").update({ status: "failed", updated_at: new Date().toISOString() }).eq("razorpay_order_id", pay.order_id).eq("status", "created");
    } else if (ev.event === "refund.processed" && ref?.payment_id) {
      await db.from("passes").update({ status: "refunded", valid_until: new Date().toISOString(), updated_at: new Date().toISOString() }).eq("razorpay_payment_id", ref.payment_id);
    }
    return new Response("ok");
  } catch (e) {
    console.error("webhook failed:", (e as Error).message);
    return new Response("error", { status: 500 });
  }
});
