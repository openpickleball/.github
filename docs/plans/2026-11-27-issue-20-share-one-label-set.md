# Plan: Share one label set across repositories (issue #20)

Risk tier: High. Forced: the sync script renames, merges, and deletes labels across every repository in the organization (a destructive data operation once run with `--apply`). The pull request itself only adds a data file, a script, tests, and docs; nothing runs against GitHub until an owner runs it.

Domain skills: superpowers:test-driven-development: invoke (new Python script). humanizer: invoke (new contributor-facing prose in CONTRIBUTING.md and the profile README). django, django-ninja-api, django-allauth, django-celery, python-fastapi, react, expo, frontend-design, dataviz: not applicable because the change is a standard-library Python script, a TOML file, and Markdown.

## Decisions (from the user, 2026-11-27)

- Priority scale: `priority:p0` to `priority:p2`, reworded to be repository-neutral. `severity:blocker` becomes `priority:p0`, `severity:high` becomes `priority:p1`, `severity:medium` and `severity:low` both become `priority:p2`.
- Type labels: GitHub's `bug`, `enhancement`, `documentation`, plus `type:chore`, `type:spike`, `type:epic`. backend's `type:docs` becomes `documentation` and `type:feature` becomes `enhancement`. The issue forms do not change.
- Ready label: `ready-for-review`. `ready-for-human-review` (in `.github` and backend) becomes `ready-for-review`.
- Scope: this pull request adds the label file, a sync script an owner runs locally (dry run by default, no stored org token, like `scripts/membership-review.sh`), its tests, and the doc links. It says `Part of #20`. Running the sync for real and seeding the starter issues in frontend, engine, and developers are follow-ups the user triggers.

## Current state (measured 2026-11-27 with `gh label list` per repository)

