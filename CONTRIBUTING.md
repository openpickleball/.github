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

Before proposing a new feature, ask whether it makes the standard more accurate, more trusted, or easier to adopt. If it doesn't, it probably belongs in a partner's product.

Please report security problems privately. See the [security policy](https://github.com/openpickleball/.github/blob/main/SECURITY.md).

## Changes to the rating spec

Anyone can propose or challenge a change to the rating spec by opening an issue. Include the evidence for it, ideally how the change affects predictive accuracy and calibration on matches the engine hasn't seen. A change that gets support becomes a written proposal (an RFC) in the [`rating-spec` repository](https://github.com/openpickleball/rating-spec), following its [RFC process](https://github.com/openpickleball/rating-spec/blob/main/rfcs/README.md). The governing board makes the final decision on changes to the official spec.

## Pull requests

1. Link the issue the pull request addresses with `Closes #N` in the description, or `Refs #N` or `Part of #N` when the issue stays open. The pull request template starts the description for you.
2. Keep each pull request to one change.
3. Add or update tests and documentation when behavior changes.
4. Sign off every commit, as described below.
5. Write each commit message as described in "Commit messages" below. Leave a type prefix such as `fix:` off the pull request title too.

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

## Becoming a maintainer

You don't need to join the GitHub organization to contribute, and there is no application. After your first merged pull request, a maintainer invites you to the organization's `contributors` team. Sustained contribution can earn a role team with write access, and later a maintainer role. Existing maintainers nominate people for both in public. Members with no activity for 90 days are removed, and can return the same way. See [contributor roles](https://github.com/openpickleball/.github/blob/main/GOVERNANCE.md#contributor-roles).

## Licensing of contributions

You keep the copyright to your work. Your contribution is licensed under the license of the repository you contribute to. See [how OPEN is licensed](https://github.com/openpickleball/.github/blob/main/LICENSING.md).
