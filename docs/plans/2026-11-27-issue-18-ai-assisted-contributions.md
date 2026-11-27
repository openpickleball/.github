# Plan: Write down how OPEN treats AI-assisted contributions (issue #18)

Risk tier: Low. A documentation-only change to CONTRIBUTING.md and the shared pull request template; no code, workflow, or CODEOWNERS-protected file changes, and the policy decisions were made by the user before planning.

Domain skills: humanizer: invoke (new contributor-facing prose; the user wants plain language, no em dashes, no emojis). django, django-ninja-api, django-allauth, django-celery, python-fastapi, react, expo, frontend-design, dataviz: not applicable because the change is Markdown only.

## Decisions (from the user, 2026-11-27)

- Disclosure is required when an AI tool wrote a meaningful part of a change: a `Co-Authored-By` trailer on the commit, or a note in the pull request description.
- Links to private AI sessions (for example `Claude-Session: https://claude.ai/code/session_...` trailers) are not allowed in public commit messages or pull request descriptions. Commits that are already merged keep their links: no history rewrite. Unmerged commits follow the rule.
- This pull request changes only the `.github` repository and uses `Part of #18`. After it, one follow-up issue per repository with its own guide (backend, frontend, developers, engine) asks that repository to link the new section and to describe its own `CLAUDE.md`, `AGENTS.md`, and `plans/`.

## Acceptance criteria

1. CONTRIBUTING.md has a section headed `## AI-assisted contributions`, placed after "Sign off your commits" and before "Becoming a maintainer", reachable at the anchor `#ai-assisted-contributions`.
2. The section says contributors may use AI tools.
3. The section says the person who signs off is responsible for the whole change and must understand it well enough to explain it and answer review questions.
4. The section says the DCO sign-off applies in full to AI-assisted work: signing off certifies the contributor has the right to submit it under the repository's license, and links to the "Sign off your commits" section.
5. The section says AI-assisted changes meet the same review and test bar as any other change.
6. The section says disclosure is required when an AI tool wrote a meaningful part of a change, and names both accepted forms: a `Co-Authored-By:` trailer on the commit, or a note in the pull request description. It says the rule is the same in every OPEN repository.
7. The section says links to private AI sessions do not belong in commit messages or pull request descriptions, gives the reason (outside readers cannot open them), and says to put what a reviewer needs in the message or description instead. It does not ask anyone to rewrite already merged history.
8. The section explains `CLAUDE.md`, `AGENTS.md`, and `plans/` (or a repository's plans directory): what each is for, and whether a newcomer is expected to read, follow, or update it. It says a repository's own README or CONTRIBUTING.md can say more.
9. The section says what maintainers do with low-effort, unreviewed AI-generated pull requests: they may close them with a link to this section, without a line-by-line review.
10. The shared pull request template's checklist has one new item asking the author to disclose AI assistance as the section describes, linking to `CONTRIBUTING.md#ai-assisted-contributions`.
11. No other file changes besides this plan. The text has no emojis and no em dashes. `python3 -I scripts/test_check_pull_request.py` still passes.

## Files that change

- `CONTRIBUTING.md`: new `## AI-assisted contributions` section (criteria 1 to 9).
- `.github/PULL_REQUEST_TEMPLATE.md`: one checklist line (criterion 10).
- `docs/plans/2026-11-27-issue-18-ai-assisted-contributions.md`: this plan.

## Order of work

1. Write the CONTRIBUTING.md section. Match the guide's existing voice: second person, short paragraphs and bullets, links to the org copy under `https://github.com/openpickleball/.github/blob/main/...` when linking other documents, and in-page anchors (`#sign-off-your-commits`) when linking within the guide. Suggested sub-structure, as short paragraphs or bullets rather than new `###` headings unless it reads better: using AI tools; your responsibility and the sign-off; disclosure; private session links; agent instruction files and plans; what maintainers do with low-effort pull requests.
2. Add the template checklist line, worded like the existing items and linking with the full org URL as the other items do.
3. Run the humanizer skill over the new prose, then check for em dashes (`grep -n $'\u2014' CONTRIBUTING.md .github/PULL_REQUEST_TEMPLATE.md` must print nothing) and emojis.
4. Run the gate.

## Risks

- Policy wording that reads stricter or looser than decided. Riskiest step: the disclosure threshold ("a meaningful part") must not turn into "any use at all" (autocomplete, spelling) or into "optional".
- Describing `CLAUDE.md`/`AGENTS.md` as files contributors must edit or must run an AI tool with. They are instructions for AI coding agents that also document the repository's conventions; a newcomer should read them for conventions, follow them when using an agent, and update them in the same pull request when a change makes them wrong. `plans/` holds implementation plans written before larger changes; reading is optional, and a plan is not a spec or a promise.
- Template line breaking the `pull-request` check for future PRs. The check reads descriptions; a checklist line with a link does not affect its rules, and the gate's tests cover the checker.
- Out of scope, deliberately: enforcing the session-link rule in `scripts/check_pull_request.py`, editing other repositories, rewriting existing commits.

## Proof

- Criteria 1 to 10: read the rendered section and template against each criterion (Phase 5 compliance pass and Phase 7 verifier). `grep -n '^## AI-assisted contributions$' CONTRIBUTING.md` locates the heading; `grep -n 'ai-assisted-contributions' .github/PULL_REQUEST_TEMPLATE.md` locates the link.
- Criterion 11: `git status --porcelain -uall` lists only the three files; the em dash grep prints nothing; `python3 -I scripts/test_check_pull_request.py` ends `18 passed, 0 failed`.
- Live drive: none required at Low beyond the above; the gate covers the checker, and the change has no runtime behavior.
- No "behave alike" or "phrase absent" tests on runtime output, so nothing to measure on origin/main.
