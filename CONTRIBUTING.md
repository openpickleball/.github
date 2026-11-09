# Contributing to OPEN

Thanks for helping build OPEN, the Open Pickleball Evaluation Network. This guide applies to every repository in the [openpickleball](https://github.com/openpickleball) organization unless a repository has its own `CONTRIBUTING.md`.

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

Anyone can propose or challenge a change to the rating spec by opening an issue. Include the evidence for it, ideally how the change affects predictive accuracy and calibration on matches the engine hasn't seen. The governing board makes the final decision on changes to the official spec.

## Pull requests

1. Link the issue the pull request addresses.
2. Keep each pull request to one change.
3. Add or update tests and documentation when behavior changes.
4. Sign off every commit, as described below.

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

You don't need to join the GitHub organization to contribute, and there is no application. People earn triager and maintainer roles by contributing, and existing maintainers nominate new maintainers in public. See [contributor roles](https://github.com/openpickleball/.github/blob/main/GOVERNANCE.md#contributor-roles).

## Licensing of contributions

You keep the copyright to your work. Your contribution is licensed under the license of the repository you contribute to. See [how OPEN is licensed](https://github.com/openpickleball/.github/blob/main/LICENSING.md).
