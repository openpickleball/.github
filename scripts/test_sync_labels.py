# SPDX-License-Identifier: Apache-2.0
"""Tests for sync_labels.py and labels.toml.

Plain functions with plain asserts, so pytest collects them, and they also
run with the standard library alone, as the `scripts` workflow runs them:

    python3 -I scripts/test_sync_labels.py

Nothing here calls GitHub: the sync runs against a fake client.
"""

from __future__ import annotations

import contextlib
import io
import json
import re
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sync_labels as sync

SCRIPT = Path(__file__).resolve().parent / "sync_labels.py"
ROOT = SCRIPT.parent.parent
LABELS = ROOT / "labels.toml"


def _load_text(text: str) -> list[sync.SharedLabel]:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "labels.toml"
        path.write_text(text, encoding="utf-8")
        return sync.load_labels(path)


def _load_error(text: str) -> str:
    try:
        _load_text(text)
    except ValueError as error:
        return str(error)
    raise AssertionError(f"no error for {text!r}")


# labels.toml


# The plan's "Label values" table (docs/plans/2026-11-27-issue-20-...).
SHARED_SET = [
    ("bug", "d73a4a", "Something isn't working", ()),
    ("enhancement", "a2eeef", "New feature or request", ("type:feature",)),
    (
        "documentation",
        "0075ca",
        "Improvements or additions to documentation",
        ("type:docs",),
    ),
    ("type:chore", "5319e7", "Tooling, infrastructure, or maintenance", ()),
    ("type:spike", "fbca04", "Decision, investigation, or ADR", ()),
    ("type:epic", "3e4b9e", "Parent issue that tracks sub-issues", ()),
    ("accessibility", "f143ab", "Barrier affecting people with disabilities", ()),
    ("governance", "0e8a16", "Charter, board, and decision-making", ()),
    ("rating-spec", "5319e7", "Changes to the official rating spec", ()),
    ("feedback", "1d76db", "Input from players, clubs, and platforms", ()),
    (
        "priority:p0",
        "b60205",
        "Blocks a release or other work: do it first",
        ("severity:blocker",),
    ),
    ("priority:p1", "d93f0b", "Needed for the current milestone", ("severity:high",)),
    (
        "priority:p2",
        "fef2c0",
        "Later, or low impact",
        ("severity:medium", "severity:low"),
    ),
    ("triage", "d4c5f9", "Waiting for a maintainer to review", ()),
    ("needs-evidence", "fbca04", "Needs data or analysis to support it", ()),
    ("needs-decision", "d93f0b", "Waiting on a maintainer decision", ()),
    ("status:blocked", "000000", "Waiting on an external decision or dependency", ()),
    (
        "ready-for-review",
        "0e8a16",
        "Checks green, awaiting human review",
        ("ready-for-human-review",),
    ),
    ("follow-up", "c5def5", "Found while working another issue", ()),
    ("good first issue", "7057ff", "Good for newcomers", ()),
    ("help wanted", "008672", "Extra attention is needed", ()),
    ("question", "d876e3", "Further information is requested", ()),
    ("duplicate", "cfd3d7", "This issue or pull request already exists", ()),
    ("invalid", "e4e669", "This doesn't seem right", ()),
    ("wontfix", "ffffff", "This will not be worked on", ()),
]


def test_the_label_file_holds_exactly_the_shared_set() -> None:
    labels = sync.load_labels(LABELS)
    assert [
        (label.name, label.color, label.description, label.aliases) for label in labels
    ] == SHARED_SET


def test_the_label_file_starts_with_its_license_and_purpose() -> None:
    lines = LABELS.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# SPDX-License-Identifier: Apache-2.0"
    assert lines[1].startswith("# ")
    assert "sync_labels.py" in LABELS.read_text(encoding="utf-8")


def _form_labels(name: str, text: str) -> list[str]:
    """The labels an issue form applies. A line it cannot read fails the test."""
    names: list[str] = []
    for line in text.splitlines():
        if not line.startswith("labels:"):
            continue
        flow = re.fullmatch(r"labels:\s*(\[.*\])\s*", line)
        assert flow, f'{name}: write labels as a ["a", "b"] list: {line!r}'
        try:
            parsed = json.loads(flow.group(1))
        except json.JSONDecodeError as error:
            raise AssertionError(f"{name}: cannot read {line!r}: {error}") from error
        assert isinstance(parsed, list), f"{name}: {line!r}"
        assert all(isinstance(item, str) for item in parsed), f"{name}: {line!r}"
        names += parsed
    return names


