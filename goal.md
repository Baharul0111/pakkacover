# PakkaCover — Goal

## The goal

PakkaCover is a phone app that sits inside a family's health insurance purchase and makes sure the claim will actually pay later. It is built by Baharul Islam (Team Solidary) for real families and for the Paytm Build for India AI Hackathon finals in Bengaluru on 31 October 2026.

Most rejected health claims in India are lost on the day the policy is bought: an illness that was never declared, a family that never knew what was covered, a claim made while a waiting period was still running. PakkaCover fixes this at the moment of purchase. The buyer talks to it for about three minutes in Hindi, English or a mix of both, and photographs their medicine strips. It turns that into an honest medical declaration, and the buyer checks and confirms every single line. It then shows a few real sample plans in order of how much each would actually pay this family, with every rupee and every date linked to the exact sentence in the plan's own wording. It gives the buyer a one-screen Promise Card that says, in plain words, what is covered and from which exact date, and it reminds them as those dates arrive. On day 12 after buying, it reads the policy the insurer sent and compares it with what the buyer declared and what they were promised, so any mistake is caught while it can still be fixed, or the policy cancelled for free, before day 30.

The golden rule of the whole product is "the AI listens and reads, plain tested counting does the maths". No AI ever decides a rupee amount or a date. A person is always in charge: nothing is sent to any insurer, no plan is ever called "best", nothing is sold, and a human advisor is one tap away on every screen.

It works in an ordinary phone browser and is built to Paytm's Mini App rules, so it can run inside the Paytm app. It uses Paytm's real test payment system, never real money. It keeps no voice recordings, photos or policy files, locks every health detail so only the app can read it, and lets people take or delete their data at any time. It runs on free hosting. The only running costs are small amounts of AI usage on the owner's own OpenAI and Anthropic keys, plus a free speech credit, about three to five rupees per buyer, with hard daily limits so costs can never run away.

## What it must do

1. **Works on any phone, in Hindi and English.** It opens in a normal phone browser and inside the Paytm app, with large buttons and simple screens. Every screen is available in Hindi and English, and people can answer in either or a mix of both. If someone opens it inside Instagram or another app's built-in browser where sign-in won't work, it tells them how to open it in Chrome or Safari without losing their progress.

2. **Asks for consent first, clearly and separately.** Before any health question it shows a plain notice listing exactly what it will collect and why, who helps process it, and how to withdraw or complain. The buyer chooses separately: build my declaration, send me date reminders, and check my policy later. A fourth choice, keep my claim record, is offered when they save. Each choice can be changed at any time.

3. **Handles the whole family carefully.** The buyer adds who is to be covered, with age and sex. For each adult they confirm "they know and agree"; for each child, "I am the parent or guardian". Children are never asked about tobacco or alcohol.

4. **Asks the questions an insurer's medical call would ask.** It asks about height and weight, illnesses and since when, medicines with dose and how often, hospital stays and operations, tests in the last six months, tobacco and alcohol, and family history. Follow-up questions depend on the answers, for example asking about the kidneys or heart when someone has BP. It asks one clear question at a time.

5. **Lets people answer by voice, and never gets stuck if voice fails.** The buyer holds a button and speaks. The app understands everyday Hindi, English and Hinglish, including medicine names. If speech is not understood, or the microphone is not available inside Paytm, the same question appears with tap buttons and a typing box. Short yes/no answers always have Haan and Nahi buttons.

6. **Reads medicine strips from a photo, and never guesses.** The buyer photographs the back of a printed strip or box. Two separate AI readers read the printed name and strength, and the app only trusts them when they agree. If they disagree, the buyer sees the photo and both readings and chooses. Because one medicine can treat several conditions, the app always asks what it is taken for ("Telmisartan BP ke liye hai, ya kidney/dil ke liye?"). It offers "I don't know", which becomes "condition to be confirmed by doctor". Handwritten prescriptions are politely declined with "please type it".

7. **Makes the buyer confirm every line, one by one.** Every fact becomes one card written the way a proposal form would say it, for example "Member 2 (F, 52): Hypertension since about 2019, on Telmisartan 40 mg once daily". The important lines are read aloud. Each card has "Sahi hai", "Galat" and "Badlo", and "Galat" or "Badlo" goes straight back to that question. Anything the AI heard rather than the buyer tapped is marked "check this". There is no "confirm all" button. Nothing is ever sent to an insurer.

