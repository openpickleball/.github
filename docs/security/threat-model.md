# Threat model

This page lists what OPEN protects, who might attack it and how, and what stops them today. It helps researchers decide what to test and helps maintainers see where the gaps are. To report a problem, follow the [security policy](../../SECURITY.md).

## Scope

The hosted service: the [backend](https://github.com/openpickleball/backend) API, the public app, the developer site at [dev.openpb.org](https://dev.openpb.org), and the [openpickleball](https://github.com/openpickleball) GitHub organization that holds their code. No OPEN rating is live, and the hosted service is not open to players yet, so it holds no real player data.

## What we protect

- Player data: accounts, legal name, birth year and month, gender division, and contact email
- Ratings and rating history
- Match results and their confirmations
- Partner OAuth credentials
- The GitHub organization and its repositories
- The openpb.org domain, its DNS, and its email

## Threats and current controls

Backend controls link to the decision record (ADR) that describes them.

### Rating manipulation

Fake or colluding matches, forged confirmations, getting around organizer verification, and sandbagging (losing on purpose to lower a rating).

- A match a player reports counts only once a player on the other team, or the event's verified organizer, confirms it. Any participant can dispute a match, which stops it counting until the dispute is settled ([ADR 0013](https://github.com/openpickleball/backend/blob/main/docs/adr/0013-match-confirmation-and-changes.md)).
- Only organizers that a moderator has verified can submit matches that count at once ([ADR 0021](https://github.com/openpickleball/backend/blob/main/docs/adr/0021-organizers-are-the-trusted-submitters.md)), and their members must use two-factor authentication to act for them ([ADR 0043](https://github.com/openpickleball/backend/blob/main/docs/adr/0043-mfa-totp-and-recovery-codes.md)).
- Duplicate matches are refused or held ([ADR 0011](https://github.com/openpickleball/backend/blob/main/docs/adr/0011-duplicate-match-detection.md)). Unusual volumes from trusted submitters are flagged ([ADR 0049](https://github.com/openpickleball/backend/blob/main/docs/adr/0049-flag-unusual-submissions.md)). A match dated outside its event is refused, and an implausible number of matches for one player in a day is flagged ([ADR 0052](https://github.com/openpickleball/backend/blob/main/docs/adr/0052-plausibility-checks-event-dates-and-player-daily-matches.md)).
- Changes to matches and ratings are recorded in an append-only audit log that the database refuses to edit or delete ([ADR 0007](https://github.com/openpickleball/backend/blob/main/docs/adr/0007-append-only-audit-log.md)).
- Nothing targets sandbagging yet. No OPEN rating is live, so there is no rating to sandbag.

### Account takeover

Credential stuffing, phishing, session theft, and takeover of a maintainer's or owner's account.

- Two-factor authentication with TOTP and recovery codes ([ADR 0043](https://github.com/openpickleball/backend/blob/main/docs/adr/0043-mfa-totp-and-recovery-codes.md)), and passkeys, which resist phishing ([ADR 0056](https://github.com/openpickleball/backend/blob/main/docs/adr/0056-passkeys.md)). Staff, moderators, and organizer members must use two-factor authentication.
- Login rate limits, a check that refuses passwords found in known breaches, session time limits, and an email for each sign-in from a new device ([ADR 0047](https://github.com/openpickleball/backend/blob/main/docs/adr/0047-account-security-limits-and-sessions.md)).
- Security headers, and session cookies that the browser keeps to one host ([ADR 0040](https://github.com/openpickleball/backend/blob/main/docs/adr/0040-security-headers-and-cookies.md)).
- Every account that controls an OPEN asset uses two-factor authentication, and each asset should be recoverable by two people ([Account recovery](../../GOVERNANCE.md#account-recovery)).

### Data leaks

An API that returns more than it should, an exposed backup or export, or personal data in logs.

- Legal name, birth year and month, gender division, and two-factor secrets are encrypted in the database. Staff see them only by a deliberate reveal that is recorded in the audit log ([ADR 0046](https://github.com/openpickleball/backend/blob/main/docs/adr/0046-encrypt-personal-data-fields.md)).
- API throttling limits how many requests one account or client IP can make ([ADR 0030](https://github.com/openpickleball/backend/blob/main/docs/adr/0030-api-throttling.md)).
- The audit log never holds passwords, tokens, secrets, or recovery codes ([ADR 0007](https://github.com/openpickleball/backend/blob/main/docs/adr/0007-append-only-audit-log.md)).

### Supply chain

A compromised dependency, GitHub Action, or workflow.

- Changes to the charter, GOVERNANCE.md, and CODEOWNERS need a code owner's review ([Reviewing the charter and governance files](../../GOVERNANCE.md#reviewing-the-charter-and-governance-files)).
- In every repository with code, pull requests check each commit for a DCO sign-off, and OpenSSF Scorecard reviews the repository's security practices.
- GitHub secret scanning for known provider patterns is on for every repository.

## Known gaps

- Secret scanning for non-provider patterns and validity checks is off. OPEN's organization is on GitHub's Free plan, and both need a paid add-on.
- Several assets, including the domain registrar, DNS, hosting, and email, have no second person who can recover them yet ([Account recovery](../../GOVERNANCE.md#account-recovery)).
- Security reports go to the same general inbox as other mail.
- A repository with one maintainer has no required second review ([Required review in each repository](../../GOVERNANCE.md#required-review-in-each-repository)).

## Keeping this current

Update this page when a new asset, kind of attacker, or control appears, and review it at least once before any OPEN rating goes live. Changes go through a normal pull request.
