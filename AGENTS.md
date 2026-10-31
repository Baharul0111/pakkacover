# PakkaCover: hackathon build instructions

Read goal.md completely, then architecture.md completely. Together they describe
the full PakkaCover product. TODAY IS THE HACKATHON FINALS (31 Oct 2026) and this
build is ONLY the hackathon demo described below. Where this file differs from
architecture.md, this file wins. Do not edit goal.md, architecture.md or
setup.md; record every hackathon deviation in HACKATHON.md.

## HARD DEADLINE: 14:30 IST today (31 Oct 2026)

Everything must be finished, tested and frozen by 14:30. The owner reserves
14:30–15:30 for testing and recording. Main features by 13:45; UI polish and
end-to-end checks by 14:15. This revision supersedes the previous demo freeze.

Run `date` at the start of every step and log the time in TRACKING.md. Follow
this schedule (IST):


| Time (IST) | Remaining work |
| --- | --- |
| 11:55–12:15 | Demo-only payment adapter, paid orders, notification persistence, reset |
| 12:15–13:05 | Simple Talk UI, live transcript/understanding, live proposal form, Check cards |
| 13:05–13:45 | Compare timeline cards, Promise timeline/calendar, Policy check actions |
| 13:45–14:15 | Laptop/phone polish and 3 full Sunita runs with Reset demo between runs |
| 14:15–14:30 | Final G0/G1/G2/G6/G7, DEMO.md, FROZEN tracking, update local demo-1 tag |

Timing rules:

- Run `date` at the start of every step and log the time.
- If anything is late, apply the existing cut list immediately and log it.
- Main features must be done by 13:45. UI polish and E2E must be done by 14:15.
- From 14:15, only fix, test and document. At 14:30 freeze and tag `demo-1`.
- Keep the app runnable at each completed small part. Never cut the engine,
  quote check, confirm-per-line, numeric guard, visible Demo labels or tracking.

## Resumability: TRACKING.md is the source of truth

I may run out of credits and continue in a NEW account with a fresh agent, so
TRACKING.md must always let a stranger resume in under 2 minutes.

Keep the existing content of TRACKING.md. At the top, under the title, maintain a
section "## Resume here" that you overwrite every time. It contains:

- current time and current step, with its sub-task
- "Next action": the exact next thing to do, specific enough to start
  immediately
- how to run the app and the tests (exact commands)
- background processes that may still be running and how to stop them
- what is done and verified, and what is half-done (file names)
- open problems and decisions taken, with a one-line reason each
- Paytm mode: `demo` only (no real gateway calls or pending credentials)

Below it, append to "## Implementation log" one timestamped line per completed
small piece of work: what was done, its test result, the commit hash.

Update TRACKING.md after every small completed piece, at least every 15
minutes, and always before any long-running command. Commit with git right after
each update (`git add -A && git commit`, excluding .env and secrets/). The very
first action of this build: `git init` if needed, write .gitignore (.env,
secrets/, node_modules, __pycache__, .venv, dist), then update TRACKING.md.

If TRACKING.md already shows implementation progress when you start, you are
resuming: read "Resume here", verify the last logged step by running its tests,
and continue from "Next action". Never redo completed, verified work.

Settle the "Items to reconcile" listed in TRACKING.md as follows, and log them:

- **Environment:** this is macOS; use Homebrew where needed.
- **Schedule:** this file replaces the old dates.
- **Retention:** out of scope today.
- **Spend:** enforce app-side caps and never rely on console hard stops.
- **Paytm:** see the Paytm section below.
- **Live model ids:** verify at startup.

## Goal of this build

goal.md item 23, the Sunita story, working end to end on my phone in under five
minutes. Use the real architecture for everything the story touches:

- consent (item 2) and member attestation (3)
- the tele-medical question flow on the Sunita path (4)
- voice with typed and chip fallback (5)
- two-reader medicine photo with ask-never-guess (6)
- confirm every line, with no confirm all (7)
- Plans A/B/C from public wordings with verified clause quotes (8, 10)
- ranking by modelled payout with the published method and no "best" label (9)
- Promise Card with exact dates (11) and the in-app upcoming dates list (12)
- the ₹1 Paytm-style demo payment, paid DB record and in-app notification
- the Day-12 audit catching planted mismatches (15)
- the advisor button labelled "Pilot callback within 24 h" (16)
- the AI never deciding money or dates (18)
- non-AI fallbacks and kill switches (19)

## Hackathon simplifications (these replace the matching parts of architecture.md)

- Runs on my Mac. FastAPI (Python 3.12) serves the built React app from the same
  origin. One command, scripts/run_demo, starts the server and a Cloudflare quick
  tunnel (cloudflared via Homebrew, no account), prints the https URL and writes
  it to PUBLIC_URL in .env. HTTPS is required so the phone mic and camera work.
