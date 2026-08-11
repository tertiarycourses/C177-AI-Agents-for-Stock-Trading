# C177 Backtest Audit Log

## Run identity

- Auditor initials:
- UTC time:
- Hypothesis SHA-256:
- Market-data CSV SHA-256:
- Code or repository commit:

## Required audit checks

| Check | Evidence path or value | Result | Auditor note |
|---|---|---|---|
| Frozen v1.0 rules used | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Data status READY_FOR_BACKTEST | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Position shifted one bar | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| No impossible OHLCV rows | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Buy-and-hold benchmark present | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Development and out-of-sample sections present | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Zero, 5, and 10 bps friction cases present | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| 15/50, 20/50, and 25/50 stability cases present | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Trial count recorded | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |
| Limitations recorded | OWNER_TO_VERIFY | OWNER_TO_VERIFY | OWNER_TO_VERIFY |

## Interpretation

- Evidence that supports continued paper research:
- Evidence that weakens the hypothesis:
- What the backtest cannot establish:
- Agent-review disagreements:

## Human decision

Decision: OWNER_TO_VERIFY

Allowed values: `CONTINUE_RESEARCH`, `HOLD`, or `REVISE`.

Reason:

Next permissible action:

Owner and UTC time:
