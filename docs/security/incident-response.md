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

Fix targets count from the day the report is confirmed. These are the same targets the [security policy](../../SECURITY.md#what-to-expect) promises.

## Keep it private

Incident work happens in a private GitHub security advisory on the affected repository, or in the advisory's private fork. Never discuss an open incident in a public issue, pull request, discussion, or commit message. Fixes are written and reviewed in the private fork and merged when the advisory is published.

## Steps

1. **Receive and acknowledge.** Reply to the reporter within 5 business days, as the security policy promises. Open a private security advisory for the report if the reporter didn't.
2. **Assess.** Reproduce the problem, work out what it affects, and set a severity from the table above. Tell the reporter the severity and the fix target.
3. **Contain.** Stop the harm before fixing the cause. That can mean turning off a feature, revoking an account's access or a partner application, voiding affected matches, or taking a service offline for a while.
4. **Rotate secrets.** Replace every secret that may have been exposed, not just the ones known to be. The kinds of secret OPEN holds are:
   - The Django secret key
   - The field encryption keys. Follow the rotation steps in the [backend README](https://github.com/openpickleball/backend/blob/main/README.md#settings); don't remove an old key until the re-encryption has finished.
   - Database and broker credentials
   - The email provider's API key
   - OAuth client secrets for partner applications
   - GitHub tokens and deploy keys
5. **Fix.** Write the fix in the private fork, with a test that shows the problem is gone, and have it reviewed. Ship it to every affected repository and service.
6. **Tell people.** See [Telling people](#telling-people).
7. **Publish.** See [Publishing](#publishing).
8. **Review.** Within 30 days of the fix shipping, write down what happened, what went well, and what to change. Update this plan and the [threat model](threat-model.md) if they need it. The review is published the same way as the incident summary.

## Telling people

Once an exposure is confirmed, OPEN tells the people it affects directly:

- Players whose data or accounts are affected
- Partners whose integrations are affected

We aim to send these notices within 72 hours of confirming the exposure. If a law that applies sets a shorter deadline, we meet that one instead.

Each notice says:

- What happened
- What data was involved
- What OPEN has done about it
- What the reader should do, such as change a password or check their match history

## Publishing

Every incident that affects players, partners, or ratings gets a public summary. It follows the rules for security records in [Administrative access](../../GOVERNANCE.md#administrative-access) and [Meetings and votes](../../GOVERNANCE.md#meetings-and-votes): a summary with no identifying details until the fix ships, and the full explanation after.

A vulnerability in OPEN code also gets a published GitHub security advisory on the affected repository. It credits the reporter unless they asked to stay anonymous.

## Checklist

Use this during an incident. Keep notes in the private advisory as you go.

- [ ] Acknowledge the reporter (within 5 business days)
- [ ] Open or confirm the private security advisory
- [ ] Reproduce the problem and set a severity
- [ ] Tell the reporter the severity and the fix target
- [ ] Contain the harm
- [ ] Rotate every secret that may have been exposed
- [ ] Fix, test, review, and ship in the private fork
- [ ] Notify affected players and partners (aim for 72 hours after confirming)
- [ ] Publish the summary, then the full explanation after the fix ships
- [ ] Publish the security advisory, with credit
- [ ] Hold the review and update this plan and the threat model
