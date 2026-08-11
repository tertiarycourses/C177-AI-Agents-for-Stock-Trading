# C177 Trainer Rejoin Checkpoint - Hypothesis v1.0

## Scenario and owner

- Scenario: Northstar SPY research exercise using a long-only 20/50-day moving-average crossover.
- Human owner: Course trainer or designated learner reviewer.
- Reviewer: C177 trainer checkpoint review.
- Paper-only boundary: Research and Alpaca paper simulation only; no live-order path.

## Questions the evidence must answer

1. Is the idea expressed as fixed, falsifiable rules before data is tested?
2. Is the market-data contract sufficiently explicit for an independent reviewer?
3. Do the backtest, risk, and paper records remain reproducible and bounded?

## Evidence table

| Claim or field | Source URL | Access date | Scope | Limitation | Owner decision |
|---|---|---|---|---|---|
| Course scope | https://www.tertiarycourses.com.sg/ai-agents-for-trading.html | 2026-08-11 | C177 learning outline | Course description, not trading evidence | Use only for learning scope |
| Agent design | https://openai.github.io/openai-agents-python/ | 2026-08-11 | Agents SDK concepts and tools | Interfaces may change | Use a bounded read-only research agent |
| Market-data feed | https://docs.alpaca.markets/us/docs/about-market-data-api | 2026-08-11 | Alpaca feed coverage | The supplied rejoin data is synthetic | Label the rejoin source visibly |
| Paper limitations | https://docs.alpaca.markets/us/docs/paper-trading | 2026-08-11 | Paper simulator behaviour | Does not reproduce every live-market effect | Treat receipts as simulator evidence only |
| Position sizing | https://www.cmegroup.com/education/courses/trade-and-risk-management/proper-position-size | 2026-08-11 | Risk and stop-distance sizing | A stop does not guarantee a fill | Apply lower risk, exposure, buying-power, and course caps |

## Assumptions

- The SPY 20/50 rule is deliberately simple and is used to teach evidence controls, not to recommend a strategy.
- Daily bars are evaluated only after completion and positions use the prior bar's signal.
- The 2023-01-01 split creates a chronological holdout for review, not proof of future performance.

## Unknowns and resolutions

| Unknown | Why it matters | Resolution | Evidence or owner |
|---|---|---|---|
| Live execution suitability | Paper evidence cannot establish live suitability | Outside course scope; no live path permitted | Human owner and Alpaca paper limitations |
| Future performance | Historical evidence cannot predict the future | No return or suitability claim is permitted | Human owner |

## Version log

| Version | UTC time | Change | Reason | Owner |
|---|---|---|---|---|
| 1.0 | 2026-08-11T00:00:00+00:00 | Initial frozen trainer rejoin hypothesis | Restore a verified learning checkpoint | C177 trainer checkpoint |
