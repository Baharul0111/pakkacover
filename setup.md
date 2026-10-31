# PakkaCover: Setup (only what YOU must provide)
> Everything below needs your identity, your browser, or your approval. Claude Code cannot do these for you. Everything else (installing tools, running commands, creating files, generating keys, pushing settings to Render, GitHub and Cloudflare) Claude Code does itself, and none of it is listed here. Finish this file once and the build never has to ask you for anything.

**Written for:** Baharul Islam (Team Solidary), solo builder, India.
**Clock:** written 29 Oct 2026, 17:00 IST. The finals are on 31 Oct. The demo build freezes at 22:00 IST on 30 Oct.
**Money:** every item is free except AI usage on your own OpenAI and Anthropic keys (about ₹70 a month at 50 pilot users, capped by the spend limits in items 10 and 11) and the optional email domain (item 18, about ₹100 to ₹900 a year, off by default).

**How values reach the build.** You paste values into **one local `.env` file** (item 19). Claude Code then pushes each value where it belongs: Render through the Render API, GitHub Actions secrets through the GitHub CLI, and Cloudflare Pages through the Cloudflare API. It never displays a value while doing this. The tokens that make this possible (`GH_TOKEN`, `RENDER_API_KEY`, `CLOUDFLARE_API_TOKEN`) are part of the items below. You never type a secret into the Render, GitHub or Cloudflare consoles.

**Console screens change.** Every step below was checked against the vendor's own docs on 29 Oct 2026 where a doc existed. A step marked *(check the official guide if a button has moved)* could not be fully confirmed. The guide link is next to every item.

## Checklist

**Start these today, right now (slowest or riskiest first)**
- [ ] 0. MFA on every account, plus a Bitwarden vault (do this first; about 30 min)
- [ ] 1. Paytm PG staging keys (**start this today**: it is unclear whether an individual without KYC can get them)
- [ ] 2. Paytm Mini App DIY onboarding (**start this today**; optional for the finals; may need days or a business)
- [ ] 3. Google sign-in: consent screen published "In production" plus a web client ID (**start this today**)

**Tonight, before the build starts**
- [ ] 4. GitHub: private repo, fine-grained token, Dependabot, Actions budget
- [ ] 5. Supabase: two Mumbai projects (prod and staging), Data API off
- [ ] 6. Neon: Singapore standby project
- [ ] 7. Render: dedicated workspace, Docker web service in Singapore, auto-deploy off, deploy hook, API key
- [ ] 8. Cloudflare Pages: repo connected, account ID, API token
- [ ] 9. Sarvam: API key and credit balance
- [ ] 10. Anthropic: workspace, API key, monthly spend limit
- [ ] 11. OpenAI: project, API key, monthly budget
- [ ] 12. Golden sets: record 20 voice clips and photograph 15 medicine strips (tonight; needed by 30 Oct 08:00 IST)
- [ ] 13. Fixed choices for the build prompt (name, team, grievance contact, advisor label, speakers)

**During or after the build**
- [ ] 14. Key escrow into Bitwarden plus an offline copy (when the build prints its "keys generated" notice)
- [ ] 15. UptimeRobot: three monitors (when the build prints its "monitor URLs" notice)
- [ ] 16. Demo-phone runs and the Supabase Security Advisor glance (30 Oct evening, 31 Oct morning)

**Before the first real user (1 to 14 Nov), not needed for the finals**
- [ ] 17. Paperwork: licensed advisor, DPAs, CERT-In text, vendor usage policies, CDCI licence, privacy link on Google

**Optional, off by default**
- [ ] 18. Email domain plus Resend (about ₹100 to ₹900 a year)

- [ ] 19. `.env` created and complete

---

## 0. MFA on every account, plus a Bitwarden vault
**Why the project needs it:** PakkaCover holds health data. One stolen password on GitHub, Render or Supabase would expose it, so every console uses an authenticator app or a passkey, never SMS (design §7.13, GM-1).
**Cost:** free   **Time:** ~30 minutes now, then 2 minutes per new account as you create it below

**Steps:**
1. Install an authenticator app on your phone (Google Authenticator, Microsoft Authenticator, or 2FAS).
2. Go to https://vault.bitwarden.com/#/register and create a **Bitwarden Free** account with a long master password you have never used before. Write the master password on paper and keep it at home. Bitwarden cannot recover it.
3. In the Bitwarden web vault, open **Settings → Security → Two-step login** and turn on **Authenticator app**. Save the Bitwarden recovery code on the same paper.
4. Turn on MFA in each account below as you create or open it. Save every recovery code as a **Secure note** in Bitwarden (**New → Secure note**).
   - **Google** (also covers Sarvam and Anthropic if you sign in with Google): https://myaccount.google.com/security → **2-Step Verification** → add **Authenticator** and a **Passkey**.
   - **GitHub:** avatar → **Settings → Password and authentication → Enable two-factor authentication**.
   - **Render:** **Account Settings → Security** (two-factor authentication) *(check the official guide if a button has moved)*.
   - **Supabase:** avatar → **Account preferences → Security → Multi-factor authentication** *(check the official guide if a button has moved)*.
   - **Cloudflare:** **My Profile → Authentication → Two-Factor Authentication**.
   - **Neon:** sign up with GitHub or Google so that account's MFA protects it.
   - **UptimeRobot:** **My Settings → Two-factor authentication** *(check the official guide if a button has moved)*.
   - **OpenAI:** **Settings → Security → Multi-factor authentication** *(check the official guide if a button has moved)*.
   - **Anthropic Console:** sign in with Google so Google's MFA protects it.
   - **Paytm dashboard:** Paytm signs you in with your mobile number and an OTP. That is SMS-based and cannot be changed, so it is the one accepted exception. Keep a strong Paytm app PIN.
5. If you add the optional domain (item 18), also turn on MFA at the domain registrar and at Resend.

**You'll end with:** every console asking for a code from your phone at sign-in, and all recovery codes stored in Bitwarden.
**Where it goes:** nowhere in `.env`. It protects every account below.
**Official guide (if a button has moved):** https://bitwarden.com/help/setup-two-step-login/ · https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication

---

## 1. Paytm PG staging keys (start this today)
**Why the project needs it:** the "real Paytm" part of the demo is a ₹1.00 TEST order through Paytm's real staging payment APIs (Initiate Transaction, CheckoutJS, server status check). No real money moves, and the screen says so.
**Cost:** free (test mode)   **Time:** ~15 minutes if the dashboard lets an individual in; if it insists on KYC first, it may take days, so start now

**Steps:**
1. Go to https://dashboard.paytmpayments.com and click **Create Account** (or **Login** if you already use Paytm). Sign in with your Paytm mobile number and the OTP.
2. If the dashboard asks for business details, fill in only what it requires to reach the dashboard. Do **not** start "Activate account" or live KYC. Test keys don't need it.
3. Open https://dashboard.paytmpayments.com/next/apikeys (left menu **Developers → API Keys**).
4. Find the section **Test API Details** and click **Generate now**.
5. The test details appear: **Test Merchant ID**, **Test Merchant Key**, and the website name **WEBSTAGING**. Copy the Merchant ID and the Merchant Key into a Bitwarden secure note for now.
6. Optional, on your Android phone: install the **Paytm UPI test app** from https://github.com/paytm/Paytm_Payments_Android_Sample_Apps/tree/master/UPI_Collect_Intent_Test_App (you may need to allow "Install unknown apps"). Without it you can still pay in test mode with a test card (CVV `123`) or the test wallet (`77777 77777` / `Paytm12345` / OTP `489871`).
7. **If step 3 or 4 is blocked** (it asks for KYC, or the Test section is empty), stop and record it. Tell the build prompt "Paytm staging keys unavailable" (item 13). The build then uses the design's simulated checkout, labelled TEST, and the deck says so honestly.

