# PakkaCover — stage demo

Live URL: **https://camping-leon-rider-performer.trycloudflare.com**

Hackathon demo · Sample public policy terms · Education only. No insurance is sold.

## Start and private login

```sh
scripts/run_demo
scripts/run_demo --status
scripts/run_demo --stop
```

The start command recovers local PostgreSQL, applies migrations, checks new golden media, builds React, starts FastAPI and a same-origin Cloudflare HTTPS tunnel, and prints the phone URL. It writes the URL to `PUBLIC_URL` in local `.env`. Keep the Mac powered and online. A full restart makes a new tunnel URL; `--restart-api` preserves the existing tunnel.

The private save passphrase is `DEMO_LOGIN_PASSPHRASE` in local `.env`. Open that file privately on the Mac and enter the value on the phone when saving the Promise Card. Never project the file or paste its contents into chat. Local `.env` credentials take precedence over unrelated keys inherited from the agent shell.

## Under-five-minute Sunita script

1. Open the HTTPS link. Choose Hindi or English. Accept disclosure consent; dates and policy audit remain separate purpose choices.
2. Talk starts at **1 / 12: Who is this cover for?** Say or tap **Mother**, then tap **I agree** for member attestation. There is no separate member form.
3. Say **Sunita**, **52 years**, **Female**, **5 foot 2**, **68 kilo**, one answer per question. Height is converted in code to **157 cm**; weight is **68 kg**. The live form fills as each answer arrives. On a phone, open **Your form** at the bottom.
4. Say **BP / hypertension**, **2019**, **Yes** for doctor diagnosis, **No** for heart/kidney involvement, **Yes** for current treatment. Use chips or the keyboard if needed. For a natural voice example, say **“Mujhe BP hai, doctor ne bataya hai.”**
5. At Medicine, photograph the printed back of a **Telma 40** strip. Check the two readings and choose the printed **Telmisartan 40 mg** candidate. Blur means ask, never guess. Then answer **1 tablet**, **Once daily**, **BP / hypertension** as the purpose. The medicine alone never decides a condition.
6. For this fictional fixture, choose **None** for hospital stays and tests, then **No** for tobacco, alcohol and family history. Under-18 interviews request guardian attestation and skip tobacco/alcohol.
7. “That's all. Let's check your answers.” Confirm **each of the 20 cards individually** with **Sahi hai**. Galat/Badlo returns to the question; changed values need a new confirmation. No confirm-all exists.
8. Compare sample payouts: **B ₹6,44,000 > C ₹3,00,000 > A ₹1,00,000**. These are totals across independent examples, not premiums, forecasts or recommendations. Show **For you**, tap a clause, and point out the common **0–36 month** BP timeline. Care's optional Smart Select is not selected, so the app does not claim a 20% co-pay.
9. **Make my Promise Card** works on all three plans. Choose **Plan B — Care Supreme + Instant Cover** for the stage. BP starts **30 Nov 2026**. The example policy/receipt date is **31 Oct 2026**; free-look action is by **29 Nov 2026**, and Day 12 is **11 Nov 2026**. Dates come from code and verified clauses. The paid Instant Cover add-on and insurer acceptance are assumptions. Tap **Add calendar** for an `.ics` file with generic, private reminder titles.
10. Tap **Pay ₹1 with Paytm**, save with the private passphrase, choose **UPI / Wallet / Card**, then continue and pay. Show Processing, the green tick, **Payment successful via Paytm**, ₹1, order ID and time. The grey **Demo** label stays visible. Show the slide-in banner and open the notification bell. The owner-scoped database order is marked paid in **demo** mode, with **verified=false**.
11. Continue to **Policy check**. Run **Instant Cover add-on missing**. Show the two statements, **Ask insurer to fix**, the free-look action date, and **Talk to advisor**. The other fixtures plant a missing declared condition and wrong age/birth details. The **clean** fixture has no flags. AI extracts source-quoted fields; code compares them. A flag asks for a check, not a verdict.
12. Tap **Advisor — Pilot callback within 24 h**. This stores a callback request for the demo operator; no licensed advisor partner is connected. The app states that clearly.
13. Open the small menu → **Reset demo**. It removes the old journey, token, orders and notifications and returns an already-consented browser to **empty Q1**. It retains purpose-consent choices and app-wide spend counters; member/guardian attestation must be given again.

## Payment wording and mode

**Paytm keys were not available; this is a clearly labelled demo payment. No real money is moved.**

Owner-requested stage line describing the intended future gateway integration:

> We couldn't get Paytm PG test keys today, so this is a demo of the payment screen; with keys this button opens the real Paytm payment sheet

The current build has **only the demo adapter**. Adding keys does not activate a gateway. Real checkout would require a later integration. There are no Paytm-host calls, S2S/provider-verification claims, or scheduled key checks. `/api/ready` always reports payment mode `demo`.

## Voice switches and recovery

```sh
.venv/bin/python scripts/switches.py voice_in=off voice_out=off
.venv/bin/python scripts/switches.py voice_in=on voice_out=on
```

