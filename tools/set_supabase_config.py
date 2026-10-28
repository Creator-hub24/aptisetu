"""Write the project's public URL and anon key into assets/js/config.js (both are public by design; RLS protects data).
Fetches the anon key with the management API using SUPABASE_ACCESS_TOKEN; prints neither the token nor the key."""
import json, os, re, urllib.request
ref, tok = os.environ["SUPABASE_PROJECT_REF"], os.environ["SUPABASE_ACCESS_TOKEN"]
assert re.fullmatch(r"[a-z0-9]{20}", ref), "SUPABASE_PROJECT_REF looks wrong"
req = urllib.request.Request(f"https://api.supabase.com/v1/projects/{ref}/api-keys", headers={"Authorization": f"Bearer {tok}"})
keys = json.load(urllib.request.urlopen(req))
anon = next(k["api_key"] for k in keys if k.get("name") == "anon")
p = "assets/js/config.js"; s = open(p, encoding="utf8").read()
s = re.sub(r'SUPABASE_URL: "[^"]*"', f'SUPABASE_URL: "https://{ref}.supabase.co"', s)
s = re.sub(r'SUPABASE_ANON_KEY: "[^"]*"', f'SUPABASE_ANON_KEY: "{anon}"', s)
open(p, "w", encoding="utf8").write(s)
print("config.js updated with the project URL and anon key. Rebuild: python3 tools/build_pages.py")
