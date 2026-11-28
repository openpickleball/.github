# SPDX-License-Identifier: Apache-2.0
"""Tests for response_report.py.

Plain functions with plain asserts, so pytest collects them, and they also
run with the standard library alone, as the `scripts` workflow runs them:

    python3 -I scripts/test_response_report.py

Nothing here calls GitHub: the client tests use a fake `gh`.
"""

import json
import sys
from collections.abc import Callable
from datetime import UTC, date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import response_report as report

# 2026-11-02 is a Monday.
MONDAY = datetime(2026, 11, 2, 10, 0, tzinfo=UTC)
FRIDAY = datetime(2026, 11, 6, 16, 0, tzinfo=UTC)
SATURDAY = datetime(2026, 11, 7, 9, 0, tzinfo=UTC)
LATE = datetime(2026, 12, 31, tzinfo=UTC)


def _pr(
    number: int = 1,
    author: str = "outsider",
    created_at: datetime = MONDAY,
    responses: tuple[report.Response, ...] = (),
    author_is_bot: bool = False,
    repo: str = "backend",
) -> report.PullRequest:
    return report.PullRequest(
        repo=repo,
        number=number,
        url=f"https://github.com/openpickleball/{repo}/pull/{number}",
        author=author,
        author_is_bot=author_is_bot,
        created_at=created_at,
        responses=responses,
    )


def _reply(at: datetime, login: str = "keeper", bot: bool = False) -> report.Response:
    return report.Response(login, bot, at)


def test_three_business_days_from_a_weekday_keep_the_time() -> None:
    assert report.add_business_days(MONDAY, 3) == datetime(
        2026, 11, 5, 10, 0, tzinfo=UTC
    )


def test_business_days_skip_the_weekend() -> None:
    assert report.add_business_days(FRIDAY, 3) == datetime(
        2026, 11, 11, 16, 0, tzinfo=UTC
    )


def test_a_weekend_start_counts_from_monday_midnight() -> None:
    assert report.add_business_days(SATURDAY, 3) == datetime(
        2026, 11, 12, 0, 0, tzinfo=UTC
    )


def test_a_sunday_start_counts_from_the_next_monday() -> None:
    sunday = datetime(2026, 11, 8, 23, 0, tzinfo=UTC)
    assert report.add_business_days(sunday, 1) == datetime(
        2026, 11, 10, 0, 0, tzinfo=UTC
    )


def test_a_reply_at_the_deadline_meets_the_target() -> None:
    deadline = datetime(2026, 11, 5, 10, 0, tzinfo=UTC)
    result = report.classify(_pr(responses=(_reply(deadline),)), LATE)
    assert result.outcome == "met"


def test_a_reply_after_the_deadline_misses_it() -> None:
    late = datetime(2026, 11, 5, 10, 1, tzinfo=UTC)
    result = report.classify(_pr(responses=(_reply(late),)), LATE)
    assert result.outcome == "missed"


def test_the_earliest_reply_counts() -> None:
    early = datetime(2026, 11, 3, tzinfo=UTC)
    late = datetime(2026, 11, 20, tzinfo=UTC)
    result = report.classify(_pr(responses=(_reply(late), _reply(early))), LATE)
    assert (result.outcome, result.first_response) == ("met", early)


def test_the_authors_own_comments_and_bots_are_not_responses() -> None:
    early = datetime(2026, 11, 3, tzinfo=UTC)
    pr = _pr(
        responses=(
            _reply(early, login="outsider"),
            _reply(early, login="github-actions[bot]", bot=True),
        )
    )
    result = report.classify(pr, LATE)
    assert (result.outcome, result.first_response) == ("missed", None)


def test_no_reply_before_the_deadline_is_pending() -> None:
    now = datetime(2026, 11, 4, tzinfo=UTC)
    assert report.classify(_pr(), now).outcome == "pending"


def test_bot_names_are_recognized() -> None:
    assert report.is_bot("dependabot[bot]")
    assert report.is_bot("some-app", "Bot")
    assert not report.is_bot("botanist", "User")


