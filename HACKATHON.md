# Hackathon deviations

Authority: AGENTS.md, 31 Oct 2026. Original goal.md, architecture.md and setup.md remain unchanged.

- Demo only, final freeze by 14:30 IST today; replaces all earlier deadlines. Preserve demo-1 as the safe fallback; the revised freeze is demo-2.
- macOS local FastAPI serves React; Cloudflare quick tunnel supplies same-origin HTTPS. GitHub/Vercel deployment is now authorized by the latest add-on; local HTTPS remains the fallback. No real users.
- One Postgres database/role with Alembic, owner-scoped queries and Fernet health fields.
- Passphrase demo login only. No Google/Mini App login, retention/export/delete screens, staff/admin console, backups, standby, email, or cloud CI/monitoring.
- Sunita interview complete; other branches may use typed/manual fallbacks.
- Sarvam demo cap ₹150/day and minimum remaining balance ₹20, overriding architecture profile caps. App caps do not assume provider budgets are hard stops.
- Payment adapter is demo only. No payment provider hosts are contacted and no gateway verification is claimed.
- Provider IDs verified at startup; unavailable requested IDs must be recorded honestly and a supported ID or deterministic fallback used.

## Source corrections found during Step 1
- The architecture's HDFC wording URL serves an older UIN (HDFHLIP23123V022223) with 15-day free look and eight-year moratorium. It must not support the requested 2024/25 UIN. Added the official `optima-secure-revision-pw.pdf` source for HDFHLIP25041V062425.
- Care Supreme's 20% outside-listed-hospital copay belongs to optional Smart Select (3.2.1); it is not automatically applied to every base policy. The demo does not select Smart Select.
- Initial Python PDF requests hit a local certificate-chain issue; system curl successfully downloaded all five original URLs. No user-supplied PDFs are currently needed.

- HDFC official wording host returned HTTP 406. Its public mirror now serves the current UIN **HDFHLIP26058V082526** (69 pages), rather than the architecture UIN. Plan A explicitly uses this actual UIN and pinned file; its source quotes confirm 36-month PED, 24-month specific wait, 60-month moratorium and 30-day free look. The obsolete 34-page PDF is retained only as provenance, never used by rules. No PDF upload is needed from the owner.
- Example consumables reflect actual wording: HDFC Protect (default retained) and Tata B12 cover specified items; Care without Claim Shield deducts the assumed 8%. Published method states these assumptions and that claims are independent.

## Step 2 runtime decisions
- Supplied DATABASE_URL hostname failed DNS resolution. Preserved its value only in local `.env` as DATABASE_URL_REMOTE and bootstrapped local Homebrew PostgreSQL 16 on loopback port 55432, data in ignored `.run/postgres`. DATABASE_URL now targets that local database. Single demo role/schema and Alembic retained.
- No golden audio clips or strip photos present at Step 2 start; pin saaras:v4 until supplied sets appear.
- Startup discovery confirmed requested OpenAI and Anthropic model IDs are available on the provided keys.

## Demo-specific implementation details
- Household UI covers one explicitly attested member for the Sunita stage path; remaining family branches are outside today's demo.
- The 60 generic names and demo brand/condition hints are hand-seeded. Conditions are always buyer-selected, not clinically inferred. Broader licensed datasets are deferred.
- All audits attempt Haiku section extraction and one Sonnet retry on failed quote/value verification. Generated fixtures additionally have a quote-verified deterministic label parser as the network/model fallback, explicitly recorded in extraction_mode. The comparison is always code. G6 unit fixtures exercise deterministic parsing; live and browser gates exercise the actual model path.
- Promise Card includes five clause-linked exclusion examples with conditional/medical exceptions labelled; the full source wording remains authoritative for all other exclusions and exceptions.

