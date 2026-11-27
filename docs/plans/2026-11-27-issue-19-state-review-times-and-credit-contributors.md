# Plan: State review times and credit contributors whose work is reworked (issue #19)

Risk tier: Low. Markdown only: a new CONTRIBUTING.md section, a new CONTRIBUTORS.md, and links to it. No code, workflow, or CODEOWNERS-protected file changes, and the user made the policy decisions before planning.

Domain skills: humanizer: invoke (new contributor-facing prose; plain language, no em dashes, no emojis). django, django-ninja-api, django-allauth, django-celery, python-fastapi, vercel-react-best-practices, expo, frontend-design, dataviz: not applicable because the change is Markdown only.

## Decisions (from the user, 2026-11-27)

- Scope is the issue's "Done when" set: the CONTRIBUTING.md response target and credit rule, and a public contributor list. The pull request uses `Part of #19`. Tracking time to first response (a change to the scheduled admin-reminders workflow or the review script) and rewording the 90-day rule in GOVERNANCE.md are left for later pull requests.
- Timelines: first response within 3 business days, from the repository's maintainers. "Changes requested" means the author updates the pull request and the reviewer looks again. A pull request is closed after 30 days with no reply from its author, with a friendly note and an offer to reopen.
- Contributor list: a new `CONTRIBUTORS.md` in this repository, kept by hand and linked from the organization profile README. It lists GitHub handles and the kind of help each person gave, code or not. A maintainer adds people after a merged pull request or other help, and anyone can ask to be removed.
- Seed list, approved by the user: `GeoBradDev` (founder and interim steward, all repositories), `ccirrincione` (frontend, backup owner), `Mr-Neutr0n` (backend: exporting the OpenAPI schema and checking it in CI, backend #200, reworked in #201). `Mugunth007` (open backend #329) is added once a pull request merges, not now.

## Acceptance criteria

1. CONTRIBUTING.md has a section headed `## What happens after you open a pull request`, placed directly after "Pull requests" and before "Commit messages".
2. The section states a first-response target of 3 business days, says who responds and reviews (the repository's maintainers), and says what to do if that time passes without a reply (comment on the pull request to remind us). It is honest that OPEN is run by volunteers without weakening the target into "a few days".
3. The section says what "changes requested" means: the author pushes updates or replies, and the reviewer looks again.
4. The section says when a stale pull request is closed: after 30 days with no reply from its author, with a friendly note, and the author can ask to reopen it or open a new one. (Changed during review: an author without write access can't reopen a pull request a maintainer closed.)
5. CONTRIBUTING.md states the credit rule: when a maintainer supersedes or reworks a contributor's pull request, the new commits carry a `Co-Authored-By:` trailer for the original author, and the comment closing the original pull request thanks the author and links the new pull request. It says how to find an author's address when it isn't public (their GitHub noreply address). The trailer spelling matches the existing `Co-Authored-By:` used in "AI-assisted contributions".
6. A new `CONTRIBUTORS.md` at the repository root lists the three seed contributors by GitHub handle (linked to their GitHub profiles), each with the kind of help they gave. It says the list includes non-code help (feedback, statistics review, design, and so on), that a maintainer adds people after a merged pull request or other help, how to ask to be added or removed, and that it covers every OPEN repository. It names no one beyond the seed list and contains no personal email addresses or real names beyond GitHub handles. (Changed during review: the project contact address info@openpb.org is allowed, as the private route for removal requests.)
7. The credit rule in CONTRIBUTING.md also says to add a credited author to CONTRIBUTORS.md, linking to it with the full org URL.
8. `profile/README.md` links to CONTRIBUTORS.md (in "How to contribute" or a nearby place), so the list is reachable from the organization page.
9. No files change besides CONTRIBUTING.md, CONTRIBUTORS.md, profile/README.md, this plan, and any doc Phase 8 finds made wrong (for example the README.md "What else is here" list). No file in `.github/CODEOWNERS` changes. The text has no emojis and no em dashes. `python3 -I scripts/test_check_pull_request.py` still passes.

## Files that change

- `CONTRIBUTING.md`: new `## What happens after you open a pull request` section (criteria 1 to 5, 7).
- `CONTRIBUTORS.md`: new file (criterion 6).
- `profile/README.md`: one link (criterion 8).
- `README.md`: one line in "What else is here" for CONTRIBUTORS.md. Added during implementation: the README lists this repository's root files, and a new root file left out would make that list wrong (allowed by criterion 9).
- `docs/plans/2026-11-27-issue-19-state-review-times-and-credit-contributors.md`: this plan.

## Order of work

1. Write the CONTRIBUTING.md section after "Pull requests". Match the guide's voice: second person ("you", "we" for maintainers), short paragraphs and bullets, full org URLs (`https://github.com/openpickleball/.github/blob/main/...`) when linking other documents, in-page anchors when linking within the guide. Suggested parts, as short paragraphs or bullets: first response and who reviews; changes requested; stale pull requests; when we rework your pull request (the credit rule). The credit rule may instead be its own `###` or bullet block inside the section; keep it under this section so one anchor covers both promises.
2. Write CONTRIBUTORS.md: a one-paragraph intro (thanks, covers every repository, includes non-code help), a table or list of `[@handle](https://github.com/handle)` with what they did, then "How to be added or removed" (a maintainer adds you after a merged pull request, a pull request a maintainer reworked or replaced, or other help; to be added or removed, ask in GitHub Discussions or open a pull request editing the file; for a private request, email info@openpb.org). Keep it short.
3. Add the CONTRIBUTORS.md link to profile/README.md, using the full org URL like the other links there.
4. Run the humanizer skill over the new prose, then check for em dashes (`grep -n $'\u2014' CONTRIBUTING.md CONTRIBUTORS.md profile/README.md README.md docs/plans/2026-11-27-issue-19-state-review-times-and-credit-contributors.md` must print nothing) and emojis.
5. Run the gate: `python3 -I scripts/test_check_pull_request.py`.

## Risks

- Promising more than volunteers can keep. Riskiest wording: the 3 business day target must read as a target for a first response (an acknowledgement or question), not a full review or a merge.
- The credit rule reading as optional. It is a rule for maintainers ("the new commits carry"), not a suggestion.
- Publishing personal data. CONTRIBUTORS.md lists only GitHub handles the user approved, no emails. The noreply address guidance must not suggest guessing or exposing a private email.
- Out of scope, deliberately: the monthly tracking report, the GOVERNANCE.md 90-day wording and alumni listing, adding a "CONTRIBUTORS.md" step to the admin-reminders checklist (a scheduled workflow), editing other repositories, and retroactively crediting backend #201 (merged history is not rewritten).

## Proof

- Criteria 1 to 8: read the new section, CONTRIBUTORS.md, and the profile link against each criterion (Phase 5 compliance pass and Phase 7 verifier). `grep -n '^## ' CONTRIBUTING.md` shows the heading order; `grep -n 'CONTRIBUTORS.md' CONTRIBUTING.md profile/README.md` locates the links; `grep -n 'Co-Authored-By' CONTRIBUTING.md` shows the trailer spelling.
- Criterion 9: `git status --porcelain -uall` lists only the expected files; the em dash grep prints nothing; `python3 -I scripts/test_check_pull_request.py` ends `18 passed, 0 failed` (baseline measured on origin/main 4a62975: `18 passed, 0 failed`).
- Live drive: none required at Low; the change has no runtime behavior, and the gate covers the checker.
- No "behave alike" or "phrase absent" tests on runtime output, so nothing to measure on origin/main.

### Results (implementation, 2026-11-27)

- Before writing: `grep -n 'CONTRIBUTORS.md' CONTRIBUTING.md profile/README.md` printed nothing (exit 1), and the heading list had no `## What happens after you open a pull request`.
- After: the heading sits at line 37, between `## Pull requests` (29) and `## Commit messages` (57). CONTRIBUTING.md line 53 and profile/README.md line 99 link the full org URL of CONTRIBUTORS.md. Both `Co-Authored-By:` uses (lines 51 and 113) share one spelling.
- Em dash grep (`grep -n $'\u2014' CONTRIBUTING.md CONTRIBUTORS.md profile/README.md README.md docs/plans/2026-11-27-issue-19-state-review-times-and-credit-contributors.md`), which covers this plan too, printed nothing; an en dash and emoji grep also printed nothing.
- Gate: `18 passed, 0 failed`.
- `git status --porcelain -uall`: CONTRIBUTING.md, README.md, profile/README.md, CONTRIBUTORS.md, and this plan. Running the gate creates `scripts/__pycache__/`, which is deleted after each run.

### Review fixes (2026-11-27)

Four doc defects found in review, each with before and after text:

1. Reopening. Before, CONTRIBUTING.md:45: "You can reopen it, or open a new one, when you're ready to pick it back up." An author without write access can't reopen a pull request a maintainer closed. After: "Ask us to reopen it, or open a new one, when you're ready to pick it back up." Criterion 4 now says the same.
2. Reworked pull requests missing from the add rule. Before, CONTRIBUTORS.md:13 named only a merged pull request or other help. After: it also names a pull request a maintainer reworks or replaces with a new one.
3. No channel for add and removal requests. Before, CONTRIBUTORS.md:13 and 15 said "open an issue" (blank issues are off in `.github/ISSUE_TEMPLATE/config.yml`, so no form fits) and "message a maintainer" (no channel named). After: GitHub Discussions or a pull request editing the file, and email to info@openpb.org (the address SECURITY.md and CODE_OF_CONDUCT.md use) for a private request.
4. Which name goes in the trailer. Before, CONTRIBUTING.md:51: "a `Co-Authored-By:` trailer with your name and email address". A maintainer could write a real name the contributor never put on GitHub. After: "with the name and email address from your original commits", and the noreply paragraph now starts "If the email address in your commits isn't public".