def test_month_bounds_cover_the_whole_month() -> None:
    assert report.month_bounds("2026-11") == (date(2026, 11, 1), date(2026, 11, 30))
    assert report.month_bounds("2026-12") == (date(2026, 12, 1), date(2026, 12, 31))
    assert report.month_bounds("2028-02") == (date(2028, 2, 1), date(2028, 2, 29))


def test_a_bad_month_is_a_clear_error() -> None:
    try:
        report.month_bounds("November")
    except ValueError as error:
        assert "YYYY-MM" in str(error)
    else:
        raise AssertionError("expected a ValueError")


def test_the_default_month_is_last_month() -> None:
    assert report.previous_month(date(2026, 12, 1)) == "2026-11"
    assert report.previous_month(date(2027, 1, 15)) == "2026-12"


def _built() -> report.Report:
    met = _pr(1, responses=(_reply(datetime(2026, 11, 2, 12, 0, tzinfo=UTC)),))
    missed = _pr(2, repo="engine")
    insider = _pr(3, author="keeper")
    bot = _pr(4, author="dependabot[bot]", author_is_bot=True)
    return report.build_report(
        "2026-11",
        [missed, met, insider, bot],
        ["newcomer", "regular", "keeper", "dependabot[bot]", "newcomer"],
        {"keeper"},
        lambda login: login == "regular",
        LATE,
    )


def test_insiders_and_bots_are_left_out() -> None:
    built = _built()
    assert [r.pull_request.number for r in built.results] == [1, 2]
    assert built.first_time == ["newcomer"]
    assert built.repeat == ["regular"]


def test_the_summary_gives_counts_and_links_but_no_logins() -> None:
    text = report.format_report(_built())
    assert "Met: 1 of 2 (50%). Missed: 1. Still pending: 0." in text
    assert "Median time to first response: 2.0 hours." in text
    assert "Missed: https://github.com/openpickleball/engine/pull/2" in text
    assert "First-time: 1. Repeat: 1." in text
    for login in ("newcomer", "regular", "keeper", "outsider", "dependabot"):
        assert login not in text


def test_an_empty_month_says_so() -> None:
    empty = report.build_report("2026-11", [], [], set(), lambda _: False, LATE)
    text = report.format_report(empty)
    assert "No pull requests from outside the maintainers team" in text
    assert "First-time: 0. Repeat: 0." in text


def test_the_logins_list_is_separate() -> None:
    text = report.format_logins(_built())
    assert "First-time: newcomer" in text
    assert "Repeat: regular" in text


class FakeGh:
    """Answers `gh api` calls from a table of path prefixes."""

    def __init__(self, answers: dict[str, object]) -> None:
        self.answers = answers
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str]) -> report.GhResult:
        self.calls.append(args)
        path = args[4]
        for prefix, answer in self.answers.items():
            if path.startswith(prefix):
                return report.GhResult(0, json.dumps(answer), "")
        return report.GhResult(1, "", f"HTTP 404: {path}")


def _client(answers: dict[str, object]) -> tuple[report.GhClient, FakeGh]:
    fake = FakeGh(answers)
    return report.GhClient("openpickleball", run=fake, sleep=lambda _: None), fake


def test_the_client_reads_insiders_from_the_team_and_the_owners() -> None:
    client, _ = _client(
        {
            "orgs/openpickleball/teams/maintainers/members": [{"login": "a"}],
            "orgs/openpickleball/members?role=admin": [{"login": "b"}],
        }
    )
    assert client.insiders() == {"a", "b"}


