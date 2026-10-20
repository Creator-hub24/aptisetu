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
  GOATCOUNTER: "",                                              // GoatCounter site code only (e.g. "aptisetu"); "" = no analytics script                                          // optional feedback form link; "" hides the button
  // Login (Supabase email magic link). Paste your project's values from Supabase > Project Settings > API.
  // While these are placeholders, login shows "Login not configured yet". The anon key is public by design; RLS protects data.
  SUPABASE_URL: "YOUR_SUPABASE_URL",                            // e.g. https://abcdefgh.supabase.co
  SUPABASE_ANON_KEY: "YOUR_SUPABASE_ANON_KEY",
  YEAR: new Date().getFullYear()
};