def _workflow_labels(text: str) -> list[str]:
    """The labels a workflow applies with `--label NAME` or `--add-label NAME`."""
    found = re.findall(r"--(?:add-)?label[= ]+(\"[^\"]*\"|'[^']*'|[^\s\"']+)", text)
    return [name.strip("\"'") for name in found]


def _issue_forms(root: Path = ROOT) -> list[Path]:
    forms = root / ".github" / "ISSUE_TEMPLATE"
    return sorted([*forms.glob("*.yml"), *forms.glob("*.yaml")])


def test_every_issue_form_label_is_a_shared_label() -> None:
    # A form that applies a label no repository has fails silently on GitHub.
    shared = {label.name for label in sync.load_labels(LABELS)}
    seen = 0
    for form in _issue_forms():
        for name in _form_labels(form.name, form.read_text(encoding="utf-8")):
            seen += 1
            assert name in shared, f"{form.name} applies {name!r}"
    assert seen >= 4


def test_an_unreadable_form_labels_line_fails_the_test() -> None:
    for line in ['labels: ["bug", triage]', "labels: bug", 'labels: [{"a": 1}]']:
        try:
            _form_labels("form.yml", line)
        except AssertionError:
            continue
        raise AssertionError(f"no failure for {line!r}")
    assert _form_labels("form.yml", 'name: x\nlabels: ["bug", "triage"]') == [
        "bug",
        "triage",
    ]


def test_issue_forms_include_yaml_files() -> None:
    with tempfile.TemporaryDirectory() as directory:
        forms = Path(directory) / ".github" / "ISSUE_TEMPLATE"
        forms.mkdir(parents=True)
        for name in ("a.yaml", "b.yml", "config.txt"):
            (forms / name).write_text("", encoding="utf-8")
        found = [form.name for form in _issue_forms(Path(directory))]
    assert found == ["a.yaml", "b.yml"]


def test_every_workflow_label_is_a_shared_label() -> None:
    shared = {label.name for label in sync.load_labels(LABELS)}
    assert _workflow_labels('gh issue create --label governance --label "a b"') == [
        "governance",
        "a b",
    ]
    seen = 0
    workflows = ROOT / ".github" / "workflows"
    for workflow in sorted([*workflows.glob("*.yml"), *workflows.glob("*.yaml")]):
        for name in _workflow_labels(workflow.read_text(encoding="utf-8")):
            seen += 1
            assert name in shared, f"{workflow.name} applies {name!r}"
    assert seen >= 1


# load_labels validation


GOOD_LABEL = (
    '[[label]]\nname = "bug"\ncolor = "d73a4a"\ndescription = "Broken"\naliases = []\n'
)


def test_a_good_label_loads() -> None:
    assert _load_text(GOOD_LABEL) == [sync.SharedLabel("bug", "d73a4a", "Broken", ())]


def test_each_invalid_label_file_reports_its_problem() -> None:
    cases = [
        ("[[label]\n", "not valid TOML"),
        ("", "no [[label]] tables"),
        ('[[label]]\ncolor = "d73a4a"\ndescription = "x"\naliases = []\n', "name"),
        (GOOD_LABEL.replace('"d73a4a"', '"#d73a4a"'), "six hex digits"),
        (GOOD_LABEL.replace('"d73a4a"', '"d73a4"'), "six hex digits"),
        (GOOD_LABEL.replace('"Broken"', '"' + "x" * 101 + '"'), "100 characters"),
        (GOOD_LABEL.replace("aliases = []", 'aliases = "old"'), "aliases"),
        (GOOD_LABEL.replace("aliases = []", "aliases = [1]"), "aliases"),
        (GOOD_LABEL + 'extra = "x"\n', "unknown key"),
        (GOOD_LABEL + GOOD_LABEL.replace('"bug"', '"Bug"'), "more than once"),
        (
            GOOD_LABEL
            + GOOD_LABEL.replace('"bug"', '"defect"').replace("[]", '["BUG"]'),
            "more than once",
        ),
        (GOOD_LABEL.replace("[]", '["bug"]'), "more than once"),
        (GOOD_LABEL.replace("aliases = []\n", ""), "needs aliases"),
        (GOOD_LABEL.replace('"bug"', '" bug"'), "spaces at the start or end"),
        (GOOD_LABEL.replace('"bug"', '"bug\\t"'), "spaces at the start or end"),
        (GOOD_LABEL.replace("[]", '["old "]'), "spaces at the start or end"),
        (GOOD_LABEL.replace('"Broken"', '"Broken "'), "spaces at the start or end"),
        (GOOD_LABEL.replace("[]", '["a,b"]'), "comma"),
        (GOOD_LABEL.replace('"bug"', '"bug,defect"'), "comma"),
        (GOOD_LABEL.replace("[]", '["."]'), "'.' or '..'"),
        (GOOD_LABEL.replace('"bug"', '".."'), "'.' or '..'"),
        (GOOD_LABEL.replace('"bug"', '"' + "b" * 51 + '"'), "50 characters"),
        (GOOD_LABEL.replace("[]", '["' + "b" * 51 + '"]'), "50 characters"),
        (GOOD_LABEL.replace('"bug"', '"stra\u00dfe"'), "ASCII"),
        (GOOD_LABEL.replace("[]", '["caf\u00e9"]'), "ASCII"),
    ]
    for text, expected in cases:
        error = _load_error(text)
        assert expected in error, (text, error)


