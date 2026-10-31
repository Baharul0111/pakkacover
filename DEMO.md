# PakkaCover — stage demo

Demo only. No insurance is sold. Use fictional stage details.

## Start

From this folder:

```sh
scripts/run_demo
```

The command starts local PostgreSQL if needed, applies Alembic, checks any newly supplied golden media, builds React, starts FastAPI, opens a Cloudflare quick tunnel, prints the phone HTTPS URL, and saves it in `PUBLIC_URL` in local `.env`. It also schedules the requested read-only 14:30 IST payment-key check and keeps the Mac awake while the API runs. Leave the Mac powered and online.

```sh
scripts/run_demo --status
scripts/run_demo --stop
```

The demo passphrase is the `DEMO_LOGIN_PASSPHRASE` value in local `.env`. Open that file privately on the Mac; do not project it or paste it into chat. Enter the passphrase on the phone only when saving the Promise Card.

## Under-five-minute stage script

1. Open the printed HTTPS URL in Chrome or Safari. Choose English or Hindi. “PakkaCover helps a family understand disclosure and sample cover before a claim.”
2. Accept disclosure consent; leave dates and audit as separate choices. Add **Sunita, self, female, age 52** and confirm agreement. No insurer receives anything.
3. Answer height **158 cm**, weight **64 kg**. Hold the microphone and say **“Mujhe BP hai, doctor ne bataya hai.”** Release to send. If the network is poor, tap **BP / hypertension** instead. Select **2019**, **Yes**, and **No** for heart/kidney involvement.
4. At the medicine question, photograph the printed back of a **Telma 40** strip. Both readers propose a printed name/strength. Check and choose it; choose **BP / hypertension** as the reason, then **Once daily**. If glare or the network prevents reading, type the printed name/strength, or tap the explicit **Telma 40 mg** fallback. The app never guesses the condition.
5. For the fictional stage case, select **None** for hospitalisation and tests, **No** for tobacco/alcohol/family history. Real users would disclose actual details; this is only a fixture.
6. Confirm **each line separately** using **Sahi hai**. “Galat / Badlo takes us back, and any changed fact must be confirmed again.” There is no confirm-all.
7. Open sample plans. With start **31 Oct 2026**, the independent example totals are **B ₹6,44,000 > C ₹3,00,000 > A ₹1,00,000**. Tap a total, a claim amount and its clause; show the published method and optional scenario sliders. These are examples, not forecasts, premiums or a recommendation.
8. Choose **Plan B — Care Supreme + Instant Cover**. The Promise Card shows BP cover from **30 Nov 2026**, and all other computed dates. Tap a date to show its clause. Dates assume continuous coverage, insurer acceptance and the selected paid add-on. The initial receipt date is 31 Oct; change it to demonstrate that only receipt-based deadlines move.
9. Save using the private demo passphrase. Create the **₹1 TEST** order. In **simulated** mode, show **“SIMULATED — Paytm test keys pending”** and complete the simulation; no payment happened. If staging keys have been added and the server restarted, use only the staging checkout and official test instruments. A callback alone never marks an order paid: the server verifies Paytm’s status, signature, order identity and ₹1 amount.
10. Open Day-12 audit. Choose **Instant Cover add-on missing** and run the check. Show both source statements and the free-look deadline. The other planted examples are missing declared condition and wrong member age/birth details. The **clean** example has no flags. “AI reads with source quotes; code compares. A flag means check, not ‘your policy is wrong’.”
11. Tap **Talk to a person / Pilot callback within 24 h**. A real, owner-scoped callback request is stored for the demo operator; the app honestly states no licensed partner is connected in this hackathon build.

All sample-policy bytes are generated/processed in memory. Uploaded photos, voice and PDFs are not stored. Field extraction, declaration data and audit results are encrypted in Postgres. Each browser has its own session, including after passphrase save; the passphrase does not create a shared family account.

## Bad network: switch off voice

From a second terminal on the Mac:

```sh
.venv/bin/python scripts/switches.py voice_in=off voice_out=off
```

Continue with chips and typing. To restore:

```sh
.venv/bin/python scripts/switches.py voice_in=on voice_out=on
```

