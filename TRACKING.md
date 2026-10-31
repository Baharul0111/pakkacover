# Pakka Cover — Work Tracker

## Resume here
- Time: 2026-10-31 10:33:50 IST. Step 1 — initialize the demo build, then policy sources and rules engine.
- Next action: inspect local tools; create Python 3.12 environment; download Plans A/B/C PDFs and implement clause-linked rules and G1/G2 tests.
- Run app: pending Step 1 runnable shell; target command `scripts/run_demo`.
- Run tests: pending environment; target `.venv/bin/python -m pytest`.
- Background processes: none.
- Done: requirements reviewed; Git initialized; `.gitignore` excludes credentials, runtime files and dependencies. Half-done: Step 1 not yet implemented.
- Decisions: macOS/Homebrew; today's AGENTS schedule supersedes old dates; retention out of scope; app-side spend caps; live model IDs checked at startup.
- Paytm: simulated pending secret-safe key-presence check; adapter will select staging only with both keys.

## Implementation log


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
