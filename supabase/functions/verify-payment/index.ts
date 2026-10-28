// POST /functions/v1/verify-payment  { razorpay_order_id, razorpay_payment_id, razorpay_signature }
// Checks the checkout HMAC signature, confirms the payment with Razorpay (status + amount), then activates the Pass.
import { admin, cors, currentUser, json, markPaid, razorpayKeys, verifyCheckoutSignature } from "../_shared/razorpay.ts";

Deno.serve(async req => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(req) });
  if (req.method !== "POST") return json(req, { error: "method not allowed" }, 405);
  try {
    const user = await currentUser(req);
    if (!user) return json(req, { error: "login required" }, 401);
    const b = await req.json().catch(() => ({}));
    const orderId = String(b.razorpay_order_id || ""), paymentId = String(b.razorpay_payment_id || ""), sig = String(b.razorpay_signature || "");
    const { keyId, keySecret } = razorpayKeys(), db = admin();
    if (!(await verifyCheckoutSignature(orderId, paymentId, sig, keySecret))) return json(req, { error: "payment signature did not match" }, 400);
    const { data: row } = await db.from("passes").select("user_id,amount_paise").eq("razorpay_order_id", orderId).maybeSingle();
    if (!row || row.user_id !== user.id) return json(req, { error: "order not found" }, 404);
    const r = await fetch(`https://api.razorpay.com/v1/payments/${encodeURIComponent(paymentId)}`, { headers: { "Authorization": "Basic " + btoa(`${keyId}:${keySecret}`) } });
    const pay = await r.json();
    if (!r.ok || pay.order_id !== orderId || pay.amount !== row.amount_paise || !["captured", "authorized"].includes(pay.status))
      return json(req, { error: "payment not confirmed yet; if money was deducted it will be activated or refunded automatically" }, 409);
    const res = await markPaid(db, orderId, paymentId);
    return json(req, { ok: res.ok, valid_until: res.valid_until ?? null });
  } catch (e) {
    console.error("verify-payment failed:", (e as Error).message);
    return json(req, { error: "server error" }, 500);
  }
});