Other available switches: `vision_read`, `llm_phrasing`, `audit_llm`, `payments`, `vendor:openai`, `vendor:anthropic`, `vendor:sarvam`, `new_sessions`. The command loads the passphrase privately. `vision_read=off` leads to manual medicine entry. If an uploaded policy cannot be read, expand the manual field form and copy the actual policy values; the deterministic comparison still runs.

## Tunnel recovery

```sh
scripts/run_demo --retunnel
```

This preserves the API/database and prints a **new** HTTPS URL; update the phone link. If the API died:

```sh
scripts/run_demo
```

A new quick-tunnel hostname is a new browser origin, so start a fresh demo there. Avoid restarting during a stage journey. The stable local preview is `http://127.0.0.1:8000`, but a phone requires the HTTPS tunnel for mic/camera permissions.

## Payment mode and 14:30 check

**Frozen payment mode: simulated.** Staging keys were absent at freeze; no real Paytm transaction is claimed. The staging adapter is implemented and covered by dummy-key/signed-response tests. The adapter is selected on server startup: both staging keys present → staging; either absent → simulated. The production Paytm host is rejected before networking.

Check current state without exposing keys:

```sh
.venv/bin/python scripts/payment_preflight.py
scripts/run_demo --status
```

The launcher runs a read-only check at **14:30 IST, 31 Oct 2026**. Its result is `.run/payment-preflight-1430.json`, PID `.run/preflight.pid`. It never rotates the tunnel or restarts a live stage session. If it reports `restart_needed: true`, `scripts/run_demo --restart-api` activates newly supplied staging keys while preserving the current tunnel URL. Reload the phone page to refresh its payment-mode banner. No code change is needed.

## Verification and fallback recording

```sh
.venv/bin/python -m pytest -q
.venv/bin/python scripts/check_quotes.py
npm run build --prefix apps/web
.venv/bin/python scripts/eval_golden.py --if-new
.venv/bin/python scripts/browser_test.py <printed-https-url> --full
```

The owner’s 20 clips and 15 labelled photos are optional until supplied under `evals/golden/`. A fresh media fingerprint triggers Sarvam v4/v3-codemix A/B; the winner is pinned in `models.yaml`. Photo tests check the supplied label CSV; blurred/handwritten inputs must not produce a candidate. No transcripts or media outputs are written into evaluation reports.

Final browser rehearsals use fictional details and a **synthetic printed test label**, not a real medicine-strip photo. The live-speech rehearsal uses a synthetic spoken answer and the actual voice endpoint. These checks do not replace testing the physical phone’s microphone/camera or the owner’s real golden media. Runtime results are in `evals/results/`; screenshots and the silent browser fallback video are in ignored `.run/`.

The stable fallback recording path is `.run/sunita-fallback.webm` after the recorded rehearsal. Open it with your normal video player. It shows the browser demo with synthetic test inputs; narrate the stage script over it if needed.

## Scope

This is the local hackathon demo, **not a pilot**. Retention jobs, export/delete screens, production infrastructure, real identity, staff TOTP, backups, licensed-partner integration and a real insurance sale are intentionally out of scope. The remote database URL that failed DNS is preserved privately as `DATABASE_URL_REMOTE`; the active database is local PostgreSQL on loopback port 55432. All deviations are in `HACKATHON.md`.

## Verified freeze results

- Python suite: **121 passed** (including G0, G1, G2, G6, G7, payment signatures, media limits and cost caps).
- Source fidelity: **44 clause references verified** against pinned downloaded PDFs.
- Three consecutive full HTTPS mobile-browser rehearsals: **39 s, 44 s, 40 s**, no browser runtime errors; each included accepted live speech, live dual-reader synthetic photo, per-line confirmation, correct Instant Cover clause tap, Promise Card and simulated payment.
- Each rehearsal ran all four audits through real model extraction: all **11 fields** quote verified, planted flags **1 / 1 / 1**, clean flags **0**.
- Owner golden files at freeze: **0 clips, 0 photos**; synthetic checks are clearly separate from real-media/hardware testing.
- Machine-readable evidence: `evals/results/freeze-verification.json`. Frozen source tag: `demo-1` once final bookkeeping is committed.
