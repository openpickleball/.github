# OPEN

**Open Pickleball Evaluation Network**

OPEN is a free, open-source, community-governed pickleball rating network. We believe player ratings, match histories, and the standards behind them should be transparent, portable, and accessible to everyone.

> **Project status:** OPEN is in early development. Ratings are not live yet, and we are testing the rating engine on real match results before anyone relies on it.

## What OPEN is

OPEN is a community-owned rating standard and the shared infrastructure behind it. Apps, league platforms, clubs, and tournaments are our partners, and anything they build can use OPEN for free.

OPEN uses the familiar 2.0 to 8.0 pickleball rating scale and works alongside the ratings players already have, so nobody has to choose.

We are building:

- **A rating spec and reference engine**, published and versioned
- **A results API** for platforms, clubs, and tournaments to submit matches
- **A ratings and stats API** so any app can show OPEN ratings, history, and stats for free
- **A public app** on web, Android, and iOS with player profiles, clubs, rankings, match history, data export, and a clear explanation of how each rating was calculated
- **Organizer tools** to upload results, confirm starting ratings, and review flagged matches

## Why it exists

A rating decides which events a player can enter, who they get matched with, and how they see their own progress. Something with that much influence should be open to inspection. Players should be able to see how their number was calculated, question it when it looks wrong, and take their record with them when they move to a different club, league, or app.

OPEN exists so that a player's rating and match history don't depend on any single company or platform.

## Mission charter

OPEN will always be free, transparent, and community-run, with portable data and one shared standard. The [mission charter](https://github.com/openpickleball/.github/blob/main/CHARTER.md) sets out these terms, and [GOVERNANCE.md](https://github.com/openpickleball/.github/blob/main/GOVERNANCE.md) explains how decisions are made.

## How ratings work

The rating engine is an Elo variant designed for doubles and singles play. It takes these factors into account:

| Factor | What it does |
| --- | --- |
| Team rating | Combines two partners' ratings to predict a match |
| Individual updates | Gives each player their own rating change |
| Point differential | Separates a close loss from a decisive one |
| Rating uncertainty | Allows larger changes for new players |
| Recency | Accounts for skill changing over time |
| Match weighting | Can count verified tournament results differently from casual matches |

Every rating comes with a reliability score from 0 to 100%. Reliability is earned through matches on OPEN, variety of opponents, and recent play. It can't be chosen.

## How we validate it

Match outcomes are the ground truth. We judge the engine by how well it predicts matches it hasn't seen:

- **Predictive accuracy** on future matches only, using Brier score and log loss
- **Calibration:** a 70% favorite should win about 70% of the time
- **Stability** for established players and quick convergence for new ones
- **Breakdowns** by skill level, recreational and tournament play, new players, and separate groups of players

New ratings run in shadow mode before anyone relies on them, so early errors cost nobody.

Results are held to the same standard. Both teams confirm a score or a verified organizer submits it, impossible scores are rejected, duplicates are caught, and outliers are flagged.

## How OPEN is funded

Players never pay. Our money rules are simple:

1. Ratings are free forever, with no paid tiers or premium features.
2. Players are never asked for money, in the app or at events.
3. Support comes with no strings attached. Donors, grant makers, and sponsors get no say over ratings.
4. Every dollar in and out is published.
5. No advertisements.

## Repositories

| Repository | Description |
| --- | --- |
| [engine](https://github.com/openpickleball/engine) | The reference rating engine |
| [backend](https://github.com/openpickleball/backend) | Backend services and APIs |
| [frontend](https://github.com/openpickleball/frontend) | The public app |
| [.github](https://github.com/openpickleball/.github) | This organization profile and shared community files |

More repositories will be listed here as they are published. You can also browse [everything in the organization](https://github.com/openpickleball?tab=repositories).

## How to contribute

Everyone who takes part agrees to the mission charter above. You don't need to write code to help:

- **Players:** tell us what you need from a rating and what would make one easier to trust.
- **Clubs and organizers:** share how you run events and record results.
- **App and league platform builders:** tell us what you'd need to send results to OPEN or show OPEN ratings.
- **Statisticians and rating enthusiasts:** review the methods and challenge the assumptions behind them.
- **Developers and designers:** help build the engine, APIs, and tools.

Before proposing a new feature, ask whether it makes the standard more accurate, more trusted, or easier to adopt. If it doesn't, it probably belongs in a partner's product.

To get started, [open an issue](https://github.com/openpickleball/.github/issues/new) with your idea, question, or feedback.

## Website and community

- **Website:** [www.openpb.org](https://www.openpb.org)
- **GitHub:** [github.com/openpickleball](https://github.com/openpickleball)
- **Questions and ideas:** [GitHub Discussions](https://github.com/openpickleball/.github/discussions)
- **Feedback and bug reports:** [GitHub issues](https://github.com/openpickleball/.github/issues)
