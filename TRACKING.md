# Pakka Cover — Work Tracker

## Resume here
- Time: 2026-10-31 12:13:18 IST. New agent taking over; validating uncommitted UI rewrite and backend preparation.
- Next action: Run `npm --prefix apps/web run build` and `.venv/bin/python -m pytest -q`; inspect App.tsx classes and implement missing responsive CSS. Keep and fix the rewrite if viable.
- Run app: `scripts/run_demo`; status `scripts/run_demo --status`; stop `scripts/run_demo --stop`.
- Run tests: `.venv/bin/python -m pytest -q`; `.venv/bin/python scripts/check_quotes.py`; `npm --prefix apps/web run build`.
- Background processes: inherited API/tunnel/caffeinate may be running; local PostgreSQL on 55432. Inspect `.run/` PID files and `scripts/run_demo --status`; stop managed services with `scripts/run_demo --stop`.
- Done and verified: demo-1 is immutable safe fallback (11:51, 121 tests, 44 clauses, 3 HTTPS runs). Payment/reset/calendar/notifications committed and pushed through 3b935a4. Do not repeat verified engine work.
- Half-done: App.tsx rewritten and UNVERIFIED; new CSS probably missing. Uncommitted config.py/db.py/routes.py and tests/test_backend.py add serverless environment/DB changes and identity review. Validate before committing those files.
- Open problems/decisions: preserve demo-1 forever, freeze revised build as demo-2 (latest user instruction supersedes AGENTS tag replacement). Supabase DNS/connection must be rechecked; skip hosted deployment if unavailable. No UI additions after 14:00; fallback by 14:10 if broken.
- Paytm mode: `demo` only. No real gateway calls, pending credentials or S2S claims.

