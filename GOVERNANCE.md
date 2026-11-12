# Governance of OPEN

This document explains how decisions are made for OPEN. It carries out the [mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md), and the charter takes precedence if the two conflict.

## Current status: founding phase

The charter says no person controls OPEN, including the founder. That is the goal, and it is not true yet. The governing board has not been seated, and the founder is currently the only administrator of the GitHub organization.

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
| Changes to the official rating spec | Governing board | The change process in the `rating-spec` repository, once published |
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
| Owner | Administers the GitHub organization and acts on the board's decisions | Chosen by the board from maintainers with a proven track record. See [Administrative access](#administrative-access). |
| Emeritus | Keeps recognition as a former maintainer, without merge access | By stepping down. Maintainers who are inactive for six months may step down or be moved to emeritus status. |

During the founding phase, the steward may directly appoint the first maintainers of a repository that has no maintainers other than the steward. Each appointment must be recorded in a public issue.

### Inactive members

Organization members with no activity in any OPEN repository for 90 days are removed from the organization. Activity means commits, pull requests, issues, reviews, or comments. Removal is routine housekeeping, not a judgment, and anyone removed this way can return through the same path after their next merged pull request. This rule is separate from the six-month emeritus rule for maintainers.

A contributor role gives no claim to a seat on the board. Board seats are filled as described above.

## Administrative access

After the founding phase, at least two people must hold owner access to the GitHub organization, and they must act on the board's decisions. Protected branches must require review before changes to the charter or to this document are merged.

## Related documents

- [Mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md)
- [Contributing guide](https://github.com/openpickleball/.github/blob/main/CONTRIBUTING.md)
- [Code of Conduct](https://github.com/openpickleball/.github/blob/main/CODE_OF_CONDUCT.md)
- [Security policy](https://github.com/openpickleball/.github/blob/main/SECURITY.md)
- [How OPEN is licensed](https://github.com/openpickleball/.github/blob/main/LICENSING.md)
- [Roadmap](https://github.com/openpickleball/.github/blob/main/ROADMAP.md)
