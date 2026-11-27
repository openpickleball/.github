# SPDX-License-Identifier: Apache-2.0
"""Tests for check_pull_request.py.

Plain functions with plain asserts, so pytest collects them, and they also
run with the standard library alone, as the `scripts` workflow runs them:

    python3 -I scripts/test_check_pull_request.py
"""

import json
import subprocess
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_pull_request as check

SCRIPT = Path(__file__).resolve().parent / "check_pull_request.py"
ROOT = SCRIPT.parent.parent

GOOD = (
    "Import email tasks before checking their registration\n"
    "\n"
    "autodiscover_tasks() loads task modules lazily outside a worker.\n"
    "\n"
    "Closes #328\n"
    "\n"
    "Signed-off-by: A Contributor <contributor@example.com>\n"
)


def _problems(message: str) -> list[str]:
    return check.check_commit_message(message)


def test_a_good_message_passes() -> None:
    assert _problems(GOOD) == []
    assert check.check_commit_message(GOOD, require_sign_off=True) == []


def test_each_rule_reports_its_problem() -> None:
    cases = [
        ("", "subject line is empty"),
        ("A" * 73 + "\n\nWhy.", "73 characters"),
        ("test: fix the routing test\n\nWhy.", "type prefix"),
        ("fix(api)!: change it\n\nWhy.", "type prefix"),
        ("fixup! Add a thing\n\nWhy.", "squashed"),
        ("add a thing\n\nWhy.", "capital letter"),
        ("Add a thing.\n\nWhy.", "period"),
        ("Add a thing\nWhy on the second line.", "blank line"),
        ("Add a thing", "Add a body"),
        ("Add a thing\n\nSigned-off-by: A <a@example.com>", "Add a body"),
        ("Add a thing\n\nWhy \x07apps.", "shell escaping"),
    ]
    for message, expected in cases:
        problems = _problems(message)
        assert any(expected in problem for problem in problems), (message, problems)


def test_the_hook_requires_a_sign_off() -> None:
    message = "Add a thing\n\nWhy it is needed."
    assert _problems(message) == []
    problems = check.check_commit_message(message, require_sign_off=True)
    assert problems == ["Sign off the commit: git commit -s."]


def test_merge_and_revert_messages_written_by_git_pass() -> None:
    assert _problems("Merge branch 'main' into issue-1-thing") == []
    revert = 'Revert "' + "A" * 80 + '"\n\nThis reverts commit abc1234.'
    assert _problems(revert) == []


def test_tab_and_crlf_are_not_problems() -> None:
    assert _problems("Add a thing\r\n\r\nWhy:\tbecause it is needed.\r\n") == []


def test_issue_links_are_accepted() -> None:
    for link in [
        "Closes #328",
        "fixes #1",
        "Resolves: #12",
        "Refs #105 (left open)",
        "Part of #306.",
        "Closes openpickleball/backend#3",
        "Closes https://github.com/openpickleball/backend/issues/3",
    ]:
        body = f"Summary.\n\n{link}\n"
        assert check.check_description("Add a thing", body) == [], link


def test_a_description_without_an_issue_link_fails() -> None:
    problems = check.check_description("Add a thing", "See issue 328.")
    assert any("Link the issue" in problem for problem in problems)


def test_a_title_prefix_and_control_characters_fail() -> None:
    problems = check.check_description("test: fix it", "Fixes #328 in \x07pps")
    assert len(problems) == 2


def test_shell_escaping_damage_fails() -> None:
    # From backend pull request 329: backticks typed in PowerShell.
    for body in [
        "Fixes #328\n\\\ttest_email_outbox_tasks_go_to_email\\ failed",
        "Fixes #328\nImport \\^Gpps.emails.tasks\\ first.",
    ]:
        problems = check.check_description("Import email tasks first", body)
        assert any("shell escaping" in problem for problem in problems), body


def test_plain_tabs_and_markdown_escapes_pass() -> None:
    body = "Closes #1\n\n| a\t| b |\n\\*not a list\\*, `code`\n"
    assert check.check_description("Add a thing", body) == []


