# Contributing to OPEN

Thanks for helping build OPEN, the Open Pickleball Evaluation Network. This guide applies to every repository in the [openpickleball](https://github.com/openpickleball) organization. A repository can also have its own `CONTRIBUTING.md` with steps for that repository. A repository guide adds to this one and does not replace it, so read both.

Everyone who takes part agrees to the [mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md) and the [Code of Conduct](https://github.com/openpickleball/.github/blob/main/CODE_OF_CONDUCT.md).

## Ways to help

You don't need to write code:

- **Players:** tell us what you need from a rating and what would make one easier to trust.
- **Clubs and organizers:** share how you run events and record results.
- **App and league platform builders:** tell us what you'd need to send results to OPEN or show OPEN ratings.
- **Statisticians and rating enthusiasts:** review the methods and challenge the assumptions behind them.
- **Developers and designers:** help build the engine, APIs, and tools.

## Start with an issue

Open an issue before starting anything large, so nobody spends time on work that can't be accepted. Use the repository the issue is about. If you aren't sure which one that is, or the project doesn't have a repository yet, [open it in `.github`](https://github.com/openpickleball/.github/issues/new).

New to OPEN and want to pick up work that's already planned? Look at the [open issues labeled `good first issue`](https://github.com/search?q=org%3Aopenpickleball+label%3A%22good+first+issue%22+is%3Aopen+is%3Aissue&type=issues) across OPEN's repositories. Each one is a good place to start.

Before proposing a new feature, ask whether it makes the standard more accurate, more trusted, or easier to adopt. If it doesn't, it probably belongs in a partner's product.

Please report security problems privately. See the [security policy](https://github.com/openpickleball/.github/blob/main/SECURITY.md).

## Changes to the rating spec

Anyone can propose or challenge a change to the rating spec by opening an issue. Include the evidence for it, ideally how the change affects predictive accuracy and calibration on matches the engine hasn't seen. A change that gets support becomes a written proposal (an RFC) in the [`rating-spec` repository](https://github.com/openpickleball/rating-spec), following its [RFC process](https://github.com/openpickleball/rating-spec/blob/main/rfcs/README.md). The governing board makes the final decision on changes to the official spec.

## Labels

Every OPEN repository uses the same set of labels, listed in [`labels.toml`](https://github.com/openpickleball/.github/blob/main/labels.toml) in this repository. A repository can add labels of its own, such as `area:` labels for parts of its code, but it can't redefine a shared one.

To change the shared set, open a pull request against `labels.toml`. After it merges, an organization owner runs `python3 scripts/sync_labels.py` to see what would change in each repository, then runs it again with `--apply` to make those changes.

To rename a shared label, change its `name` and add the old name to its `aliases`. In a repository that has only the old label, the sync renames it, and its issues and pull requests keep it. In a repository that has both, the sync adds the new label to every issue and pull request with the old one, then deletes the old one. It won't do that in a repository with discussions turned on, because it can't move discussion labels. It reports the merge as refused and changes nothing for that label. An owner then adds the new label to its issues, pull requests, and discussions by hand, and deletes the old one. Without the alias, the sync creates a new label and leaves the old one in place. Removing a label from `labels.toml` changes nothing in the repositories: the sync never deletes a label that isn't in the file.

## Pull requests

1. Link the issue the pull request addresses with `Closes #N` in the description, or `Refs #N` or `Part of #N` when the issue stays open. The pull request template starts the description for you.
2. Keep each pull request to one change.
3. Add or update tests and documentation when behavior changes.
4. Sign off every commit, as described below.
5. Write each commit message as described in "Commit messages" below. Leave a type prefix such as `fix:` off the pull request title too.

## What happens after you open a pull request

The maintainers of the repository you opened it in respond to your pull request and review it. OPEN is run by volunteers, and we still hold ourselves to a target: you get a first response within 3 business days. A first response can be a review, a question, or a note saying when we'll get to it. It isn't always a full review or a merge.

If 3 business days pass with no reply, comment on the pull request to remind us.

When a reviewer requests changes, push updates to the same pull request, or reply if you disagree. Either way, the reviewer then looks at it again.

If we're waiting on you and you don't reply for 30 days, we close the pull request with a friendly note. Ask us to reopen it, or open a new one, when you're ready to pick it back up.

### When we rework your pull request

Sometimes a maintainer reworks your change, or finishes it in a new pull request that replaces yours. When that happens, you still get credit:

- The new commits carry a `Co-Authored-By:` trailer with the name and email address from your original commits, for example `Co-Authored-By: Your Name <you@example.com>`.
- The comment that closes your pull request thanks you and links the new pull request.
- A maintainer adds you to the [contributor list](https://github.com/openpickleball/.github/blob/main/CONTRIBUTORS.md).

If the email address in your commits isn't public, the trailer uses your GitHub noreply address instead: `ID+username@users.noreply.github.com`. `ID` is your GitHub account number, which `gh api users/username --jq .id` shows. Maintainers never guess or publish a private address.

## Commit messages

Write each commit message like this:

```
Import email tasks before checking their registration

autodiscover_tasks() loads task modules lazily outside a worker, so the
routing test failed when it ran alone.

Closes #328

Signed-off-by: Your Name <you@example.com>
```

- The subject is imperative ("Add", "Fix", "Refuse"), starts with a capital letter, has no period at the end, and is at most 72 characters.
- No type prefix such as `test:` or `fix(api):`.
- A blank line, then a body that says why the change is needed.
- No `fixup!` or `squash!` commits left in a pull request: squash them with `git rebase -i --autosquash`.

The `pull-request` check runs these rules on every pull request, and again when you edit its title or description. It also flags a description or message damaged by shell escaping: in a double-quoted PowerShell string a backtick is an escape character, so pass text from a file instead (`gh pr create --body-file`, `git commit -F`). To reword a commit that is already pushed, use `git rebase -i`, then `git push --force-with-lease`.

Repositories that use pre-commit also install a `commit-msg` hook that checks these rules and the sign-off before you push. Run `pre-commit install` (or the repository's own install command) to get it.

## Keep player data out

Do not put real player names, contact details, or match histories in issues, pull requests, test fixtures, or screenshots. Use made-up or properly de-identified data.

## Sign off your commits

OPEN uses the [Developer Certificate of Origin](https://developercertificate.org/) (DCO). By signing off, you certify that you wrote the contribution or otherwise have the right to submit it under the repository's license.

Add the sign-off with the `-s` flag:

```
git commit -s -m "Describe your change"
```

This adds a line to your commit message, using a name you're known by and an email address you can be reached at:

```
Signed-off-by: Your Name <you@example.com>
```

We can't accept commits without a sign-off.

## AI-assisted contributions

You may use AI tools, such as coding assistants and chat models, to help with your contribution.

You are responsible for the whole change, including any part an AI tool wrote. Understand it well enough to explain it and to answer review questions about it. AI-assisted changes meet the same review and test bar as any other change.

Your sign-off applies in full. When you sign off AI-assisted work, you certify that you have the right to submit all of it under the repository's license, as described in [Sign off your commits](#sign-off-your-commits).

Say so when an AI tool wrote a meaningful part of your change. You don't need to mention autocomplete or spelling fixes. Use either of these:

- A `Co-Authored-By:` trailer on the commit, for example `Co-Authored-By: Claude <noreply@anthropic.com>`.
- A note in the pull request description that says which tool you used and what it wrote.

This rule is the same in every OPEN repository.

Don't put links to private AI sessions in commit messages or pull request descriptions. Outside readers can't open them, so they don't help reviewers or anyone reading the history later. Put what a reviewer needs to know in the message or description itself. Commits that are already merged and contain such links can stay as they are.

Some repositories have files written for AI coding tools:

- **`CLAUDE.md` and `AGENTS.md`** give instructions to AI coding tools, and they also record the repository's conventions. Read them to learn those conventions. If you use an AI tool, follow them. If your change makes one of them wrong, update it in the same pull request. You don't need an AI tool to contribute.
- **`plans/`** (or the repository's plans directory) holds plans written before larger changes. Reading them is optional. A plan shows how someone intended to do the work. It isn't a spec or a promise.

A repository's own README or `CONTRIBUTING.md` can say more about these files.

If a pull request looks like low-effort AI output that its author hasn't reviewed, maintainers may close it with a link to this section. They don't need to review it line by line first.

## Releases and versioning

Each repository says how it is versioned in its own README or `CONTRIBUTING.md`. The rules below are the same everywhere.

| Repository | Version scheme | Release notes |
| --- | --- | --- |
| `engine` | [Semantic Versioning](https://semver.org/), with the stability promise in its README | `CHANGELOG.md`, a GitHub release, and the package on PyPI |
| `.github` (the shared `commit-message` hook and the reusable `pull-request` workflow) | Semantic Versioning (see below) | `CHANGELOG.md` and a GitHub release |
| `rating-spec` | The spec's own Semantic Versioning, in its README | `CHANGELOG.md`, with the RFC that approved each version |
| `backend` and `frontend` | Calendar versions, `YYYY.MM.N` (for example `2026.12.0` for the first release in December 2026) | GitHub releases with generated notes |
| `developers`, `evaluation`, and `brand-assets` | Not versioned. `main` is the current version. | None |

- **Tags.** A release is a tag named `v` plus the version, such as `v1.2.0` or `v2026.12.0`. A tag never moves and is never deleted. Fixing a release means cutting a new one.
- **Who cuts a release.** A maintainer of that repository. During the founding phase, an owner can too.
- **First release of `backend` and `frontend`.** Each service cuts its first release when it first deploys to production, and then one for every production deploy.
- **The shared checks in `.github`.** A major version is any change that can make a commit or pull request fail when it passed before, such as a new or stricter rule. A minor version adds something without failing anything that passed. A patch fixes a bug or improves a message. Every release gets a `CHANGELOG.md` entry and a GitHub release.
- **Pinning the shared checks.** Other repositories pin the hook and the workflow to the release's commit SHA with the version in a comment (`@<sha> # v1.0.0`). Dependabot keeps the pins current: the `github-actions` ecosystem for the workflow, and the `pre-commit` ecosystem for the hook.

## Becoming a maintainer

You don't need to join the GitHub organization to contribute, and there is no application. After your first merged pull request, a maintainer invites you to the organization's `contributors` team. Sustained contribution can earn a role team with write access, and later a maintainer role. Existing maintainers nominate people for both in public. Members with no activity for 90 days are removed, and can return the same way. See [contributor roles](https://github.com/openpickleball/.github/blob/main/GOVERNANCE.md#contributor-roles).

## Licensing of contributions

You keep the copyright to your work. Your contribution is licensed under the license of the repository you contribute to. See [how OPEN is licensed](https://github.com/openpickleball/.github/blob/main/LICENSING.md).