8. **Uses real plans, labelled honestly as samples.** It contains the terms of three real Indian health plans taken word for word from their public policy wordings: HDFC ERGO my:Optima Secure (Plan A), Care Supreme with the Instant Cover add-on (Plan B) and Tata AIG MediCare Premier (Plan C). A fourth, Niva Bupa ReAssure 2.0, is added after the finals. Every plan screen says "Sample terms from public policy wording — education only". Every term in the app can be traced to the exact sentence and page it came from, and is checked against the plan's own document.

9. **Ranks plans by what they would pay this family, never by price and never with a "best" label.** For the conditions the buyer confirmed, it works out what each plan would pay on a published set of example claims at different points in time (for example a BP-related hospital stay in months 3, 18 and 30, plus an accident and, for older members, a cataract operation). The buyer can adjust the example amounts with sliders. Plans are listed by total modelled payout, with the per-claim table shown and a "how we rank" page one tap away. No "best", "top" or "recommended" words, badges, stars or logos appear anywhere. Premiums are not shown. Instead it marks where an add-on is needed and says honestly that declaring a condition can change the premium, which the insurer decides.

10. **Shows where every number comes from.** Every date and rupee amount on every screen can be tapped to show the exact sentence from the plan's wording that produced it, and the steps that led to the number ("kyun?"). If any term is unclear, the app says "check with an advisor" instead of guessing. Where a date sits on a boundary, it always picks the safer side for the buyer: cover never starts earlier, and deadlines never fall later.

11. **Gives a Promise Card with exact dates.** One screen per chosen plan, in Hindi and English. It shows when accidents are covered (from day one), when most illnesses are covered (from the 31st day), and the exact date each declared condition is covered, such as BP from day 31 on Plan B. It also shows when listed operations like cataract and hernia are covered, the main things never covered, the five-year date after which non-disclosure can no longer be held against the buyer, and the last day to cancel for free. All of it is calculated, never written by AI.

12. **Reminds people as their dates arrive, for free.** An "upcoming dates" list appears every time the app is opened. In a normal browser the buyer can also add all the dates to their phone calendar with one tap. Reminder text never names a medical condition. A reminder on day 12 prompts the buyer to upload their policy for checking. Email reminders are switched on only if the owner later adds an email domain.

13. **Lets people save their record without forcing a login early.** Everything up to the Promise Card works without signing in. Sign-in is asked for only when the buyer wants to save, get reminders or run the policy check. That is Google sign-in in a normal browser and Paytm login inside Paytm. A one-time demo sign-in exists only in demo mode and is protected by a passphrase.

14. **Shows a real Paytm test payment, clearly labelled.** For the finals, a ₹1 test order goes through Paytm's real test payment system with Paytm's test card, wallet or UPI. It is only marked as paid after Paytm's own system confirms it. A red banner says "TEST PAYMENT — koi paisa nahi katega. Launch par yeh step licensed broker ka checkout hoga". Real pilot users never see a payment step; they are handed to the advisor instead.

15. **Checks the issued policy on day 12 and catches mistakes before day 30.** The buyer uploads the policy document the insurer sent. For the demo, the app can make sample policy documents, one clean and three with planted mistakes: the Instant Cover add-on missing, a declared condition missing, and a wrong date of birth. The app reads the document section by section and checks every value against the actual sentence on the page. It then compares the result with the buyer's confirmed declaration and the Promise Card. Each difference is shown as a flag with both sentences side by side, what it means in plain words, and the actions: get the insurer to fix it, cancel for free by the last free-look date, or talk to an advisor. Anything it cannot confirm is marked "please check by hand". It never says "your policy is wrong". It must catch all three planted mistakes and raise no false alarm on the clean one.

16. **Keeps a human advisor one tap away.** Every screen has "Advisor se baat karein". Tapping it creates a request with a short prepared summary for the advisor. Until a licensed partner is named, the button is honestly labelled "pilot callback within 24 hours"; it is never a dead button.

17. **Protects health data and respects people's rights.** Voice recordings, photos and policy files are never stored; they are used and thrown away. Every health detail is locked so that only the app can read it, including inside backups. One family can never see another family's data, whatever they try. People can download everything about themselves and delete it instantly. Unsaved visits are deleted within 48 hours, and saved records are deleted after the free-look period unless the buyer chose "keep my claim record" (kept until their five-year date). Only a log of what happened, with no health details in it, is kept for one year, as the law requires. A privacy page and a named grievance contact are available in both languages. Logging out never deletes anyone's record.

