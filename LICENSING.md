# How OPEN is licensed

Different parts of OPEN are licensed differently, because code, documentation, data, and the OPEN name each need something different. This page explains the policy. The `LICENSE` file in each repository is what legally applies to that repository, and it takes precedence over this page.

| What | License |
| --- | --- |
| Hosted application, backend, and reference rating engine (the `frontend`, `backend`, and `engine` repositories) | [AGPL-3.0-or-later](https://www.gnu.org/licenses/agpl-3.0.html) |
| SDKs, client libraries, API specifications, and integration libraries | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Documentation, including the developer site's text (the `developers` repository), the published rating spec (the `rating-spec` repository), and the published evaluation of the reference engine, with its aggregate results, tables, and figures (the `evaluation` repository) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| The developer site's code: its build configuration, workflows, and scripts (the `developers` repository) | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) |
| Player and match data | Not openly licensed (see below) |
| The OPEN name and logo | Not licensed (see below) |
| Brand files (the `brand-assets` repository) | The horizon artwork is CC BY 4.0. The fonts keep their [SIL Open Font License](https://openfontlicense.org/). Files that show the OPEN name or logo are not licensed (see below). The repository's `LICENSE.md` says which terms apply to each file. |

## Why these licenses

**Platform code is AGPL** so that improvements stay open. Anyone can read, run, modify, or fork it, including to run their own service. If they offer a modified version to users over a network, they must publish their source code under the same license.

**SDKs and API specifications are Apache-2.0** so that any app, league platform, club, or tournament can integrate with OPEN, including in closed-source products.

**Documentation and the rating spec are CC BY 4.0** so that anyone can share and build on them with attribution.

## The OPEN name

Open licenses let people change and redistribute the work. They don't decide what can be called OPEN. Nothing in these licenses grants rights to the OPEN name or logo.

Anyone can fork the code or adapt the spec, but a modified version can't present itself as the official OPEN standard or show an OPEN rating unless it conforms to the official spec, as the [mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md) requires.

## Player and match data

Player data is about real people, so the licenses above don't apply to it. Players and leagues can export their own data at any time. OPEN will not publish a dataset containing player data until a data policy covering consent, export, deletion, and de-identification is in place.

## This repository

This repository holds both documentation and code, so it has two license files:

- Code (the `scripts` directory, the `labels.toml` file the label sync reads, and any other script or program added here) is licensed under Apache-2.0, in `LICENSE-APACHE`. Each script, and `labels.toml`, carries an `SPDX-License-Identifier: Apache-2.0` line.
- Everything else is documentation, licensed under CC BY 4.0, in `LICENSE`. Creative Commons advises against its licenses for software, which is why the code is licensed separately.

The exception is `CODE_OF_CONDUCT.md`, which is adapted from the Contributor Covenant and licensed under CC BY-SA 4.0.

## Contributions

Contributors keep the copyright to their work and license it under the license of the repository they contribute to. Every commit is signed off under the [Developer Certificate of Origin](https://developercertificate.org/). See the [contributing guide](https://github.com/openpickleball/.github/blob/main/CONTRIBUTING.md).