## Implementation log
- 2026-10-31 12:13:18 IST | Takeover checkpoint | Recorded true unverified UI/backend state; preserved demo-1; next action is build/tests/CSS. Tests: takeover inspection only; baseline verification next. Commit: `3b935a4` (inherited checkpoint).
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
- 2026-10-31 11:12:15 IST | Step 7: final fallback and media checks | Added measured audio duration in worker, worker allocation cap, handwriting/unit guards and manual audit entry fallback | Tests: New tests cover actual audio bounds, concurrent cost-cap reservations and manual audit comparison; execution next | Commit: `62c32df`
- 2026-10-31 11:13:15 IST | Step 7: correcting final hardening failures | HTTPS full story passed in 38s with real Haiku audit; final tests exposed Mac resource-limit hard ceiling, broken ffprobe binary and one manual-form JSX parenthesis | Tests: Last run: 103 passed, 2 failed (audio tool and worker initialization); web build failed on new manual form. All three causes addressed in source; verification next. | Commit: `4c3f593`
- 2026-10-31 11:15:32 IST | Step 7: Mac media compatibility fix | PyAV audio-duration test passes; corrected manual form compiles. Mac rejects resource-limit setters, so worker now uses parent RSS watchdog with timeout/respawn fallback | Tests: 19/20 focused checks passed; remaining initializer failure addressed by watchdog. Need updated tests after psutil install. | Commit: `bd4a20e`
- 2026-10-31 11:17:26 IST | Step 7: final test fixes pass; operator tools added | Mac media compatibility fixed; operator voice/AI switches and read-only 14:30 payment preflight scripts added; calculation modal now explains actual arithmetic | Tests: Full suite/build just completed after media fix; check output. Prior HTTPS E2E passed with model-verified audit fields. | Commit: `82bde45`
- 2026-10-31 11:20:14 IST | Step 7: ready for final production-build rehearsals | Added golden-media A/B/no-fabrication runner (no media supplied), startup pin reload, timed 14:30 read-only key check, and fallback-video/live-voice browser rehearsal support | Tests: 105 tests passed before these small operator/test additions; golden runner reports 0 clips/0 photos and pins v4. Final checks next. | Commit: `e04766e`
- 2026-10-31 11:22:57 IST | Step 7: final HTTPS rehearsals about to run | 105 tests and latest production build passed; DEMO.md stage/operator guide drafted; audio/media/cap/manual fallbacks verified | Tests: Golden runner confirms no supplied files; actual-model HTTPS audit previously verified all 11 fields. Final three runs pending. | Commit: `b15bc83`
- 2026-10-31 11:24:53 IST | Step 7: live speech route diagnosis | Final build passed; real HTTPS voice rehearsal exposed a recognition/extraction-path failure before freezing. Original docs unchanged, secret leakage/log checks passed. | Tests: 105 automated tests pass; live voice rehearsal failed accepted-slot assertion. Need diagnosis and final rehearsals. | Commit: `56fa41e`
- 2026-10-31 11:27:44 IST | Step 7: voice-path correctness fix | Isolated failure to slot extraction/quote handling rather than audio/STT; added BP language aliases and a source-anchored explicit-answer fallback, preserving strict quote and numeric guards | Tests: Decoder and STT probe passed; new tests cover Hindi/English BP, negations, bad-quote fallback and amber marking of all voice-derived facts | Commit: `c552a16`
- 2026-10-31 11:29:54 IST | Step 7: live voice probe passed; final rehearsal restart | Live decoded/STT/extracted synthetic BP answer now passes with correct condition. Added explicit negation tests and fixed a unit-test DB event-loop leak (production API unaffected). | Tests: Live probe: measured audio 2.48s, STT and condition preserved; total 9.32s including generating speech. 69/70 focused tests passed before correcting test isolation; full suite next. | Commit: `6f1058a`
- 2026-10-31 11:31:41 IST | Step 7: final rehearsal 1/3 passed | First final live-voice/photo HTTPS rehearsal passed in 44s with 0 browser errors; fallback video saved at .run/sunita-fallback.webm | Tests: 120 Python tests passed; real voice slot preserved; all 4 audit variants passed through live model extraction/comparison in the full browser flow | Commit: `23778c3`
- 2026-10-31 11:33:55 IST | Step 7: final clause trace correction | Second HTTPS rehearsal passed; final review found a tied-date trace choosing the initial-wait clause instead of Instant Cover. Corrected trace priority without changing any date or payout. | Tests: Added regression for Plan B BP citation and a browser assertion that its date opens the 31st-day add-on quote. Final rehearsal counter restarts after this source change. | Commit: `74b2041`
- 2026-10-31 11:37:17 IST | Step 7: final source fidelity and real-network fallback check | Fixed Instant Cover citation tie and completed five cited exclusion examples per plan. Rehearsal now records voice success/fallback instead of treating a deliberate network fallback as a crash. | Tests: 121 Python tests passed before exclusion/data updates. Live route has succeeded previously; transient provider/deadline fallback must also complete the journey. Final tests/rehearsals pending. | Commit: `bdaa247`
- 2026-10-31 11:40:19 IST | Step 7: final revised-build rehearsal 1/3 passed | Revised build passed full HTTPS story in 39s: voice accepted, live dual readers, correct Instant Cover citation, all 3 model-verified mismatches and clean PDF; fallback video refreshed | Tests: 121 Python tests passed; G2 validates 44 clauses; all 4 live audits verified 11 fields each, with flags 1/1/1/0; browser errors 0 | Commit: `47bbda8`
- 2026-10-31 11:42:54 IST | Step 7: final revised-build rehearsal 2/3 passed | Second revised-build full HTTPS story passed in 44s with accepted live voice, dual-reader photo, correct clause tap and audit flags 1/1/1/0 | Tests: 121 Python tests passed; 44 clause references verified; both final rehearsals have 0 browser errors and all audit fields model/quote verified | Commit: `d2e868f`
- 2026-10-31 11:46:21 IST | Freeze: all feature and rehearsal gates passed | All 3 final HTTPS rehearsals passed (39/44/40s); DEMO.md complete; freeze evidence saved; historical tracker text clearly marked | Tests: 121 tests passed; 44 source clauses verified; live audit fields all 11 verified per PDF with flags1/1/1/0; recorded video exists | Commit: `b5a271e`
- 2026-10-31 11:51:16 IST | FROZEN — demo complete | All seven build steps complete; fresh stage instance ready; DEMO.md and WebM/MP4 fallback recordings saved; original documents unchanged | Tests: Final run: 121 passed; G2 44 source clauses verified; 3 consecutive full HTTPS runs 39/44/40s with accepted live speech, correct clause taps, 3/3 audit mismatches and 0 clean false flags; secret scan passed | Commit: `fa851a2`