## macOS media verification
- System ffprobe aborts on this Mac, so bundled PyAV decodes microphone bytes in the isolated worker and measures actual duration without disk files.
- This macOS environment rejects RLIMIT_DATA/RLIMIT_AS changes even below the reported limit. A parent RSS watchdog checks the worker every 50 ms against measured baseline + 150 MB (200 MB minimum), kills/respawns on breach, and retains wall-clock deadlines and input/pixel limits. Unsupported kernel caps no longer prevent startup.

## UI and local demo implementation choices
- React/TypeScript/Vite uses plain responsive CSS and Lucide icons, with explicit English/Hindi phrase maps rather than Tailwind/shadcn and react-i18next. It remains a built React app served by FastAPI at one origin.
- Anthropic/OpenAI calls use native structured-output JSON schemas over bounded httpx REST calls instead of SDK parse helpers; returned model IDs and conservative spend reservations are stored without health content.
- TTS calls Sarvam's streaming endpoint, then returns the completed in-memory WAV for straightforward browser playback; stale read-aloud responses are discarded when the question changes.
- Passphrase Save authorizes a private per-browser journey instead of merging users into the architecture's fixed shared demo account. Tokens live for the hackathon session; no cross-device real identity is claimed.
- Complex typed answers still use model extraction; a simple, explicit BP/diabetes answer can use a source-anchored code fallback after a model quote/schema failure. Negations and ambiguous/borderline answers do not use that fallback. Every voice-derived fact is marked for individual checking.
- Full production-role provisioning, retention/erasure, log chains, load/security gates and operational systems remain deferred as authorized by AGENTS.md. The local demo keeps encryption, ownership, per-purpose consent, cap reservations, input bounds and the required correctness gates.

## User change of plan — 31 Oct 2026 11:55 IST (supersedes prior freeze)
- New final deadline 14:30 IST; main features13:45, polish/E2E14:15.
- Remove staging Paytm and credential waiting; one explicitly labelled Demo payment sheet with UPI/Wallet/Card, paid DB status, timestamp, top notification and persisted bell list. No gateway calls, no real money and no S2S verification claim.
- Replace earthy UI with a simple light-blue/navy visual flow, live form panel/drawer, mic and live understanding, timeline comparisons/Promise Card, calendar export and actionable policy flags.
- Add Reset demo and verify three consecutive runs using that control. Preserve the existing demo-1 tag; create demo-2 after revised verification (latest takeover instruction).

## Takeover revision (12:13 IST)
- Latest user schedule takes precedence: UI working by13:30, hosted attempt13:30–14:00 (30 minutes maximum), rehearsals14:00–14:20, freeze14:30. No UI additions after14:00; fallback if broken14:10.
- Identity now has its own individual review card. Correcting identity restarts member attestation and answers so health facts cannot retain stale age/sex context.
- Rewritten React UI retained after a successful TypeScript/Vite build. Plain responsive CSS provides the requested blue/navy theme, live-form drawer, recording/payment/audit animations, and original Lucide icons.

## Talk and Compare fixes — 12:48 IST
- New voice-first identity questions replace the member form. Twelve numbered groups contain explicit branch questions; treatment and dose are separate answers. Feet/inches are converted in code using 2.54 cm/inch, rounded down to whole cm (5 foot 2 →157); kg and age are parsed in code. The AI numeric guard remains unchanged.
- Reset deletes health data, old tokens, orders and notices; it renews only the same browser's explicit purpose-consent choices so an already-consented demo starts immediately at empty Q1. Member/guardian attestation must be given again.
- Compare rejection diagnosis: existing completed journeys can have every stored line confirmed while the updated FSM expects a newly added answer. Metadata audit found selected journeys in this state, and no selected journey with unconfirmed stored lines. Structured review-required responses now distinguish an unanswered Talk question from an exact changed/unconfirmed Check line. Selection rechecks confirmation under the journey lock; the UI never bypasses the gate.
- For-you summary facts and 0–36 calendar-month timelines are deterministic. Care Smart Select is not selected; do not claim a 20% co-pay. Room-rent checks use pinned clauses; Tata's available clause does not establish a cap, so it asks to verify the schedule instead of inventing one.
- Supabase transaction pooler DNS failed outside the sandbox on preflight. Vercel is skipped under the owner's explicit fallback rule; the existing Mac/Postgres/HTTPS tunnel remains the demo.