- One Postgres from DATABASE_URL (Supabase session pooler, port 5432; use asyncpg
  with statement_cache_size=0), schema app, one role, Alembic migrations. If
  DATABASE_URL is empty, install and run Postgres locally with Homebrew and fill
  DATABASE_URL yourself.
- Skip today: Render, Cloudflare Pages, GitHub Actions, UptimeRobot, Neon,
  backups, the staging DB, Google sign-in, Paytm Mini App login, email, staff TOTP,
  the advisor console, retention jobs, and the DPDP export and delete screens.
- Keep: owner-scoped data access, Fernet encryption of health columns, no stored
  audio, photos or PDFs, and per-purpose consent rows.
- Login: the demo-profile passphrase login only, using DEMO_LOGIN_PASSPHRASE.
- Profile: demo (Sarvam speaks every question; ₹1 Paytm-style demo payment on).
- Interview: build the Sunita path fully. Other branches may be skeletons that
  fall back to typed answers.

## Speech: Sarvam for all of it (I have Sarvam credits)

- STT: saaras:v4 with keyterms (BP, sugar, thyroid, Telma, Telmisartan,
  Amlodipine, Metformin and the other demo drug names). Run a quick A/B against
  saaras:v3 with mode=codemix on my clips in evals/golden/stt/ and pin the
  winner. If the clips are not there yet, pin saaras:v4, log it, and rerun the
  A/B when they appear.
- TTS: bulbul:v4-flash, speaking every question in demo mode. Use the
  aparna_hi_customer voice for Hindi and simran_enhi_customer for mixed lines.
- Call the Sarvam REST API directly with httpx and the api-subscription-key header.
- Cost limits: Sarvam daily cap ₹150, tracked against SARVAM_BALANCE_INR. Switch
  voice to typed plus chips only when the remaining balance drops below ₹20.

## Other models (keys in .env)

- Anthropic claude-haiku-5-5 for slot extraction and audit extraction, with one
  claude-sonnet-5-5 retry when a quote check fails.
- OpenAI gpt-6.1-terra plus claude-haiku-5-5 as the two parallel strip readers.
- OpenAI gpt-6-luna as the interview fallback, and omni-moderation-latest.
- Pin the exact model ids by calling each provider's models endpoint at startup,
  and log the returned id per call.
- Every outside call has an explicit timeout.

## Paytm: demo only; no keys will be available

- Drop the real staging integration and all waiting/checking for keys. Keep one
  payment adapter, implemented only as `demo`. Never call Paytm hosts.
- “Pay ₹1 with Paytm” opens a Paytm-style sheet with **UPI, Wallet and Card**
  choices. Use simple original icons; no copied logos/images. These terms are
  explicitly requested by the owner and override any skill vocabulary rule.
- After choosing an option, show “Processing…” for about 2 seconds, then a big
  green tick, “Payment successful via Paytm”, amount, order ID and time.
- A subtle grey **Demo** chip stays visible on both sheet and success screen.
  This is a simulation; no real money moves and no gateway verification is claimed.
- At success, slide a phone-style banner from the top: “Paytm · ₹1 paid for your
  health cover · Order PC…”. Also persist it in the owner-scoped in-app
  notifications list, opened by a bell icon. Keep the demo context identifiable.
- Mark the order paid in Postgres through the payment adapter. Preserve mode
  `demo` and do not claim provider/S2S verification.
- Show `demo` on `/ready` and in TRACKING.md. Cancel the obsolete 14:30 key check.

## UI — very simple, visual first

Use very little text, short sentences, large icons and large buttons. One font,
rounded shapes, generous spacing. White background, light grey cards, primary
light blue **#00BAF2**, navy **#002E6E** headings/top bar, green success and amber
“please check”. It must work on the laptop for recording and on a phone.

- Top progress: 4 icon steps **Talk → Check → Compare → Promise Card**, then a
  fifth **Policy check** for the Day-12 audit. Hindi/English toggle top-right.
- Talk: one short spoken question at top with replay speaker. Centre a BIG round
  mic “Hold to talk / Bolne ke liye dabayein”, pulsing while recording. Tap mode
  also works. Under it a small Live box: “You said: …” and “We understood: BP
  since 2019”, with tick/? markers. Big Haan/Nahi chips for yes/no; a small
  keyboard icon reveals typing. A camera button “Photo of medicine” supports
  capture/upload, thumbnail, “Telmisartan 40 mg ✓”, and two choices on disagreement.
- “Your form” fills live as she talks: Name, Age, Height/Weight, Illness, Since,
  Medicine, Hospital stays. Right-side panel on laptop, pull-up drawer on phone.
  Animate each field; green confirmed dot, amber AI-heard/check dot.