def test_names_at_the_limits_load() -> None:
    longest = "b" * 50
    labels = _load_text(GOOD_LABEL.replace('"bug"', f'"{longest}"'))
    assert labels[0].name == longest
    assert _load_text(GOOD_LABEL.replace('"bug"', '"good first issue"'))


def test_a_missing_label_file_is_a_clear_error() -> None:
    try:
        sync.load_labels(ROOT / "does-not-exist.toml")
    except ValueError as error:
        assert "does-not-exist.toml" in str(error)
    else:
        raise AssertionError("no error for a missing file")


# plan_repo


BUG = sync.SharedLabel("bug", "d73a4a", "Something isn't working", ())
DOCS = sync.SharedLabel("documentation", "0075ca", "Docs", ("type:docs",))
P2 = sync.SharedLabel(
    "priority:p2", "fef2c0", "Later", ("severity:medium", "severity:low")
)


def _label(name: str, color: str = "ededed", description: str = "") -> sync.Label:
    return sync.Label(name, color, description)


def _same(shared: sync.SharedLabel) -> sync.Label:
    return sync.Label(shared.name, shared.color, shared.description)


def test_a_missing_label_is_created() -> None:
    assert sync.plan_repo([BUG], []) == [sync.Create(BUG)]


def test_a_matching_label_needs_nothing() -> None:
    assert sync.plan_repo([BUG], [_same(BUG)]) == []


def test_color_case_is_not_drift() -> None:
    assert sync.plan_repo([BUG], [_label("bug", "D73A4A", BUG.description)]) == []


def test_a_drifted_color_or_description_is_updated() -> None:
    color = _label("bug", "ff0000", BUG.description)
    description = _label("bug", BUG.color, "Broken")
    assert sync.plan_repo([BUG], [color]) == [sync.Update(color, BUG)]
    assert sync.plan_repo([BUG], [description]) == [sync.Update(description, BUG)]


def test_names_match_case_insensitively() -> None:
    # GitHub treats Bug and bug as one label, so creating bug would fail.
    existing = _label("Bug", BUG.color, BUG.description)
    assert sync.plan_repo([BUG], [existing]) == [sync.Update(existing, BUG)]


def test_non_ascii_names_do_not_fold_into_shared_names() -> None:
    # casefold() turns "\u00df" into "ss"; GitHub does not.
    strasse = sync.SharedLabel("strasse", "ededed", "", ())
    assert sync.plan_repo([strasse], [_label("stra\u00dfe")]) == [sync.Create(strasse)]


def test_a_single_alias_is_renamed() -> None:
    old = _label("type:docs", "ededed", "Docs work")
    assert sync.plan_repo([DOCS], [old]) == [sync.Rename(old, DOCS)]


def test_an_alias_is_merged_into_a_present_target() -> None:
    old = _label("type:docs")
    assert sync.plan_repo([DOCS], [_same(DOCS), old]) == [
        sync.Merge("type:docs", "documentation")
    ]


def test_an_alias_matches_case_insensitively() -> None:
    old = _label("Type:Docs")
    assert sync.plan_repo([DOCS], [_same(DOCS), old]) == [
        sync.Merge("Type:Docs", "documentation")
    ]


def test_the_first_present_alias_is_renamed_and_the_rest_merged() -> None:
    low = _label("severity:low")
    medium = _label("severity:medium")
    assert sync.plan_repo([P2], [low, medium]) == [
        sync.Rename(medium, P2),
        sync.Merge("severity:low", "priority:p2"),
    ]
    assert sync.plan_repo([P2], [low]) == [sync.Rename(low, P2)]


