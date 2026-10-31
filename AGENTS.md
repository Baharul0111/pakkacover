# PakkaCover: hackathon build instructions

Read goal.md completely, then architecture.md completely. Together they describe
the full PakkaCover product. TODAY IS THE HACKATHON FINALS (31 Oct 2026) and this
build is ONLY the hackathon demo described below. Where this file differs from
architecture.md, this file wins. Do not edit goal.md, architecture.md or
setup.md; record every hackathon deviation in HACKATHON.md.

## HARD DEADLINE: 15:00 IST today. The demo must be frozen and runnable by 14:45.

Run `date` at the start of every step and log the time in TRACKING.md. Follow
this schedule (IST):


| Time           | Step                                              |
| -------------- | ------------------------------------------------- |
| 10:30 to 11:15 | Step 1: rules engine, Plans A/B/C, tests          |
| 11:15 to 12:15 | Step 2: backend, consent, interview, Sarvam voice |
| 12:15 to 12:50 | Step 3: medicine photo pipeline                   |
| 12:50 to 13:35 | Step 4: review cards, ranking, Promise Card       |
| 13:35 to 14:05 | Step 5: sample policies and the Day-12 audit      |
| 14:05 to 14:20 | Step 6: payment (real staging or simulated)       |
| 14:20 to 14:40 | Step 7: run_demo, tunnel, end-to-end checks       |
| 14:40 to 14:45 | Freeze: DEMO.md, final test run, git tag demo-1   |

Timing rules:

- If a step runs more than 15 minutes over, apply the cut list immediately, log
  it in TRACKING.md, and move on.
- At 14:30 start no new feature; only fix, test and document.
- At 14:45 freeze, whatever state the work is in. The app must be runnable at the
  end of every step, so a frozen build is always demoable.

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
- whether Paytm is in real-staging or simulated mode

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
- the ₹1 TEST payment (14)
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
- Profile: demo (every question spoken aloud, ₹1 TEST payment on).
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

## Paytm: keys may or may not arrive

I could not generate Paytm staging keys yet. I may add PAYTM_MID and
PAYTM_MERCHANT_KEY to .env later today, or not at all. Build for both cases:

- Put payments behind one adapter with two implementations, selected
  automatically at startup:
  - **staging**, used when both keys are present
  - **simulated**, used when either is empty
- **Simulated:** the same screens and order records, with a banner reading
  "SIMULATED — Paytm test keys pending".
- **Staging:** the real PG staging flow from architecture.md:
  - Initiate Transaction with the paytmchecksum package (pin pycryptodome)
  - CheckoutJS from PAYTM_HOST
  - callback with checksum verification
  - server-to-server order status check
  - red TEST banner
  - callbackUrl built from PUBLIC_URL
    Write this code fully and unit-test the checksum round-trip with a dummy key,
    even if real keys never arrive.
- Re-check .env for the keys at the start of step 6 and again at 14:30. Switching
  modes must need only a restart, never a code change.
- Log the current mode in TRACKING.md and show it on /ready.
- Never touch production Paytm hosts.

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
6. Payment adapter (staging or simulated, as above).
7. scripts/run_demo with the tunnel, then the end-to-end checks.

If time runs short, cut in this order:

1. Plan C becomes a summary card.
2. Typed answers replace voice for non-demo branches.
3. TTS read-back becomes text only.
4. The audit runs on the generated sample PDFs only.

Never cut: the engine tests, the quote check, confirm per line, the numeric guard,
the TEST or SIMULATED labelling, and the TRACKING.md updates.

## Done means (by 14:45)

- The G1 engine tests and G2 quote tests pass.
- G6 catches 3/3 planted mismatches with 0 false alarms on the clean PDF.
- G7 numeric guard shows 0 leaks.
- A G0 test proves one session cannot read another's data.
- My clips and photos, if present in evals/golden/, keep the demo slots and drug
  names intact, with no invented medicine (blurred means ask the buyer).
- A scripted end-to-end run of the Sunita story passes against the tunnel URL.
- DEMO.md is written, containing:
  - the stage script
  - the start command
  - where the demo passphrase is (in .env, never printed)
  - how to flip the voice_in and voice_out kill switches if the Wi-Fi is bad
  - how to recover if the tunnel dies
  - the current payment mode
- Git tag demo-1 is made, and TRACKING.md says "FROZEN" with the final state.

## Rules for working

- Work continuously through every build step. Do not stop at a "good stopping
  point" or hand me a summary of remaining work. Stop only when "Done means" is
  true or 14:45 arrives.
- Load .env values with python-dotenv. Never print, cat or log .env or any secret,
  and never write secrets into TRACKING.md.
- Generate FERNET_KEYS, PEPPER and DEMO_LOGIN_PASSPHRASE yourself and write them
  into .env if empty.
- Install every tool and package you need yourself. Use non-interactive commands
  only. Run servers and the tunnel in the background, and stop them cleanly after
  tests.
- Already provided by me, never ask for them:
  - in .env: ANTHROPIC_API_KEY, OPENAI_API_KEY, SARVAM_API_KEY,
    SARVAM_BALANCE_INR, DATABASE_URL (or empty, meaning go local), and
    PAYTM_WEBSITE / PAYTM_HOST (PAYTM_MID and PAYTM_MERCHANT_KEY may be empty)
  - my clips in evals/golden/stt/ and photos in evals/golden/vision/ (they may
    arrive mid-build)
- If something only I can provide is truly missing, list every missing item once
  in one message, log it in TRACKING.md, and keep building everything else
  meanwhile.
