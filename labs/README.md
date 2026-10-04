# AI Agents for Stock Trading (C177) — Hands-On Labs

4 labs across 2 topics · 1 day · 7.5 instructional hours · 8 clock hours including tea breaks · 4 hours 5 minutes hands-on labs

Work through the labs in order — each one builds on the artifacts you produced in the labs before it.


## Rejoin Path

If you join after Lab 1 or resume after a gap, do not skip the connected inputs. Reconstruct and verify the smallest baseline below before starting the target lab. The supplied starter files reduce setup time but do not replace the required checks.

| Rejoin point | Minimum verified baseline |
|---|---|
| Before Lab 2 | Copy labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis into your pack, verify fingerprints.json, and confirm the SPY long-only 20/50-day rule plus zero unresolved fields before fetching data. |
| Before Lab 3 | Copy labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis and 02-market-data into your pack, verify both manifests, and confirm the data is visibly labelled synthetic and READY_FOR_BACKTEST before the backtest exercise. |
| Before Lab 4 | Copy all three folders from labs/resources/rejoin/C177-trading-agent-pack into your pack, verify every manifest, rerun compare_review.py, and inspect the benchmark, holdout, costs, drawdown, and CONTINUE_RESEARCH decision before producing a ticket. |

## Topic 1 — From Trading Idea to Quality Market Data

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 1 | [Research an Idea and Freeze a Testable Hypothesis](lab-01-research-an-idea-and-freeze-a-testable-hypothesis.md) | Python 3.11+, OpenAI Agents SDK, trainer-approved OpenAI API key, Pydantic, scenario brief, approved source notes, text or JSON editor | C177-trading-agent-pack/01-hypothesis/ containing hypothesis_spec.json, research_log.md, agent_run_manifest.json, validation_report.json, and fingerprints.json for the frozen SPY 20/50-day moving-average hypothesis |
| 2 | [Fetch Market Data and Prove It Is Fit for Purpose](lab-02-fetch-market-data-and-prove-it-is-fit-for-purpose.md) | Alpaca Paper Only account, alpaca-py StockHistoricalDataClient, pandas, deterministic quality validator, OpenAI Agents SDK read-only artifact tool | C177-trading-agent-pack/02-market-data/ containing spy_daily.csv, market_data_contract.json, data_quality_report.json, data_agent_review.json, retrieval_manifest.json, and fingerprints.json |

## Topic 2 — The Six-Step Trading Workflow and Staying in Control

| # | Lab | Tools | You Build |
|---|-----|-------|-----------|
| 3 | [Backtest the Rules and Audit the Evidence](lab-03-backtest-the-rules-and-audit-the-evidence.md) | pandas, NumPy, Matplotlib, deterministic C177 backtest engine, OpenAI Agents SDK read-only artifact review, Markdown editor | C177-trading-agent-pack/03-backtest-audit/ containing strategy_spec.json, signal_sample.csv, trades.csv, equity_curve.csv, equity_curve.png, backtest_metrics.json, sensitivity_report.json, audit_log.md, backtest_agent_review.json, run_manifest.json, and fingerprints.json |
| 4 | [Size Risk, Approve, and Verify a Paper Trade](lab-04-size-risk-approve-and-verify-a-paper-trade.md) | Alpaca TradingClient in paper mode, deterministic C177 risk and order guardrails, OpenAI Agents SDK read-only ticket review, paper dashboard, text editor | C177-trading-agent-pack/04-paper-trade/ containing risk_calculation.json, paper_order_ticket.json, ticket_agent_review.json, human_approval.md, submission_attempt.json, a paper receipt or structured error, reconciliation_log.md, rollback_record.md, final_manifest.json, and fingerprints.json |

---

> Use only authorised accounts, placeholder or synthetic inputs, and paper-trading credentials. This course does not provide financial advice and includes no live-order path.


_Tertiary Infotech Academy Pte Ltd · C177 · v1.1 (4 October 2026)_
