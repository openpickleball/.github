# openpickleball/.github

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/openpickleball/.github/badge)](https://scorecard.dev/viewer/?uri=github.com/openpickleball/.github)

This repository holds the organization profile and shared community files for OPEN, the Open Pickleball Evaluation Network. To learn about the project itself, see the [organization page](https://github.com/openpickleball).

## Where the work lives

| Repository | What it holds |
| --- | --- |
| [rating-spec](https://github.com/openpickleball/rating-spec) | The official, versioned rating spec and its RFC process |
| [engine](https://github.com/openpickleball/engine) | The reference rating engine |
| [backend](https://github.com/openpickleball/backend) | Backend services and APIs |
| [frontend](https://github.com/openpickleball/frontend) | The public app |
| [developers](https://github.com/openpickleball/developers) | The developer site at [dev.openpb.org](https://dev.openpb.org) |
| [brand-assets](https://github.com/openpickleball/brand-assets) | Logos, colors, typography, and the brand guidelines |

## Shared community files

GitHub uses the community files here as defaults for any repository in the organization that doesn't have its own copy. A repository's `LICENSE` is not inherited, so each repository needs its own.

| Document | Purpose |
| --- | --- |
| [Organization profile](profile/README.md) | What OPEN is and how it works |
| [Mission charter](CHARTER.md) | The terms OPEN is built on |
| [Governance](GOVERNANCE.md) | How decisions are made |
| [Roadmap](ROADMAP.md) | Priorities across the project |
| [Contributing guide](CONTRIBUTING.md) | How to take part |
| [Code of Conduct](CODE_OF_CONDUCT.md) | How we treat each other |
| [Security policy](SECURITY.md) | How to report a security problem |
| [Support](SUPPORT.md) | Where to get help |
| [Licensing](LICENSING.md) | How each part of OPEN is licensed |

The issue forms and pull request template in [`.github`](.github) are shared the same way. Blank issues are turned off, so every new issue starts from a form: a bug report, a feature request, community feedback, or a rating spec change.

## What else is here

- [`FUNDING.yml`](FUNDING.yml): the sponsor links GitHub shows on OPEN's repositories, pointing to [Open Collective](https://opencollective.com/open-pickleball), where every dollar in and out is published.
- [`.github/workflows`](.github/workflows): this repository's own checks (DCO sign-off and OpenSSF Scorecard) and a monthly reminder issue for the membership review in [GOVERNANCE.md](GOVERNANCE.md).
- [`scripts`](scripts): `membership-review.sh`, which an organization owner runs locally for that review. It only reports and never changes membership.

## License

The documentation here is licensed under CC BY 4.0 ([`LICENSE`](LICENSE)), and the code in `scripts` under Apache-2.0 ([`LICENSE-APACHE`](LICENSE-APACHE)). The Code of Conduct is adapted from the Contributor Covenant and licensed under CC BY-SA 4.0. See [LICENSING.md](LICENSING.md) for details.
