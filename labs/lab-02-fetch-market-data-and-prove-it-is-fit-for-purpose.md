# Lab 2 — Fetch Market Data and Prove It Is Fit for Purpose

- **Course:** AI Agents for Stock Trading (C177)
- **Version:** v1.1 (4 October 2026)
- **Topic 1:** From Trading Idea to Quality Market Data
- **Maps to:** LO3: connect the workflow to authorised Alpaca market data, record the data contract, run deterministic quality gates, and let the agent interpret only the verified report
- **Tools:** Alpaca Paper Only account, alpaca-py StockHistoricalDataClient, pandas, deterministic quality validator, OpenAI Agents SDK read-only artifact tool

**Duration:** 60 minutes

---

## Goal

Produce an authorised SPY daily-bar dataset whose complete data contract, deterministic quality report, agent review, and SHA-256 fingerprint all agree.

## What You Will Do

Verify the frozen hypothesis, connect to Alpaca's historical stock-data client, fetch the declared SPY daily bars, and produce a source contract, CSV, quality report, and fingerprint. Then give the research agent read-only access to the structured quality report so it can recommend READY_FOR_BACKTEST or HOLD_DATA without changing any numeric observation.

## What You Will Build

C177-trading-agent-pack/02-market-data/ containing spy_daily.csv, market_data_contract.json, data_quality_report.json, data_agent_review.json, retrieval_manifest.json, and fingerprints.json

## Prerequisites

- Lab 1 is frozen and C177-trading-agent-pack/01-hypothesis/fingerprints.json still matches its files.
- ALPACA_API_KEY and ALPACA_SECRET_KEY are stored only in the ignored .env file; ALPACA_PAPER_ONLY remains true.
- The account entitlement and intended feed are understood: the default course request uses the IEX feed and records its single-exchange scope.
- Internet access is available. The synthetic generator is a labelled rejoin fallback and must not be described as real market data.

> **Rejoin path.** If a prerequisite artifact is missing, use the Rejoin Path in [the labs index](README.md), reconstruct the named checkpoint, and verify it before continuing.

> **Data note.** Use only authorised accounts, placeholder or synthetic inputs, and paper-trading credentials. This course does not provide financial advice and includes no live-order path.

## Steps

**1. Create the Lab 2 folder and recheck the Lab 1 fingerprints. Stop if any frozen file changed; restore it or create a documented new version before fetching data.**

```text
python labs/resources/workspace.py mkdir C177-trading-agent-pack/02-market-data
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
```

**2. Run preflight for Alpaca credentials. The script checks presence and the paper-only flag without displaying secret values.**

```text
python labs/resources/preflight.py --require alpaca
```

**3. Fetch the exact symbol, dates, interval, adjustment, and feed from the frozen hypothesis. The tool writes raw observations before any agent is asked to interpret them.**

```text
python labs/resources/fetch_validate_data.py --hypothesis C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --source alpaca --output-dir C177-trading-agent-pack/02-market-data
```

**4. If the provider is unavailable during class, generate the labelled synthetic rejoin checkpoint in a separate folder. Never rename it to hide its source and do not combine it with the Alpaca run.**

```text
python labs/resources/fetch_validate_data.py --hypothesis C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --source synthetic --output-dir C177-trading-agent-pack/02-market-data-rejoin
```

**5. Inspect market_data_contract.json. Confirm provider, endpoint, feed, entitlement scope, symbol, interval, start, end, timezone, session, adjustment, retrieved_at_utc, intended_use, and CSV fingerprint.**

```text
python -m json.tool C177-trading-agent-pack/02-market-data/market_data_contract.json
```

**6. Inspect data_quality_report.json. Resolve every critical failure; distinguish an expected market closure from an unexplained long calendar gap, and record any accepted warning with its owner and scope.**

```text
python -m json.tool C177-trading-agent-pack/02-market-data/data_quality_report.json
```

**7. Spot-check the first three and last three rows. Verify ordered unique timestamps, numeric OHLCV fields, high at least open and close, low at most open and close, and non-negative volume.**

```text
python labs/resources/inspect_market_data.py C177-trading-agent-pack/02-market-data/spy_daily.csv --head 3 --tail 3
```

**8. Run the research agent in read-only data-review mode. It must cite check names and values from the quality report and must not invent a price, fill a gap, or rewrite the status.**

```text
python labs/resources/trading_research_agent.py review-data --mode agent --pack C177-trading-agent-pack --output C177-trading-agent-pack/02-market-data/data_agent_review.json --manifest C177-trading-agent-pack/02-market-data/agent_review_manifest.json
```

**9. Compare the agent review with the deterministic status. If they disagree, the deterministic report controls and the disagreement is recorded as an agent defect.**

```text
python labs/resources/compare_review.py --report C177-trading-agent-pack/02-market-data/data_quality_report.json --review C177-trading-agent-pack/02-market-data/data_agent_review.json
```

**10. Freeze the Lab 2 checkpoint and verify it immediately. Lab 3 must receive the exact CSV whose hash appears in both the contract and quality report.**

```text
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --output C177-trading-agent-pack/02-market-data/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --verify C177-trading-agent-pack/02-market-data/fingerprints.json
```

## Test It

data_quality_report.json must show status READY_FOR_BACKTEST, critical_failures 0, duplicate_timestamps 0, missing_required_values 0, invalid_ohlc_rows 0, negative_volume_rows 0, and the same csv_sha256 recorded in market_data_contract.json. compare_review.py must report REVIEW_ALIGNED. fingerprints.json must verify every Lab 2 artifact. If you used the synthetic rejoin folder, the provider and intended_use fields must visibly identify it as synthetic and the real-data objective remains to be completed.

## Checkpoint for the Next Lab

Keep 02-market-data unchanged. Lab 3 verifies the CSV fingerprint, uses only the accepted dataset, and writes backtest outputs to a new 03-backtest-audit folder.

## Troubleshooting

- **The API returns an authentication or entitlement error:** Confirm you used paper-account API keys and the IEX feed. Do not switch to an undocumented endpoint or paste keys into the script. Use the labelled synthetic rejoin path while the trainer resolves access.
- **The quality report shows HOLD_DATA:** Open the critical_checks list, correct the source, date, schema, or corrupted file, and rerun from a clean Lab 2 folder. Never edit prices merely to make the gate green.
- **The agent calls the data ready while the report says HOLD_DATA:** Keep HOLD_DATA, record an agent-review defect, and rerun the agent after checking the supplied instructions and artifact path.

## Challenge

Fetch the same bounded date window from a second authorised feed or provider, record a separate contract, and explain why row counts, volume, or prices can differ without declaring either dataset automatically wrong.

## Reflection

Which market-data contract field would be easiest to omit and most damaging to a later interpretation?

---

[← Lab 1](lab-01-research-an-idea-and-freeze-a-testable-hypothesis.md) · [Lab 3 →](lab-03-backtest-the-rules-and-audit-the-evidence.md)
