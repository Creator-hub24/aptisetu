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
  YEAR: new Date().getFullYear()
};
