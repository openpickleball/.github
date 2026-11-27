#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Sync the shared labels in labels.toml to every OPEN repository.

An organization owner runs this locally with their own `gh` login, so no
organization token is stored anywhere. It uses the standard library and
the `gh` CLI only.

    python3 scripts/sync_labels.py                 # dry run, every repository
    python3 scripts/sync_labels.py --repo backend  # dry run, one repository
    python3 scripts/sync_labels.py --apply         # make the changes

The dry run prints every action it would take and changes nothing. For
each shared label it creates the label, fixes its color or description,
or renames an old name (an alias) to it, which keeps the label's issues.
When a repository has both a shared label and one of its aliases, it adds
the shared label to every issue and pull request that has the alias, then
deletes the alias. Labels that are not in labels.toml are never touched.

It waits a second between changes, as GitHub asks, and a rerun picks up
where a stopped run left off. It refuses to merge in a repository with
discussions, since the API it uses cannot see their labels.
"""

import argparse
import json
import subprocess
import sys
import time
import tomllib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from urllib.parse import quote

ORG = "openpickleball"
LABELS = Path(__file__).resolve().parent.parent / "labels.toml"
# GitHub asks for at least a second between requests that change content.
WRITE_PAUSE = 1.0
# How many times a merge lists the alias's issues before giving up.
MERGE_PASSES = 5
NAME_MAX = 50
DESCRIPTION_MAX = 100
HEX_COLOR = frozenset("0123456789abcdefABCDEF")
KEYS = frozenset({"name", "color", "description", "aliases"})


class LabelFileError(ValueError):
    """The label file is missing or breaks a rule."""


@dataclass(frozen=True)
class SharedLabel:
    name: str
    color: str
    description: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class Label:
    """A label as a repository has it now."""

    name: str
    color: str
    description: str


@dataclass(frozen=True)
class Create:
    label: SharedLabel


@dataclass(frozen=True)
class Update:
    """Fix the name's case, the color, or the description of a shared label."""

    current: Label
    label: SharedLabel


@dataclass(frozen=True)
class Rename:
    """Rename an alias to the shared label, keeping its issues."""

    current: Label
    label: SharedLabel


@dataclass(frozen=True)
class Merge:
    """Add the target to every issue that has the alias, then delete the alias."""

    alias: str
    target: str


type Action = Create | Update | Rename | Merge


def _name_problem(name: str) -> str | None:
    """Why GitHub, or this script, cannot use this label name, if it cannot."""
    if name != name.strip():
        return f"{name!r} has spaces at the start or end"
    if "," in name:
        # The issues API reads labels=a,b as "has a and b".
        return f"{name!r} contains a comma"
    if name in {".", ".."}:
        return f"{name!r} would be a path segment: a name cannot be '.' or '..'"
    if len(name) > NAME_MAX:
        return (
            f"{name!r} is {len(name)} characters; GitHub allows {NAME_MAX} characters"
        )
    if not name.isascii():
        # GitHub's case-insensitive matching of other characters differs
        # from Python's, so only ASCII names match reliably.
        return f"{name!r} must be ASCII"
    return None


def _label_from_table(index: int, table: object) -> SharedLabel:
    where = f"label {index}"
    if not isinstance(table, dict):
        raise LabelFileError(f"{where}: is not a [[label]] table")
    name = table.get("name")
    if not isinstance(name, str) or not name:
        raise LabelFileError(f"{where}: needs a name")
    where = f"label {index} ({name.strip()})"
    problem = _name_problem(name)
    if problem:
        raise LabelFileError(f"{where}: {problem}")
    unknown = sorted(set(table) - KEYS)
    if unknown:
        raise LabelFileError(f"{where}: unknown key {', '.join(unknown)}")
    color = table.get("color")
    if not isinstance(color, str) or len(color) != 6 or not set(color) <= HEX_COLOR:
        raise LabelFileError(f"{where}: color must be six hex digits, without #")
    description = table.get("description")
    if not isinstance(description, str):
        raise LabelFileError(f"{where}: needs a description")
    if description != description.strip():
        raise LabelFileError(f"{where}: description has spaces at the start or end")
    if len(description) > DESCRIPTION_MAX:
        raise LabelFileError(
            f"{where}: description is {len(description)} characters; "
            f"GitHub allows {DESCRIPTION_MAX} characters"
        )
    if "aliases" not in table:
        raise LabelFileError(f"{where}: needs aliases (aliases = [] for none)")
    aliases = table["aliases"]
    if not isinstance(aliases, list) or not all(
        isinstance(alias, str) and alias for alias in aliases
    ):
        raise LabelFileError(f"{where}: aliases must be a list of label names")
    for alias in aliases:
        problem = _name_problem(alias)
        if problem:
            raise LabelFileError(f"{where}: alias {problem}")
    return SharedLabel(name, color, description, tuple(aliases))