## Inherited API key diagnosis — 12:54 to 12:58 IST (resolved)
- The inherited shell ANTHROPIC_API_KEY differed from the owner-provided .env key and overrode it in serverless-preparation code. That unrelated key returned HTTP400 credit-balance errors. The owner’s screenshot showed funded organization credits; the owner’s .env key succeeds. No balance top-up or key replacement was needed. Local dotenv credentials now override ambient shell values; hosted runtimes still use production environment values.
- Both medicine readers now work: fresh live printed fixture has two agreeing readers; blank fixture has no candidates. The explicit one-reader buyer-confirmation fallback remains available for genuine provider outages.
- Live policy extraction is restored after using the correct key. Generated samples retain quote-verified deterministic fallback for outages; arbitrary PDFs retain manual field entry. No audit cut is currently required.
- Known rejected, unexecuted credit requests release their spend reservation and trigger a bounded 60-second provider cooldown. All actual/uncertain calls retain conservative reservations and the original app caps. Automatic retry after cooldown supports restored credit without a code change.

## Header overlay recovery — 13:07 IST
- The failed consecutive-run reset was a visible overlay bug: a still-open notification panel covered the Reset menu. Bell/Menu are now mutually exclusive and disabled while the current request finishes. The reset endpoint itself passed local and HTTPS paid-session reproductions. Final consecutive runs restart after this UI fix.

## Revised final freeze — 13:12 IST
- All requested functional and required test gates completed before the hard deadline. The final three HTTPS runs (49/42/44s) use the repaired current UI and Reset between runs, with accepted live voice, two readers, per-line review, all plan selection, demo payment/notification and four live audits each.
- demo-1 remains at 3be16f73aacde128aa6b1caf6d8146f4f98f4402. Revised source freezes as demo-2; no tag is moved. Original freeze evidence is archived as evals/results/freeze-verification-demo-1.json.
- Current stage API was restarted cleanly on the same HTTPS tunnel. Both local fallback video formats are refreshed. Obsolete timed payment checks no longer inspect credentials or wait until14:30.

## Owner-requested PDF exports — 13:28 IST
- Exported two explicitly fictional, one-page Plan B/Sunita52F/hypertension/2026-10-31 PDFs into demo-files/ for manual upload: missing Instant Cover and clean. This is an explicit synthetic fixture export requested by the owner; uploaded buyer PDFs remain transient and are never stored. Application code and both frozen tags remain unchanged.

## Owner-requested final review step — 13:30 IST
- The owner requested an explicit way to finish after the policy audit. Add an owner-scoped, persisted Finish review acknowledgment and a bilingual completion summary. Flagged differences stay open and visible; completing the review never accepts an insurance policy or resolves an issue. Clean results show completion without a follow-up warning.
- Completion is tied to the latest audit and confirmed context; changed answers/plan invalidate it. Existing owner audits from before this feature can be re-compared in code without uploading or paying again. Reset clears completion.
- Prior demo-1/demo-2 tags remain unchanged. The new finishing-step revision will use demo-3 after its tests and browser checks; no frozen engine/payment/date behavior is changed.

- 13:56 IST tunnel recovery: the old anonymous tunnel returned Tunnel not found and stopped resolving; local API remained healthy. Replaced only the tunnel. New stage URL: https://camping-leon-rider-performer.trycloudflare.com. New hostname means a new browser origin/session; no cross-owner session merging was introduced.

- Finishing-step freeze 2026-10-31T13:59:11.210950+05:30: demo-3;150 Python tests,44 clauses, build and scoped local/new-HTTPS completion browser checks pass. Base demo-2 live rehearsals remain separately identified; expensive model calls were not repeated for an isolated completion addition. Prior tags and engine/date/payment semantics remain unchanged.
