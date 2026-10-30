// POST /functions/v1/create-order  (logged-in user)  ->  { order_id, amount, currency, key_id, plan }
// The price is set on the server (APTISETU_PASS_PRICE_PAISE); the browser cannot choose it.
import { admin, cors, currentUser, json, paymentsEnabled, plan, razorpayKeys } from "../_shared/razorpay.ts";

Deno.serve(async req => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(req) });
  if (req.method !== "POST") return json(req, { error: "method not allowed" }, 405);
  try {
    if (!paymentsEnabled()) return json(req, { error: "AptiSetu Pass is not on sale yet" }, 503);
    const user = await currentUser(req);
    if (!user) return json(req, { error: "login required" }, 401);
    const p = plan(), { keyId, keySecret, live } = razorpayKeys(), db = admin();
    // service-role client: auth.uid() is empty here, so check this user's paid, unexpired pass directly
    const { data: active, error: pe } = await db.from("passes").select("id").eq("user_id", user.id).eq("status", "paid")
      .or(`valid_until.is.null,valid_until.gt.${new Date().toISOString()}`).limit(1);
    if (pe) throw pe;
    if (active && active.length) return json(req, { error: "you already have an active AptiSetu Pass" }, 409);
    const r = await fetch("https://api.razorpay.com/v1/orders", {
      method: "POST",
      headers: { "Authorization": "Basic " + btoa(`${keyId}:${keySecret}`), "Content-Type": "application/json" },
      body: JSON.stringify({ amount: p.amount, currency: "INR", receipt: `ap-${user.id.slice(0, 8)}-${Date.now()}`, notes: { user_id: user.id, plan: p.id } }),
    });
    const order = await r.json();
    if (!r.ok || !order.id) return json(req, { error: "could not create the order, please try again" }, 502);
    const { error } = await db.from("passes").insert({ user_id: user.id, plan: p.id, amount_paise: p.amount, currency: "INR", razorpay_order_id: order.id, status: "created", live_mode: live });
    if (error) throw error;
    return json(req, { order_id: order.id, amount: p.amount, currency: "INR", key_id: keyId, plan: p.id, test_mode: !live });
  } catch (e) {
    console.error("create-order failed:", (e as Error).message);
    return json(req, { error: "server error" }, 500);
  }
});