def test_an_update_comes_before_its_merges() -> None:
    target = _label("priority:p2", "000000", "Old")
    assert sync.plan_repo([P2], [_label("severity:low"), target]) == [
        sync.Update(target, P2),
        sync.Merge("severity:low", "priority:p2"),
    ]


def test_labels_outside_the_set_are_left_alone() -> None:
    existing = [
        _label("area:api"),
        _label("size:M"),
        _label("dependencies"),
        _label("python:uv"),
    ]
    assert sync.plan_repo([BUG, DOCS, P2], existing) == [
        sync.Create(BUG),
        sync.Create(DOCS),
        sync.Create(P2),
    ]


# apply_actions and main, against a fake GitHub


WRITES = frozenset({"create_label", "update_label", "add_label", "delete_label"})


class FakeClient:
    """An in-memory GitHub that keeps labels on issues as GitHub does."""

    def __init__(
        self,
        repos: dict[str, list[sync.Label]],
        issues: dict[str, dict[int, set[str]]] | None = None,
        fail_add: frozenset[int] = frozenset(),
        discussions: frozenset[str] = frozenset(),
    ) -> None:
        self.labels = {repo: list(labels) for repo, labels in repos.items()}
        self.issues = issues or {repo: {} for repo in repos}
        self.fail_add = fail_add
        self.add_error: type[sync.GhError] = sync.GhError
        self.discussions = discussions
        self.calls: list[tuple[str, ...]] = []

    def _find(self, repo: str, name: str) -> int:
        for index, label in enumerate(self.labels[repo]):
            if label.name.casefold() == name.casefold():
                return index
        raise sync.GhError(f"{repo}: no label {name}")

    def list_repos(self) -> list[sync.Repo]:
        self.calls.append(("list_repos",))
        return [
            sync.Repo(name, name in self.discussions) for name in sorted(self.labels)
        ]

    def list_labels(self, repo: str) -> list[sync.Label]:
        self.calls.append(("list_labels", repo))
        if repo not in self.labels:
            raise sync.GhError(f"{repo}: HTTP 404")
        return list(self.labels[repo])

    def create_label(self, repo: str, name: str, color: str, description: str) -> None:
        self.calls.append(("create_label", repo, name))
        self.labels[repo].append(sync.Label(name, color, description))

    def update_label(
        self, repo: str, current: str, name: str, color: str, description: str
    ) -> None:
        self.calls.append(("update_label", repo, current, name))
        old = self.labels[repo][self._find(repo, current)].name
        self.labels[repo][self._find(repo, current)] = sync.Label(
            name, color, description
        )
        for names in self.issues[repo].values():
            if old in names:
                names.discard(old)
                names.add(name)

    def issues_with_label(self, repo: str, name: str) -> list[sync.Issue]:
        self.calls.append(("issues_with_label", repo, name))
        return [
            sync.Issue(number, tuple(sorted(names)))
            for number, names in sorted(self.issues[repo].items())
            if name.casefold() in {n.casefold() for n in names}
        ]

    def add_label(self, repo: str, number: int, name: str) -> None:
        self.calls.append(("add_label", repo, str(number), name))
        if number in self.fail_add:
            raise self.add_error(f"{repo}#{number}: HTTP 502")
        self.issues[repo][number].add(name)

    def delete_label(self, repo: str, name: str) -> None:
        self.calls.append(("delete_label", repo, name))
        del self.labels[repo][self._find(repo, name)]
        for names in self.issues[repo].values():
            names -= {n for n in names if n.casefold() == name.casefold()}


def _backend() -> FakeClient:
    return FakeClient(
        {
            "backend": [
                _label("type:docs"),
                _label("type:feature"),
                _label("enhancement", "a2eeef", "New feature or request"),
                _label("ready-for-human-review"),
                _label("area:api"),
                _label("size:M"),
            ],
            "evaluation": [_label("bug", "d73a4a", "Something isn't working")],
        },
        {
            "backend": {
                1: {"type:feature"},
                2: {"type:feature", "area:api"},
                3: {"type:docs"},
                4: {"size:M"},
            },
            "evaluation": {},
        },
    )


def _run(argv: list[str], client: FakeClient) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = sync.main(argv, client=client)
    return code, out.getvalue(), err.getvalue()


def test_a_merge_adds_the_target_to_every_issue_before_deleting() -> None:
    client = _backend()
    sync.apply_actions(client, "backend", [sync.Merge("type:feature", "enhancement")])
    writes = [call for call in client.calls if call[0] in WRITES]
    assert writes == [
        ("add_label", "backend", "1", "enhancement"),
        ("add_label", "backend", "2", "enhancement"),
        ("delete_label", "backend", "type:feature"),
    ]
    assert client.issues["backend"][1] == {"enhancement"}
    assert client.issues["backend"][2] == {"enhancement", "area:api"}


