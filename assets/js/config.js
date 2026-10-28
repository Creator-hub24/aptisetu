// ===== Site configuration: the single source of truth =====
// tools/build_pages.py reads the quoted values below at build time, so after
// editing them run: python3 tools/build_pages.py
// Keep each value on one line as KEY: "value". Leave a value "" to hide that feature.
window.SITE = {
  BRAND: "AptiSetu",
  TAGLINE: "Aptitude se Selection tak ka Setu",
  SITE_URL: "https://aptisetu.com/",                         // must end with "/"; change for a custom domain
  EMAIL: "edumaths360@gmail.com",                               // public contact address
  GOOGLE_FORM_URL: "",
  GOATCOUNTER: "aptisetu",                                              // GoatCounter site code only (e.g. "aptisetu"); "" = no analytics script                                          // optional feedback form link; "" hides the button
  // Login (Supabase email magic link). Paste your project's values from Supabase > Project Settings > API.
  // While these are placeholders, login shows "Login not configured yet". The anon key is public by design; RLS protects data.
  SUPABASE_URL: "YOUR_SUPABASE_URL",                            // e.g. https://abcdefgh.supabase.co
  SUPABASE_ANON_KEY: "YOUR_SUPABASE_ANON_KEY",
  // Google login button on login.html: "on" only after enabling Google in Supabase > Authentication > Providers.
  GOOGLE_LOGIN: "off",
  // AptiSetu Pass (Razorpay). Keep "off" until the price is confirmed. While off, no payment UI or Razorpay script
  // is loaded and every feature stays free. The real price is charged by the server (PASS_PRICE_PAISE secret);
  // PASS_PRICE here is only the label shown on the button and must match it.
  PAYMENTS_ENABLED: "off",
  PASS_PRICE: "",
  YEAR: new Date().getFullYear()
};