- Check: one card per line, 3 big buttons **✓ Sahi hai / ✗ Galat / ✎ Badlo**;
  no confirm-all. Read aloud. Green “Saved ✓” toast after every confirmation.
- Compare: 3 cards side by side on laptop, stacked on phone. One large “Would
  pay: ₹X”, BP cover timeline (grey waiting / blue covered), “Why?” opens the
  clause. No best badge. Small “How we rank” link.
- Promise Card: vertical icon timeline for accident, illness, BP, operations,
  free-cancel date; one short line and date per row, hi/en toggle. Buttons
  “Add to calendar” and “Pay ₹1 with Paytm”. Keep all engine-derived date facts.
- Policy check: upload, Checking animation, then green ticks and red flags. Each
  flag has both quotes side by side and buttons “Ask insurer to fix”, “Cancel
  free by <date>”, “Talk to advisor”. Preserve generated clean/3-mismatch samples.
- Everywhere: floating **Advisor** with headset icon bottom-right, notifications
  bell, and **Reset demo** in a small menu. Reset must start a clean Sunita run.
- Friendly empty/loading/error states with icons; never raw errors.

## Policy wording PDFs

Download them from the URLs in architecture.md into data/plans/src/. If a download
is blocked, log the exact list in TRACKING.md and HACKATHON.md and tell me which
PDFs to save there, while you continue with everything else.

## Build steps

After each step, run its tests, update TRACKING.md, commit, and print one line
saying what I can try on my phone.

1. Plan Rules JSON for A/B/C (demo-path fields), check_quotes.py, the rules engine
   and its tests (the Sunita fixture shows B > C > A with dates).
2. Backend scaffold, consent, the interview state machine on the Sunita path,
   Sarvam voice, Haiku slot extraction, typed and chip fallback.
3. Medicine pipeline: two readers, salt match, condition table, DISAMBIGUATE.
4. Review cards with read-back, the ranking screen with clause taps and the method
   page, the Promise Card (hi/en), the upcoming dates list.
5. sample_policy.py (clean plus 3 planted mismatches) and the Day-12 audit.
6. Demo-only payment adapter, sheet/success, paid order and in-app notification.
7. scripts/run_demo with the tunnel, then the end-to-end checks.

If time runs short, cut in this order:

1. Plan C becomes a summary card.
2. Typed answers replace voice for non-demo branches.
3. TTS read-back becomes text only.
4. The audit runs on the generated sample PDFs only.

Never cut: the engine tests, the quote check, confirm per line, the numeric guard,
the always-visible Demo labelling, and the TRACKING.md updates.

## Done means (by 14:30)

- G1 engine, G2 quotes, G6 (3/3 planted mismatches, 0 clean false flags), G7
  numeric guard (0 leaks), and G0 session isolation pass.
- Full story: talk → medicine photo → confirm each line → compare → Promise Card
  → Paytm demo payment with success/notification → Day-12 planted mismatch.
- Three consecutive full runs through `scripts/run_demo`, using **Reset demo**
  between runs, on the current laptop/phone-responsive UI.
- Owner clips/photos, if present, preserve demo slots/drugs; blur means ask.
- DEMO.md contains the stage script and the line: **“Paytm keys were not available;
  this is a clearly labelled demo payment. No real money is moved.”**
- DEMO.md also covers start, private passphrase location, voice kill switches,
  recovery and demo payment mode. No secrets are printed.
- Update/replace only our local `demo-1` tag with the revised frozen build;
  TRACKING.md says **FROZEN**. The prior freeze is superseded by this plan.

## Rules for working

- Work continuously through every build step. Do not stop at a "good stopping
  point" or hand me a summary of remaining work. Stop only when "Done means" is
  true or 14:30 arrives.
- Load .env values with python-dotenv. Never print, cat or log .env or any secret,
  and never write secrets into TRACKING.md.
- Generate FERNET_KEYS, PEPPER and DEMO_LOGIN_PASSPHRASE yourself and write them
  into .env if empty.
- Install every tool and package you need yourself. Use non-interactive commands
  only. Run servers and the tunnel in the background, and stop them cleanly after
  tests.
- Already provided by me, never ask for them:
  - in .env: ANTHROPIC_API_KEY, OPENAI_API_KEY, SARVAM_API_KEY,
    SARVAM_BALANCE_INR, DATABASE_URL (or empty, meaning go local).
    No Paytm credentials are needed or expected.
  - my clips in evals/golden/stt/ and photos in evals/golden/vision/ (they may
    arrive mid-build)
- If something only I can provide is truly missing, list every missing item once
  in one message, log it in TRACKING.md, and keep building everything else
  meanwhile.
