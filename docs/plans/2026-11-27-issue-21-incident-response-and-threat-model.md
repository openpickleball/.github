# Plan: Add an incident response plan, a threat model, and dedicated report inboxes (issue #21)

Risk tier: Medium. Docs only, no code, but SECURITY.md makes public promises (fix targets, a disclosure window) that researchers and players will hold OPEN to, and the change spans several files.

Domain skills: humanizer: invoke (new public-facing prose). superpowers:test-driven-development: not applicable because no code or test changes; the gate is the existing script tests and the pull request check. django, django-ninja-api, django-allauth, django-celery, python-fastapi, react, expo, frontend-design, dataviz: not applicable because the change is Markdown only.

## Decisions (from the user, 2026-11-27)

- Report addresses: keep `info@openpb.org` in this pull request. The `security@` and `conduct@` aliases do not exist yet. Switching SECURITY.md, CODE_OF_CONDUCT.md, SUPPORT.md, and backend's `security.txt` contact to them is a follow-up issue.
- Fix targets: Critical 7 days, High 30 days, Medium 90 days, Low best effort. Coordinated disclosure 90 days after the report, or sooner once a fix ships. Both clocks count from the day the report arrives (user decision in review), so an on-time fix never lands after disclosure. Fixes to OPEN code are announced as GitHub security advisories with credit; other problems in the public incident summary, also with credit.
- Location: `docs/security/` in this repository, since the plan covers every repository and hosted service.
- Secret scanning: turn on non-provider patterns and validity checks on every repository now, with `gh api`.

## Current state (measured 2026-11-27)

- Secret scanning: `PATCH repos/openpickleball/<repo>` with `secret_scanning_non_provider_patterns` and `secret_scanning_validity_checks` set to `enabled` returned 200 on all eight repositories, but both stayed `disabled`. The organization is on GitHub's Free plan (`gh api orgs/openpickleball --jq .plan.name` prints `free`), and both features belong to the paid GitHub Secret Protection add-on. Basic secret scanning (provider patterns) is `enabled` everywhere. This task stays open on #21 until the plan changes or GitHub offers the features to public repositories on Free.
- `security.txt` is served by backend (`config/security_txt.py`); its `Contact` comes from the `SECURITY_TXT_CONTACT` environment setting.
- SECURITY.md promises acknowledgment within 5 business days and nothing about fix times, disclosure, or advisories.
- GOVERNANCE.md already says security records are published in summary until the fix ships and in full after ("Administrative access"), and that confidential matters are published in summary ("Meetings and votes"). It names the steward as interim decision maker and a backup owner for when the primary owner cannot be reached.

## Acceptance criteria