def test_api_pages_skip_merge_commits() -> None:
    page_one = [
        {"sha": "a" * 40, "parents": [{}], "commit": {"message": GOOD}},
        {"sha": "b" * 40, "parents": [{}, {}], "commit": {"message": "Merge"}},
    ]
    page_two = [{"sha": "c" * 40, "parents": [{}], "commit": {"message": "x"}}]
    pages = json.dumps(page_one) + "\n" + json.dumps(page_two) + "\n"
    commits = check.commits_from_api(pages)
    assert [commit.sha[0] for commit in commits] == ["a", "c"]


def test_a_pull_request_reports_each_commit_and_the_description() -> None:
    commits = [check.Commit("d717dfab" + "0" * 32, "test: fix it")]
    problems = check.check_pull_request(commits, "test: fix it", "", "someone")
    assert any(problem.startswith("Pull request: ") for problem in problems)
    assert any(
        problem.startswith("Commit d717dfa (test: fix it): ") for problem in problems
    )


def test_dependabot_pull_requests_are_exempt() -> None:
    commits = [check.Commit("a" * 40, "Bump redis from 8.1.0 to 8.2.0 " + "x" * 60)]
    assert check.check_pull_request(commits, "Bump redis", "", "dependabot[bot]") == []


def test_git_comments_and_the_scissors_diff_are_stripped() -> None:
    message = (
        "Add a thing\n\nWhy it is needed.\n\n"
        "# Please enter the commit message for your changes.\n"
        "# ------------------------ >8 ------------------------\n"
        "diff --git a/x b/x\n"
    )
    assert check.strip_git_comments(message) == "Add a thing\n\nWhy it is needed."


def _run(
    args: list[str], env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", str(SCRIPT), *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_the_commit_msg_command_exits_with_the_result() -> None:
    with tempfile.TemporaryDirectory() as directory:
        good = Path(directory) / "good"
        good.write_text(GOOD, encoding="utf-8")
        bad = Path(directory) / "bad"
        bad.write_text("test: fix it\n", encoding="utf-8")
        assert _run(["commit-msg", str(good)]).returncode == 0
        result = _run(["commit-msg", str(bad)])
    assert result.returncode == 1
    assert "type prefix" in result.stdout


def test_the_pr_command_reads_the_environment() -> None:
    with tempfile.TemporaryDirectory() as directory:
        commits = Path(directory) / "commits.json"
        commits.write_text(
            json.dumps(
                [{"sha": "a" * 40, "parents": [{}], "commit": {"message": GOOD}}]
            ),
            encoding="utf-8",
        )
        env = {
            "PR_TITLE": "Add a thing",
            "PR_BODY": "Closes #1",
            "PR_AUTHOR": "someone",
        }
        assert _run(["pr", str(commits)], env).returncode == 0
        env["PR_BODY"] = "No link here"
        assert _run(["pr", str(commits)], env).returncode == 1


def test_the_script_is_executable_for_the_pre_commit_hook() -> None:
    # The hook uses `language: script`, which runs the file directly.
    assert SCRIPT.stat().st_mode & 0o111
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3\n")
    hooks = (ROOT / ".pre-commit-hooks.yaml").read_text(encoding="utf-8")
    assert "entry: scripts/check_pull_request.py commit-msg" in hooks


def test_the_reusable_workflow_keeps_the_title_and_body_out_of_the_shell() -> None:
    # A crafted title pasted into a run: block could run commands.
    action = (ROOT / "actions" / "pull-request-check" / "action.yml").read_text(
        encoding="utf-8"
    )
    workflow = (ROOT / ".github" / "workflows" / "pull-request.yml").read_text(
        encoding="utf-8"
    )
    for text in (action, workflow):
        for line in text.splitlines():
            if "pull_request.title" in line or "pull_request.body" in line:
                assert line.strip().startswith(("PR_TITLE:", "PR_BODY:")), line


def main() -> int:
    tests: list[tuple[str, Callable[[], None]]] = [
        (name, value)
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]
    failed = 0
    for name, test in tests:
        try:
            test()
        except AssertionError as error:
            failed += 1
            print(f"FAIL {name}: {error!r}")
        else:
            print(f"ok   {name}")
    print(f"{len(tests) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