**You'll end with:**
- a **MID**: letters and digits, typically about 20 characters (shape `AbCdEf12345678901234`)
- a **Merchant Key**: typically 16 characters, often containing `#`, `@`, `!` or `$`

**Where it goes:** the `PAYTM_MID=` and `PAYTM_MERCHANT_KEY=` lines of `.env`. **Keep the double quotes.** An unquoted `#` silently cuts the key short and every payment fails with `resultCode 227`. `PAYTM_WEBSITE="WEBSTAGING"`, `PAYTM_HOST` and `PAYTM_ENVIRONMENT` are pre-filled in the template.
**Official guide (if a button has moved):** https://github.com/paytm/paytm-agent-skills (skill `getting-started`: "Staging (test mode): dashboard.paytmpayments.com/next/apikeys → Generate now (under Test API Details)") · https://www.paytmpayments.com/docs/getting-started · test instruments: https://www.paytmpayments.com/docs/test-instruments/testing-integration

---

## 2. Paytm Mini App DIY onboarding (start this today; optional for the finals)
**Why the project needs it:** Paytm consent login and the in-Paytm camera work only inside the Paytm Developer Mini App, and only with Mini App credentials. Without them, the demo runs as a standalone web app with Google sign-in, and the app is described as "built to Paytm Mini App spec, running on Paytm PG staging". That is fine for the finals.
**Cost:** free to try   **Time:** ~30 minutes to try; if Paytm asks for business documents, days, with eligibility for an individual **unverified**

**Steps:**
1. On https://dashboard.paytmpayments.com (same login as item 1), open **Mini Apps** in the left menu and choose the **DIY** onboarding *(check the official guide if a button has moved)*.
2. Fill in the app details: name **PakkaCover**, and the category that honestly fits. If the form demands a licence, GST or business proof you don't have, stop here. This item is optional.
3. When onboarding finishes, the Mini App details page shows four things: an **App QR**, a **Mini App ID**, an **Auth client ID** and a **client secret**. Copy the last three into Bitwarden. The client secret may be shown only once.
4. Skip the "unlimited merchant" PG MID on that page. It needs KYC, and the demo pays through item 1's staging keys instead.
5. On your **Android** phone, open the Paytm app and scan the App QR. The **Developer Mini App** opens.
6. After item 8 gives you the Pages URL, set it as the Mini App's H5 URL inside the Developer Mini App *(check the official guide if a button has moved; the docs don't show this screen)*. Open it there once to check that the page loads.
7. Do **not** tap **App Submission** or **Take your app live**. Publishing is public and needs Paytm's review, so it waits for your explicit go-ahead later.

**You'll end with:** a Mini App ID, an auth client ID and a client secret (opaque strings; shapes not documented). Or a note that onboarding was blocked.
**Where it goes:** the `PAYTM_MINIAPP_ID=`, `PAYTM_MINIAPP_CLIENT_ID=` and `PAYTM_MINIAPP_CLIENT_SECRET=` lines of `.env`. If blocked, leave all three blank. Paytm login then stays off and Google sign-in is the only sign-in.
**Official guide (if a button has moved):** https://www.paytmpayments.com/docs/miniapps/integration-steps · login flow: https://www.paytmpayments.com/docs/miniapps/login-flow

---

## 3. Google sign-in: consent screen published and a web client ID (start this today)
**Why the project needs it:** "Sign in with Google" is how a standalone user saves a disclosure, gets date alerts or runs the Day-12 audit. It is free and needs no domain. A consent screen left in **Testing** blocks everyone who isn't listed, so it must be published "In production" (design §7.10, R2-m3).
**Cost:** free (no billing account needed)   **Time:** ~20 minutes, plus a 2-minute return visit after item 8. Google says origin changes take 5 minutes to a few hours to apply, so do this today.

**Steps:**
1. Go to https://console.cloud.google.com and sign in with your own Google account.
2. In the top bar, click the **project picker → New project**. Name it `PakkaCover` and click **Create**. Make sure it is the selected project.
3. Open https://console.cloud.google.com/auth/overview (**Google Auth Platform**) and click **Get started**.
   - **App information:** app name `PakkaCover`, user support email = your email. Click **Next**.
   - **Audience:** choose **External**. Click **Next**.
   - **Contact information:** your email. Click **Next**.
   - Tick the agreement, then click **Continue** and **Create**.
4. Open **Data Access**. Add **no** scopes. Sign-in uses only the default `openid`, `email` and `profile`, which are not sensitive.
5. Open **Branding**. Leave the **logo empty**: uploading a logo can trigger brand verification. Leave the homepage and privacy links empty for now (they are added in item 17). Click **Save**.
6. Open **Clients → Create client**.
   - **Application type:** Web application. **Name:** `PakkaCover web`.
   - **Authorized JavaScript origins:** add `http://localhost` and `http://localhost:5173`.
   - Leave **Authorized redirect URIs** empty.
   - Click **Create**.
7. Copy the **Client ID**. You can close the client-secret dialog without saving the secret, because the design verifies Google's ID token and never uses the secret.
8. Open **Audience**. Under **Publishing status: Testing**, click **Publish app** and confirm. The status must now say **In production**. With only basic scopes, no verification should be needed; Google's audience page confirms that sign-in-only apps are exempt from the test-user limit (**[verify]**: if Google asks for verification, tell the build prompt, and the design's demo login covers the finals).
9. **Come back after item 8.** In **Clients → PakkaCover web**, add your Pages URL (for example `https://pakkacover.pages.dev`) to **Authorized JavaScript origins** and click **Save**.
10. Create a separate **demo Google account** at https://accounts.google.com/signup (for example `pakkacover.demo…@gmail.com`). Turn on its 2-Step Verification and save its login in Bitwarden. On stage you sign in with this account, never your personal one.

**You'll end with:** a client ID like `123456789012-abc123def456ghi789.apps.googleusercontent.com`, a consent screen showing **In production**, and a demo Google account.
**Where it goes:** the `GOOGLE_OAUTH_CLIENT_ID=` line of `.env`. Claude Code copies it into the front-end variable `VITE_GOOGLE_CLIENT_ID` itself. The demo account stays in Bitwarden only.
**Official guide (if a button has moved):** https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid · https://support.google.com/cloud/answer/15549257 (clients) · https://support.google.com/cloud/answer/15549945 (audience and publishing)

---

## 4. GitHub: private repo, fine-grained token, Dependabot, Actions budget
**Why the project needs it:** the code lives in a **private** repo. GitHub Actions runs CI, the deploy job (migrate, then call Render), the daily tick and the nightly encrypted backup. Private matters for two reasons: scheduled jobs in public repos switch off after 60 days without activity, and the insurer wordings and security posture shouldn't be public.
**Cost:** free (GitHub Free includes about 2,000 private Actions minutes a month; the design budgets about 1,340)   **Time:** ~15 minutes

**Steps:**
1. Go to https://github.com/new.
   - **Repository name:** `pakkacover`. **Visibility:** **Private**.
   - Tick **Add a README file**, so a `main` branch exists for Render and Pages to connect to.
   - Click **Create repository**.
2. Create the token Claude Code uses to push code and set Actions secrets:
   - Open https://github.com/settings/personal-access-tokens/new (avatar → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**).
   - **Token name:** `pakkacover-build`. **Expiration:** 90 days. **Repository access:** **Only select repositories → pakkacover**.
   - Under **Repository permissions**, set **Read and write** for **Actions**, **Contents**, **Secrets**, **Variables** and **Workflows**. Metadata is read-only automatically.
   - Click **Generate token** and copy it now. It is shown once.
3. Turn on Dependabot: in the repo, open **Settings → Advanced Security** (on some accounts **Code security**). Click **Enable** for **Dependabot alerts** and **Dependabot security updates**.
4. Cap Actions spending at ₹0:
   - Open https://github.com/settings/billing → **Budgets and alerts → New budget**.
   - **Budget type:** **Product-level budget → Actions**. **Scope:** your account.
   - **Amount:** `0`. Tick **Stop usage when budget limit is reached** and **Receive budget threshold alerts**.
   - Click **Create budget**.
   - Whether GitHub can also alert at 75% of the *included* minutes is **[unverified]**. Check **Billing → Usage** once a week; the design's CI trims itself when over budget.
5. **Plan limit you should know about:** on GitHub Free, a **private** repo can't use deployment *environments* or environment secrets (GitHub docs: "environment secrets are only available in public repositories" on Free). So the design's `prod` environment becomes **repository-level Actions secrets**, and the deploy job runs only on pushes to `main`. You are the only person with write access, so this is equivalent for a solo repo. Claude Code sets these secrets with `GH_TOKEN`, and you don't click anything for them.

**You'll end with:** `https://github.com/<your-username>/pakkacover` (private), and a token starting `github_pat_` (about 93 characters).
**Where it goes:** the `GH_TOKEN=` and `GITHUB_REPO=` (as `<your-username>/pakkacover`) lines of `.env`. Local only, never sent to Render or Pages.
**Official guide (if a button has moved):** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens · https://docs.github.com/en/billing/how-tos/set-up-budgets · https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments

---

## 5. Supabase: two Mumbai projects (prod and staging), Data API off
**Why the project needs it:** the database. **prod** holds the app's data in Mumbai. **staging** is where every migration and the database role test run first, and where the evals run. The browser never talks to Supabase. Only the API server does, so the auto-generated Data API is switched off (design §7.1, §7.13).
**Cost:** free (Supabase Free allows 2 projects, 500 MB each)   **Time:** ~15 minutes

**Steps:**
1. Go to https://supabase.com/dashboard and sign up with GitHub. Create the free organization if it asks.
2. Click **New project**.
   - **Name:** `pakkacover-prod`.
   - **Database password:** click **Generate a password** and copy it straight into Bitwarden.
   - **Region:** **South Asia (Mumbai)**.
   - If the form shows **Security options → Enable Data API**, untick it.
   - Click **Create new project** and wait about 2 minutes.
