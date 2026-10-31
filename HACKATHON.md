# Hackathon deviations

Authority: AGENTS.md, 31 Oct 2026. Original goal.md, architecture.md and setup.md remain unchanged.

- Demo only, frozen by 14:45 IST today; replaces the original 29–30 Oct build schedule.
- macOS local FastAPI serves React; Cloudflare quick tunnel supplies same-origin HTTPS. No production hosting or real users.
- One Postgres database/role with Alembic, owner-scoped queries and Fernet health fields.
- Passphrase demo login only. No Google/Mini App login, retention/export/delete screens, staff/admin console, backups, standby, email, or cloud CI/monitoring.
- Sunita interview complete; other branches may use typed/manual fallbacks.
- Sarvam demo cap ₹150/day and minimum remaining balance ₹20, overriding architecture profile caps. App caps do not assume provider budgets are hard stops.
- Payment adapter automatically selects staging with both keys, otherwise explicitly simulated. Production payment hosts forbidden.
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
- Promise Card shows the demo-relevant exclusion example (unproven treatments) and explicitly states other exclusions/conditions apply; full exclusion authoring is deferred.

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
