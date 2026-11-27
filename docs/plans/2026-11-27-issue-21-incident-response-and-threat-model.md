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
   - Fix targets count from the day the report arrives, matching SECURITY.md.
   - Steps in order: receive and acknowledge (aim for 5 business days, as SECURITY.md says), assess and set severity, contain, rotate secrets, fix (reviewed in the private fork, tests run locally because Actions don't run there, then merged and deployed), tell people, publish (after the fix is deployed), review (aim to write it within 30 days of the fix shipping, published under the same rules as the incident summary). Rotation names the kinds of secret (Django secret key, with the caveat from ADRs 0047 and 0056 that an exposed old key must not stay in `SECRET_KEY_FALLBACKS` and what that breaks, field encryption keys, database and broker credentials, email provider API key, OAuth client secrets, GitHub tokens and deploy keys) and points to backend's README for the field encryption key rotation steps instead of copying them.
   - Telling people: players whose data or accounts are affected and partners whose integrations are affected are told directly once the exposure is confirmed, aiming for 72 hours, and sooner if a law that applies sets a shorter deadline. The notice says what happened, what data, what OPEN did, and what they should do.
   - Publishing: a public record for every incident that affects players, partners, or ratings: a summary before the fix ships and the full explanation after, which still leaves out details that identify anyone involved (GOVERNANCE.md "Meetings and votes"). Records under "Administrative access" follow that section's own rule. A vulnerability in OPEN code also gets a GitHub security advisory.
   - A short checklist a responder can follow during an incident.
   - Private handling: incident work happens in a private security advisory or its private fork. Details stay out of public issues and pull requests until the fix ships; the only public records before then are the summary-level ones this plan and GOVERNANCE.md require.
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
   - Says fixes to OPEN code are announced as GitHub security advisories, and other problems (hosting, DNS, email) in the public incident summary, both crediting the reporter unless they ask to stay anonymous.
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
