// Shared helpers for the AptiSetu Pass Edge Functions. Secrets come only from Deno.env (set with `supabase secrets set`);
// nothing here logs or returns a secret. Our secret names start with APTISETU_ because the Supabase project is shared
// with another app (SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY are Supabase built-ins and keep their names).
import { createClient, type SupabaseClient } from "npm:@supabase/supabase-js@2.118.0";

const enc = new TextEncoder();

export async function hmacHex(secret: string, message: string): Promise<string> {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = new Uint8Array(await crypto.subtle.sign("HMAC", key, enc.encode(message)));
  return Array.from(sig, b => b.toString(16).padStart(2, "0")).join("");
}

// constant-time comparison of two hex strings
export function safeEqual(a: string, b: string): boolean {
  if (typeof a !== "string" || typeof b !== "string" || a.length !== b.length) return false;
  let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

// Checkout signature: HMAC_SHA256(order_id + "|" + payment_id, key_secret)
export async function verifyCheckoutSignature(orderId: string, paymentId: string, signature: string, keySecret: string) {
  if (!orderId || !paymentId || !signature || !keySecret) return false;
  return safeEqual(await hmacHex(keySecret, `${orderId}|${paymentId}`), String(signature).toLowerCase());
}

// Webhook signature: HMAC_SHA256(raw request body, webhook_secret), sent in X-Razorpay-Signature
export async function verifyWebhookSignature(rawBody: string, signature: string | null, webhookSecret: string) {
  if (!signature || !webhookSecret) return false;
  return safeEqual(await hmacHex(webhookSecret, rawBody), signature.toLowerCase());
}

export function env(name: string, fallback?: string): string {
  const v = Deno.env.get(name) ?? fallback;
  if (v === undefined || v === "") throw new Error(`server is missing ${name}`);   // the name only, never the value
  return v;
}

export function plan() {
  return {
    id: Deno.env.get("APTISETU_PASS_PLAN_ID") || "pass-cat-2027",
    amount: parseInt(env("APTISETU_PASS_PRICE_PAISE"), 10),           // e.g. 29900 for Rs 299 (price test: Rs 199-499)
    days: parseInt(Deno.env.get("APTISETU_PASS_VALID_DAYS") || "365", 10),
  };
}

export function razorpayKeys() {
  const keyId = env("APTISETU_RAZORPAY_KEY_ID"), keySecret = env("APTISETU_RAZORPAY_KEY_SECRET");
  const live = keyId.startsWith("rzp_live_");
  if (live && Deno.env.get("APTISETU_ALLOW_LIVE_PAYMENTS") !== "true") throw new Error("live Razorpay keys are blocked until APTISETU_ALLOW_LIVE_PAYMENTS=true");
  return { keyId, keySecret, live };
}

export function admin(): SupabaseClient {
  return createClient(env("SUPABASE_URL"), env("SUPABASE_SERVICE_ROLE_KEY"), { auth: { persistSession: false } });
}

export async function currentUser(req: Request) {
  const auth = req.headers.get("Authorization") || "";
  if (!auth.startsWith("Bearer ")) return null;
  const c = createClient(env("SUPABASE_URL"), env("SUPABASE_ANON_KEY"), { global: { headers: { Authorization: auth } }, auth: { persistSession: false } });
  const { data, error } = await c.auth.getUser();
  return error ? null : data.user;
}

const ORIGINS = () => (Deno.env.get("APTISETU_SITE_ORIGINS") || "https://aptisetu.com,https://www.aptisetu.com").split(",").map(s => s.trim());
export function cors(req: Request): Record<string, string> {
  const o = req.headers.get("Origin") || "";
  return {
    "Access-Control-Allow-Origin": ORIGINS().includes(o) ? o : ORIGINS()[0],
    "Access-Control-Allow-Headers": "authorization, content-type, apikey, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}
export function json(req: Request, body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors(req), "Content-Type": "application/json" } });
}
export const paymentsEnabled = () => Deno.env.get("APTISETU_PAYMENTS_ENABLED") === "true";

// Mark a pass paid exactly once (used by verify-payment and the webhook; safe to call twice).
export async function markPaid(db: SupabaseClient, orderId: string, paymentId: string) {
  const { data: row, error } = await db.from("passes").select("id,status,amount_paise,user_id").eq("razorpay_order_id", orderId).maybeSingle();
  if (error) throw error;
  if (!row) return { ok: false, reason: "unknown order" };
  if (row.status === "paid" || row.status === "refunded") return { ok: true, already: true, user_id: row.user_id };
  const until = new Date(Date.now() + plan().days * 86400000).toISOString();
  const { error: e2 } = await db.from("passes").update({ status: "paid", razorpay_payment_id: paymentId, valid_until: until, updated_at: new Date().toISOString() })
    .eq("id", row.id).neq("status", "paid");
  if (e2) throw e2;
  return { ok: true, user_id: row.user_id, valid_until: until };
}