def load_labels(path: Path) -> list[SharedLabel]:
    """Read and check the shared labels, raising LabelFileError on any problem."""
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise LabelFileError(f"{path}: cannot read: {error.strerror}") from error
    except tomllib.TOMLDecodeError as error:
        raise LabelFileError(f"{path}: not valid TOML: {error}") from error
    tables = data.get("label")
    if not isinstance(tables, list) or not tables:
        raise LabelFileError(f"{path}: has no [[label]] tables")
    labels = [_label_from_table(i, table) for i, table in enumerate(tables, 1)]
    # GitHub label names are case-insensitive, so "Bug" and "bug" collide.
    seen: dict[str, str] = {}
    for label in labels:
        for name in (label.name, *label.aliases):
            key = _key(name)
            if key in seen:
                raise LabelFileError(
                    f"{path}: {name!r} is used more than once "
                    f"(by labels {seen[key]!r} and {label.name!r})"
                )
            seen[key] = label.name
    return labels


def _key(name: str) -> str:
    """The name GitHub compares: ASCII letters ignore case.

    Shared names are ASCII, so a name with other characters never matches
    one; casefold() would match "stra\u00dfe" to "strasse".
    """
    return name.lower() if name.isascii() else name


def _differs(current: Label, label: SharedLabel) -> bool:
    return (
        current.name != label.name
        or current.color.lower() != label.color.lower()
        or current.description != label.description
    )


def plan_repo(shared: list[SharedLabel], existing: list[Label]) -> list[Action]:
    """Return what to change so a repository has the shared labels.

    Names match case-insensitively, as on GitHub. A label whose name is not
    a shared name or alias never appears in an action.
    """
    by_name = {_key(label.name): label for label in existing}
    actions: list[Action] = []
    for label in shared:
        present = [
            by_name[_key(alias)] for alias in label.aliases if _key(alias) in by_name
        ]
        target = by_name.get(_key(label.name))
        if target is not None:
            if _differs(target, label):
                actions.append(Update(target, label))
        elif present:
            actions.append(Rename(present.pop(0), label))
        else:
            actions.append(Create(label))
        actions += [Merge(alias.name, label.name) for alias in present]
    return actions


class GhError(Exception):
    """A GitHub call failed."""


class RateLimitError(GhError):
    """GitHub refused a call because of a rate limit."""


@dataclass(frozen=True)
class Repo:
    name: str
    # Discussions carry repository labels, but the issues API does not
    # return them, so a merge here would strip the alias from them.
    has_discussions: bool


@dataclass(frozen=True)
class Issue:
    """An issue or pull request and the names of its labels."""

    number: int
    labels: tuple[str, ...]


class Client(Protocol):
    def list_repos(self) -> list[Repo]: ...

    def list_labels(self, repo: str) -> list[Label]: ...

    def create_label(
        self, repo: str, name: str, color: str, description: str
    ) -> None: ...

    def update_label(
        self, repo: str, current: str, name: str, color: str, description: str
    ) -> None: ...

    def issues_with_label(self, repo: str, name: str) -> list[Issue]: ...

    def add_label(self, repo: str, number: int, name: str) -> None: ...

    def delete_label(self, repo: str, name: str) -> None: ...


@dataclass(frozen=True)
class GhResult:
    returncode: int
    stdout: str
    stderr: str


type GhRunner = Callable[[list[str], str | None], GhResult]


