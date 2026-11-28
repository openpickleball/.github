# Incident response plan

This plan says what OPEN does when something goes wrong with security: a reported vulnerability, a leak of player data, a taken-over account, or tampering with ratings or match results. It covers every repository in the [openpickleball](https://github.com/openpickleball) organization and every service OPEN runs. To report a problem, follow the [security policy](../../SECURITY.md).

## Who leads

During the founding phase, the steward, who is also the primary owner of the GitHub organization, leads every incident (see [Current status: founding phase](../../GOVERNANCE.md#current-status-founding-phase)). The backup owner takes over only under the triggers listed in [Backup owner](../../GOVERNANCE.md#backup-owner), for example when the primary owner's account is the thing that was compromised. Once the board is seated, the board names who leads.

The person leading can ask maintainers or outside experts for help. Anyone brought in works in the private space described below and keeps the details to themselves until they are published.

## Severity

| Severity | What it means | Fix target |
| --- | --- | --- |
| Critical | Someone can reach many players' private data, take over accounts at will, or change ratings or match results without any control stopping them. | 7 days |
| High | Someone can reach one player's private data, take over a single account, or get around a control that protects ratings, such as score confirmation or organizer verification. | 30 days |
| Medium | A weakness that exposes little data or needs unusual conditions to use, such as an attacker who already holds a victim's session. | 90 days |
| Low | A hardening gap with no direct way to harm players, accounts, or ratings. | Best effort |

Fix targets count from the day the report arrives, the same day the disclosure window starts, or from the day OPEN finds the problem itself if nobody reported it. These are the targets the [security policy](../../SECURITY.md#what-to-expect) says we aim for.

## Keep it private

Keep the details out of public issues, pull requests, discussions, and chat until the fix ships. Commit messages never carry them, at any point: merging makes them public, and they can't be changed afterwards. Before the fix ships, the only public records are the ones [GOVERNANCE.md](../../GOVERNANCE.md) requires, such as a backup owner's record of acting, and an early summary under [Publishing](#publishing).

## First steps for every incident

1. **Receive and acknowledge.** Aim to reply to the reporter within 5 business days, as the security policy says.
2. **Open a private security advisory** on the affected repository, or on the [.github](https://github.com/openpickleball/.github) repository when no repository is affected (hosting, DNS, email, or an account). Keep notes there.
3. **Assess.** Reproduce the problem, work out what it affects, and set a severity from the table above. Tell the reporter the severity and the fix target.
4. **Contain.** Stop the harm before fixing the cause. That can mean turning off a feature, revoking an account's access or a partner application, voiding affected matches, or taking a service offline for a while.
5. **Rotate secrets.** Replace every secret that may have been exposed, not just the ones known to be. If the cause could expose the new secrets too, rotate again after the fix and before anything is published. The kinds of secret OPEN holds are:
   - The Django secret key. If the old key was exposed, don't keep it in `SECRET_KEY_FALLBACKS`. Passkeys made before the rotation then stop working for passkey login until the player removes and adds them again ([ADR 0056](https://github.com/openpickleball/backend/blob/main/docs/adr/0056-passkeys.md)), and every device looks new, so each account's next sign-in sends an alert ([ADR 0047](https://github.com/openpickleball/backend/blob/main/docs/adr/0047-account-security-limits-and-sessions.md)).
   - The field encryption keys. Follow the rotation steps in the [backend README](https://github.com/openpickleball/backend/blob/main/README.md#settings); don't remove an old key until the re-encryption has finished.
   - The admin's private path (`ADMIN_URL`), which the [backend README](https://github.com/openpickleball/backend/blob/main/README.md#app-platform) treats as a secret
   - Database and broker credentials
   - The email provider's API key
   - OAuth client secrets for partner applications
   - GitHub tokens and deploy keys
   - The logins for the domain registrar, DNS, hosting, and Open Collective (see [Account recovery](../../GOVERNANCE.md#account-recovery))
6. **Tell people.** Once the exposure is confirmed, tell the affected players and partners. Don't wait for the fix or for a slow rotation. See [Telling people](#telling-people).

Then follow the track that fits.

## Code vulnerability

1. Write the fix in the advisory's private fork, with a test that shows the problem is gone.
2. Run the tests locally, since GitHub Actions don't run in the private fork, and have the fix reviewed.
3. Merge it. If required status checks block the merge, an owner bypasses them for this fix only and records why in the advisory.
4. Deploy it right away.
5. Rotate again if needed (see step 5 above), then publish the advisory on the date set under [Publishing](#publishing).

## Operational incident

For hosting, DNS, email, accounts, or a leaked credential:

1. Fix the configuration or access, and confirm the path that leaked is closed. Rotate again if needed (see step 5 above).
2. Announce it in a public summary on the date set under [Publishing](#publishing). The incident's advisory stays private as the working notes and is never published, whichever repository it is on.

## Telling people

Once an exposure is confirmed, OPEN tells the people it affects directly:

- Players whose data or accounts are affected
- Partners whose integrations are affected

We aim to send these notices within 72 hours of confirming the exposure. If a law that applies sets a shorter deadline, we aim to meet that one.

Each notice says what happened, what data was involved, what OPEN has done, and what the reader should do, such as change a password or check their match history. It never says how the problem works, or how to use it while it is unfixed.

## Publishing

Once the fix ships, announce every confirmed problem once: a code vulnerability by its advisory, and every other problem by a public summary. Agree the date with the reporter, as the [security policy](../../SECURITY.md#disclosure) says: no later than the end of the disclosure window, and sooner if you both agree. When OPEN found the problem itself, the incident lead sets the date, as soon as is practical after the fix ships. Credit the reporter unless they asked to stay anonymous.

If the fix won't be ready by the end of the window, ask the reporter for a later date. If they won't agree, publish a summary of what is affected and what to do, never how the problem works, and keep working toward the fix.

The announcement leaves out details that identify anyone involved, other than a reporter who chose to be credited, as [Meetings and votes](../../GOVERNANCE.md#meetings-and-votes) requires for security issues. A record that [Administrative access](../../GOVERNANCE.md#administrative-access) requires stays a summary until the announcement date, which still gives the full explanation after the fix ships, as that section says.

A summary before the fix ships is the incident lead's call, made only when the incident is already public. Like every notice, it says what is affected and what to do, never how the problem works or that it can still be used.

## Review

Aim to write down what happened, what went well, and what to change within 30 days of the fix shipping. Update this plan and the [threat model](threat-model.md) if they need it. Publish the review under the same rules as the summary.

## Checklist

- [ ] Acknowledge the reporter (aim for 5 business days)
- [ ] Open the private advisory (on .github if no repository is affected; an operational incident's advisory is never published)
- [ ] Reproduce, set a severity, and tell the reporter the fix target
- [ ] Contain the harm
- [ ] Rotate every secret that may have been exposed
- [ ] Notify affected players and partners (aim for 72 hours after confirming)
- [ ] Code: fix with a test, test locally, review, merge (owner bypass recorded if needed), and deploy
- [ ] Operational: fix the configuration or access, and confirm the leak is closed
- [ ] Rotate again if the cause could have exposed the new secrets
- [ ] Code: publish the advisory, with credit, on the agreed date
- [ ] Operational: publish the public summary, with credit, on the agreed date
- [ ] Hold the review and update this plan and the threat model
