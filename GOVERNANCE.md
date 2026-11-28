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

### If the steward is gone for good

The steward's absence counts as permanent when any of these happens:

- The steward hasn't responded on any channel for 90 days.
- The steward says so in writing.
- Their family or legal representative confirms that the steward has died or is permanently unable to act. This counts at once.

The backup owner then becomes acting steward and records it in a public issue that says which case applied. For the 90-day case, the issue also names the channels used to try to reach the steward, without giving contact details.

The acting steward has every power and every limit this document gives the steward, and becomes the primary owner. That includes appointing a new backup owner and nominating the first board, with the same 30 days of public comment, by the same December 31, 2027 deadline. Their first duty is to appoint a new backup owner within 30 days, so OPEN has two owners again. From then on, "the steward" in this document means the acting steward.

If the steward returns after a permanent absence was declared, the acting steward stays in place. The role passes back only if both agree in a public issue.

### Changing this document before the board is seated

Until the board is seated, a change to this document needs all of the following:

1. A public pull request.
2. Approval from a code owner who didn't write or push any part of it (see [Reviewing the charter and governance files](#reviewing-the-charter-and-governance-files)).
3. At least 14 days between opening the pull request and merging it, so anyone can comment.

A change that only corrects an error, fixes a link, or rewords text without changing what any rule means can merge without the 14 days. Its pull request says so.

Some changes can't be made this way and wait for the board: a change that removes or loosens any of the steward's limits above, reduces the board's powers, moves the December 31, 2027 deadline later, or loosens this section or the code owner review.

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
| Changes to this document | Governing board | Public pull request and majority vote. Before the board is seated, see [Changing this document before the board is seated](#changing-this-document-before-the-board-is-seated). |
| Changes to the charter | Governing board | See [Amending the charter](#amending-the-charter). Before the board is seated, the steward can only correct errors or clarify wording, through a public pull request with code owner approval (see [Current status](#current-status-founding-phase)). |

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

Reviewing changes to the files under code owner review (see [Reviewing the charter and governance files](#reviewing-the-charter-and-governance-files)) is part of the role. It needs no trigger and no public issue.

Beyond that review, the backup owner may act as an owner only when:

- The primary owner can't be reached for 30 days
- The primary owner can't be reached within 4 hours of a confirmed security incident, only to lead that incident's response (see below)
- The primary owner's account is compromised or locked
- The primary owner asks them to, in writing, in a public issue
- The board asks them to, once it is seated

When they act, the backup owner:

- Can't change the charter except to correct errors or clarify wording
- Can't sell or transfer the project or its assets to anyone other than the board or an entity it controls
- Can't declare an OPEN rating official
- Records each action in a public issue that says which trigger applied. For the 30-day trigger, it also names the channels they used to try to reach the primary owner, without giving contact details.

Under the 4-hour incident trigger, the backup owner leads the response as the [incident response plan](docs/security/incident-response.md) describes: containing the problem, rotating secrets and tokens, turning off affected apps or webhooks, preserving evidence, fixing the problem, and telling affected players and partners. Nothing else. Any other owner action, such as changing membership, rules, or access beyond what containment needs, still needs another trigger. Their authority under this trigger ends when the primary owner responds and takes the incident back. Their public record gives only a summary until the fix ships, as the rule for security problems at the start of this section says.

Under every other trigger, the backup owner's authority ends as soon as the primary owner responds, unless the primary owner asks them to finish a task. A permanent absence is different: see [If the steward is gone for good](#if-the-steward-is-gone-for-good).

### Recovery contact

The recovery contact is the path back in if the primary owner and the backup owner are both out of reach. During the founding phase, the steward appoints the recovery contact. Once the board is seated, the board does. The recovery contact can't be either owner. Each appointment, and every change to it, is recorded in a public issue.

The recovery contact holds no access day to day. They keep a sealed copy, offline, of a letter signed by both owners that names them as recovery contact, and the steps for asking GitHub Support and Open Source Collective to restore access. They never hold anyone's personal recovery codes (see [Account recovery](#account-recovery)). They open it only when neither owner has responded on any channel for 30 days, and they record that in a public issue that names the channels used, without giving contact details.

They may then act only to appoint two new owners, who become primary owner and backup owner. The new primary owner becomes acting steward, with the steward's limits, as described in [If the steward is gone for good](#if-the-steward-is-gone-for-good). The recovery contact can't change the charter, sell or transfer the project or its assets, or declare an OPEN rating official.

### Reviewing the charter and governance files

A change to any file listed in `.github/CODEOWNERS` needs an approving review from a code owner who didn't write or push any part of the change. That file is the list of covered paths and their code owners. It covers:

- The charter and governance files: `CHARTER.md`, `GOVERNANCE.md`, and `.github/CODEOWNERS`.
- The files that decide where money and security reports go: `FUNDING.yml` and `SECURITY.md`.
- The checks other OPEN repositories rely on: `.github/workflows/`, `actions/`, `scripts/`, and `.pre-commit-hooks.yaml`.
- The organization profile: `profile/`.

GitHub can't fully enforce this. Anyone with admin access to the repository, which includes every owner, can skip the review or change the rule itself. They may skip the review only from inside a pull request, only to fix a security problem or restore access, and they must explain why in that pull request. Every change to the repository's rules is recorded in a public issue.

### Required review in each repository

Once a repository has at least two maintainers (the primary owner counts as one if they maintain it), its default branch must require one approving review for every change. An owner sets this up within 7 days of the second maintainer's appointment and records it in that appointment issue.

If a repository drops back to one maintainer, that maintainer can't approve their own changes. The requirement may then be lifted until there are two maintainers again. Lifting it is recorded in a public issue, and never lifts the code owner review of the files listed in `.github/CODEOWNERS`.

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
