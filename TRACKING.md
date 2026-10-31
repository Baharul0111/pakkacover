# Pakka Cover — Work Tracker

## Resume here
- Time: 2026-10-31 11:10:23 IST. Step 7: actual-model audit and HTTPS E2E verification.
- Next action: Run full mobile story over the current HTTPS tunnel, inspect audit extraction modes; add actual audio-duration validation and final cost-cap checks.
- Run app: `.venv/bin/python -m uvicorn apps.api.app.main:app --host 0.0.0.0 --port 8000` (once shell exists); final `scripts/run_demo`
- Run tests: `.venv/bin/python -m pytest -q`
- Background processes: API/tunnel current URL https://east-guru-howard-larry.trycloudflare.com; PIDs .run/api.pid and .run/tunnel.pid; Postgres55432. Stop: scripts/run_demo --stop.
- Done and verified / half-done: Rebuilt and restarted latest code; 99 Python tests passed again; tracked files and built JS pass secret leakage scan; verification: G1/G2/G0/G6/G7/payment checks green. Current tunnel ready; no real golden media present.. The next action above identifies unfinished work.
- Open problems and decisions: Audit now uses model extraction first; must verify live path rather than relying solely on generated-label fallback.
- Paytm mode: simulated.

## Implementation log
- 2026-10-31 10:34:15 IST | Step 1: dependencies and policy sources | Initialized Git, secret exclusions, hackathon deviations, and resumable checkpoint helper | Tests: Git initialized; .env excluded | Commit: `7ccc385`
- 2026-10-31 10:35:29 IST | Step 1: policy provenance | Installed locked Python 3.12 dependencies and downloaded all original policy source PDFs | Tests: Five PDFs parsed successfully; source SHA256 hashes recorded | Commit: `7599ad8`
- 2026-10-31 10:39:16 IST | Step 1: engine and rules written; verification next | Authored Plans A/B/C with page-linked quotes, Decimal/date engine, scenario ranking, Promise Card facts, method, and G1/G2 tests | Tests: Hand calculation: B ₹644000, C ₹300000, A ₹100000; automated tests pending | Commit: `935cc08`
- 2026-10-31 10:39:57 IST | Step 1 COMPLETE; Step 2 starting | Step 1 complete: A/B/C engine, 29 verified clause references, method and runnable FastAPI shell | Tests: G1/G2: 14 passed; FastAPI shell and B>C>A API smoke passed | Commit: `756f69c`
- 2026-10-31 10:42:14 IST | Step 2: encrypted database and provider discovery | Added encrypted SQLAlchemy schema, Alembic migration, owner-scoped repository and secret bootstrap | Tests: Secret-safe model discovery verified all requested OpenAI/Anthropic IDs; supplied DB failed DNS resolution | Commit: `e4123b7`
- 2026-10-31 10:45:36 IST | Step 2: backend and interview written | Migrated local encrypted Postgres; implemented per-purpose consent, member attestation, explicit FSM, Sarvam and bounded model gateway, confirmation, saved sessions and kill switches | Tests: Database migration succeeded; all requested model IDs verified; 0 golden media files currently | Commit: `04c3d72`
- 2026-10-31 10:47:12 IST | Step 2: G0/G7 passed; live provider smoke in progress | G0 ownership/consent/encryption/idempotency, 50 adversarial numeric cases and interview confirmation gates pass; correction keeps versioned lines | Tests: 59 backend/numeric tests passed; provider smoke running independently | Commit: `332f1b2`
- 2026-10-31 10:48:02 IST | Step 3 starting: medicine photo pipeline | Step 2 complete: backend, consent, Sunita FSM, voice, encryption, owner scoping, numeric guard and explicit confirmation | Tests: 59 automated tests passed; live Haiku extraction and Sarvam STT/TTS passed (evals/results/provider-smoke.json) | Commit: `c8e14d6`
- 2026-10-31 10:48:35 IST | Step 3: two-reader pipeline written; verification next | Implemented in-memory photo sanitation in spawned worker, 60-generic lookup, dual readers, agreement/disagreement and explicit buyer choice | Tests: Photo tests written; tests and live reader smoke next | Commit: `84de70a`
- 2026-10-31 10:50:03 IST | Step 4 starting: phone UI, review, ranking and Promise Card | Step 3 photo pipeline and guard tests complete; 60 hand-seeded generics and explicit condition choice | Tests: 66 backend/numeric/medicine tests passed; live synthetic vision result in evals/results/vision-smoke.json when finished | Commit: `290b328`
- 2026-10-31 10:54:45 IST | Step 4: React UI written; build/browser checks next | Built bilingual mobile-first React UI, recording/photo controls, review cards, scenario sliders, clause modal, Promise Card and upcoming dates | Tests: TypeScript/Vite build in progress; backend engine/ownership tests already passed | Commit: `1be7a58`
- 2026-10-31 10:56:25 IST | Step 4: mobile browser verification | React build succeeded; added automated mobile Sunita browser journey and card/backend checks | Tests: TypeScript/Vite build passed; card and backend regressions running; browser check next | Commit: `98adf31`
- 2026-10-31 10:57:48 IST | Step 5 starting: generated policies and Day-12 audit | Step 4 UI builds; bilingual review/ranking/card APIs and 68 regressions pass; mobile browser check running | Tests: TypeScript/Vite passed; 68 backend/card/numeric/medicine checks passed; initial browser launch raced server startup, readiness wait added | Commit: `2a39ed7`
- 2026-10-31 10:58:24 IST | Step 5: audit implementation written | Generated clean plus 3 planted sample PDFs in memory; added quote-verified extraction, deterministic comparison and encrypted audit persistence | Tests: G6 tests written; sample labels use deterministic verified parsing; arbitrary uploads use Haiku sections and one Sonnet retry | Commit: `4335043`
- 2026-10-31 10:59:17 IST | Step 6 starting: payment adapter | Step 5 audit written; sample G6 and quote-grounding tests executed; mobile test synchronization fixed | Tests: See G6 test output; Step 4 build and 68 regressions passed; mobile browser test initially clicked old checkbox before member screen, test now waits for heading | Commit: `e2dd64d`
- 2026-10-31 11:01:20 IST | Step 6: staging and simulation adapters written | Implemented signed staging init, signature-verified callback and S2S status, exact ₹1 amount checks, simulated adapter and mode on /ready | Tests: Dummy-key roundtrip, tamper, host allowlist, mocked staging and simulated-route tests written; execution next | Commit: `a997934`
- 2026-10-31 11:02:59 IST | Step 7 starting: one-command launcher and tunnel | Payment adapters complete, staging cryptography covered with dummy key, simulation stays explicit; entering launcher/E2E stage | Tests: Full pytest suite and Vite build just run; check previous output. Temporary Step 4 QA API stopped cleanly. | Commit: `fb8940b`
- 2026-10-31 11:04:07 IST | Step 7: launcher written; tunnel validation next | Created background API/quick-tunnel launcher, local Postgres recovery, migrations/build, PUBLIC_URL update, --status/--stop/--retunnel | Tests: 99 Python tests and production web build passed before launcher work | Commit: `a940d47`
- 2026-10-31 11:05:31 IST | Step 7: HTTPS preview running; full browser synchronization fixes | One-command launcher started HTTPS demo and background API/tunnel; full browser test reached simulated payment after photo, confirmation, ranking and Promise Card | Tests: 99 Python tests and Vite build passed. Browser script needed an explicit wait for order panel after async order creation; fixed test race. | Commit: `291537e`
- 2026-10-31 11:08:22 IST | Step 7: full local browser pass; requirement hardening | Full local mobile story passed in 10 seconds with live dual-reader photo, per-line confirmation, ranking, simulation and 4 audit variants; audit now attempts actual Haiku before sample fallback | Tests: Local browser passed with 0 runtime errors; 99 Python tests previously passed; updated code requires regression run | Commit: `b99098c`
- 2026-10-31 11:10:23 IST | Step 7: actual-model audit and HTTPS E2E verification | Rebuilt and restarted latest code; 99 Python tests passed again; tracked files and built JS pass secret leakage scan | Tests: G1/G2/G0/G6/G7/payment checks green. Current tunnel ready; no real golden media present. | Commit: `c7c6a17`