def test_a_failed_add_keeps_the_alias() -> None:
    client = _backend()
    client.fail_add = frozenset({2})
    try:
        sync.apply_actions(
            client, "backend", [sync.Merge("type:feature", "enhancement")]
        )
    except sync.GhError as error:
        assert "502" in str(error)
    else:
        raise AssertionError("no error for a failed add")
    assert ("delete_label", "backend", "type:feature") not in client.calls
    assert "type:feature" in [label.name for label in client.labels["backend"]]
    assert "type:feature" in client.issues["backend"][2]


def test_a_failed_apply_exits_non_zero_and_stops() -> None:
    client = _backend()
    client.fail_add = frozenset({1})
    code, _, err = _run(["--apply", "--labels", str(LABELS)], client)
    assert code == 1
    assert "502" in err
    # backend sorts first, so the run stopped before evaluation.
    assert not [c for c in client.calls if c[0] in WRITES and c[1] == "evaluation"]


def test_a_merge_skips_issues_that_already_have_the_target() -> None:
    client = _backend()
    client.issues["backend"][1] = {"type:feature", "Enhancement"}
    sync.apply_actions(client, "backend", [sync.Merge("type:feature", "enhancement")])
    adds = [call for call in client.calls if call[0] == "add_label"]
    assert adds == [("add_label", "backend", "2", "enhancement")]


def test_a_rerun_after_a_failed_merge_adds_only_what_is_left() -> None:
    client = _backend()
    client.issues["backend"][5] = {"type:feature"}
    client.fail_add = frozenset({2})
    code, _, _ = _run(["--apply", "--repo", "backend"], client)
    assert code == 1
    client.fail_add = frozenset()
    client.calls.clear()
    code, _, err = _run(["--apply", "--repo", "backend"], client)
    assert code == 0, err
    adds = [call for call in client.calls if call[0] == "add_label"]
    assert adds == [
        ("add_label", "backend", "2", "enhancement"),
        ("add_label", "backend", "5", "enhancement"),
    ]


class GrowingClient(FakeClient):
    """Someone adds the alias to issue 9 while the merge is adding labels."""

    def add_label(self, repo: str, number: int, name: str) -> None:
        super().add_label(repo, number, name)
        if 9 not in self.issues[repo]:
            self.issues[repo][9] = {"type:feature"}


def test_a_merge_lists_again_before_deleting_the_alias() -> None:
    base = _backend()
    client = GrowingClient(base.labels, base.issues)
    sync.apply_actions(client, "backend", [sync.Merge("type:feature", "enhancement")])
    writes = [call for call in client.calls if call[0] in WRITES]
    assert writes == [
        ("add_label", "backend", "1", "enhancement"),
        ("add_label", "backend", "2", "enhancement"),
        ("add_label", "backend", "9", "enhancement"),
        ("delete_label", "backend", "type:feature"),
    ]
    assert client.issues["backend"][9] == {"enhancement"}


class EndlessClient(FakeClient):
    """Every add puts the alias on a new issue, so the merge never settles."""

    def add_label(self, repo: str, number: int, name: str) -> None:
        super().add_label(repo, number, name)
        self.issues[repo][max(self.issues[repo]) + 1] = {"type:feature"}


def test_a_merge_that_never_settles_stops_and_keeps_the_alias() -> None:
    base = _backend()
    client = EndlessClient(base.labels, base.issues)
    try:
        sync.apply_actions(
            client, "backend", [sync.Merge("type:feature", "enhancement")]
        )
    except sync.GhError as error:
        assert "type:feature" in str(error)
    else:
        raise AssertionError("no error for a merge that never settles")
    assert ("delete_label", "backend", "type:feature") not in client.calls


def _with_discussions() -> FakeClient:
    client = _backend()
    client.discussions = frozenset({"backend"})
    return client


def test_the_dry_run_refuses_a_merge_where_discussions_are_on() -> None:
    code, out, err = _run([], _with_discussions())
    assert code == 0, err
    line = next(line for line in out.splitlines() if "type:feature" in line)
    assert line.strip().startswith("refused: merge type:feature into enhancement")
    assert "discussions" in line
    assert "rename type:docs -> documentation" in out
    assert "1 refused" in out