3. Make sure the Data API is off: open the project's **Data API** page (left sidebar **Integrations → Data API**, page "Data API integration overview"). Switch **Enable Data API** off *(check the official guide if a button has moved)*.
4. Note the Postgres major version: **Project Settings → Infrastructure → Postgres version** (Supabase's default is 17). You need it for Neon in item 6 *(check the official guide if a button has moved)*.
5. Copy the connection string: click **Connect** at the top of the project page and choose **Session pooler** (port **5432**). Copy the string and replace `[YOUR-PASSWORD]` with the password from step 2.
6. Repeat steps 2 to 5 for a second project named `pakkacover-staging`, also in Mumbai, with its **own** generated password.
7. That's all you do here. You don't run any SQL. Claude Code uses these two admin strings to create the schema `app`, the four least-privilege roles (`pc_migrate`, `pc_app`, `pc_purge`, `pc_backup`) with passwords it generates, `pg_trgm`, and the revokes from `anon`, `authenticated` and `PUBLIC`, by running `infra/supabase.sql` on both projects. After that, the deploy job re-applies it on every deploy. Claude Code composes the per-role connection strings itself.

**You'll end with:** two strings shaped like
`postgresql://postgres.abcdefghijklmnopqrst:YOURPASSWORD@aws-1-ap-south-1.pooler.supabase.com:5432/postgres`
(the 20-letter project ref differs per project; copy the host exactly as shown, because the `aws-N-` index can't be guessed).
**Where it goes:** the `SUPABASE_PROD_ADMIN_URL=` and `SUPABASE_STAGING_ADMIN_URL=` lines of `.env`. Local only: they are never sent to Render or GitHub, which get only the per-role strings.
**Official guide (if a button has moved):** https://supabase.com/docs/guides/database/connecting-to-postgres · https://supabase.com/docs/guides/api/securing-your-api · https://supabase.com/docs/guides/platform/regions

---

## 6. Neon: Singapore standby project
**Why the project needs it:** Supabase Free has no backups. Every night a GitHub job restores the encrypted dump into Neon, so a second, independent copy of the database always exists (design §7.16, C7).
**Cost:** free (1 GB, 100 compute-hours a month)   **Time:** ~5 minutes

**Steps:**
1. Go to https://console.neon.tech and sign up with GitHub or Google.
2. Click **New Project**.
   - **Name:** `pakkacover-standby`.
   - **Postgres version:** the **same major version** you noted in item 5 step 4 (normally 17). The backup tools refuse to cross major versions.
   - **Region:** **AWS Asia Pacific (Singapore)**, `aws-ap-southeast-1`.
   - Click **Create project**.
3. On the project dashboard, click **Connect**. Keep role `neondb_owner` and database `neondb`, and turn **Connection pooling** off (a direct connection) *(check the official guide if a button has moved)*. Copy the string.
4. Claude Code creates the restore-only role with a long random password itself, using this owner string.

**You'll end with:** `postgresql://neondb_owner:npg_xxxxxxxx@ep-word-word-123456.ap-southeast-1.aws.neon.tech/neondb?sslmode=require`
**Where it goes:** the `NEON_ADMIN_URL=` line of `.env` (local only). Claude Code fills `NEON_DATABASE_URL` (the restore role) and sends that one to GitHub.
**Official guide (if a button has moved):** https://neon.com/docs/manage/projects · https://neon.com/docs/connect/connect-from-any-app

---

## 7. Render: dedicated workspace, Docker web service in Singapore, auto-deploy off, deploy hook, API key
**Why the project needs it:** the API server runs here. Render's free 750 hours are counted **per workspace**, and the always-on API uses 744 of them, so it needs a workspace with **no other free service** in it (R2-m4). Deploys happen only when the GitHub deploy job calls the deploy hook, after migrations have run. That is why auto-deploy is off (R2-m2).
**Cost:** free (0.1 CPU, 512 MB; sleeps after 15 minutes idle, which UptimeRobot prevents)   **Time:** ~15 minutes

**Steps:**
1. Go to https://dashboard.render.com and sign up with GitHub.
2. Create the workspace: open the **workspace switcher** (top left) → **New Workspace**. Name it `PakkaCover` and keep the free Hobby plan *(check the official guide if a button has moved)*.
   - **[verify]** If Render asks you to pay for a second workspace, use your existing personal workspace instead, after suspending or deleting every other **free** web service in it. The point is that nothing else consumes the 750 hours.
3. In the PakkaCover workspace, click **+ New → Web Service**.
   - **Git provider:** GitHub. Click **Configure account / Connect GitHub** and allow Render access to **only** the `pakkacover` repo. Select it.
   - **Name:** `pakkacover-api`.
   - **Language:** **Docker**.
   - **Branch:** `main`.
   - **Region:** **Singapore (Southeast Asia)**.
   - **Instance type:** **Free**.
   - Under **Advanced:** **Dockerfile Path** `./apps/api/Dockerfile`, **Docker Build Context Directory** `.`, **Health Check Path** `/health`. If **Auto-Deploy** is shown here, set it to **Off**.
   - Skip environment variables (Claude Code sets them through the API).
   - Click **Deploy Web Service**.
4. The first deploy **fails**, because the repo holds only a README. That is expected and harmless.
5. Open the service's **Settings**.
   - Set **Auto-Deploy** to **Off** (options are On Commit / After CI Checks Pass / Off).
   - Find **Deploy Hook** and copy the URL. Treat it as a password; if it ever leaks, click **Regenerate Hook**.
6. Copy two more values:
   - the service URL shown at the top of the service page (for example `https://pakkacover-api.onrender.com`)
   - the service ID, which is the `srv-…` part of the page address `dashboard.render.com/web/srv-…`
7. Create the API key Claude Code uses to set the service's environment variables: avatar → **Account Settings → API Keys → Create API Key**. Name it `pakkacover-build` and copy it. It is shown once.
8. Once a week during the pilot, glance at the workspace's **Billing / Usage** page. Render Hobby includes **500 build minutes a month** and every deploy builds the Docker image (R3-m4). That's a habit, not setup.

**You'll end with:**
- a deploy hook like `https://api.render.com/deploy/srv-abc123def456?key=AbCdEf123456`
- a service ID like `srv-abc123def456ghi789`
- a service URL like `https://pakkacover-api.onrender.com`
- an API key starting `rnd_`

**Where it goes:** the `RENDER_DEPLOY_HOOK=`, `RENDER_SERVICE_ID=`, `API_BASE_URL=` and `RENDER_API_KEY=` lines of `.env`. Claude Code puts `RENDER_DEPLOY_HOOK` into GitHub Actions secrets and appends `&ref=<commit SHA>` when calling it. `RENDER_API_KEY` and `RENDER_SERVICE_ID` stay local.
**Official guide (if a button has moved):** https://render.com/docs/docker · https://render.com/docs/deploy-hooks · https://render.com/docs/deploys · https://render.com/docs/free · https://render.com/docs/api

---

## 8. Cloudflare Pages: repo connected, account ID, API token
**Why the project needs it:** the phone web app (PWA) is served from Cloudflare Pages. It rebuilds automatically from `main` and gets its security headers from the repo's `_headers` file.
**Cost:** free (500 builds a month)   **Time:** ~10 minutes

**Steps:**
1. Go to https://dash.cloudflare.com/sign-up and create an account. Turn on MFA (item 0).
2. Open **Workers & Pages → Create application → Pages → Connect to Git**.
3. Choose **GitHub**. Under **Install & Authorize**, allow only the `pakkacover` repo, then click **Begin setup**.
4. Fill in the build settings:
   - **Project name:** `pakkacover`. This sets the address `https://pakkacover.pages.dev`; if the name is taken, Cloudflare shows a different one, so use whatever it shows.
   - **Production branch:** `main`.
   - **Framework preset:** **React (Vite)** if listed, otherwise **None**.
   - **Build command:** `npm run build`. **Build output directory:** `dist`.
   - **Root directory (advanced) → Path:** `apps/web`.
   - Leave environment variables empty (Claude Code sets them through the API).
   - Click **Save and Deploy**.
5. The first build fails because the repo is empty. That's expected. Copy the `*.pages.dev` address shown for the project.
6. Copy your **Account ID**: it is on the **Workers & Pages** overview, in the right-hand column *(check the official guide if a button has moved)*.
7. Create an API token: avatar → **My Profile → API Tokens → Create Token → Create Custom Token**.
   - **Name:** `pakkacover-pages`.
   - **Permissions:** **Account → Cloudflare Pages → Edit**. **Account resources:** your account.
   - Click **Continue to summary → Create Token** and copy it. It is shown once.
8. Now go back to **item 3 step 9** and add the `*.pages.dev` address to Google's Authorized JavaScript origins. If you did item 2, also set it as the Mini App H5 URL.

**You'll end with:** a site address like `https://pakkacover.pages.dev`, a 32-character hex Account ID, and an API token (about 40 characters).
**Where it goes:** the `WEB_BASE_URL=`, `PAGES_PROJECT_NAME=`, `CLOUDFLARE_ACCOUNT_ID=` and `CLOUDFLARE_API_TOKEN=` lines of `.env` (the token stays local). Claude Code sets the Pages build variables (`VITE_API_URL` and the others) through the Cloudflare API.
**Official guide (if a button has moved):** https://developers.cloudflare.com/pages/get-started/git-integration/ · https://developers.cloudflare.com/fundamentals/api/get-started/create-token/

---

## 9. Sarvam: API key and credit balance
**Why the project needs it:** Sarvam turns the buyer's Hindi or Hinglish speech into text (`saaras`) and reads high-impact lines back aloud (`bulbul`). The ₹100 signup credit is the whole speech budget. The app tracks it and switches voice off before it runs out (design §7.13, R3-M1, R3-m8).
**Cost:** free (₹100 signup credit; enough for about 30 to 35 pilot voice journeys after the demo days)   **Time:** ~5 minutes

**Steps:**
1. Go to https://indus.sarvam.ai and click **Sign Up**. Sign up with Google, and complete the verification it asks for. The credit is given to verified users.
2. Open **API Keys** at https://indus.sarvam.ai/key-management and create a new key. Copy it immediately; it is shown only once.
3. Open **Billing** at https://indus.sarvam.ai/billing and note the credit balance in rupees (it should be ₹100).
4. **On the morning of 31 Oct:** open the app's `/admin/report` (Claude Code shows you how). Go on stage only if at least ₹15 of the day's Sarvam allowance remains (R3-M1).
5. **At pilot open (item 17):** re-enter the Billing page balance, not the app's own estimate. The demo days spend about ₹30 of the credit (R3-m8).

**You'll end with:** an API key (an opaque string; the shape isn't documented) and a balance figure such as `100`.
**Where it goes:** the `SARVAM_API_KEY=` and `SARVAM_BALANCE_INR=` lines of `.env`. The build seeds the app's credit tracking from the balance.
**Official guide (if a button has moved):** https://docs.sarvam.ai/api-reference/authentication · https://docs.sarvam.ai/api-reference-docs/ratelimits

---

## 10. Anthropic: workspace, API key, monthly spend limit
**Why the project needs it:** Claude Haiku 5.5 extracts the interview answers, is the second strip reader, and extracts the Day-12 audit. Claude Sonnet 5.5 retries a failing audit section once. A hard monthly limit stops a bug from running up a bill.
**Cost:** your own credit; about ₹35 a month typical at 50 users   **Time:** ~5 minutes

**Steps:**
1. Go to https://platform.claude.com and sign in (with Google). Make sure the organization has prepaid credit (at least $5) under **Settings → Billing**.
2. Create a workspace, because spend limits can't be set on the Default workspace:
   - Open https://platform.claude.com/settings/workspaces and click **Create workspace**.
   - Name it `PakkaCover`, pick a colour, and click **Create workspace**.
3. Set the limit: on the same **Workspaces** page, select **PakkaCover**, and in the panel click **Spend limits**. Set a monthly limit of **$10** (about ₹880) and alerts at 50% and 80%.
4. Also set the organization limit as a backstop: **Settings → Billing → Spend limits → Set limit** (for example $15).
5. Create the key:
   - Open https://platform.claude.com/settings/keys and click **Create key**.
   - **Name:** `pakkacover-prod`. Choose an expiration. **Linked account:** yourself. **Workspace:** **PakkaCover**.
   - Create it and copy the key now; it is shown once.
6. You don't pick model IDs. Claude Code lists the models with your key and pins the exact IDs.

**You'll end with:** a key starting `sk-ant-api03-` (about 108 characters).
**Where it goes:** the `ANTHROPIC_API_KEY=` line of `.env`.
**Official guide (if a button has moved):** https://platform.claude.com/docs/en/get-api-key · https://platform.claude.com/docs/en/manage-claude/workspaces · https://platform.claude.com/docs/en/api/rate-limits

---

## 11. OpenAI: project, API key, monthly budget
**Why the project needs it:** `gpt-6.1-terra` is the first medicine-strip reader. `gpt-6-luna` is the interview fallback. `omni-moderation-latest` (free) screens free text and photos. `gpt-transcribe` becomes a speech fallback only if it passes the quality gate.
**Cost:** your own credit; about ₹35 a month typical at 50 users   **Time:** ~5 minutes

**Steps:**
1. Go to https://platform.openai.com and sign in. Make sure the organization has prepaid credit.
2. Hover over the **project name** (top left) and choose **Create project**. Name it `PakkaCover` and click **Create**.
3. Open **Settings** (gear icon) → **Projects → PakkaCover → Limits**. Set **Monthly spend limit** to **$10** and **Notification threshold** to 80%. If a hard-limit option is shown, turn it on. OpenAI's help page says the monthly limit is soft by default.
4. In the PakkaCover project, open **API keys → + Create new secret key**.
   - **Owned by:** You. **Project:** PakkaCover. **Permissions:** All.
   - Click **Create secret key** and copy it now; it is shown once.

**You'll end with:** a key starting `sk-proj-`.
**Where it goes:** the `OPENAI_API_KEY=` line of `.env`.
**Official guide (if a button has moved):** https://help.openai.com/en/articles/9186755-managing-your-work-in-the-api-platform-with-projects · https://platform.openai.com/docs/guides/production-best-practices

---

## 12. Golden sets: 20 voice clips and 15 strip photos (tonight; needed by 30 Oct 08:00 IST)
**Why the project needs it:** the speech and vision models are chosen and gated on **your** voices and **real** Indian medicine strips (G3 and G4 in design §7.14). On 30 Oct morning the build runs the Sarvam v4 vs v3 test on these clips and pins the winner. Only you can provide real voices and real strips.
**Cost:** free   **Time:** ~60 to 90 minutes with two helpers

**Privacy first:** say only the **scripted, made-up** lines below. Don't say real names or anyone's real health details. Photograph medicine strips only, never a prescription or label with a patient's name. The files go into the private repo.

### A. 20 voice clips → `evals/golden/stt/`
- **Who:** 3 speakers. **spk1** is you. **spk2** is a woman, ideally 45 or older (a family member). **spk3** is anyone else.
- **How:** use your phone's normal voice recorder. Hold the phone at chat distance and speak naturally, not slowly. Each clip must be **under 25 seconds**. Any common format works (`.m4a`, `.ogg`, `.webm`, `.wav`).
- **Background:** record clips 3, 6, 9, 12, 15 and 18 with a **fan** running. Record clips 4, 10, 16 and 20 with a **TV** on low. The rest are quiet.
- **File names:** `stt-NN_spkX.ext`, for example `stt-09_spk1.m4a`. `NN` is the line number below and `spkX` is the speaker.

| # | Speaker | Say exactly |
|---|---|---|
| 01 | spk1 | Haan |
| 02 | spk1 | Nahi |
| 03 | spk2 | Haan ji, sahi hai |
| 04 | spk2 | Galat hai |
| 05 | spk1 | Bawan saal |
| 06 | spk3 | Paanch saal se |
| 07 | spk3 | Din mein ek baar |
| 08 | spk3 | Pata nahi |
| 09 | spk1 | Meri mummy ko BP hai, 2019 se Telma 40 leti hain, roz subah ek goli. |
| 10 | spk1 | Mujhe sugar hai, Metformin 500 din mein do baar leta hoon. |
| 11 | spk2 | Papa ko thyroid hai, Thyronorm 50 khaali pet lete hain. |
| 12 | spk2 | Amlodipine 5 mg chal rahi hai, doctor ne teen saal pehle di thi. |
| 13 | spk3 | Cholesterol ke liye Atorvastatin 10 raat ko leti hoon. |
| 14 | spk2 | Sugar border pe hai, abhi koi dawai nahi chal rahi. |
| 15 | spk2 | Pichhle saal hernia ka operation hua tha, teen din hospital mein rahe. |
| 16 | spk2 | Telmisartan pehle leti thi, chhe mahine pehle band kar di. |
| 17 | spk1 | My mother has high blood pressure since 2019 and takes Telmisartan 40 mg once a day. |
| 18 | spk1 | I am 52 years old, 158 centimetres tall and weigh 64 kilos. |
| 19 | spk2 | No hospitalisation in the last five years. |
| 20 | spk3 | My father had a heart attack before sixty. |

Lines 05, 09 and 17 are the **stage script** lines you will say during the demo. Say them the way you will say them on stage.

### B. 15 photos → `evals/golden/vision/`
- **Strips:** borrow from the family medicine box or a chemist. You need **Telma 40** (Telmisartan 40 mg; this is the demo strip), an **Amlodipine** brand (for example Amlong 5 or Amlokind 5), a **Metformin** brand (for example Glycomet 500), **Thyronorm 50**, and an **Atorvastatin** brand (for example Atorva 10 or Storvas 10).
- **How:** use the normal phone camera. If it shoots in a 48 or 50 MP mode, switch to 12 MP. Photograph the **back** of the strip (where the composition is printed) unless the line says otherwise.
- **File names:** `vis-NN_<what>.jpg`.

| # | File name | What to shoot |
|---|---|---|
| 01 | `vis-01_telma40_clean.jpg` | Telma 40, back, flat, good light (**the demo strip**) |
| 02 | `vis-02_telma40_glare.jpg` | Telma 40, back, with light glare across the foil |
| 03 | `vis-03_amlodipine_curved.jpg` | Amlodipine strip, back, bent into a curve |
| 04 | `vis-04_amlodipine_carton.jpg` | Amlodipine carton (box), side with the composition |
| 05 | `vis-05_metformin_torn.jpg` | Metformin strip, back, torn (a few pockets missing) |
| 06 | `vis-06_metformin_clean.jpg` | Metformin strip, back, flat |
| 07 | `vis-07_thyronorm_bottle.jpg` | Thyronorm bottle or box label |
| 08 | `vis-08_atorvastatin_glare.jpg` | Atorvastatin strip, back, with glare |
| 09 | `vis-09_atorvastatin_clean.jpg` | Atorvastatin strip, back, flat |
| 10 | `vis-10_other_chronic.jpg` | Any other BP, sugar, thyroid or cholesterol strip at home |
| 11 | `vis-11_blur_motion.jpg` | Telma 40, deliberately moved while shooting (blurred) |
| 12 | `vis-12_blur_focus.jpg` | Metformin, out of focus (tap-to-focus on the background) |
| 13 | `vis-13_blur_far.jpg` | Any strip, shot from far away so the text is tiny |
| 14 | `vis-14_handwritten_1.jpg` | On plain paper, write by hand: `Tab Telma 40  1-0-0` |
| 15 | `vis-15_handwritten_2.jpg` | On plain paper, write by hand: `Glycomet 500  1-0-1` |

### C. One label file → `evals/golden/vision/labels.csv`
Type exactly what is **printed** on each strip, so the test knows the truth. Use Notepad and save it as `labels.csv`:

```
file,brand,salt_text,strength,expected
vis-01_telma40_clean.jpg,Telma 40,Telmisartan Tablets IP,40 mg,read
vis-11_blur_motion.jpg,,,,null
vis-14_handwritten_1.jpg,,,,please_type
```

Write one line per photo, 15 in total. Copy `salt_text` and `strength` exactly as printed. For `expected`, use `read` for photos 01 to 10, `null` for the blurred photos 11 to 13, and `please_type` for the handwritten photos 14 and 15.

### D. Getting the files to the laptop
Copy everything over USB or Google Drive into the project folder: `evals/golden/stt/` and `evals/golden/vision/`. If a folder doesn't exist yet, create it.

**You'll end with:** 20 audio files, 15 photos and one `labels.csv`.
**Where it goes:** the folders above (not `.env`). Tell the build prompt who spk1 to spk3 are (item 13).
**Official guide (if a button has moved):** design §7.14 (G3, G4) in `architecture.md`

---

## 13. Fixed choices for the build prompt (not secrets)
**Why the project needs it:** some decisions are yours alone: names, who answers complaints, and how the advisor button is labelled. Claude Code writes them into the consent notice, the `/privacy` page and the screens.
**Cost:** free (an optional new Gmail address)   **Time:** ~10 minutes

**Steps:**
1. **Product name:** `PakkaCover`. **Team:** `Solidary` (Paytm Build for India AI Hackathon, Track 2). **Builder:** Baharul Islam.
2. **Grievance officer:** a named person and an email address. These are published in the notice and on `/privacy`, and the law requires an answer within 90 days.
   - The default is you, Baharul Islam.
   - For the email, create a dedicated free Gmail (for example `pakkacover.help@gmail.com`, whatever is available) at https://accounts.google.com/signup, turn on its 2-Step Verification, and save its login in Bitwarden. Or use your own email.
3. **Advisor button label:** until you have a named, IRDAI-licensed partner who agrees (item 17), the label is **"Pilot callback within 24 h"**. It is never a dead button.
4. **Speakers for item 12:** for example `spk1 = Baharul, M, under 45, Assam accent; spk2 = F, 45+, Assam; spk3 = M, under 45, …`. The evals report results per age band, sex and accent.
5. **Paytm status:** whether item 1 worked ("staging keys present" or "staging keys unavailable"), and whether item 2 worked.
6. **Fixed by the design** (repeat them so the build never asks):
   - repo `<you>/pakkacover`, Render service `pakkacover-api`, Pages project `pakkacover`
   - API Dockerfile at `apps/api/Dockerfile`, web app at `apps/web`
   - GitHub repository-level secrets, not environments (GitHub Free private-repo limit, item 4 step 5)
   - start in the `demo` profile (`payments_mode=staging_demo`, ₹1.00 TEST order, Sarvam cap ₹40 a day, global cap ₹150 a day); switch to `pilot` (payments off, ₹10 and ₹60 caps) before the first real user
   - no email domain; email stays off
   - CDCI drug data not loaded (hand seed only)

**You'll end with:** a short list of choices.
**Where it goes:** tell it in the build prompt. These are not secrets and don't go in `.env`.
**Official guide (if a button has moved):** design §7.10, §7.12, §7.21 and the production gate round 3 (R3-M1, R3-M2) in `architecture.md`

---

## 14. Key escrow into Bitwarden plus an offline copy (when the build prints "keys generated")
**Why the project needs it:** Claude Code **generates** the encryption keys locally: `FERNET_KEYS`, `PEPPER`, the `age` key pair for backups, the database role passwords, and the internal tokens. If they are lost, every encrypted health record and every backup becomes unreadable for good. Only you can keep the recovery copy (design §7.13 GM-9, §7.21 item 1).
**Cost:** free   **Time:** ~15 minutes, tonight while the build runs; repeat after any key rotation

**Steps:**
1. Wait for the build to print a notice like **"KEYS GENERATED: move secrets/escrow-bundle.txt into escrow"**. Claude Code never prints a secret value into the chat. It writes the generated values into your `.env` and into the local file `secrets/escrow-bundle.txt` (which git ignores). The bundle also contains the **`age` private key**, which exists nowhere else: not in `.env`, not on Render, not on GitHub. GitHub gets only the public key.
2. Open `secrets/escrow-bundle.txt` in Notepad.
3. In the Bitwarden web vault, click **New → Secure note**. Name it `PakkaCover escrow 2026-10-30` and paste the **whole** file into the note. Click **Save**. (Bitwarden Free has no attachments, so paste the text.)
4. Make the offline copy. Either print the note and seal it in an envelope, or save it to a USB stick encrypted with VeraCrypt or BitLocker. Keep it in a **second physical place**, away from your laptop: for example at home in Barpeta while you travel to Bengaluru. Optionally, a trusted second person can hold a sealed copy.
5. Delete the bundle: in Explorer select `secrets/escrow-bundle.txt`, press **Shift+Delete**, and confirm. Or tell Claude Code "escrow done, delete the bundle" and it deletes the file.
6. Whenever Claude Code later rotates a key (runbook 5), it writes a new bundle. Repeat steps 2 to 5 the **same day**, then delete the old Bitwarden note.

**You'll end with:** one Bitwarden secure note, one offline copy in a second place, and no bundle file left on disk.
**Where it goes:** Bitwarden and the offline copy only. The generated values are already in `.env`, Render and GitHub, placed by Claude Code.
**Official guide (if a button has moved):** https://bitwarden.com/help/managing-items/

---

## 15. UptimeRobot: three monitors (when the build prints "monitor URLs")
**Why the project needs it:** a check every 5 minutes keeps the free Render server awake (it sleeps after 15 minutes) and keeps both Supabase projects from pausing. The keyword monitor is how alarms reach your phone: high error rate, Sarvam credit low, spend cap hit, a stale backup, and so on (design §7.15, §7.16).
**Cost:** free (50 monitors, 5-minute interval)   **Time:** ~10 minutes, after the first deploy (30 Oct evening)

**Steps:**
1. Go to https://uptimerobot.com, sign up for the **Free** plan, verify your email, and turn on MFA (item 0).
2. Make sure your own email inbox has phone notifications on. Email is the guaranteed alert channel. Also install the UptimeRobot mobile app; whether push works on the Free plan is **[verify]**.
3. Wait for the build's notice **"MONITOR URLS written to secrets/escrow-bundle.txt"**. Two of the URLs contain secret tokens, so they are in the bundle, not in chat. Then click **+ New monitor** three times:
   - **Monitor 1:** **Monitor type** HTTP(s). **URL** `<API_BASE_URL>/ready`. **Friendly name** `PakkaCover prod ready`. **Interval** 5 minutes. **Notify** your email. If offered, alert only after **2** failures.
   - **Monitor 2:** **Monitor type** Keyword. **URL** the `/internal/alarms/<token>` URL from the bundle. **Keyword** `OK`. Alert when the keyword **does not exist**. **Interval** 5 minutes. **Friendly name** `PakkaCover alarms`.
   - **Monitor 3:** **Monitor type** HTTP(s). **URL** the `/ready-staging/<token>` URL from the bundle. **Interval** 5 minutes. **Friendly name** `PakkaCover staging keep-awake`.
4. Click **Create monitor** for each one *(check the official guide if a button has moved)*. Within 10 minutes all three should be green.

**You'll end with:** three green monitors and an alert email address you will actually see.
**Where it goes:** nowhere in `.env`. The monitors live in UptimeRobot.
**Official guide (if a button has moved):** https://uptimerobot.com/help/ · https://uptimerobot.com/keyword-monitoring/

---

## 16. Demo-phone runs and the Supabase Security Advisor glance (30 Oct evening, 31 Oct morning)
**Why the project needs it:** the end-to-end gate (G8) is three full Sunita journeys on **your phone over mobile data**, under 5 minutes each. Claude Code can't hold the phone. One console check also needs your eyes.
**Cost:** free (a few rupees of Sarvam credit, inside the demo cap)   **Time:** ~25 minutes on 30 Oct after deploy, ~20 minutes on 31 Oct morning

**Steps:**
1. **30 Oct, about 20:00, after the deploy:** on your phone, with Wi-Fi **off**, open the Pages URL in **Chrome** (not inside Instagram or WhatsApp).
2. Run the Sunita journey three times in a row, following Claude Code's script. Use lines 05, 09 and 17 from item 12 and photo `vis-01`. Sign in with the **demo Google account** (item 3 step 10), which is not a test user. Pay with the test card (CVV `123`) if item 1 worked. Tell Claude Code the time each run took and anything that looked wrong.
3. **Supabase Security Advisor:** in each project, open **Advisors → Security Advisor**. The only expected findings are **"RLS disabled"** on the `app` tables. That is accepted by design: the Data API is off and access is grant-only. Tell Claude Code if you see anything else *(check the official guide if a button has moved)*.
4. **31 Oct morning at the venue:** repeat one run on the venue network. Check the Sarvam allowance in `/admin/report` (item 9 step 4). Open the API URL 5 minutes before you go on stage so the server is awake.

**You'll end with:** three timed runs reported to Claude Code, and the advisor check confirmed.
**Where it goes:** tell it to Claude Code in chat. No secrets are involved.
**Official guide (if a button has moved):** https://supabase.com/docs/guides/database/database-advisors

---

## 17. Paperwork before the first real user (1 to 14 Nov; not needed for the finals)
**Why the project needs it:** real users bring legal duties under DPDP, the SPDI Rules, CERT-In and IRDAI. These are signatures, readings and agreements that only you can give (design §7.12, §7.18 phase 2 items 9 and 10, §7.21 items 13 to 18).
**Cost:** free   **Time:** ~2 to 3 hours spread over the week

**Steps:**
1. **Licensed advisor:** ask an IRDAI-licensed broker or POSP you know whether they will take pilot callbacks and hold the single "Pause new intake" button. If they agree, give Claude Code their name and licence number. They enrol their own authenticator at first sign-in. If nobody agrees, the "Pilot callback within 24 h" label stays.
2. **DPAs:** for each processor (OpenAI, Anthropic, Supabase, Render, Neon, Cloudflare, GitHub, Google, Sarvam, UptimeRobot), find the vendor's Data Processing Addendum. Search "<vendor> DPA" on the vendor's own site. Accept or sign it where a form exists; otherwise download the PDF. Save each one into `docs/dpa/` as `<vendor>-dpa-<date>.pdf`. For Sarvam and UptimeRobot, if there's no public DPA, email their support and save the reply.
3. **CERT-In:** read the CERT-In Directions of 28 April 2022 on cert-in.org.in. Confirm the 6-hour reporting rule and the address `incident@cert-in.org.in`, then tell Claude Code "CERT-In confirmed" (or what differs) so the breach runbook is marked primary-checked.
4. **Vendor usage policies:** read the Anthropic and OpenAI usage policies for a consumer health and insurance-education app. Tell Claude Code your conclusion, and it records it in `docs/`.
5. **CDCI drug data (optional):** if you want the full government brand list, download the CDCI package and read `License.txt`. Tell Claude Code "CDCI licence OK to use" only if it allows this use.
6. **Google privacy link:** in Google Auth Platform → **Branding**, add **Application Homepage link** `<WEB_BASE_URL>` and **Application Privacy Policy link** `<WEB_BASE_URL>/privacy`, then **Save**. **[verify]** Google may not accept a `pages.dev` address as an authorized domain. If it refuses, leave the links empty; basic-scope sign-in keeps working.
7. **Sarvam balance at pilot open:** re-enter the Billing page figure (item 9 step 5).

**You'll end with:** a named advisor or a deliberate "pilot callback" label, ten DPAs in `docs/dpa/`, and three confirmations given to Claude Code.
**Where it goes:** `docs/dpa/`, and tell it to Claude Code. No `.env` lines.
**Official guide (if a button has moved):** https://www.cert-in.org.in · https://support.google.com/cloud/answer/15549049 (branding)

---

## 18. Optional, off by default: email domain plus Resend (about ₹100 to ₹900 a year)
**Why the project needs it:** without a domain, date reminders work through the in-app card and the calendar (`.ics`) file. A domain adds email sign-in codes and email reminders. Skip it for the finals.
**Cost:** about ₹100 to ₹900 a year for the domain; Resend Free covers 100 emails a day   **Time:** ~30 minutes plus DNS wait

**Steps:**
1. Buy a domain at any registrar. Turn on **auto-renew** and MFA.
2. Sign up at https://resend.com and open **Domains → Add Domain**. Enter the domain.
3. Add the SPF, DKIM and DMARC records Resend shows at your registrar's DNS page. Use DMARC `p=none` first and `p=quarantine` after a week.
4. Back in Resend, click **Verify**. Then open **API Keys → Create API Key**, choose **Sending access**, and copy the key.
5. In UptimeRobot, add a domain-expiry and SSL monitor for the domain.
6. Tell Claude Code "email domain added". It turns on `email_enabled`.

**You'll end with:** a verified domain and a Resend key starting `re_`.
**Where it goes:** the `RESEND_API_KEY=` and `EMAIL_FROM=` (for example `PakkaCover <no-reply@yourdomain.in>`) lines of `.env`. Leave both blank if you skip this item.
**Official guide (if a button has moved):** https://resend.com/docs/dashboard/domains/introduction

---

## 19. The .env file
1. In the project folder, create a file named exactly `.env`.
2. Paste this template into it, then fill every **"YOU PASTE"** line with the values from the items above. Keep **every value inside double quotes**; Paytm keys often contain `#`. Leave every **"generated by the build"** line empty. Claude Code fills those lines itself, writing them straight into the file without printing them.

```env
# =====================================================================
# PakkaCover .env  (never commit, never share, never paste into a chat)
# Tags show where Claude Code pushes each value:
#   [local]  stays in this file only
#   [render] Render service env vars (pushed via RENDER_API_KEY)
#   [github] GitHub repository Actions secrets (pushed via GH_TOKEN)
#   [pages]  Cloudflare Pages build variables (pushed via CLOUDFLARE_API_TOKEN)
# =====================================================================

# ---------------- A. YOU PASTE: Paytm PG staging (item 1) -------------
PAYTM_ENVIRONMENT="staging"                                   # [render] fixed
PAYTM_MID=""                                                  # [render] Test Merchant ID
PAYTM_MERCHANT_KEY=""                                         # [render] Test Merchant Key, keep the quotes
PAYTM_WEBSITE="WEBSTAGING"                                    # [render] fixed for staging
PAYTM_HOST="https://securestage.paytmpayments.com"            # [render] fixed for staging

# ---------------- A. YOU PASTE: Paytm Mini App (item 2, optional) -----
PAYTM_MINIAPP_ID=""                                           # [render] blank = Paytm login off
PAYTM_MINIAPP_CLIENT_ID=""                                    # [render]
PAYTM_MINIAPP_CLIENT_SECRET=""                                # [render] server only, never front end
PAYTM_AUTH_HOST="https://accounts-uat.paytm.com"              # [render] UAT auth host

# ---------------- A. YOU PASTE: Google sign-in (item 3) ---------------
GOOGLE_OAUTH_CLIENT_ID=""                                     # [render] ...apps.googleusercontent.com

# ---------------- A. YOU PASTE: AI and speech (items 9 to 11) ---------
ANTHROPIC_API_KEY=""                                          # [render] sk-ant-api03-...
OPENAI_API_KEY=""                                             # [render] sk-proj-...
SARVAM_API_KEY=""                                             # [render]
SARVAM_BALANCE_INR=""                                         # [render] dashboard balance, e.g. "100"

# ---------------- A. YOU PASTE: databases, admin bootstrap (items 5, 6)
SUPABASE_PROD_ADMIN_URL=""                                    # [local] session pooler :5432, postgres.<ref>
SUPABASE_STAGING_ADMIN_URL=""                                 # [local] same, staging project
NEON_ADMIN_URL=""                                             # [local] neondb_owner, direct, sslmode=require

# ---------------- A. YOU PASTE: GitHub (item 4) -----------------------
GITHUB_REPO=""                                                # [local] <your-username>/pakkacover
GH_TOKEN=""                                                   # [local] github_pat_... fine-grained

# ---------------- A. YOU PASTE: Render (item 7) -----------------------
RENDER_API_KEY=""                                             # [local] rnd_...
RENDER_SERVICE_ID=""                                          # [local] srv-...
RENDER_DEPLOY_HOOK=""                                         # [github] https://api.render.com/deploy/srv-...?key=...
API_BASE_URL=""                                               # [github] https://pakkacover-api.onrender.com

# ---------------- A. YOU PASTE: Cloudflare Pages (item 8) -------------
CLOUDFLARE_ACCOUNT_ID=""                                      # [local]
CLOUDFLARE_API_TOKEN=""                                       # [local] Pages:Edit only
PAGES_PROJECT_NAME="pakkacover"                               # [local] change if Cloudflare gave another name
WEB_BASE_URL=""                                               # [render] https://pakkacover.pages.dev (CORS allowlist)

# ---------------- A. YOU PASTE: optional email (item 18) --------------
RESEND_API_KEY=""                                             # [render] blank = email off (default)
EMAIL_FROM=""                                                 # [render] PakkaCover <no-reply@yourdomain.in>

# ---------------- B. GENERATED BY THE BUILD: leave empty --------------
# Claude Code generates these locally, writes them here and into
# secrets/escrow-bundle.txt, and never prints them. You escrow them (item 14).
FERNET_KEYS=""                       # generated by the build  [render] comma-separated, newest first
PEPPER=""                            # generated by the build  [render] HMAC pepper for email_hmac/subject_hmac
AGE_PUBLIC_KEY=""                    # generated by the build  [github] backup encryption (private half: escrow only)
DATABASE_URL_APP=""                  # generated by the build  [render] pc_app, prod
DATABASE_URL_PURGE=""                # generated by the build  [render] pc_purge, prod (1-year log purge)
DATABASE_URL_MIGRATE=""              # generated by the build  [github] pc_migrate, prod (deploy job)
DATABASE_URL_BACKUP=""               # generated by the build  [github] pc_backup, prod (nightly dump)
STAGING_DATABASE_URL_APP=""          # generated by the build  [render][github] staging keep-awake + role test
STAGING_DATABASE_URL_MIGRATE=""      # generated by the build  [github] migrate staging first
STAGING_DATABASE_URL_PURGE=""        # generated by the build  [github] role test
STAGING_DATABASE_URL_BACKUP=""       # generated by the build  [github] role test pg_dump
NEON_DATABASE_URL=""                 # generated by the build  [github] restore-only role on Neon
INTERNAL_JOB_TOKEN=""                # generated by the build  [render][github] /internal/tick and /internal/job-report
ALARMS_PATH_TOKEN=""                 # generated by the build  [render] secret path of /internal/alarms/<token>
STAGING_READY_TOKEN=""               # generated by the build  [render] secret path of /ready-staging/<token>
DEMO_LOGIN_PASSPHRASE=""             # generated by the build  [render] demo profile only; removed in phase 2

# ---------------- C. FILLED BY THE BUILD FROM SECTION A: leave empty --
VITE_API_URL=""                      # generated by the build (= API_BASE_URL)            [pages]
VITE_GOOGLE_CLIENT_ID=""             # generated by the build (= GOOGLE_OAUTH_CLIENT_ID)  [pages] public
VITE_PAYTM_MID=""                    # generated by the build (= PAYTM_MID)               [pages] public (CheckoutJS URL)
VITE_PAYTM_HOST=""                   # generated by the build (= PAYTM_HOST)              [pages]
VITE_PAYTM_MINIAPP_CLIENT_ID=""      # generated by the build (= PAYTM_MINIAPP_CLIENT_ID) [pages] public

# ---------------- D. TUNING (pre-filled; the build may change after measuring)
TRUSTED_HOPS="1"                     # [render] set by the header-echo experiment in the deploy slot
MEDIA_HEADROOM_MB="150"              # [render] set from the measured media-worker baseline

# Not in .env on purpose:
# - DEMO_MODE no longer exists. Demo vs pilot behaviour (payments_mode, per-IP
#   limits, Sarvam/global caps, CSP mode, demo login) lives in
#   infra/profiles/{demo,pilot}.json, applied by scripts/set_profile.py (R3-M2).
#   PAYMENTS_MODE is set there: staging_demo in "demo", off in "pilot".
# - The age PRIVATE key, staff TOTP secrets and the Supabase/Neon master
#   passwords live only in escrow (item 14) and Bitwarden.
# - UptimeRobot needs no key; you create its monitors by hand (item 15).
```

3. Three rules:
   - `.env` is never committed or shared.
   - Never paste its values into any chat.
   - Claude Code never prints it or shows any of its values. It loads them into the environment while building, adds the values it generates without echoing them, and passes them to Render, GitHub and Cloudflare by API without displaying them.
