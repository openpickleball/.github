#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Report last month's pull request response times and new contributors.

CONTRIBUTING.md promises a first response to every pull request within 3
business days. This script checks that promise for pull requests opened in
one month, in every OPEN repository, by anyone outside the `maintainers`
team and the organization owners. It also counts the month's first-time and
repeat contributors.

An organization owner runs it locally with their own `gh` login, for the
monthly membership review:

    gh auth refresh -h github.com -s read:org
    python3 scripts/response_report.py            # last month
    python3 scripts/response_report.py 2026-11    # a given month

The summary names no organization member, only public pull requests and
counts, so it can go in the monthly reminder issue. The contributor logins
printed after it are for updating CONTRIBUTORS.md.

Definitions:
- A first response is the earliest review, comment, or review comment by
  anyone other than the author who isn't a bot.
- Business days are Monday to Friday, in UTC, with no holidays. A pull
  request opened on a weekend starts its clock on Monday at 00:00 UTC.
- A pull request with no response yet is "pending" until its deadline
  passes, and "missed" after.
- A contributor is the author of a pull request merged in the month, other
  than a bot, a maintainer, or an owner. A first-time contributor has no
  earlier merged pull request in any OPEN repository.

It uses the standard library and the `gh` CLI only, and it changes nothing.
"""

import argparse
import json
import subprocess
import sys
import time
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime, timedelta
from typing import Literal, Protocol
from urllib.parse import quote

ORG = "openpickleball"
TARGET_BUSINESS_DAYS = 3
# The search API allows 30 requests a minute.
SEARCH_PAUSE = 2.5
# A run makes several calls per pull request, so a dropped connection is
# retried rather than ending the run.
GET_ATTEMPTS = 3
RETRY_PAUSE = 5.0

type Outcome = Literal["met", "missed", "pending"]


class GhError(Exception):
    """A `gh` call failed."""


@dataclass(frozen=True)
class Response:
    login: str
    is_bot: bool
    at: datetime


@dataclass(frozen=True)
class PullRequest:
    repo: str
    number: int
    url: str
    author: str
    author_is_bot: bool
    created_at: datetime
    responses: tuple[Response, ...] = ()


@dataclass(frozen=True)
class Result:
    pull_request: PullRequest
    outcome: Outcome
    first_response: datetime | None


@dataclass
class Report:
    month: str
    results: list[Result] = field(default_factory=list)
    first_time: list[str] = field(default_factory=list)
    repeat: list[str] = field(default_factory=list)


def is_bot(login: str, account_type: str | None = None) -> bool:
    return account_type == "Bot" or login.endswith("[bot]")


def add_business_days(start: datetime, days: int) -> datetime:
    """The moment `days` business days after `start`, skipping weekends.

    A start on a weekend moves to the next Monday at 00:00 UTC first.
    """
    start = start.astimezone(UTC)
    if start.weekday() >= 5:
        monday = start.date() + timedelta(days=7 - start.weekday())
        start = datetime(monday.year, monday.month, monday.day, tzinfo=UTC)
    moment = start
    left = days
    while left > 0:
        moment += timedelta(days=1)
        if moment.weekday() < 5:
            left -= 1
    return moment


def first_response(pull_request: PullRequest) -> datetime | None:
    times = [
        response.at
        for response in pull_request.responses
        if response.login != pull_request.author and not response.is_bot
    ]
    return min(times, default=None)


def classify(pull_request: PullRequest, now: datetime) -> Result:
    deadline = add_business_days(pull_request.created_at, TARGET_BUSINESS_DAYS)
    first = first_response(pull_request)
    if first is not None:
        outcome: Outcome = "met" if first <= deadline else "missed"
    else:
        outcome = "missed" if now > deadline else "pending"
    return Result(pull_request, outcome, first)


def counts_toward_target(pull_request: PullRequest, insiders: set[str]) -> bool:
    return not pull_request.author_is_bot and pull_request.author not in insiders


def month_bounds(month: str) -> tuple[date, date]:
    """The first and last day of a YYYY-MM month."""
    try:
        first = datetime.strptime(month, "%Y-%m").date()
    except ValueError as error:
        raise ValueError(f"{month!r} is not a month in the form YYYY-MM") from error
    following = (first.replace(day=28) + timedelta(days=4)).replace(day=1)
    return first, following - timedelta(days=1)


def previous_month(today: date) -> str:
    return (today.replace(day=1) - timedelta(days=1)).strftime("%Y-%m")


def build_report(
    month: str,
    pull_requests: Iterable[PullRequest],
    merged_authors: Iterable[str],
    insiders: set[str],
    merged_before: Callable[[str], bool],
    now: datetime,
) -> Report:
    report = Report(month)
    for pull_request in pull_requests:
        if counts_toward_target(pull_request, insiders):
            report.results.append(classify(pull_request, now))
    report.results.sort(
        key=lambda result: (result.pull_request.repo, result.pull_request.number)
    )
    for login in sorted(set(merged_authors), key=str.lower):
        if is_bot(login) or login in insiders:
            continue
        (report.repeat if merged_before(login) else report.first_time).append(login)
    return report


def _hours(result: Result) -> float | None:
    if result.first_response is None:
        return None
    elapsed = result.first_response - result.pull_request.created_at
    return elapsed.total_seconds() / 3600


def format_report(report: Report) -> str:
    results = report.results
    met = [result for result in results if result.outcome == "met"]
    missed = [result for result in results if result.outcome == "missed"]
    pending = [result for result in results if result.outcome == "pending"]
    decided = len(met) + len(missed)
    lines = [
        (
            f"**Pull request responses, {report.month}** "
            f"(target: first response within {TARGET_BUSINESS_DAYS} business days)"
        ),
        "",
    ]
    if not results:
        lines.append(
            "- No pull requests from outside the maintainers team were opened."
        )
    else:
        share = f" ({round(100 * len(met) / decided)}%)" if decided else ""
        lines.append(
            f"- {len(results)} pull request(s) from outside the maintainers team. "
            f"Met: {len(met)} of {decided}{share}. Missed: {len(missed)}. "
            f"Still pending: {len(pending)}."
        )
        hours = sorted(h for result in results if (h := _hours(result)) is not None)
        if hours:
            middle = len(hours) // 2
            median = (
                hours[middle]
                if len(hours) % 2
                else (hours[middle - 1] + hours[middle]) / 2
            )
            lines.append(f"- Median time to first response: {median:.1f} hours.")
        for result in missed:
            lines.append(f"- Missed: {result.pull_request.url}")
        for result in pending:
            lines.append(f"- Pending: {result.pull_request.url}")
    lines += [
        "",
        f"**Contributors, {report.month}** (merged pull requests)",
        "",
        f"- First-time: {len(report.first_time)}. Repeat: {len(report.repeat)}.",
    ]
    return "\n".join(lines)


def format_logins(report: Report) -> str:
    def joined(logins: list[str]) -> str:
        return ", ".join(logins) if logins else "none"

    return "\n".join(
        [
            "For CONTRIBUTORS.md:",
            f"  First-time: {joined(report.first_time)}",
            f"  Repeat: {joined(report.repeat)}",
        ]
    )


class Client(Protocol):
    def insiders(self) -> set[str]: ...

    def pull_requests_opened(self, first: date, last: date) -> list[PullRequest]: ...

    def responses(self, repo: str, number: int) -> list[Response]: ...

    def authors_merged(self, first: date, last: date) -> list[str]: ...

    def merged_before(self, login: str, first: date) -> bool: ...


@dataclass(frozen=True)
class GhResult:
    returncode: int
    stdout: str
    stderr: str


type GhRunner = Callable[[list[str]], GhResult]


def run_gh(args: list[str]) -> GhResult:
    try:
        done = subprocess.run(
            ["gh", *args], capture_output=True, text=True, check=False
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


def _time(value: object) -> datetime:
    return datetime.fromisoformat(str(value))


def _user(item: dict[str, object]) -> tuple[str, bool]:
    user = item.get("user")
    if not isinstance(user, dict):
        # A deleted account.
        return "ghost", False
    login = str(user.get("login", "ghost"))
    return login, is_bot(login, user.get("type"))


class GhClient:
    """The GitHub REST API through `gh api`, as the logged-in user."""

    def __init__(
        self,
        org: str = ORG,
        run: GhRunner = run_gh,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.org = org
        self.run = run
        self.sleep = sleep

    def _get(self, path: str, jq: str | None = None) -> list[dict[str, object]]:
        args = ["api", "--paginate", "--method", "GET", path]
        if jq:
            args += ["--jq", jq]
        for attempt in range(1, GET_ATTEMPTS + 1):
            result = self.run(args)
            if result.returncode == 0:
                return _pages(result.stdout)
            # Retry a dropped connection or a server error, not a 4xx answer.
            if "HTTP 4" in result.stderr or attempt == GET_ATTEMPTS:
                break
            self.sleep(RETRY_PAUSE * attempt)
        raise GhError(f"gh api GET {path} failed: {result.stderr.strip()}")

    def _search(self, query: str) -> list[dict[str, object]]:
        self.sleep(SEARCH_PAUSE)
        return self._get(
            f"search/issues?per_page=100&q={quote(query, safe='')}", jq=".items"
        )

    def insiders(self) -> set[str]:
        maintainers = self._get(f"orgs/{self.org}/teams/maintainers/members")
        owners = self._get(f"orgs/{self.org}/members?role=admin")
        return {str(member["login"]) for member in maintainers + owners}

    def pull_requests_opened(self, first: date, last: date) -> list[PullRequest]:
        found = self._search(f"org:{self.org} type:pr created:{first}..{last}")
        pull_requests = []
        for item in found:
            repo = str(item["repository_url"]).rsplit("/", 1)[1]
            number = int(str(item["number"]))
            author, author_is_bot = _user(item)
            pull_requests.append(
                PullRequest(
                    repo=repo,
                    number=number,
                    url=str(item["html_url"]),
                    author=author,
                    author_is_bot=author_is_bot,
                    created_at=_time(item["created_at"]),
                )
            )
        return pull_requests

    def responses(self, repo: str, number: int) -> list[Response]:
        base = f"repos/{self.org}/{repo}"
        responses = []
        for review in self._get(f"{base}/pulls/{number}/reviews?per_page=100"):
            # A pending review has no submitted_at and isn't visible yet.
            if review.get("submitted_at"):
                login, bot = _user(review)
                responses.append(Response(login, bot, _time(review["submitted_at"])))
        for path in (
            f"{base}/issues/{number}/comments?per_page=100",
            f"{base}/pulls/{number}/comments?per_page=100",
        ):
            for comment in self._get(path):
                login, bot = _user(comment)
                responses.append(Response(login, bot, _time(comment["created_at"])))
        return responses

    def authors_merged(self, first: date, last: date) -> list[str]:
        found = self._search(f"org:{self.org} type:pr is:merged merged:{first}..{last}")
        return [_user(item)[0] for item in found]

    def merged_before(self, login: str, first: date) -> bool:
        found = self._search(
            f"org:{self.org} type:pr is:merged author:{login} merged:<{first}"
        )
        return bool(found)


def run(client: Client, month: str, now: datetime) -> Report:
    first, last = month_bounds(month)
    insiders = client.insiders()
    # Only the pull requests the report counts need their responses fetched.
    counted = [
        replace(
            pull_request,
            responses=tuple(client.responses(pull_request.repo, pull_request.number)),
        )
        for pull_request in client.pull_requests_opened(first, last)
        if counts_toward_target(pull_request, insiders)
    ]
    return build_report(
        month,
        counted,
        client.authors_merged(first, last),
        insiders,
        lambda login: client.merged_before(login, first),
        now,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "month", nargs="?", help="the month to report, YYYY-MM (default: last month)"
    )
    args = parser.parse_args(argv)
    now = datetime.now(UTC)
    month = args.month or previous_month(now.date())
    try:
        report = run(GhClient(), month, now)
    except (GhError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(format_report(report))
    print()
    print(format_logins(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
