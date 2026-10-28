// deno test supabase/functions/_shared/razorpay_test.ts  (no network, no real secrets)
import { hmacHex, safeEqual, verifyCheckoutSignature, verifyWebhookSignature } from "./razorpay.ts";
const eq = (a: unknown, b: unknown) => { if (a !== b) throw new Error(`${a} !== ${b}`); };
Deno.test("HMAC-SHA256 matches RFC 4231 test case 2", async () => {
  eq(await hmacHex("Jefe", "what do ya want for nothing?"), "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843");
});
Deno.test("checkout signature: order_id|payment_id", async () => {
  const s = "test_secret_not_real", sig = await hmacHex(s, "order_ABC|pay_XYZ");
  eq(await verifyCheckoutSignature("order_ABC", "pay_XYZ", sig, s), true);
  eq(await verifyCheckoutSignature("order_ABC", "pay_OTHER", sig, s), false);
  eq(await verifyCheckoutSignature("order_ABC", "pay_XYZ", sig, "wrong"), false);
  eq(await verifyCheckoutSignature("order_ABC", "pay_XYZ", "", s), false);
});
Deno.test("webhook signature over the raw body", async () => {
  const s = "whsec_not_real", body = '{"event":"payment.captured"}', sig = await hmacHex(s, body);
  eq(await verifyWebhookSignature(body, sig, s), true);
  eq(await verifyWebhookSignature(body + " ", sig, s), false);
  eq(await verifyWebhookSignature(body, null, s), false);
  eq(safeEqual("ab", "abc"), false);
});
