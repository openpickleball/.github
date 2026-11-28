# Changelog

This file records changes to what other OPEN repositories use from this one: the `commit-message` pre-commit hook (`.pre-commit-hooks.yaml`), the reusable `pull-request` workflow (`.github/workflows/pull-request.yml`), and the `pull-request-check` action and script behind them. Versions follow [Semantic Versioning](https://semver.org/) as described in [Releases and versioning](CONTRIBUTING.md#releases-and-versioning). Changes to the community files and governance documents are not versioned and are not listed here.

## [Unreleased]

No changes to the shared checks since 1.0.0.

## [1.0.0] - 2026-11-27

The first release of the shared checks.

- The `commit-message` pre-commit hook checks each commit message against [Commit messages](CONTRIBUTING.md#commit-messages): an imperative subject of at most 72 characters that starts with a capital letter, with no period at the end and no type prefix; a blank line and a body; no leftover `fixup!`, `squash!`, or `amend!` commits; no control characters; and a `Signed-off-by` line.
- The reusable `pull-request` workflow runs the same message checks on every commit in a pull request, except the sign-off, which each repository's DCO check covers. Merge commits are skipped. It also checks the title for a type prefix, checks that the description links an issue (`Closes #N`, `Refs #N`, or `Part of #N`), and flags text damaged by shell escaping. Its status check is `pull-request / check`.

[Unreleased]: https://github.com/openpickleball/.github/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/openpickleball/.github/releases/tag/v1.0.0
