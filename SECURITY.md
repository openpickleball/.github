# Security Policy

OPEN will hold player profiles, match histories, and ratings that people depend on, so we take reports seriously. This policy applies to every repository in the [openpickleball](https://github.com/openpickleball) organization unless a repository has its own `SECURITY.md`.

## Reporting a vulnerability

**Please do not report security problems in public issues, pull requests, or discussions.**

Report them privately in one of these ways:

- Email **info@openpb.org**.
- Use GitHub's private reporting on the affected repository: open the **Security** tab and choose **Report a vulnerability**.

Please include:

- The repository, service, or URL affected
- Steps to reproduce the problem
- What an attacker could do with it
- Any suggested fix

## What's in scope

- Vulnerabilities in OPEN code or hosted services
- Access to player data or accounts that should be private
- Ways to change, forge, or manipulate ratings or match results, such as bypassing score confirmation or organizer verification

Problems with the rating math that don't involve bypassing a control are welcome as regular issues.

## What to expect

We aim to acknowledge reports within 5 business days. We'll keep you updated while we investigate and fix the problem.

Once we confirm a report, we set its severity and aim to fix it within:

| Severity | Fix target |
| --- | --- |
| [Critical](https://github.com/openpickleball/.github/blob/main/docs/security/incident-response.md#severity) | 7 days |
| [High](https://github.com/openpickleball/.github/blob/main/docs/security/incident-response.md#severity) | 30 days |
| [Medium](https://github.com/openpickleball/.github/blob/main/docs/security/incident-response.md#severity) | 90 days |
| [Low](https://github.com/openpickleball/.github/blob/main/docs/security/incident-response.md#severity) | Best effort |

Each target counts from the day we confirm the report.

We announce each fix in a GitHub security advisory on the affected repository. The advisory credits you unless you'd prefer to stay anonymous.

## Disclosure

We follow coordinated disclosure. Please keep the details private until 90 days after your report. If a fix ships sooner, we'll agree with you on when to share them. If a fix needs more time, we can agree together on a later date.

## How we handle incidents

- The [incident response plan](https://github.com/openpickleball/.github/blob/main/docs/security/incident-response.md) says who leads, how we rate severity, and the steps we follow, including how we tell affected players and partners.
- The [threat model](https://github.com/openpickleball/.github/blob/main/docs/security/threat-model.md) lists what OPEN protects, the threats we expect, the controls in place today, and the known gaps.

## Supported versions

OPEN is in early development and has no stable releases yet. Security fixes are made on each repository's default branch.

## Good-faith research

We won't pursue complaints against anyone who researches and reports in good faith under this policy. Please test only with accounts and data you own, don't access or keep other people's data, and avoid disrupting the service. If you come across personal data by accident, stop and tell us.
