# Lab 3 — Backtest the Rules and Audit the Evidence

- **Course:** AI Agents for Stock Trading (C177)
- **Version:** v1.1 (4 October 2026)
- **Topic 2:** The Six-Step Trading Workflow and Staying in Control
- **Maps to:** LO4: run a causal deterministic backtest, compare a benchmark and holdout, stress stated assumptions, and record an auditable research decision
- **Tools:** pandas, NumPy, Matplotlib, deterministic C177 backtest engine, OpenAI Agents SDK read-only artifact review, Markdown editor

**Duration:** 65 minutes

---

## Goal

Produce a reproducible causal backtest with benchmark, holdout, friction and parameter sensitivities, plus aligned deterministic, agent, and human audit decisions.

## What You Will Do

Verify the accepted hypothesis and market-data fingerprints, run the fixed 20/50-day crossover engine with a one-bar signal shift and declared frictions, then inspect trades, development and out-of-sample metrics, benchmark results, drawdown, and sensitivity checks. The agent receives only read-only report tools and drafts a review that the human auditor must reconcile with deterministic checks.

## What You Will Build

C177-trading-agent-pack/03-backtest-audit/ containing strategy_spec.json, signal_sample.csv, trades.csv, equity_curve.csv, equity_curve.png, backtest_metrics.json, sensitivity_report.json, audit_log.md, backtest_agent_review.json, run_manifest.json, and fingerprints.json

## Prerequisites

- Lab 1 and Lab 2 fingerprints verify and the deterministic market-data status is READY_FOR_BACKTEST.
- The CSV hash matches both market_data_contract.json and data_quality_report.json.
- The hypothesis remains version 1.0; parameter or date changes require a separately documented version rather than an overwrite.
- The learner understands that historical and out-of-sample results do not guarantee future behaviour.

> **Rejoin path.** If a prerequisite artifact is missing, use the Rejoin Path in [the labs index](README.md), reconstruct the named checkpoint, and verify it before continuing.

> **Data note.** Use only authorised accounts, placeholder or synthetic inputs, and paper-trading credentials. This course does not provide financial advice and includes no live-order path.

## Steps

**1. Create the Lab 3 folder and verify both upstream checkpoints. Stop on any mismatch instead of accepting a stale or edited input.**

```text
python labs/resources/workspace.py mkdir C177-trading-agent-pack/03-backtest-audit
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --verify C177-trading-agent-pack/02-market-data/fingerprints.json
```

**2. Run the deterministic engine from the frozen specification and accepted CSV. Do not ask the model to calculate returns, drawdown, Sharpe ratio, trades, or quantity.**

```text
python labs/resources/backtest_and_audit.py --hypothesis C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --data C177-trading-agent-pack/02-market-data/spy_daily.csv --quality-report C177-trading-agent-pack/02-market-data/data_quality_report.json --output-dir C177-trading-agent-pack/03-backtest-audit
```

**3. Inspect signal_sample.csv around at least one crossover. Confirm the raw signal is computed from completed bars, position_used is shifted by one row, and the same row's return never receives an unshifted signal.**

```text
python labs/resources/inspect_signal_timing.py C177-trading-agent-pack/03-backtest-audit/signal_sample.csv
```

**4. Read backtest_metrics.json as a system. Compare full, development, and out-of-sample strategy metrics with buy-and-hold; record trade count, total return, annualised return, volatility, Sharpe ratio, maximum drawdown, turnover, and benchmark gap.**

```text
python -m json.tool C177-trading-agent-pack/03-backtest-audit/backtest_metrics.json
```

**5. Open equity_curve.png and trades.csv. Find the largest drawdown period and inspect at least two entry-exit sequences; confirm the trade rows reconcile with changes in the position column.**

```text
python labs/resources/workspace.py locate C177-trading-agent-pack/03-backtest-audit/equity_curve.png C177-trading-agent-pack/03-backtest-audit/trades.csv
```

**6. Inspect sensitivity_report.json. Compare the declared friction case with zero and higher friction, then compare nearby 15/50 and 25/50 windows without selecting a new winner during this run.**

```text
python -m json.tool C177-trading-agent-pack/03-backtest-audit/sensitivity_report.json
```

**7. Complete the human audit log. Record leakage check, data lineage, trial count, benchmark, split date, cost assumptions, parameter stability, limitations, and a CONTINUE_RESEARCH, HOLD, or REVISE decision with reasons.**

```text
python labs/resources/workspace.py copy labs/resources/backtest_audit_starter.md C177-trading-agent-pack/03-backtest-audit/audit_log.md
python labs/resources/workspace.py locate C177-trading-agent-pack/03-backtest-audit/audit_log.md
```

**8. Run the agent in read-only backtest-review mode. It must cite report paths and values, preserve the deterministic status, and name limitations instead of recommending a trade.**

```text
python labs/resources/trading_research_agent.py review-backtest --mode agent --pack C177-trading-agent-pack --output C177-trading-agent-pack/03-backtest-audit/backtest_agent_review.json --manifest C177-trading-agent-pack/03-backtest-audit/agent_review_manifest.json
```

**9. Reconcile human, agent, and deterministic decisions. A disagreement is documented; it is never resolved by rewriting metrics. Lab 4 is enabled only when the deterministic checks allow CONTINUE_RESEARCH and the human audit agrees.**

```text
python labs/resources/compare_review.py --report C177-trading-agent-pack/03-backtest-audit/backtest_metrics.json --review C177-trading-agent-pack/03-backtest-audit/backtest_agent_review.json --human C177-trading-agent-pack/03-backtest-audit/audit_log.md
```

**10. Freeze and verify the Lab 3 checkpoint. The audit decision permits only a bounded paper exercise; it is not a statement of expected return or suitability for live capital.**

```text
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --output C177-trading-agent-pack/03-backtest-audit/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --verify C177-trading-agent-pack/03-backtest-audit/fingerprints.json
```

## Test It

The run manifest must show matching hypothesis and data fingerprints. signal_sample.csv must demonstrate a one-row position shift. backtest_metrics.json must contain full, development, out_of_sample, and benchmark sections plus deterministic_status. sensitivity_report.json must include at least three friction cases and the 15/50, 20/50, and 25/50 parameter cases. compare_review.py must report the deterministic, agent, and human decisions explicitly. All Lab 3 fingerprints must verify.

## Checkpoint for the Next Lab

Keep the verified 03-backtest-audit folder. Lab 4 reads the accepted audit decision and latest data reference, calculates a bounded quantity, generates a dry-run ticket, and submits only after the explicit human paper-approval gate.

## Troubleshooting

- **The engine reports an input fingerprint mismatch:** Restore the exact frozen file or create a new version and rerun its upstream gate. Do not edit the manifest to match a changed file.
- **The signal-timing inspection shows the position was not shifted:** Stop the run, inspect the position_used construction, and rerun from a clean output folder. Any metrics from the biased run are invalid.
- **Out-of-sample evidence or friction sensitivity is weak:** Record HOLD or REVISE. Preserve the result; do not tune on the same holdout and then relabel it as untouched evidence.

## Challenge

Add a walk-forward report with at least three chronological windows while preserving the original v1.0 run and trial log; explain what the extra windows reveal and what they still cannot prove.

## Reflection

Which audit check changed your interpretation of the headline return most, and why?

---

[← Lab 2](lab-02-fetch-market-data-and-prove-it-is-fit-for-purpose.md) · [Lab 4 →](lab-04-size-risk-approve-and-verify-a-paper-trade.md)