def test_the_client_collects_reviews_and_both_kinds_of_comments() -> None:
    base = "repos/openpickleball/backend"
    client, fake = _client(
        {
            "search/issues": [
                {
                    "repository_url": "https://api.github.com/repos/openpickleball/backend",
                    "number": 7,
                    "html_url": "https://github.com/openpickleball/backend/pull/7",
                    "user": {"login": "outsider", "type": "User"},
                    "created_at": "2026-11-02T10:00:00Z",
                }
            ],
            f"{base}/pulls/7/reviews": [
                {
                    "user": {"login": "m", "type": "User"},
                    "submitted_at": "2026-11-03T00:00:00Z",
                },
                {"user": {"login": "m", "type": "User"}, "submitted_at": None},
            ],
            f"{base}/issues/7/comments": [
                {
                    "user": {"login": "ci[bot]", "type": "Bot"},
                    "created_at": "2026-11-02T10:05:00Z",
                }
            ],
            f"{base}/pulls/7/comments": [
                {"user": None, "created_at": "2026-11-04T00:00:00Z"}
            ],
        }
    )
    (pr,) = client.pull_requests_opened(date(2026, 11, 1), date(2026, 11, 30))
    assert (pr.repo, pr.number, pr.author) == ("backend", 7, "outsider")
    assert pr.created_at == MONDAY
    assert pr.responses == ()
    responses = client.responses("backend", 7)
    assert [(r.login, r.is_bot) for r in responses] == [
        ("m", False),
        ("ci[bot]", True),
        ("ghost", False),
    ]
    search = fake.calls[0]
    assert "--jq" in search and ".items" in search
    assert "created%3A2026-11-01..2026-11-30" in search[4]


def test_a_failed_gh_call_raises() -> None:
    client, _ = _client({})
    try:
        client.insiders()
    except report.GhError as error:
        assert "HTTP 404" in str(error)
    else:
        raise AssertionError("expected a GhError")


def test_a_4xx_answer_is_not_retried() -> None:
    client, fake = _client({})
    try:
        client.insiders()
    except report.GhError:
        pass
    assert len(fake.calls) == 1


def test_a_dropped_connection_is_retried() -> None:
    answers = [
        report.GhResult(1, "", "net/http: TLS handshake timeout"),
        report.GhResult(0, json.dumps([{"login": "a"}]), ""),
    ]
    calls: list[list[str]] = []

    def flaky(args: list[str]) -> report.GhResult:
        calls.append(args)
        return answers.pop(0) if answers else report.GhResult(0, "[]", "")

    client = report.GhClient("openpickleball", run=flaky, sleep=lambda _: None)
    assert client.insiders() == {"a"}
    assert len(calls) == 3


def test_a_connection_that_keeps_failing_gives_up() -> None:
    calls: list[list[str]] = []

    def down(args: list[str]) -> report.GhResult:
        calls.append(args)
        return report.GhResult(1, "", "error connecting to api.github.com")

    client = report.GhClient("openpickleball", run=down, sleep=lambda _: None)
    try:
        client.insiders()
    except report.GhError as error:
        assert "error connecting" in str(error)
    else:
        raise AssertionError("expected a GhError")
    assert len(calls) == report.GET_ATTEMPTS


class FakeClient:
    def __init__(self) -> None:
        self.asked: list[int] = []

    def insiders(self) -> set[str]:
        return {"keeper"}

    def pull_requests_opened(self, first: date, last: date) -> list[report.PullRequest]:
        assert (first, last) == (date(2026, 11, 1), date(2026, 11, 30))
        return [
            _pr(1),
            _pr(2, author="keeper"),
            _pr(3, author="dependabot[bot]", author_is_bot=True),
        ]

    def responses(self, repo: str, number: int) -> list[report.Response]:
        self.asked.append(number)
        return [_reply(datetime(2026, 11, 2, 11, 0, tzinfo=UTC))]

    def authors_merged(self, first: date, last: date) -> list[str]:
        return ["outsider", "keeper"]

    def merged_before(self, login: str, first: date) -> bool:
        assert first == date(2026, 11, 1)
        return False


def test_run_fetches_responses_only_for_counted_pull_requests() -> None:
    client = FakeClient()
    built = report.run(client, "2026-11", LATE)
    assert client.asked == [1]
    assert [(r.pull_request.number, r.outcome) for r in built.results] == [(1, "met")]
    assert built.first_time == ["outsider"]


def test_main_reports_a_bad_month_without_a_traceback() -> None:
    assert report.main(["2026-13"]) == 1


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
