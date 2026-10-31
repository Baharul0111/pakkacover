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