- Eight non-archived repositories: `.github`, backend, frontend, engine, developers, evaluation, rating-spec, brand-assets.
- Only `.github` has discussions enabled (`has_discussions` in the organization's repository listing).
- evaluation, rating-spec, and brand-assets have only GitHub's defaults (plus `accessibility`).
- backend: `type:docs` (no `documentation`), `type:feature` and `enhancement` both present, `ready-for-human-review`, `priority:p0..p2`, `needs-decision`, `status:blocked`, `type:chore/spike/epic`, plus repository-specific `area:*` and `size:*`.
- engine and developers: `severity:blocker/high/medium/low`, `ready-for-review`, `follow-up`.
- frontend: `ready-for-review`. `.github`: `ready-for-human-review`.
- `ready-for-review` differs between repositories: frontend has `0e8a16` and "Checks green, awaiting human review" (the shared values); engine and developers have `5319E7` and "Checks green, ready for maintainer review", so the sync updates both there.
- Merges and their sizes (read-only count, 2026-11-27): backend `type:feature` into `enhancement`, 143 issues and pull requests; engine `severity:low` into `priority:p2`, 22; developers `severity:low`, 0 (deleted after no adds).
- Dependabot labels (`dependencies`, `github_actions`, `docker`, `javascript`, `python`, `uv`, `python:uv`) and repository topics (`math`, `packaging`, `testing`, `code-quality`, `design`, `review-sweep-v1`) are repository-specific and stay untouched.

## Acceptance criteria

1. `labels.toml` at the repository root holds the shared set as `[[label]]` tables, each with `name`, `color` (six hex digits, no `#`), `description` (at most 100 characters, GitHub's limit), and `aliases` (a list of old names that become this label, possibly empty). It starts with `# SPDX-License-Identifier: Apache-2.0` and a comment saying what it is and how to change it. It holds exactly these labels: Every table must have all four keys. Names and aliases must be ASCII, at most 50 characters (GitHub's limit), have no spaces at either end, contain no comma (the issues API reads `labels=a,b` as both), and not be `.` or `..` (they would become path segments); a description must have no spaces at either end. Each rule fails with a clear message.
   - Type: `bug`, `enhancement` (aliases `type:feature`), `documentation` (aliases `type:docs`), `type:chore`, `type:spike`, `type:epic`.
   - Topic: `accessibility`, `governance`, `rating-spec`, `feedback`.
   - Priority: `priority:p0` (aliases `severity:blocker`), `priority:p1` (aliases `severity:high`), `priority:p2` (aliases `severity:medium`, `severity:low`), with repository-neutral descriptions.
   - Status: `triage`, `needs-evidence`, `needs-decision`, `status:blocked`, `ready-for-review` (aliases `ready-for-human-review`), `follow-up`.
   - Community: `good first issue`, `help wanted`, `question`, `duplicate`, `invalid`, `wontfix`.
   Colors and descriptions reuse the current ones where a label already exists (see "Label values" below).
2. Every label that a form in `.github/ISSUE_TEMPLATE/` applies is named in `labels.toml`, and a test checks it by reading the forms, so a new form label without a shared label fails CI. The test reads `*.yml` and `*.yaml` forms, an unreadable `labels:` line fails the test, and labels this repository's workflows apply with `--label` (such as `governance` in `admin-reminders.yml`) are checked the same way.
3. `scripts/sync_labels.py` uses the standard library and the `gh` CLI only. `python3 scripts/sync_labels.py` prints, per repository, every action it would take and changes nothing. `--apply` performs the actions. `--repo NAME` (repeatable) limits the run to those repositories; without it, every non-archived repository in `openpickleball` is synced. `--labels PATH` overrides the label file (default: `labels.toml` next to the `scripts` directory). An empty repository listing (a login that cannot see the organization) is an error. Every change waits at least one second after the previous one (GitHub's guidance for content-changing requests), and a rate-limit failure (HTTP 403 or 429 naming a rate limit) stops the run with a message saying it was rate limited and, with `--apply`, that rerunning resumes (on a dry run, to run the dry run again). On a failure during `--apply`, the message depends on where it happened: inside an action, it says the last listed action did not finish and the ones before it are done; during a read between actions (the repository listing or a repository's labels), it says the error came while reading and every listed action that was not refused is done.
4. The sync never edits or deletes a label whose name (case-insensitive) is not a `name` or alias in `labels.toml`. Repository-specific labels such as `area:api`, `size:M`, and `dependencies` are left alone.
5. Per shared label, per repository, compared case-insensitively:
   - Target present: update its color or description only if they differ (color compared case-insensitively). Then merge each alias also present.
   - Target absent, one or more aliases present: rename the first present alias (in `aliases` order) to the target with the shared color and description, which keeps its issues and pull requests. Merge any other present alias into it.
   - Neither present: create the target.
   - Merging alias A into target T: list every issue and pull request, open and closed, that carries A, with its labels; add T to each one that lacks it (case-insensitive), skipping those that already have it, so a rerun resumes; then list again and repeat until no listed item lacks T (at most 5 passes, else stop and keep A); only then delete A. A is deleted only if every add succeeded; on any failure the run stops with a non-zero exit and A stays.
   - Discussions: discussions carry repository labels, but the issues API does not return them. In a repository with discussions enabled (from the organization's repository listing; today only `.github`; a missing or non-boolean `has_discussions` counts as enabled, so the guard fails safe), a Merge is refused: the dry run prints it as `refused:` with the reason, and `--apply` skips it before it makes any call, still runs the renames, updates, and creates, and exits non-zero naming each refused merge and saying to move the labels on issues and discussions by hand. It names them on the error path too, when a later call fails.
6. A second run on a synced repository plans no actions (idempotent).
7. `scripts/test_sync_labels.py` follows `scripts/test_check_pull_request.py`'s style (plain functions with plain asserts, collected by pytest, runnable as `python3 -I scripts/test_sync_labels.py` with its own `main()`), covers criteria 1, 2, 4, 5, and 6 against a fake client with no network, and the `Scripts` workflow runs it. It asserts all four fields of every row of "Label values".
8. Docs:
   - CONTRIBUTING.md gets a `## Labels` section: `labels.toml` is the shared set every repository uses; a repository may add its own labels (for example `area:` labels) but not redefine a shared one; to change the shared set, open a pull request against `labels.toml`, and after it merges an organization owner runs `scripts/sync_labels.py` (dry run first, then `--apply`). It also says that renaming a shared label means adding the old name to `aliases` (without it, the sync creates the new label and leaves the old one), and that removing a label from the file changes nothing in the repositories. The `labels.toml` header says the same, and the `Scripts` workflow header names the label sync.
   - CONTRIBUTING.md gets a pointer to first issues: the organization-wide search for open `good first issue` issues, `https://github.com/search?q=org%3Aopenpickleball+label%3A%22good+first+issue%22+is%3Aopen+is%3Aissue&type=issues`, placed where a newcomer reads it (in or next to "Start with an issue"). (`github.com/issues` returns 404 to signed-out visitors; `github.com/search` works for them)
   - `profile/README.md` links the same search near "To get started".
   - README.md's "What else is here" lists `labels.toml` and the sync script in `scripts`.
   - If LICENSING.md enumerates files or paths by license, it covers `labels.toml`.
9. No emojis and no em dashes in any changed file. `python3 -I scripts/test_check_pull_request.py` still passes.

## Label values

| name | color | description | aliases |
| --- | --- | --- | --- |
| bug | d73a4a | Something isn't working | |
| enhancement | a2eeef | New feature or request | type:feature |
| documentation | 0075ca | Improvements or additions to documentation | type:docs |
| type:chore | 5319e7 | Tooling, infrastructure, or maintenance | |
| type:spike | fbca04 | Decision, investigation, or ADR | |
| type:epic | 3e4b9e | Parent issue that tracks sub-issues | |
| accessibility | f143ab | Barrier affecting people with disabilities | |
| governance | 0e8a16 | Charter, board, and decision-making | |
| rating-spec | 5319e7 | Changes to the official rating spec | |
| feedback | 1d76db | Input from players, clubs, and platforms | |
| priority:p0 | b60205 | Blocks a release or other work: do it first | severity:blocker |
| priority:p1 | d93f0b | Needed for the current milestone | severity:high |
| priority:p2 | fef2c0 | Later, or low impact | severity:medium, severity:low |
| triage | d4c5f9 | Waiting for a maintainer to review | |
| needs-evidence | fbca04 | Needs data or analysis to support it | |
| needs-decision | d93f0b | Waiting on a maintainer decision | |
| status:blocked | 000000 | Waiting on an external decision or dependency | |
| ready-for-review | 0e8a16 | Checks green, awaiting human review | ready-for-human-review |
| follow-up | c5def5 | Found while working another issue | |
| good first issue | 7057ff | Good for newcomers | |
| help wanted | 008672 | Extra attention is needed | |
| question | d876e3 | Further information is requested | |
| duplicate | cfd3d7 | This issue or pull request already exists | |
| invalid | e4e669 | This doesn't seem right | |
| wontfix | ffffff | This will not be worked on | |

## Files that change

- `labels.toml` (new): the shared set (criterion 1).
- `scripts/sync_labels.py` (new): the sync (criteria 3 to 6).
- `scripts/test_sync_labels.py` (new): its tests (criterion 7).
- `.github/workflows/scripts.yml`: one more `run:` step for the new tests.
- `CONTRIBUTING.md`, `profile/README.md`, `README.md`, and `LICENSING.md` (it enumerates the Apache-2.0 paths, so it now names `labels.toml`; README.md's License paragraph enumerates them too and also names it) (criterion 8).
- This plan.

## Order of work

1. Tests for `labels.toml` validity and issue-form coverage (red: no file), then `labels.toml`.
2. Script design, pure core first:
   - `load_labels(path) -> list[SharedLabel]` (a frozen dataclass: name, color, description, aliases) using `tomllib`, validating as criterion 1 says and raising `LabelFileError`, a `ValueError` subclass (ruff's TRY004 flags a plain `ValueError` after an `isinstance` check), with a clear message. Names and aliases must be unique across the file, case-insensitively, and unknown keys are rejected.
   - `plan_repo(shared, existing) -> list[Action]`, where `existing` is the repository's labels (name, color, description) and `Action` is a small dataclass or a union of dataclasses: `Create(label)`, `Update(current, label)`, `Rename(current, label)`, `Merge(alias, target)`, where `current` is the repository's existing label so the output can say what changes. `Update` also fixes a name that differs only in case. Pure, no I/O. Implements criteria 4 to 6.
   - A `Client` protocol with the operations the actions need: `list_labels(repo)`, `create_label`, `update_label(repo, current_name, new_name, color, description)`, `issues_with_label(repo, name) -> list[Issue]` (state all, issues and pull requests, each with its label names), `add_label(repo, number, name)`, `delete_label(repo, name)`, `list_repos()` (non-archived, as `Repo(name, has_discussions)`).
   - `GhClient` implementing it over `subprocess.run(["gh", "api", ...])`, with label names URL-encoded in paths (`urllib.parse.quote(name, safe="")`, so `good first issue` and `priority:p0` work) and pagination handled. The installed `gh` is 2.45, which has no `--slurp`: either `--paginate --jq '.[]'` (one JSON value per line) or parse concatenated arrays with `json.JSONDecoder.raw_decode` as `check_pull_request.py` does. It sleeps `WRITE_PAUSE` (1 second) before each write after the first, through an injectable `sleep` so tests do not wait, and raises `RateLimitError` (a `GhError`) when the error names a rate limit or HTTP 429.
   - `apply_actions(client, repo, actions)` in order, merges as criterion 5 says (skip items that have the target, list again, delete last). `refusal(repo, action)` returns why a Merge cannot run in a repository with discussions.
   - `main(argv, client=None) -> int` with argparse (the client parameter lets tests pass the fake); `--repo` names are checked against `list_repos` first, so an unknown or archived name fails with the list of valid ones before any label call; dry run prints each action in a readable line per repository and a total; `--apply` prints each action as it runs. Use `print` for this CLI output, consistent with the existing scripts.
   Write each test red first: plan cases (create, update on drift, no-op, color case, name case, rename single alias, merge alias into present target, rename first and merge second alias, unlisted labels untouched, idempotent after applying), apply cases (merge adds to every issue before delete; an add failure leaves the alias and returns non-zero; dry run makes no write calls), and the path encoding. Review fixes added: merge skips labeled items and resumes, merge lists again before deleting and gives up after 5 passes, pacing, rate-limit detection and message, discussions refusal in dry run and apply, the not-finished wording, the empty listing, each new loader rule, ASCII-only matching, every label field, `.yaml` forms, unreadable form lines, workflow `--label` uses, and the doc links and wording.
3. Add the test run to `.github/workflows/scripts.yml`, matching the existing step.
4. Docs (criterion 8), with the humanizer skill on the new prose.
5. Gate.

## Risks

- **Data loss on merge.** Deleting an alias removes it from every issue. Mitigated by adding the target first, deleting only after every add succeeds, dry run by default, and tests for the failure path. The merge lists again after its adds and deletes only when no listed item lacks the target, so an issue labeled during the run is not lost. Merges in a repository with discussions are refused, because the sync cannot see or relabel discussion labels.
- **Label names the API mishandles.** A comma, a `.` or `..`, surrounding spaces, more than 50 characters, or non-ASCII letters would make the sync filter, address, or match labels wrongly. The loader rejects them, and matching folds only ASCII case.
- **Case-insensitive names.** GitHub treats `Bug` and `bug` as the same label. Matching must be case-insensitive, or the sync tries to create a duplicate and fails.
- **Renaming meaning.** backend's priority descriptions change wording (user accepted). `severity:low` and `severity:medium` collapse into `priority:p2` (user accepted).
- **Partial runs.** A run interrupted mid-repository leaves it half synced; rerunning is safe because planning reads current state (idempotence test).
- **Other repositories' docs and local agent profiles** that name `ready-for-human-review`, `type:docs`, or `severity:*` go stale after the sync runs. Out of scope here; the final report lists them as follow-ups.
- **Rate limits.** backend's `type:feature` merge is 143 issues and pull requests (measured 2026-11-27), one add each. GitHub's secondary limit allows about 80 content-creating requests a minute and asks for at least a second between them, so an unpaced run could be stopped at the same point on every rerun. Mitigated by a one-second pause between writes (about 60 a minute), skipping items that already have the target so a rerun resumes, and a rate-limit message that says to wait and rerun.

Not doing: a GitHub Actions workflow that syncs automatically (needs an org-wide token; the user chose an owner-run script), deleting labels outside the set, running the sync, writing starter issues.

## Proof

- Criteria 1 and 2: `test_sync_labels.py` file-validity and issue-form tests. Measured on `origin/main` (24109c0): `grep -rn labels .github/ISSUE_TEMPLATE/` gives `bug`, `triage`, `enhancement`, `feedback`, `rating-spec`, `needs-evidence`, all in the set above.
- Criteria 4 to 6: plan and apply tests against the fake client.
- Criterion 3 and live drive: run `python3 scripts/sync_labels.py` (dry run, real `gh`, read-only API calls) against the organization and check the printed plan matches "Current state": backend renames `type:docs` and `ready-for-human-review`, merges `type:feature` into `enhancement`; engine and developers rename `severity:blocker/high/medium` and merge `severity:low` into `priority:p2`; evaluation, rating-spec, and brand-assets get creates; no line names a label outside the set. Also `--repo backend` limits output to backend. Failure and edge paths (High tier): the fake-client failure test, plus a dry run with `--labels` pointing at an invalid file (duplicate name) exits non-zero with a clear message, and `--repo does-not-exist` fails clearly. Never run `--apply` in this run.
- Criterion 9: grep changed files for the em dash character; both test files pass under `python3 -I`; `ruff check` and `ruff format --check` on the new script and test (via `uvx ruff`) since the user's standard asks for ruff even though CI does not run it.

### Results before review (2026-11-27)

- Both test files pass under `python3 -I` (18 and 32 tests); `uvx ruff check` and `uvx ruff format --check` are clean.
- `python3 scripts/sync_labels.py` (dry run, GET calls only) planned 91 actions in 8 repositories, matching "Current state": backend merges `type:feature` into `enhancement`, renames `type:docs` to `documentation` and `ready-for-human-review` to `ready-for-review`, rewords the three priority descriptions, and creates `follow-up`; `.github` renames `ready-for-human-review`; engine and developers rename `severity:blocker/high/medium` to `priority:p0/p1/p2`, merge `severity:low` into `priority:p2`, and update `ready-for-review`'s color and description; evaluation, rating-spec, and brand-assets get 15 creates each; frontend gets 9 creates. No line names a label outside the set (`area:*`, `size:*`, Dependabot, and topic labels are absent).
- `--repo backend` printed only backend (7 actions).
- `--labels` with a duplicate `Bug` exits 1: `'Bug' is used more than once (by labels 'bug' and 'Bug')`. A missing file exits 1: `cannot read: No such file or directory`.
- `--repo does-not-exist` exits 1: `does-not-exist: not a non-archived repository in openpickleball. Repositories: .github, backend, ...`.
- `--apply` was not run.

### Review fixes R1 to R8: failing tests before the fix (2026-11-27)

The review found eight defects. Their tests were written first, in `scripts/test_sync_labels.py`, which was then frozen in `.claude/fix-lock`. Run with `uvx --with pytest pytest -q --tb=line scripts/test_sync_labels.py` (pytest reports every failure; the file's own runner stops at the first crash): 25 failed, 26 passed. The failures, by defect:

- R1 (merge re-adds to labeled issues, unpaced writes, no rate-limit message): `test_a_merge_skips_issues_that_already_have_the_target`, `test_a_rerun_after_a_failed_merge_adds_only_what_is_left`, and `test_reads_join_every_page` fail with `AttributeError: module 'sync_labels' has no attribute 'Issue'`; `test_writes_are_paced_and_reads_are_not` fails with `TypeError: GhClient.__init__() got an unexpected keyword argument 'sleep'`; `test_a_rate_limit_response_raises_rate_limit_error` and `test_a_rate_limited_apply_says_so_and_that_rerunning_resumes` fail with `AttributeError: module 'sync_labels' has no attribute 'RateLimitError'`.
- R2 (alias added during a merge is lost): `test_a_merge_lists_again_before_deleting_the_alias` and `test_a_merge_that_never_settles_stops_and_keeps_the_alias` fail with `AttributeError: ... 'Issue'`.
- R3 and R7d (loader accepts bad names): `test_each_invalid_label_file_reports_its_problem` fails with `AssertionError: no error for '[[label]]\nname = "bug"\ncolor = "d73a4a"\ndescription = "Broken"\n'` (no `aliases`). Each new case checked on its own also loads with no error: `" bug"`, alias `"a,b"`, alias `"."`, a 51-character name, `"straße"`, and description `"Broken "`. `test_non_ascii_names_do_not_fold_into_shared_names` fails with `assert [Update(...)] == [Create(...)]` (casefold matched `straße` to `strasse`).
- R4 (merges in a repository with discussions): `test_the_dry_run_refuses_a_merge_where_discussions_are_on` and `test_apply_skips_a_merge_where_discussions_are_on_and_fails` fail with `AttributeError: module 'sync_labels' has no attribute 'Repo'`. The other fake-client tests fail the same way because the fake now returns `Repo` and `Issue` values.
- R5 (failed action reported as done): `test_a_failed_action_is_reported_as_not_done` fails with `AttributeError: ... 'Repo'`; before the fake changed, the message was "The actions above this one are done", which counted the failed action.
- R6 (first-issue link 404s signed out): `test_the_first_issue_links_work_signed_out` fails with `AssertionError: CONTRIBUTING.md`.
- R7 (a, b, c): `test_the_label_file_holds_exactly_the_shared_set`, `test_an_unreadable_form_labels_line_fails_the_test`, `test_issue_forms_include_yaml_files`, and `test_every_workflow_label_is_a_shared_label` pass at once: they check labels.toml, the forms, and the workflows, which were already right, so the defect was missing coverage rather than wrong code.
- R8 (a, b, c): `test_the_docs_say_how_renames_and_removals_work` fails with `assert 'aliases' in '\n\nEvery OPEN repository uses the same set of labels, ...'`; `test_the_workflow_header_names_the_label_sync` fails with `assert 'label sync' in '# SPDX-License-Identifier: Apache-2.0\n# Tests the scripts that other repositories run.\n'`; `test_no_visible_repositories_is_an_error` fails with `assert 0 == 1` (exit 0 on an empty listing).

### Results after the review fixes (2026-11-27)

- `.claude/fix-lock` held `scripts/test_sync_labels.py` while production code changed; its sha256 was unchanged at green, and the lock was removed. `python3 -I scripts/test_sync_labels.py`: 51 passed. `python3 -I scripts/test_check_pull_request.py`: 18 passed. ruff check and format check clean. No em dashes.
- The org-wide dry run plans the same 91 actions in 8 repositories as before; no merge falls in `.github`, so nothing is refused today. `--repo backend`: 7 actions. `--repo does-not-exist`: exit 1 with the list of repositories.
- One invalid `--labels` file per rule, each exit 1 with its message: duplicate `Bug`, missing `aliases` (`needs aliases (aliases = [] for none)`), name `" bug"`, alias `"old "`, description with a trailing space, alias `"a,b"` (`contains a comma`), alias `"."` and name `".."` (`would be a path segment`), a 51-character name (`GitHub allows 50 characters`), and `"straße"` (`must be ASCII`).
- Discussions, read only: a scratch file giving `bug` the alias `documentation` (both exist in `.github`) with `--repo .github --repo backend` printed `refused: merge documentation into bug (...): this repository has discussions, ...` for `.github` only, and `3 actions planned in 2 repositories (1 refused)`. The `--apply` side (skip, run the rest, exit 1) is covered by `test_apply_skips_a_merge_where_discussions_are_on_and_fails`, since `--apply` is never run here.
- Pacing and rate-limit handling are covered by `test_writes_are_paced_and_reads_are_not` and the rate-limit tests. Checking them live would need writes.


### Review fixes F1 to F3: failing tests before the fix (2026-11-27)

Five new test functions were added to `scripts/test_sync_labels.py` (no existing test changed; a diff against the previous copy shows additions only), and the file was frozen again in `.claude/fix-lock`. `python3 -I scripts/test_sync_labels.py`: 51 passed, 5 failed. pytest reasons:

- F1 (a read error reported as an unfinished action): `test_a_failed_read_after_actions_does_not_call_them_unfinished` (every backend action ran, the last line printed was `create ...`, then `list_labels("evaluation")` raised HTTP 502) and `test_a_failed_repository_listing_is_reported_as_a_read` fail with `assert 'did not finish' not in '... The last action listed above did not finish (a merge may have added some labels already); the actions before it are done. ...'`. `test_a_rate_limited_dry_run_says_to_rerun_the_dry_run` fails with `assert 'resumes' not in '... run again: it resumes where it stopped.'` on a dry run.
- F2 (refused merges not named on the error path): `test_a_failure_after_a_refused_merge_still_names_it` fails with `assert 'refused these merges' in 'sync_labels: gh api GET repos/openpickleball/evaluation: HTTP 502\nsync_labels: stopped. ...'`.
- F3 (missing `has_discussions` fails open): `test_a_missing_discussions_field_counts_as_discussions_on` fails with `At index 0 diff: Repo(name='a', has_discussions=False) != Repo(name='a', has_discussions=True)`.

### Results after F1 to F3 (2026-11-27)

- The lock was released at green with the file's sha256 unchanged. `python3 -I scripts/test_sync_labels.py`: 56 passed. The gate and the live dry runs were rerun: `test_check_pull_request.py` 18 passed, `test_sync_labels.py` 56 passed, ruff check and format clean, no em dashes; the full dry run planned the same 91 actions in 8 repositories (exit 0), `--repo backend` planned 7, and `--repo does-not-exist` exited 1 listing the valid repositories. A fresh verifier then exercised the `--apply` paths through an in-memory fake (adds before delete, skip of items that already have the target, refusal where discussions are on, resume after a failed add, idempotent second pass) and found nothing.

