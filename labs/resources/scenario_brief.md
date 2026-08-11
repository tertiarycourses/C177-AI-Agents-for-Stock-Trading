# C177 Connected Scenario: Northstar SPY Research Pack

## Purpose

The fictional Northstar research team wants to learn whether a simple, transparent trend rule is worth further paper-only investigation. The exercise is about evidence quality and control. It is not a recommendation, a forecast, or permission to use live capital.

## Fixed hypothesis inputs

- Instrument: SPY, a US-listed exchange-traded fund
- Bar interval: daily
- Research window: 2018-01-01 through 2025-12-31
- Data adjustment: all available price adjustments declared by the provider
- Signal: 20-day simple moving average compared with the 50-day simple moving average
- State: long-only, either zero or one unit of exposure
- Entry: after the 20-day average crosses above the 50-day average
- Exit: after the 20-day average crosses below the 50-day average
- Timing: compute from a completed bar and apply the position no earlier than the next bar
- Benchmark: buy-and-hold over the accepted dates using comparable data assumptions
- Friction case: 5 basis points on each position change; also show zero and 10 basis-point sensitivity cases
- Development/out-of-sample split: 2023-01-01
- Human owner: Course Learner, reviewed by Course Trainer

## Rejection and hold conditions

The workflow must stop when a critical data-quality check fails, an input fingerprint changes, signal timing uses future information, the benchmark or out-of-sample section is missing, or an order path is not paper-only. Weak, unstable, or sparse evidence leads to HOLD or REVISE rather than a stronger claim.

## Execution boundary

Only an Alpaca paper account may be used. The supplied code allowlists SPY, caps quantity at 20 shares, defaults to dry run, requires a human approval token, uses a unique client order ID, and constructs the trading client with `paper=True`. No live-mode option is provided.