## Hosting add-on — GitHub now, Vercel by 14:15
- GitHub: authenticated Baharul0111, https://github.com/Baharul0111/pakkacover, main. Secret/media audit then push now; push each subsequent completed checkpoint.
- Vercel: authenticated CLI, project pakkacover. Same React/FastAPI app, relative /api routes, bounded inline media on serverless, Supabase transaction pooler6543 + NullPool. Deployment around13:45; stop trying at14:15 if unsuccessful.
- 14:30 freeze unchanged. Current live fallback: https://slide-stage-seller-republican.trycloudflare.com. Production URL pending deployment.

## Takeover schedule — latest user instruction

| Time (IST) | Work |
| --- | --- |
| 12:13–12:30 | Verify inherited rewrite/backend; implement missing CSS; build and regressions |
| 12:30–13:30 | Complete and browser-check responsive Sunita UI, medicine, per-line Check, compare, Promise, payment, audit |
| 13:30–14:00 | Vercel attempt, at most 30 minutes; skip if remote DB fails; retain tunnel |
| 14:00–14:20 | Three full HTTPS runs with Reset demo; docs and recovery |
| 14:20–14:30 | Final gates, secret audit, push, immutable demo-1 plus new demo-2; FROZEN |

## Revised schedule — user change of plan at 11:55 IST

The earlier 11:51 freeze is superseded. Deadline is **14:30 IST**; owner testing/recording is 14:30–15:30. Preserve the verified engine, quotes, confirmation and numeric guard.

| Time (IST) | Work |
| --- | --- |
| 11:55–12:15 | Demo-only payment, paid orders/notifications, reset |
| 12:15–13:05 | Talk, live form, Check UI |
| 13:05–13:45 | Compare/Promise/calendar/Policy check UI |
| 13:45–14:15 | Responsive polish and 3 runs with Reset demo |
| 14:15–14:30 | Final required gates, DEMO.md, FROZEN, demo-1 |

Payment decision: `demo` only; remove real staging code and scheduled credential checks. UI: #00BAF2 / #002E6E, white/grey cards, big icons/buttons, minimal copy. Full current requirements are in AGENTS.md.
- 2026-10-31 11:57:00 IST | Revised build: plan recorded; demo payment/reset/notifications first | Read the entire change of plan; updated AGENTS.md and TRACKING.md with the 14:30 deadline, revised schedule, demo-only payment and full new UI requirements | Tests: Previous frozen baseline: 121 tests, 44 verified clauses, 3 HTTPS runs. Baseline verification next. | Commit: `9ed31d6`
- 2026-10-31 11:59:36 IST | Hosting add-on: GitHub audit and first push now | Recorded GitHub/Vercel add-on in AGENTS.md and TRACKING.md; strengthened private-media/dump/env exclusions while allowing labels.csv; added README | Tests: Prior baseline test run pending result; secret/media push audit next | Commit: `60c06b3`
- 2026-10-31 12:01:13 IST | GitHub: secret audit passed; pushing main now | Verified all required .gitignore paths and label CSV exception; scanned tracked files plus entire history with no detected secrets or private media; authenticated GitHub repo exists and is empty | Tests: 121 baseline tests passed; full-history secret audit PASS; ignore/media checks PASS | Commit: `d80e3c7`
- 2026-10-31 12:02:42 IST | GitHub initial push complete; demo payment implementation | Pushed existing commits to Baharul0111/pakkacover main after full-history secret/media audit; enabled audited automatic pushes after every checkpoint | Tests: 121 baseline tests passed; GitHub push verified by CLI; ignore and staged/history scans passed | Commit: `e5570f2`
- 2026-10-31 12:07:12 IST | Demo payment backend complete; Vercel preparation | Replaced all payment networking with demo-only paid orders; added idempotent owner-scoped notifications, Reset demo retaining spend, privacy-safe calendar export and unified /api routes; stopped obsolete key watcher | Tests: 113 baseline/new tests passed; calendar health-bearing UID caught by test and fixed; 3 focused payment/reset/calendar tests and production web build now pass | Commit: `6b08921`

## Original orientation notes

Historical review notes below are preserved as requested. The current state is always in **Resume here** above.

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