Continue with chips and typing when voice is off. Every question has a replay speaker. A short tap starts recording; tap again to send, or hold and release. The recorder stops after 25 seconds. Reset cancels an active recording instead of submitting it to the old session.

Other operator switches: `vision_read`, `llm_phrasing`, `audit_llm`, `payments`, `vendor:openai`, `vendor:anthropic`, `vendor:sarvam`, `new_sessions`. The switch helper privately loads the passphrase.

- **Poor medicine photo:** retake it or type the printed name/strength. If only one reader is available, the UI says so and requires the buyer to check and choose. No two-reader agreement is claimed.
- **Policy reader unavailable:** generated samples have a quote-verified deterministic fallback. Uploaded policies offer buyer-checked manual field entry. Raw PDF bytes are discarded.
- **A changed/unanswered fact at Compare:** the app returns to the exact Check card or missing Talk question. It preserves the confirmation gate and clears stale notices.
- **Tunnel failure:** `scripts/run_demo --retunnel` preserves the API/database and prints a new phone URL.
- **API failure:** `scripts/run_demo --restart-api` preserves the tunnel. Reload the browser after readiness returns.
- **Fresh start:** Menu → Reset demo. A new tunnel hostname is a new browser origin, so start fresh there.

The stable laptop URL is `http://127.0.0.1:8000`; the phone needs HTTPS for mic/camera access. Voice/photos/PDFs stay in memory and are not stored. Health fields are encrypted in owner-scoped PostgreSQL rows. The passphrase does not merge different browsers into one family.

## Verification and recordings

```sh
.venv/bin/python -m pytest -q
.venv/bin/python scripts/check_quotes.py
npm --prefix apps/web run build
.venv/bin/python scripts/eval_golden.py --if-new
.venv/bin/python scripts/browser_test.py https://camping-leon-rider-performer.trycloudflare.com --full --live-voice --runs=3 --record
```

Current verification and freeze status are in `TRACKING.md` and `evals/results/freeze-verification.json`. The original `demo-1` and verified `demo-2` tags are immutable; the finishing-step revision uses `demo-3`. The old 11:51 results remain historical evidence, not revised-build verification.

Browser rehearsals use a **synthetic printed medicine label** and synthetic spoken answer through the real provider APIs. They check phone/laptop layouts and browser behavior, and do not certify a physical phone's microphone/camera or real medicine-strip photos. No owner golden media has been supplied so far; `saaras:v4` remains pinned until clips arrive and trigger the v4/v3-codemix A/B.

The live Q1-through-measurements probe is `.venv/bin/python scripts/check_talk_voice.py`; it uses synthetic Hindi answers and records only pass/fail metadata.

The refreshed fallback recording is `.run/sunita-fallback.webm`; `.run/sunita-fallback.mp4` is the normal-player copy. Both are ignored local artifacts, without passphrase keystroke disclosure. Narrate the script over the silent browser recording if needed.

## Hosting and scope

GitHub: https://github.com/Baharul0111/pakkacover

The authorized Vercel attempt was skipped under the owner's explicit rule because the supplied remote Supabase hostname failed DNS outside the sandbox. No localhost database credentials were uploaded. Local PostgreSQL on port **55432** and the HTTPS tunnel remain the stage demo. The remote configuration stays private as `DATABASE_URL_REMOTE`.

This hackathon build defers real identity, retention/export/delete screens, production operations, backups, staff TOTP and licensed-partner integration. The required rules engine, quote checks, numeric guard, individual confirmation, ownership, consent, encryption, app-side caps and visible Demo labels remain in place.

## Historical verified demo-2 build

**FROZEN: 2026-10-31T13:11:47.318947+05:30 — demo-2.** Original demo-1 is unchanged.

- 146 Python tests; 44 source-aligned clauses; G0/G1/G2/G6/G7 pass.
- Three consecutive HTTPS runs with Reset: 49 s /42 s /44 s, no browser errors.
- Each run: live accepted voice, two agreeing medicine readers, four live 11-field quote-verified audits with flags1/1/1/0, paid demo order and persisted notification.
- All three plans and exact corrected-line recovery pass; seven real Hindi identity/measurement voice probes pass.
- Both WebM and MP4 local fallback recordings refreshed. Stage API restarted cleanly while preserving the URL.
- No owner media or physical-phone hardware validation was supplied; synthetic/provider and responsive-browser evidence is identified above.

## Finish the process

After a policy check, scroll to **Finish review**. With a flagged policy, tick **I have reviewed these differences. Follow-up is still needed**, then finish. The completion screen saves the review and keeps the flagged difference and deadline visible. With the clean PDF, finish directly to show the completed review without a follow-up warning.

The summary includes the saved Promise Card and actual demo-payment status. It persists after reload. Use **View my Promise Card**, **Review differences & next steps**, or the menu's **Reset demo**. Finishing a review does not accept an insurance contract or mark unresolved differences fixed.

The earlier Cloudflare hostname retired around13:55 IST. The live link at the top is its replacement; a new hostname needs a fresh browser demo session. On the Mac, `http://127.0.0.1:8000` also serves the updated app.