1. `docs/security/incident-response.md` exists and covers:
   - Who is on point: during the founding phase, the steward (primary owner) leads every incident; the backup owner takes over under the triggers GOVERNANCE.md lists (primary owner unreachable, primary owner's account compromised, or asked in writing). After the board is seated, the board names who leads. It links GOVERNANCE.md rather than restating the triggers.
   - Severity: Critical, High, Medium, and Low, each defined in one line by impact on player data, accounts, and ratings, with the same names and the fix targets SECURITY.md uses.
   - Fix targets count from the day the report arrives, matching SECURITY.md, or from the day OPEN finds the problem itself when nobody reported it.
   - Private handling: details stay out of public issues, pull requests, discussions, and chat until the announcement, and out of commit messages always, since merging makes them public. Before the announcement, the only public records are the ones GOVERNANCE.md requires and an interim notice under the publication rule.
   - Shared first steps for every incident: receive and acknowledge (aim for 5 business days), open a private advisory (on the affected repository, or on .github when none is affected), assess and set severity, contain, rotate secrets (rotate again after the fix and before the announcement if the cause could expose the new ones), tell people (without waiting for the fix or a slow rotation). Rotation names the kinds of secret (Django secret key, with the caveat from ADRs 0047 and 0056 that an exposed old key must not stay in `SECRET_KEY_FALLBACKS` and what that breaks, field encryption keys, backend's `ADMIN_URL`, database and broker credentials, email provider API key, OAuth client secrets, GitHub tokens and deploy keys, and the logins for the registrar, DNS, hosting, and Open Collective) and points to backend's README for the field encryption key rotation steps instead of copying them.
   - Code vulnerability track: fix in the advisory's private fork with a test, run tests locally (Actions don't run there), review, merge (an owner bypasses blocked required checks for this fix only and records why in the advisory), deploy right away, rotate again if needed, then publish the advisory on the date set under Publishing.
   - Operational incident track (hosting, DNS, email, accounts, a leaked credential): fix the configuration or access, confirm the leak path is closed, rotate again if needed, announce in a public summary on the date set under Publishing. The incident's advisory stays private as working notes and is never published, whichever repository it is on.
   - Telling people: players whose data or accounts are affected and partners whose integrations are affected are told directly once the exposure is confirmed, aiming for 72 hours, and aiming to meet a shorter deadline if a law that applies sets one. The notice says what happened, what data, what OPEN did, and what they should do, and never how the problem works or how to use it while unfixed.
   - Publishing, one rule for both tracks: once the fix ships, each confirmed problem is announced once, a code vulnerability by its advisory and every other problem by a public summary. The date is agreed with the reporter as SECURITY.md says (no later than the end of the disclosure window, sooner if both agree), with credit; with no reporter, or when the window has passed without an agreed later date, the incident lead sets it as soon as is practical after the fix ships and tells any reporter. If the fix misses the window, ask the reporter for a later date and keep working on the fix. The announcement leaves out details that identify anyone involved, except a reporter who chose credit, following GOVERNANCE.md "Meetings and votes". A record under "Administrative access" gives only a summary until the fix ships and the full explanation after, as that section says; GOVERNANCE.md sets no deadline for the full explanation, so the plan adds it once the announcement is out, keeping the date agreed with the reporter. An interim notice, which is not the announcement, comes before the fix only when the incident is already public or the window ends before the fix and the reporter won't extend it; the incident lead decides the wording, and it says what is affected and what to do, never how the problem works or that it can still be used.
   - Review: aim to write it within 30 days of the fix shipping, published under Publishing.
   - A short checklist that mirrors the shared steps and the two tracks, with an interim notice line for its two cases and separate publish lines for the advisory and the public summary that cover problems with no reporter.
2. `docs/security/threat-model.md` exists, fits on about one page, and covers:
   - Scope: the hosted service (backend API, the public app, the developer site, the GitHub organization), with a note that no OPEN rating is live and the hosted service does not yet hold real player data in production.
   - Assets: player data (accounts, legal name, birth year and month, gender division, contact email), ratings and rating history, match results and confirmations, partner OAuth credentials, the GitHub organization and its repositories, and the openpb.org domain, DNS, and email.
   - Actors and threats: rating manipulation (fake or colluding matches, forged confirmations, bypassing organizer verification, sandbagging), account takeover (credential stuffing, phishing, session theft, a maintainer or owner account), data leaks (an API returning more than it should, an exposed backup or export, logs), and supply chain (a compromised dependency or workflow). The rating manipulation items match SECURITY.md's scope.
   - Current controls per threat, stated only where they exist today and linking backend's README or ADRs for each backend control: score confirmation and disputes (ADR 0013), organizer verification and trusted submitters (ADR 0021), duplicate and plausibility checks (ADRs 0011, 0049, 0052), MFA with TOTP, recovery codes, and passkeys (ADRs 0043, 0056), login rate limits and the breached password check (ADR 0047; ADR 0039, which the plan first named, covers only the signup password check, so the threat model cites 0047 alone), API throttling (ADR 0030), field encryption (ADR 0046), the append-only audit log (ADR 0007), security headers (ADR 0040), two-factor authentication on every account that controls an OPEN asset and two-person recovery (GOVERNANCE.md), code owner review of governance files, DCO sign-off, OpenSSF Scorecard, and secret scanning for provider patterns.
   - Known gaps, including: secret scanning for non-provider patterns and validity checks is off (Free plan); several assets have no second person who can recover them (GOVERNANCE.md "Account recovery"); reports share a general inbox; during the founding phase the backup owner can act only after 30 days or on a written request (GOVERNANCE.md "Backup owner"), longer than the Critical fix target; and repositories with one maintainer have no required second review.
   - When to update it: when a new asset, actor, or control appears, and at least once before ratings go live.
3. SECURITY.md:
   - Keeps `info@openpb.org` and GitHub private reporting as the report channels.
   - Adds fix targets by severity (Critical 7 days, High 30 days, Medium 90 days, Low best effort), counted from the day the report arrives (the same day the disclosure window starts), with the severity names linked to the incident plan.
   - Replaces "Please give us a reasonable chance to fix the problem before sharing details publicly" with coordinated disclosure: 90 days after the report, or sooner once a fix ships and the reporter agrees, extendable by agreement.
   - Says that once a problem is fixed, a vulnerability in OPEN code is announced in a GitHub security advisory and any other problem in a public summary, crediting the reporter either way unless they ask to stay anonymous. The disclosure section says the announcement date is agreed with the reporter: no later than the end of the 90-day window, sooner if both agree once a fix ships, and later only by agreement. If the reporter won't agree to a later date, OPEN publishes a short notice of what is affected and what to do, without details of how the problem works.
   - Links the incident response plan and the threat model.
4. README.md lists `docs/security/` (the incident plan and threat model) where readers find the repository's contents. No other doc changes unless their text becomes wrong.
5. No change to CODE_OF_CONDUCT.md, SUPPORT.md, or any email address.
6. The pull request says `Part of #21`, not `Closes`, and its body lists what remains on #21: the two aliases (and backend's `SECURITY_TXT_CONTACT`), and secret scanning for non-provider patterns and validity checks, blocked by the Free plan.
7. No emojis and no em dashes in any changed file. `python3 -I scripts/test_check_pull_request.py` and `python3 -I scripts/test_sync_labels.py` still pass.

## Files that change

- `docs/security/incident-response.md` (new)
- `docs/security/threat-model.md` (new)
- `SECURITY.md`
- `README.md`
- this plan

## Order of work

1. Write `docs/security/incident-response.md` (criterion 1).
2. Write `docs/security/threat-model.md` (criterion 2). Before naming a backend control, confirm the ADR exists and says what the threat model claims: `gh api repos/openpickleball/backend/contents/docs/adr/<file> --jq .content | base64 -d`.
3. Edit SECURITY.md (criterion 3).
4. Edit README.md (criterion 4).
5. Run humanizer over the new prose. Check for emojis and em dashes: `grep -nP '\x{2014}|[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' <files>` prints nothing.
6. Run the gate: `python3 -I scripts/test_check_pull_request.py` and `python3 -I scripts/test_sync_labels.py`.
7. Commit the implementation after this plan's own commit (review fixes come as further commits), each signed off (`git commit -s`), with an imperative subject under 72 characters, no type prefix, and a body that says why and `Part of #21`.

## Departures found while writing

- ADR 0039 is the signup password check. Login rate limits and the breached password check are ADR 0047, so the threat model cites 0047 alone.
- ADR 0052 refuses a match dated outside its event rather than flagging it; the threat model says so.
- The threat model also cites ADR 0043 for the rule that organizer members need two-factor authentication to act for an organizer.
- DCO and OpenSSF Scorecard workflows run in every repository with code. brand-assets has no workflows, so the threat model scopes both to repositories with code.
- The threat model's supply chain section also lists controls verified with `gh api`: this repository's workflows pin Actions to commit SHAs, and backend has Dependabot (Python, Actions, base images) and a dependency audit workflow.
- The threat model says the per-IP throttle is built for public operations but none is mounted (ADRs 0030 and 0031), and that MFA is required of staff, superusers, moderators, and production application owners, with organizer members needing it to act for an organizer (ADR 0043).
- Delta review (second round): notifying affected people moved before the fix so the 72-hour aim fits the step order; the public record and advisory wait until the fix ships unless the incident is already public; commit messages never carry details; incidents with no repository use a private advisory on .github; and the `Protect main` rulesets (checked with `gh api repos/openpickleball/<repo>/rulesets` on .github and backend) require Actions checks that don't run in the private fork, with the repository admin role as bypass actor, so an owner bypasses them for that fix and records why.
- The rotation list adds `ADMIN_URL`, which backend's README (App Platform) declares as a secret, and the logins for the assets in GOVERNANCE.md "Account recovery".
- The threat model words the audit log control as ADR 0007 states it (app code and a trigger refuse changes) and adds as a known gap that the table owner or a superuser can disable the trigger, with the role work still open on backend #103. It also cites ADR 0031 for "no public operation is mounted".
- Third review round: the incident plan is restructured into shared first steps and two tracks (code vulnerability, operational incident) with one publication rule, because one set of steps contradicted itself for incidents with no code fix. "Deploy from the fork first" is dropped, since backend has no defined path for it. Notices and early summaries never say how a problem works. The threat model now says GOVERNANCE.md requires two-factor authentication on asset accounts, rather than stating that they use it.
- Final wording round: one announcement per problem (advisory for code, summary otherwise), the second rotation before anything is published, the missed-window fallback, the announcement date for self-found problems, credited reporters exempt from the no-identifying-details rule, "Administrative access" records held as summaries until the announcement date, and operational advisories never published on any repository. The law deadline is worded as an aim.
- Follow-up wording round: the day-90 fallback and the already-public case merge into one interim notice rule, named so it is not an announcement; the second rotation comes before the announcement; the credit exception is this plan's own rule rather than GOVERNANCE.md's; "Administrative access" records stay summaries until the fix ships and the announcement is out; the checklist gains an interim notice line and publish lines for problems with no reporter; and SECURITY.md tells reporters about the short notice if they won't agree to a later date.
- Final GOVERNANCE.md alignment: details stay private until the announcement rather than until the fix ships; the no-identifying-details rule is stated as following "Meetings and votes" with the credited reporter as the only exception; "Administrative access" records keep that section's rule, with the full explanation added once the announcement is out since GOVERNANCE.md sets no deadline; and the incident lead sets the date, telling the reporter, when the window passes without an agreed later date.
- Checklist wording: the publish lines name both cases in which the incident lead sets the date (no reporter, or the window passed without an agreed date), matching Publishing.
- SECURITY.md keeps "the day we receive the report" only; the "or the day OPEN finds the problem itself" case is in the incident plan, since SECURITY.md speaks to reporters.
- SECURITY.md is the organization-wide default and shows in other repositories, so its links to `docs/security/` use full https://github.com/openpickleball/.github/... URLs. README.md and the new pages use relative links.

## Risks

- Over-promising. A fix target or a notice deadline the volunteers cannot meet is worse than none. The 7/30/90 targets are the user's choice; the 72-hour notice is worded as an aim.
- Claiming controls that do not exist. Every control in the threat model must be checked against backend's README or the named ADR. A wrong claim misleads researchers about what to test.
- Restating GOVERNANCE.md. The incident plan links GOVERNANCE.md for who acts and how records are published, so the two cannot drift.
- Giving attackers a map. The threat model names threats and controls at the level SECURITY.md's scope already does, and names gaps that are already public (the Free plan, the governance recovery table). It names no unfixed vulnerability.

## Proof

- Criteria 1 to 4: a reviewer reads each new or changed file against the criterion's list. No automated test covers prose.
- Criterion 2's controls: each ADR cited is fetched and read (the order of work, step 2).
- Criterion 5: `git diff --stat origin/main` lists only the files above.
- Criterion 7: the grep in step 5 prints nothing, and both script tests pass (`18 passed`, `56 passed` on origin/main, measured 2026-11-27).
- No live drive: there is nothing to run. The pull request check (`pull-request / check`) runs on the PR.
- No "behave alike" or "phrase absent" tests in this plan.