Updated: 2026-10-31 (Asia/Kolkata)

## Working agreement
- Record each small completed piece of work here, with a short note on what remains.
- Current scope: understand the existing files; wait for the user's implementation prompt.

## Progress
1. **Workspace inventory — complete.** Found `goal.md`, `architecture.md`, and `setup.md`. No application code or Git repository is present. No applicable `AGENTS.md` was found.
   - Remaining at this step: read the three documents and record their purpose, key requirements, and any open questions.
2. **Product goals and architecture overview — reviewed.** Read all 26 requirements and the completion criteria in `goal.md`, plus the opening architecture requirements and system diagrams. The journey is consent → family interview/medicine photo → individual fact confirmation → sample-plan payout comparison → Promise Card → optional save/test payment → day-12 policy audit. AI reads and phrases; deterministic code calculates money, dates, rankings, and differences. Plans are educational samples, with human-advisor access throughout.
   - Remaining at this step: review detailed components, data/security, build gates, and operator setup.
3. **Core design and delivery plan — reviewed.** Planned stack: React/Vite/TypeScript PWA, FastAPI/Python, server-only Postgres in Supabase Mumbai, Cloudflare Pages, Render, and Neon standby. The architecture specifies an explicit interview state machine, clause-linked deterministic rules, two medicine readers with human disambiguation, quote-verified policy extraction, a bounded media subprocess, and separate demo/pilot runtime profiles. Phase 1 covers the Sunita demo; phase 2 gates real users on operational, privacy, and security checks. Reviewed setup prerequisites for identity, Paytm, Google sign-in, and the private repository.
   - Remaining at this step: review model/fallback policy, data model, retention and operations, evaluation gates, and the rest of setup. The source schedule assumes a 30 Oct 2026 freeze (already past on this review date); do not silently reuse those deadlines for implementation.
