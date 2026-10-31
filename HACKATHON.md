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