def test_apply_skips_a_merge_where_discussions_are_on_and_fails() -> None:
    client = _with_discussions()
    code, _, err = _run(["--apply"], client)
    assert code == 1
    assert "discussions" in err
    assert "by hand" in err
    merge_calls = [call for call in client.calls if "type:feature" in call]
    assert merge_calls == [], merge_calls
    names = {label.name for label in client.labels["backend"]}
    # The renames, updates, and creates still ran.
    assert {"documentation", "ready-for-review", "follow-up"} <= names
    assert "type:feature" in names
    assert "good first issue" in {label.name for label in client.labels["evaluation"]}


def test_a_failed_action_is_reported_as_not_done() -> None:
    client = _backend()
    client.fail_add = frozenset({1})
    code, _, err = _run(["--apply"], client)
    assert code == 1
    assert "above this one are done" not in err
    assert "did not finish" in err
    assert "Run again" in err


def test_a_rate_limited_apply_says_so_and_that_rerunning_resumes() -> None:
    client = _backend()
    client.fail_add = frozenset({1})
    client.add_error = sync.RateLimitError
    code, _, err = _run(["--apply"], client)
    assert code == 1
    assert "rate limited" in err
    assert "resumes" in err


def test_no_visible_repositories_is_an_error() -> None:
    client = FakeClient({})
    code, out, err = _run([], client)
    assert code == 1
    assert "no repositories" in err
    assert "gh auth status" in err
    assert "0 actions" not in out


def test_applying_then_planning_again_needs_nothing() -> None:
    client = _backend()
    shared = sync.load_labels(LABELS)
    code, _, _ = _run(["--apply"], client)
    assert code == 0
    for repo in client.labels:
        assert sync.plan_repo(shared, client.list_labels(repo)) == [], repo
    names = {label.name for label in client.labels["backend"]}
    assert {"area:api", "size:M", "documentation", "ready-for-review"} <= names
    assert not names & {"type:docs", "type:feature", "ready-for-human-review"}
    assert client.issues["backend"][3] == {"documentation"}
    assert client.issues["backend"][4] == {"size:M"}
    code, out, _ = _run([], client)
    assert code == 0
    assert "0 actions" in out


def test_the_dry_run_prints_the_plan_and_writes_nothing() -> None:
    client = _backend()
    code, out, err = _run([], client)
    assert code == 0, err
    assert not [call for call in client.calls if call[0] in WRITES]
    assert "rename type:docs -> documentation" in out
    assert "merge type:feature into enhancement" in out
    assert "rename ready-for-human-review -> ready-for-review" in out
    assert "create good first issue" in out
    assert "area:api" not in out
    assert "size:M" not in out
    assert "--apply" in out


def test_an_update_line_says_what_changes() -> None:
    client = FakeClient({"r": [_label("bug", "D73A4A", "Broken")]})
    code, out, _ = _run([], client)
    assert code == 0
    assert "update bug: description 'Broken' -> \"Something isn't working\"" in out
    assert "color" not in out.split("update bug")[1].splitlines()[0]


def test_repo_limits_the_run() -> None:
    client = _backend()
    code, out, _ = _run(["--repo", "evaluation"], client)
    assert code == 0
    assert "openpickleball/evaluation" in out
    assert "backend" not in out
    assert ("list_labels", "backend") not in client.calls


def test_an_unknown_repo_fails_clearly() -> None:
    client = _backend()
    code, _, err = _run(["--repo", "does-not-exist"], client)
    assert code == 1
    assert "does-not-exist" in err
    assert "not a non-archived repository" in err
    assert not [call for call in client.calls if call[0] == "list_labels"]


def test_an_invalid_label_file_fails_clearly() -> None:
    client = _backend()
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "labels.toml"
        path.write_text(GOOD_LABEL + GOOD_LABEL, encoding="utf-8")
        code, _, err = _run(["--labels", str(path)], client)
    assert code == 1
    assert "more than once" in err
    assert client.calls == []


# GhClient, against a fake gh


class FakeGh:
    def __init__(self, stdout: str = "", returncode: int = 0, stderr: str = "") -> None:
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = stderr
        self.calls: list[tuple[list[str], str | None]] = []

    def __call__(self, args: list[str], stdin: str | None) -> sync.GhResult:
        self.calls.append((args, stdin))
        return sync.GhResult(self.returncode, self.stdout, self.stderr)