4. **Data, safety, evaluation, and operations — reviewed.** Health fields use MultiFernet encryption; credentials are separate from data roots; owner-scoped repositories enforce access; `erase_subject()` centralizes deletion. Consent has four purposes, raw media is transient, backups have seven generations, and restore must replay erasures. The design includes staff TOTP, kill switches, cost caps, monitoring/auto-pause, and G0–G14 evaluation gates. Provider/model identifiers and other assumptions marked unverified must be checked when implementation begins; this review does not validate live vendor or legal claims.
   - Remaining at this step: finish operator setup and supporting architecture sections; consolidate unresolved document differences and the implementation handoff.
5. **Setup and supporting sections — reviewed; initial orientation complete.** Reviewed all setup items, the empty `.env` template, golden-set requirements (20 voice clips, 15 photos, labels), secret routing/escrow, manual checks, runbooks, rejected alternatives, and the source register. Setup completion is unknown: unchecked instructions are not evidence that accounts or credentials exist. No application code, credentials, external accounts, or deployment settings were created or changed. The three original documents are unchanged.
   - Remaining: wait for the user's next prompt; keep this tracker updated after each small completed part.
6. **Final workspace check — complete.** Confirmed the tracker was saved. A local `.env` appeared during the review; its contents were not opened, printed, or validated.
   - Remaining: use credentials only as needed for the forthcoming authorized task, without exposing values.

## File map
- `goal.md`: product behavior, 26 requirements, and completion criteria.
- `architecture.md`: approved technical design, planned repository, build sequence, evaluation gates, operations, risks, and source references. Changes to that design must be reflected there when authorized.
- `setup.md`: owner-provided accounts, choices, test media, manual checks, and secret-handling instructions.
- `TRACKING.md`: ongoing work log and short remaining-work notes.
- `.env`: local configuration/secrets file; contents not inspected during this review.

## Items to reconcile when implementation is requested
- **Schedule/environment:** the documents assume a Windows/Claude Code build starting 29 Oct and freezing 30 Oct 2026. This workspace is macOS and the review date is 31 Oct 2026. Adapt commands and agree the current delivery target from the next prompt.
- **Saved-record retention:** `goal.md` says deletion after the free-look period without P4; `architecture.md` specifies free-look last day + 30 days, or 60 days after last activity when no D0 exists. Resolve before implementing retention or notices.
- **Spend guarantees:** architecture calls for hard console budgets, while setup notes OpenAI's project budget is soft by default. Verify provider behavior and implement app-side caps without assuming a console hard stop.
- **Unavailable Paytm keys:** setup describes simulated TEST checkout; an architecture operator note mentions a recorded staging run. Preserve honest labels and settle the fallback against actual access.
- **Live assumptions:** model availability/IDs, prices, free-tier limits, policy clauses, data licenses, and legal applicability require verification during the relevant build work; this orientation only reviewed the supplied text.

## Current status
Requested file review is complete. Implementation has not started. Next action: receive the user's task prompt.
