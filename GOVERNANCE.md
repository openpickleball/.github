# Governance of OPEN

This document explains how decisions are made for OPEN. It carries out the [mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md), and the charter takes precedence if the two conflict.

## Current status: founding phase

The charter says no person controls OPEN, including the founder. That is the goal, and it is not true yet. The governing board has not been seated. The founder is the primary owner of the GitHub organization, and a backup owner holds owner access for emergencies (see [Administrative access](#administrative-access)).

Until the board is seated, the founder acts as interim steward. The steward:

- Makes project decisions in public, on GitHub, wherever confidentiality isn't required
- Can't change the charter except to correct errors or clarify wording, and must record any such change publicly
- Can't sell or transfer the project or its assets to anyone other than the board or an entity it controls
- Can't declare an OPEN rating official

The steward must seat the first board before any OPEN rating goes live, and no later than **December 31, 2027**.

When the board is seated, control of every project asset passes to the board or a legal entity it controls. That includes the GitHub organization, domain names, the OPEN name and logo, hosted services, accounts, and funds.

## Governing board

### Responsibilities

The board:

- Approves changes to the official rating spec
- Protects the charter and decides on amendments to it
- Decides which tools conform to the spec and can show an OPEN rating
- Oversees project funds and their publication
- Appoints and removes maintainers when a repository can't resolve this itself

### Members

The board has five seats, and each member serves a two-year term. Terms are staggered so that the whole board doesn't change at once. Together, the members should represent players, clubs and organizers, developers, and people with rating or statistics expertise.

- No more than one member may work for, or be paid by, the same company or organization.
- Donors, grant makers, and sponsors get no seat or say because of their support.
- The founder may serve as a member, with the same single vote and no veto or special powers.

### Selecting and removing members

The steward nominates the first board publicly and allows 30 days for public comment before seating it.

After that, open seats are announced publicly, anyone can nominate a candidate, and the board votes after 30 days of public comment.

A member can be removed by a two-thirds vote of the other members for breaking the charter, the [Code of Conduct](https://github.com/openpickleball/.github/blob/main/CODE_OF_CONDUCT.md), or the conflict of interest rule below, or for sustained absence.

### Conflicts of interest

Members must disclose any financial or professional interest in a decision, and must not vote on it. Members may not vote on matters involving their own rating or a platform they work with.

### Meetings and votes

A majority of seated members is a quorum, and decisions pass by a majority of those voting unless this document says otherwise. Votes and meeting summaries are published. Confidential matters, such as conduct reports and security issues, are published only in summary, without details that identify anyone involved.

## How decisions are made

| Decision | Who decides | How |
| --- | --- | --- |
| Day-to-day code and documentation changes | Repository maintainers | Pull request review |
| Disagreements within a repository | Repository maintainers, then the board | Discussion first, then a maintainer majority. The board decides if that fails. |
| Changes to the official rating spec | Governing board | The [RFC process](https://github.com/openpickleball/rating-spec/blob/main/rfcs/README.md) in the `rating-spec` repository |
| Which tools can show an OPEN rating | Governing board | Published conformance requirements |
| Changes to this document | Governing board | Public pull request and majority vote |
| Changes to the charter | Governing board | See below |

## Amending the charter

A charter amendment requires all of the following:

1. A public proposal, open for comment for at least 30 days
2. A two-thirds vote of the full board
3. Publication of the vote and the reasons for it

An amendment can clarify or strengthen the five charter terms. It can't weaken or remove them.

## Contributor roles

You don't need to join the GitHub organization to take part in OPEN. There is no application process. Access is earned through contribution, one step at a time.

| Role | What they can do | How someone gets the role |
| --- | --- | --- |
| Contributor | Open issues, join discussions, and submit pull requests | By taking part. No permissions are needed. |
| Organization member | Belongs to the `contributors` team, with triage access: label, assign, and close issues and pull requests | A maintainer invites them after their first merged pull request |
| Role team member | Belongs to a role team (`backend`, `frontend`, `algorithm`, or `devops`), with write access to that team's repositories | A maintainer nominates them in a public issue, based on sustained, good-faith contribution, and a majority of the relevant repository's maintainers agree |
| Maintainer | Belongs to the `maintainers` team. Reviews and merges changes, and nominates new members and maintainers | An existing maintainer nominates them in a public issue, based on sustained, good-faith contribution, and a majority of the repository's maintainers agree |
| Owner | Administers the GitHub organization and acts on the board's decisions | Chosen by the board from maintainers with a proven track record. The backup owner need not be a maintainer, and during the founding phase the steward appoints them. See [Administrative access](#administrative-access). |
| Emeritus | Keeps recognition as a former maintainer, without merge access | By stepping down. Maintainers who are inactive for six months may step down or be moved to emeritus status. |

During the founding phase, the steward may directly appoint the first maintainers of a repository that has no maintainers other than the steward. Each appointment must be recorded in a public issue.

### Inactive members

Organization members with no activity in any OPEN repository for 90 days are removed from the organization. Activity means commits, pull requests, issues, reviews, or comments. Removal is routine housekeeping, not a judgment, and anyone removed this way can return through the same path after their next merged pull request. This rule is separate from the six-month emeritus rule for maintainers. Owners are exempt, because the backup owner is often inactive by design.

A contributor role gives no claim to a seat on the board. Board seats are filled as described above.

## Funds

[Open Source Collective](https://www.oscollective.org) (OSC), a nonprofit fiscal host, holds OPEN's funds. They are never kept in a personal account. Every dollar in and out is published on [OPEN's Open Collective page](https://opencollective.com/open-pickleball).

OSC is a 501(c)(6) organization, so donations through it are not tax-deductible in the United States.

### Expense policy

Funds may pay only for:

- Hosting and infrastructure
- Domain names
- Services the project runs on, such as email delivery
- Development tools for volunteer contributors
- Accessibility and security work

Funds never pay for advertising, or for anything that would break the charter.

Every expense is submitted on Open Collective with its receipt or invoice attached. Before OSC pays, a collective admin must approve it. That admin can't be the person who submitted it or the person it pays.

### Collective admins

The collective must have at least two admins, so access to the funds never depends on one person. During the founding phase, the admins must be the steward and at least one other trusted person. The steward adds the second admin before the collective accepts any funds. The admins are listed on the collective's page, and every change to them is recorded in a public issue.

Once the board is seated, the collective's admins are its seated members. Any other admin steps down, and a member who leaves the board stops being an admin. If the board moves the funds to a legal entity it controls, the collective is closed once its balance has moved.

## Administrative access

OPEN must always have two owners of the GitHub organization, including during the founding phase: a primary owner and a backup owner. When either seat is empty, whoever appoints that seat fills it within 30 days. During the founding phase, the steward is the primary owner. Once the board is seated, the board names the primary owner, and owners act on the board's decisions.

Records this section requires are public. For a security problem that isn't public yet, a record gives only a summary until the fix ships, and the full explanation after.

### Backup owner

The backup owner holds owner access so that OPEN never depends on one account. During the founding phase, the steward appoints the backup owner. Once the board is seated, the board does. Each appointment, and every change to it, is recorded in a public issue.

Reviewing changes to the charter and governance files is part of the role. It needs no trigger and no public issue.

Beyond that review, the backup owner may act as an owner only when:

- The primary owner can't be reached for 30 days
- The primary owner's account is compromised or locked
- The primary owner asks them to, in writing, in a public issue
- The board asks them to, once it is seated

When they act, the backup owner:

- Can't change the charter except to correct errors or clarify wording
- Can't sell or transfer the project or its assets to anyone other than the board or an entity it controls
- Can't declare an OPEN rating official
- Records each action in a public issue that says which trigger applied. For the 30-day trigger, it also names the channels they used to try to reach the primary owner, without giving contact details.

### Reviewing the charter and governance files

A change to `CHARTER.md`, `GOVERNANCE.md`, or `.github/CODEOWNERS` needs an approving review from a code owner who didn't write or push any part of the change. The code owners are listed in `.github/CODEOWNERS`.

GitHub can't fully enforce this. Anyone with admin access to the repository, which includes every owner, can skip the review or change the rule itself. They may skip the review only from inside a pull request, only to fix a security problem or restore access, and they must explain why in that pull request. Every change to the repository's rules is recorded in a public issue.

### Required review in each repository

Once a repository has at least two maintainers (the primary owner counts as one if they maintain it), its default branch must require one approving review for every change. An owner sets this up within 7 days of the second maintainer's appointment and records it in that appointment issue.

If a repository drops back to one maintainer, that maintainer can't approve their own changes. The requirement may then be lifted until there are two maintainers again. Lifting it is recorded in a public issue, and never lifts the review of the charter and governance files.

### Account recovery

Every account that controls an OPEN asset uses two-factor authentication, and a hardware security key if the service supports one.

Each asset must be recoverable by two people:

- If the service allows a second user, each person has their own login.
- If it allows only one login, the second holder keeps a sealed, printed copy of everything needed to sign in, including the recovery codes, offline. The copy is replaced whenever any of it changes, and is never sent by chat or email.

Nobody shares their personal recovery codes. Recovery codes are stored offline, either printed or in an offline password manager. They are never kept in a repository, an issue, or a shared drive.

| Asset | Primary | Second |
| --- | --- | --- |
| GitHub organization | Primary owner | Backup owner |
| Domain registrar for openpb.org | Primary owner | Pending |
| DNS for openpb.org | Primary owner | Pending |
| Hosting | Primary owner | Pending |
| Email for openpb.org | Primary owner | Pending |
| Open Collective | Steward | Second [collective admin](#collective-admins) (pending, issue #7) |

Pending means no second person can recover that asset yet.

## Related documents

- [Mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md)
- [Contributing guide](https://github.com/openpickleball/.github/blob/main/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/openpickleball/.github/blob/main/CODE_OF_CONDUCT.md)
- [Security policy](https://github.com/openpickleball/.github/blob/main/SECURITY.md)
- [How OPEN is licensed](https://github.com/openpickleball/.github/blob/main/LICENSING.md)
- [Roadmap](https://github.com/openpickleball/.github/blob/main/ROADMAP.md)