def test_label_names_are_encoded_in_paths() -> None:
    gh = FakeGh()
    client = sync.GhClient("openpickleball", run=gh)
    client.update_label("r", "good first issue", "priority:p0", "b60205", "First")
    client.delete_label("r", "type:docs")
    client.issues_with_label("r", "good first issue")
    paths = [next(a for a in args if a.startswith("repos/")) for args, _ in gh.calls]
    assert paths == [
        "repos/openpickleball/r/labels/good%20first%20issue",
        "repos/openpickleball/r/labels/type%3Adocs",
        "repos/openpickleball/r/issues?labels=good%20first%20issue&state=all&per_page=100",
    ]
    body = json.loads(gh.calls[0][1] or "")
    assert body == {
        "new_name": "priority:p0",
        "color": "b60205",
        "description": "First",
    }
    assert "--paginate" in gh.calls[2][0]


def test_reads_join_every_page() -> None:
    pages = (
        '[{"number": 1, "labels": [{"name": "bug"}]},'
        ' {"number": 2, "labels": [{"name": "bug"}, {"name": "triage"}]}]\n'
        '[{"number": 3, "labels": []}]'
    )
    client = sync.GhClient("openpickleball", run=FakeGh(pages))
    assert client.issues_with_label("r", "bug") == [
        sync.Issue(1, ("bug",)),
        sync.Issue(2, ("bug", "triage")),
        sync.Issue(3, ()),
    ]
    labels = '[{"name": "bug", "color": "d73a4a", "description": null}][]'
    client = sync.GhClient("openpickleball", run=FakeGh(labels))
    assert client.list_labels("r") == [sync.Label("bug", "d73a4a", "")]
    repos = (
        '[{"name": "b", "archived": false, "has_discussions": true},'
        ' {"name": "old", "archived": true, "has_discussions": false}]'
        '[{"name": "a", "archived": false, "has_discussions": false}]'
    )
    client = sync.GhClient("openpickleball", run=FakeGh(repos))
    assert client.list_repos() == [sync.Repo("a", False), sync.Repo("b", True)]


def test_writes_send_json_bodies() -> None:
    gh = FakeGh()
    client = sync.GhClient("openpickleball", run=gh)
    client.create_label("r", "good first issue", "7057ff", "Good for newcomers")
    client.add_label("r", 7, "priority:p0")
    (create, create_body), (add, add_body) = gh.calls
    assert create[create.index("--method") + 1] == "POST"
    assert json.loads(create_body or "") == {
        "name": "good first issue",
        "color": "7057ff",
        "description": "Good for newcomers",
    }
    assert "repos/openpickleball/r/issues/7/labels" in add
    assert json.loads(add_body or "") == {"labels": ["priority:p0"]}


def test_a_failed_gh_call_raises_with_its_message() -> None:
    gh = FakeGh(returncode=1, stderr="gh: Not Found (HTTP 404)\n")
    client = sync.GhClient("openpickleball", run=gh)
    try:
        client.list_labels("does-not-exist")
    except sync.GhError as error:
        assert "HTTP 404" in str(error)
        assert "does-not-exist" in str(error)
    else:
        raise AssertionError("no error for a failed call")


def test_writes_are_paced_and_reads_are_not() -> None:
    gh = FakeGh('[{"name": "bug", "color": "d73a4a", "description": ""}]')
    sleeps: list[float] = []
    client = sync.GhClient("openpickleball", run=gh, sleep=sleeps.append)
    client.list_labels("r")
    client.create_label("r", "bug", "d73a4a", "")
    client.list_labels("r")
    client.add_label("r", 1, "bug")
    client.delete_label("r", "old")
    assert sleeps == [sync.WRITE_PAUSE, sync.WRITE_PAUSE]
    assert sync.WRITE_PAUSE >= 1.0


def test_a_rate_limit_response_raises_rate_limit_error() -> None:
    for stderr in [
        "gh: You have exceeded a secondary rate limit. (HTTP 403)",
        "gh: API rate limit exceeded for user. (HTTP 403)",
        "gh: Too Many Requests (HTTP 429)",
    ]:
        client = sync.GhClient(
            "openpickleball", run=FakeGh(returncode=1, stderr=stderr)
        )
        try:
            client.add_label("r", 1, "bug")
        except sync.RateLimitError:
            continue
        raise AssertionError(f"no RateLimitError for {stderr!r}")
    client = sync.GhClient(
        "openpickleball",
        run=FakeGh(returncode=1, stderr="gh: Must have admin rights (HTTP 403)"),
    )
    try:
        client.add_label("r", 1, "bug")
    except sync.RateLimitError as error:
        raise AssertionError("a permission error is not a rate limit") from error
    except sync.GhError:
        pass


def test_the_script_is_executable_python() -> None:
    assert SCRIPT.read_text(encoding="utf-8").startswith("#!/usr/bin/env python3\n")