def run_gh(args: list[str], stdin: str | None) -> GhResult:
    """Run `gh` with these arguments, sending stdin when it is given."""
    try:
        done = subprocess.run(
            ["gh", *args],
            input=stdin,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        raise GhError("gh is not installed: https://cli.github.com") from error
    return GhResult(done.returncode, done.stdout, done.stderr)


def _pages(text: str) -> list[dict[str, object]]:
    """Join the JSON arrays that `gh api --paginate` prints, one per page."""
    decoder = json.JSONDecoder()
    items: list[dict[str, object]] = []
    position = 0
    text = text.strip()
    while position < len(text):
        page, position = decoder.raw_decode(text, position)
        while position < len(text) and text[position].isspace():
            position += 1
        items += page
    return items


class GhClient:
    """The GitHub REST API through `gh api`, as the logged-in user."""

    def __init__(
        self,
        org: str,
        run: GhRunner = run_gh,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.org = org
        self.run = run
        self.sleep = sleep
        self.wrote = False

    def _repo(self, repo: str) -> str:
        return f"repos/{quote(self.org, safe='')}/{quote(repo, safe='')}"

    def _call(
        self, method: str, path: str, body: dict[str, object] | None = None
    ) -> str:
        args = ["api", "--method", method, path]
        if method == "GET":
            args.insert(1, "--paginate")
        else:
            if self.wrote:
                self.sleep(WRITE_PAUSE)
            self.wrote = True
        stdin = None
        if body is not None:
            args += ["--input", "-"]
            stdin = json.dumps(body)
        result = self.run(args, stdin)
        if result.returncode != 0:
            message = f"gh api {method} {path} failed: {result.stderr.strip()}"
            lowered = result.stderr.lower()
            if "rate limit" in lowered or "http 429" in lowered:
                raise RateLimitError(message)
            raise GhError(message)
        return result.stdout

    def list_repos(self) -> list[Repo]:
        items = _pages(
            self._call("GET", f"orgs/{self.org}/repos?type=all&per_page=100")
        )
        repos = [
            # Fail safe: only an explicit false allows merges.
            Repo(str(item["name"]), item.get("has_discussions") is not False)
            for item in items
            if not item["archived"]
        ]
        return sorted(repos, key=lambda repo: repo.name)

    def list_labels(self, repo: str) -> list[Label]:
        items = _pages(self._call("GET", f"{self._repo(repo)}/labels?per_page=100"))
        return [
            Label(str(item["name"]), str(item["color"]), str(item["description"] or ""))
            for item in items
        ]

    def create_label(self, repo: str, name: str, color: str, description: str) -> None:
        body: dict[str, object] = {
            "name": name,
            "color": color,
            "description": description,
        }
        self._call("POST", f"{self._repo(repo)}/labels", body)

    def update_label(
        self, repo: str, current: str, name: str, color: str, description: str
    ) -> None:
        body: dict[str, object] = {
            "new_name": name,
            "color": color,
            "description": description,
        }
        path = f"{self._repo(repo)}/labels/{quote(current, safe='')}"
        self._call("PATCH", path, body)

    def issues_with_label(self, repo: str, name: str) -> list[Issue]:
        # The issues endpoint returns pull requests too.
        path = (
            f"{self._repo(repo)}/issues?labels={quote(name, safe='')}"
            "&state=all&per_page=100"
        )
        issues = []
        for item in _pages(self._call("GET", path)):
            labels = item.get("labels")
            names = tuple(
                str(label["name"])
                for label in (labels if isinstance(labels, list) else [])
                if isinstance(label, dict)
            )
            issues.append(Issue(int(str(item["number"])), names))
        return issues

    def add_label(self, repo: str, number: int, name: str) -> None:
        body: dict[str, object] = {"labels": [name]}
        self._call("POST", f"{self._repo(repo)}/issues/{number}/labels", body)

    def delete_label(self, repo: str, name: str) -> None:
        self._call("DELETE", f"{self._repo(repo)}/labels/{quote(name, safe='')}")


def apply_actions(client: Client, repo: str, actions: list[Action]) -> None:
    """Make the changes in order. A failed call raises GhError and stops."""
    for action in actions:
        match action:
            case Create(label):
                client.create_label(repo, label.name, label.color, label.description)
            case Update(current, label) | Rename(current, label):
                client.update_label(
                    repo, current.name, label.name, label.color, label.description
                )
            case Merge(alias, target):
                _merge(client, repo, alias, target)


def _merge(client: Client, repo: str, alias: str, target: str) -> None:
    """Add the target wherever the alias is, then delete the alias.

    The alias is deleted only once a fresh listing shows every issue with
    it also has the target, so a failure, or an issue labeled during the
    run, loses no labels. Issues that already have the target are skipped,
    so a rerun after a failure resumes where it stopped.
    """
    for _ in range(MERGE_PASSES):
        missing = [
            issue.number
            for issue in client.issues_with_label(repo, alias)
            if _key(target) not in {_key(name) for name in issue.labels}
        ]
        if not missing:
            client.delete_label(repo, alias)
            return
        for number in missing:
            client.add_label(repo, number, target)
    raise GhError(
        f"{repo}: issues kept getting {alias} without {target} during the "
        f"merge, after {MERGE_PASSES} passes. {alias} is kept; run again."
    )


def refusal(repo: Repo, action: Action) -> str | None:
    """Why this action must not run in this repository, if it must not."""
    if isinstance(action, Merge) and repo.has_discussions:
        return (
            "this repository has discussions, which can carry "
            f"{action.alias} but which the sync cannot relabel"
        )
    return None


def describe(action: Action) -> str:
    """One readable line for an action."""
    match action:
        case Create(label):
            return f"create {label.name}"
        case Update(current, label):
            changes = []
            if current.name != label.name:
                changes.append(f"name {current.name} -> {label.name}")
            if current.color.lower() != label.color.lower():
                changes.append(f"color {current.color} -> {label.color}")
            if current.description != label.description:
                changes.append(
                    f"description {current.description!r} -> {label.description!r}"
                )
            return f"update {label.name}: {'; '.join(changes)}"
        case Rename(current, label):
            return f"rename {current.name} -> {label.name}"
        case Merge(alias, target):
            return (
                f"merge {alias} into {target} (add {target} to every issue and "
                f"pull request with {alias}, then delete {alias})"
            )


def _report_refused(refused: list[str], finished: bool) -> None:
    print(
        "sync_labels: refused these merges, because the sync cannot "
        "relabel discussions:\n  " + "\n  ".join(refused) + "\nMove each "
        "alias to its target on the repository's issues and discussions by "
        "hand, then delete the alias."
        + (" The other actions ran." if finished else ""),
        file=sys.stderr,
    )


def _count(count: int, one: str, many: str) -> str:
    return f"{count} {one if count == 1 else many}"


def main(argv: list[str] | None = None, client: Client | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--apply", action="store_true", help="make the changes (default: dry run)"
    )
    parser.add_argument(
        "--repo",
        action="append",
        metavar="NAME",
        help=f"sync only this repository in {ORG} (repeatable)",
    )
    parser.add_argument(
        "--labels",
        type=Path,
        default=LABELS,
        metavar="PATH",
        help="the label file (default: labels.toml)",
    )
    args = parser.parse_args(argv)

    try:
        shared = load_labels(args.labels)
    except ValueError as error:
        print(f"sync_labels: {error}", file=sys.stderr)
        return 1
    if client is None:
        client = GhClient(ORG)

    refused: list[str] = []
    # True only while an action is running, so an error from a read between
    # actions is not reported as an unfinished action.
    in_action = False
    try:
        repos = client.list_repos()
        if not repos:
            print(
                f"sync_labels: gh lists no repositories in {ORG}. Check "
                "`gh auth status` and that this login can see the organization.",
                file=sys.stderr,
            )
            return 1
        if args.repo:
            known = {repo.name: repo for repo in repos}
            unknown = [name for name in args.repo if name not in known]
            if unknown:
                print(
                    f"sync_labels: {', '.join(unknown)}: not a non-archived "
                    f"repository in {ORG}. Repositories: {', '.join(known)}",
                    file=sys.stderr,
                )
                return 1
            repos = [known[name] for name in dict.fromkeys(args.repo)]
        total = 0
        for repo in repos:
            actions = plan_repo(shared, client.list_labels(repo.name))
            total += len(actions)
            print(f"{ORG}/{repo.name}")
            if not actions:
                print("  nothing to change")
            for action in actions:
                reason = refusal(repo, action)
                if reason:
                    print(f"  refused: {describe(action)}: {reason}")
                    refused.append(f"{ORG}/{repo.name}: {describe(action)}")
                    continue
                print(f"  {describe(action)}", flush=True)
                if args.apply:
                    in_action = True
                    apply_actions(client, repo.name, [action])
                    in_action = False
    except GhError as error:
        print(f"sync_labels: {error}", file=sys.stderr)
        if isinstance(error, RateLimitError):
            again = (
                "run again: it resumes where it stopped"
                if args.apply
                else "run the dry run again"
            )
            print(
                "sync_labels: GitHub rate limited this run. Wait a few minutes "
                f"and {again}.",
                file=sys.stderr,
            )
        if args.apply and in_action:
            print(
                "sync_labels: stopped. The last action listed above did not "
                "finish (a merge may have added some labels already); the "
                "actions before it are done. Run again to finish: the next "
                "run plans only what is left.",
                file=sys.stderr,
            )
        elif args.apply:
            print(
                "sync_labels: stopped while reading from GitHub, between "
                "actions. Every listed action that was not refused is done. "
                "Run again to finish: the next run plans only what is left.",
                file=sys.stderr,
            )
        if refused and args.apply:
            _report_refused(refused, finished=False)
        return 1

    done = _count(total, "action", "actions")
    where = _count(len(repos), "repository", "repositories")
    note = f" ({len(refused)} refused)" if refused else ""
    if args.apply:
        print(
            f"{_count(total - len(refused), 'action', 'actions')} applied in {where}{note}."
        )
    else:
        print(
            f"{done} planned in {where}{note}. This was a dry run and changed "
            "nothing. Run again with --apply to make these changes."
        )
    if refused and args.apply:
        _report_refused(refused, finished=True)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