18. **Never lets the AI decide money or dates.** The AI only listens, reads and words the questions politely. Every date, rupee amount, ranking, Promise Card line and policy-check result comes from plain tested calculations. If an AI-worded question contains any number that was not in the buyer's own answers, the app throws that wording away and uses its standard question instead. Text from documents, photos or speech is always treated as information, never as instructions.

19. **Keeps working when something breaks.** Every AI step has a non-AI fallback: typing and buttons instead of voice, text instead of read-aloud, manual medicine entry, and manual policy-field entry with the comparison still working. The owner can switch any part off instantly without redeploying. Every outside call has a time limit, so the app never hangs. When the free server is waking up, the buyer sees a friendly "server jag raha hai" message instead of an error.

20. **Keeps costs tiny and capped.** Hosting is free. AI usage costs about three to five rupees per buyer on the owner's own keys and the free speech credit. Daily spending limits, a separate daily limit for speech, and per-visit limits switch the costly parts off before money runs away, and the app tracks how much free speech credit is left.

21. **Is safe to run as a real pilot.** Advisors and admins sign in with Google plus a second code from an authenticator app, and every time staff look at someone's health record it is logged. The app is protected against people flooding it or faking their location. Seven daily encrypted backups and a standby copy are kept, and a full restore has been tested using only the escrowed keys. The owner is alerted when the app is down, errors spike, costs or speech credit run low, a scheduled job is late, or a safety switch has tripped. The advisor can pause new sign-ups with one button, and new sign-ups pause automatically if an alarm stays unanswered for 72 hours.

22. **Has a demo mode and a pilot mode that can't be confused.** Demo mode (for the finals) speaks every question aloud, allows the ₹1 test payment and the passphrase demo sign-in, and has higher limits for the venue Wi-Fi. Pilot mode (for real users) turns all of that off. The app shows which mode it is in, raises an alarm if demo mode is ever live for real users, and has a tested checklist for opening the pilot.

23. **Delivers the Sunita story on stage in under five minutes.** On the demo phone over mobile data, Sunita (52, BP tablet) consents, speaks in Hindi, photographs a Telma 40 strip, confirms "Telmisartan for hypertension", and sees the three plans ranked B, C, A with clause-linked amounts. She then gets her Promise Card with exact dates, completes the ₹1 Paytm test payment, and watches the day-12 check catch a planted mistake. This must run cleanly three times in a row. A demo-ready version is frozen and labelled by 10 pm on 30 October 2026, and a fallback video of the full journey is recorded.

24. **Is ready for Paytm, honestly.** It follows Paytm's Mini App rules: Paytm login and Paytm payment only inside Paytm, camera only after asking permission, and no links out of Paytm. It contains Paytm's real login flow, ready to switch on once Mini App credentials exist. The deck line it supports is: "Built to Paytm Mini App spec, running on real Paytm PG staging".

25. **Proves its quality before anyone uses it.** It comes with test sets that must pass before the demo:
    - every date and payout calculation correct, including month-ends and leap years;
    - every plan sentence found in its source document;
    - 20 real recorded voice clips understood well enough, with medicine names and numbers kept intact;
    - 15 strip photos read without inventing any medicine;
    - 10 Hinglish conversations turned into the right facts;
    - all 3 planted policy mistakes caught;
    - no AI number ever slipping through;
    - one family never able to see another's data, and deletion removing everything.

    Before real users it must also pass:
    - a test with 5 to 8 people, including low-literacy users, catching at least 80% of deliberately wrong lines;
    - a medicine-table accuracy check;
    - a load test at twice the expected peak;
    - a basic security scan;
    - a restore drill.

26. **Is documented for the owner.** Short step-by-step guides (runbooks) cover the common emergencies: the app is down, the database is paused or blocked, an AI service is down, the speech credit ran out, keys need changing or restoring, and pausing the pilot. A breach plan follows India's reporting deadlines: report to CERT-In within 6 hours, and the Data Protection Board's 72-hour detailed report. A written plan describes how the product grows from 50 users to Paytm scale.

## How we know it is finished

PakkaCover is finished when the whole thing can be set up fresh from this folder and every item above works from start to finish. First the demo version runs the Sunita story cleanly three times in a row on a phone over mobile data, and is frozen by 10 pm on 30 October 2026. Then the full pilot version is complete, with every protection, reminder, deletion, backup, alert and pilot-mode safety in place. Every behaviour listed above must be proven by automated tests that pass, plus the recorded results of the human, load, security and restore checks. Nothing counts as done because it "should work". Two steps wait for Baharul's explicit go-ahead because they are public and hard to undo: switching the app to pilot mode and inviting real users, and submitting the Mini App to Paytm for review.