def test_the_workflow_runs_these_tests() -> None:
    workflow = (ROOT / ".github" / "workflows" / "scripts.yml").read_text(
        encoding="utf-8"
    )
    assert "python3 -I scripts/test_sync_labels.py" in workflow


SEARCH = (
    "https://github.com/search?q=org%3Aopenpickleball+label%3A%22good+first+issue%22"
    "+is%3Aopen+is%3Aissue&type=issues"
)


def test_the_first_issue_links_work_signed_out() -> None:
    # github.com/issues needs a login; github.com/search does not.
    for page in ("CONTRIBUTING.md", "profile/README.md"):
        text = (ROOT / page).read_text(encoding="utf-8")
        assert SEARCH in text, page
        assert "github.com/issues?" not in text, page


def test_the_docs_say_how_renames_and_removals_work() -> None:
    guide = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    section = guide.split("## Labels", 1)[1].split("\n## ", 1)[0]
    header = LABELS.read_text(encoding="utf-8").split("[[label]]", 1)[0]
    for text in (section, header):
        assert "aliases" in text
        assert "old name" in text
        assert "Removing a label" in text


def test_the_workflow_header_names_the_label_sync() -> None:
    header = (ROOT / ".github" / "workflows" / "scripts.yml").read_text(
        encoding="utf-8"
    )
    assert "label sync" in header.split("name:", 1)[0]


# Errors between actions (review findings F1 to F3)


class FailingReadClient(FakeClient):
    """Reading one repository's labels fails, as a 502 or a rate limit."""

    def __init__(
        self,
        base: FakeClient,
        fail_repo: str,
        error: type[sync.GhError] = sync.GhError,
    ) -> None:
        super().__init__(base.labels, base.issues, discussions=base.discussions)
        self.fail_repo = fail_repo
        self.read_error = error

    def list_labels(self, repo: str) -> list[sync.Label]:
        if repo == self.fail_repo:
            self.calls.append(("list_labels", repo))
            raise self.read_error(f"gh api GET repos/openpickleball/{repo}: HTTP 502")
        return super().list_labels(repo)


class FailingReposClient(FakeClient):
    def list_repos(self) -> list[sync.Repo]:
        raise sync.GhError("gh api GET orgs/openpickleball/repos: HTTP 502")


def test_a_failed_read_after_actions_does_not_call_them_unfinished() -> None:
    client = FailingReadClient(_backend(), "evaluation")
    code, out, err = _run(["--apply"], client)
    assert code == 1
    # Every backend action ran before evaluation's labels were read.
    assert "follow-up" in {label.name for label in client.labels["backend"]}
    assert out.strip().splitlines()[-1].strip().startswith("create")
    assert "did not finish" not in err
    assert "while reading" in err
    assert "not refused is done" in err


def test_a_failed_repository_listing_is_reported_as_a_read() -> None:
    code, _, err = _run(["--apply"], FailingReposClient({"backend": []}))
    assert code == 1
    assert "did not finish" not in err
    assert "while reading" in err


def test_a_rate_limited_dry_run_says_to_rerun_the_dry_run() -> None:
    client = FailingReadClient(_backend(), "evaluation", sync.RateLimitError)
    code, _, err = _run([], client)
    assert code == 1
    assert "rate limited" in err
    assert "resumes" not in err
    assert "dry run again" in err
    assert "did not finish" not in err


def test_a_failure_after_a_refused_merge_still_names_it() -> None:
    base = _backend()
    base.discussions = frozenset({"backend"})
    client = FailingReadClient(base, "evaluation")
    code, _, err = _run(["--apply"], client)
    assert code == 1
    assert "refused these merges" in err
    assert "merge type:feature into enhancement" in err
    assert "by hand" in err


def test_a_missing_discussions_field_counts_as_discussions_on() -> None:
    # Failing safe: a merge there would strip labels from discussions.
    repos = (
        '[{"name": "a", "archived": false},'
        ' {"name": "b", "archived": false, "has_discussions": null},'
        ' {"name": "c", "archived": false, "has_discussions": "false"},'
        ' {"name": "d", "archived": false, "has_discussions": false},'
        ' {"name": "e", "archived": false, "has_discussions": true}]'
    )
    client = sync.GhClient("openpickleball", run=FakeGh(repos))
    assert client.list_repos() == [
        sync.Repo("a", True),
        sync.Repo("b", True),
        sync.Repo("c", True),
        sync.Repo("d", False),
        sync.Repo("e", True),
    ]


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
