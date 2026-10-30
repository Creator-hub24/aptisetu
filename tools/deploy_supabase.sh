#!/usr/bin/env bash
# Deploy the AptiSetu backend to Supabase: migrations, Edge Functions and function secrets.
# Reads everything from environment variables and NEVER prints a secret value.
#
# Required:  SUPABASE_ACCESS_TOKEN   personal access token (supabase.com > Account > Access Tokens)
#            SUPABASE_PROJECT_REF    project ref (the "abcd..." in https://abcd....supabase.co)
#            SUPABASE_DB_PASSWORD    database password (needed by `supabase db push`)
# Optional (payments; test keys first). Export either NAME or APTISETU_NAME; they are stored as APTISETU_NAME
# because the Supabase project is shared with another app and must not overwrite its secrets:
#            RAZORPAY_KEY_ID  RAZORPAY_KEY_SECRET  RAZORPAY_WEBHOOK_SECRET
#            PASS_PRICE_PAISE (e.g. 29900)  PASS_VALID_DAYS (365)  PAYMENTS_ENABLED (false)
#            ALLOW_LIVE_PAYMENTS (false; live keys are refused until this is true)  PASS_PLAN_ID  SITE_ORIGINS
# Usage:     bash tools/deploy_supabase.sh            (then: python3 tools/set_supabase_config.py)
set -euo pipefail
cd "$(dirname "$0")/.."
: "${SUPABASE_ACCESS_TOKEN:?set SUPABASE_ACCESS_TOKEN}" "${SUPABASE_PROJECT_REF:?set SUPABASE_PROJECT_REF}" "${SUPABASE_DB_PASSWORD:?set SUPABASE_DB_PASSWORD}"
export SUPABASE_ACCESS_TOKEN
SB="npx --yes supabase@2"
set +x
echo "== link project $SUPABASE_PROJECT_REF"
$SB link --project-ref "$SUPABASE_PROJECT_REF" --password "$SUPABASE_DB_PASSWORD" >/dev/null
echo "== apply migrations"
$SB db push --password "$SUPABASE_DB_PASSWORD" --include-all
echo "== function secrets (names only)"
tmp="$(mktemp)"; chmod 600 "$tmp"; trap 'rm -f "$tmp"' EXIT
for k in RAZORPAY_KEY_ID RAZORPAY_KEY_SECRET RAZORPAY_WEBHOOK_SECRET PASS_PRICE_PAISE PASS_VALID_DAYS PASS_PLAN_ID PAYMENTS_ENABLED ALLOW_LIVE_PAYMENTS SITE_ORIGINS; do
  p="APTISETU_$k"; v="${!p:-${!k:-}}"
  if [ -n "$v" ]; then printf '%s=%s\n' "$p" "$v" >>"$tmp"; echo "  set $p"; fi
done
grep -q '^APTISETU_PAYMENTS_ENABLED=' "$tmp" || { echo "APTISETU_PAYMENTS_ENABLED=false" >>"$tmp"; echo "  set APTISETU_PAYMENTS_ENABLED=false (default)"; }
$SB secrets set --project-ref "$SUPABASE_PROJECT_REF" --env-file "$tmp" >/dev/null
echo "== deploy Edge Functions"
for f in create-order verify-payment; do $SB functions deploy "$f" --project-ref "$SUPABASE_PROJECT_REF"; done
$SB functions deploy razorpay-webhook --project-ref "$SUPABASE_PROJECT_REF" --no-verify-jwt
echo "== auth settings: ADD the AptiSetu redirect URLs (shared project: keep every existing URL and the existing site URL)"
cur="$(curl -fsS "https://api.supabase.com/v1/projects/$SUPABASE_PROJECT_REF/config/auth" -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN")"
body="$(printf '%s' "$cur" | python3 -c '
import json, sys
c = json.load(sys.stdin)
have = [u.strip() for u in (c.get("uri_allow_list") or "").split(",") if u.strip()]
add = [u for u in ("https://aptisetu.com/**", "https://www.aptisetu.com/**") if u not in have]
out = {"uri_allow_list": ",".join(have + add)}
if not (c.get("site_url") or "").strip() or c.get("site_url") == "http://localhost:3000": out["site_url"] = "https://aptisetu.com"
print(json.dumps(out)); print("  redirect URLs: %d kept, %d added%s" % (len(have), len(add), ", site URL set" if "site_url" in out else ", site URL unchanged"), file=sys.stderr)
')"
curl -fsS -X PATCH "https://api.supabase.com/v1/projects/$SUPABASE_PROJECT_REF/config/auth" \
  -H "Authorization: Bearer $SUPABASE_ACCESS_TOKEN" -H "Content-Type: application/json" -d "$body" >/dev/null && echo "  ok"
echo "Done. Webhook URL for Razorpay Dashboard > Webhooks (events: payment.captured, order.paid, payment.failed, refund.processed):"
echo "  https://$SUPABASE_PROJECT_REF.supabase.co/functions/v1/razorpay-webhook"
echo "Next: python3 tools/set_supabase_config.py && python3 tools/build_pages.py"
