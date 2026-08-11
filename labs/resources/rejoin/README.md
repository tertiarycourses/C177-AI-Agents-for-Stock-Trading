# C177 Verified Rejoin Checkpoints

These trainer-supplied files let a learner rejoin a connected activity after an upstream API or credential problem. The market data is deterministic **synthetic training data**, not market evidence. Rejoining restores the software and evidence-control exercise; it does not satisfy the authorised-real-data objective in Lab 2.

Run commands from the repository root. Copy only into a new or empty `C177-trading-agent-pack`; the helper refuses to overwrite an existing destination.

## Before Lab 2

```text
python labs/resources/workspace.py copytree labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis C177-trading-agent-pack/01-hypothesis
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
```

## Before Lab 3

```text
python labs/resources/workspace.py copytree labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis C177-trading-agent-pack/01-hypothesis
python labs/resources/workspace.py copytree labs/resources/rejoin/C177-trading-agent-pack/02-market-data C177-trading-agent-pack/02-market-data
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --verify C177-trading-agent-pack/02-market-data/fingerprints.json
python -m json.tool C177-trading-agent-pack/02-market-data/data_quality_report.json
```

## Before Lab 4

```text
python labs/resources/workspace.py copytree labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis C177-trading-agent-pack/01-hypothesis
python labs/resources/workspace.py copytree labs/resources/rejoin/C177-trading-agent-pack/02-market-data C177-trading-agent-pack/02-market-data
python labs/resources/workspace.py copytree labs/resources/rejoin/C177-trading-agent-pack/03-backtest-audit C177-trading-agent-pack/03-backtest-audit
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --verify C177-trading-agent-pack/02-market-data/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --verify C177-trading-agent-pack/03-backtest-audit/fingerprints.json
python labs/resources/compare_review.py --report C177-trading-agent-pack/03-backtest-audit/backtest_metrics.json --review C177-trading-agent-pack/03-backtest-audit/backtest_agent_review.json --human C177-trading-agent-pack/03-backtest-audit/audit_log.md
python labs/resources/paper_trade.py check-gate --pack C177-trading-agent-pack
```

If a destination already exists, preserve it and choose a new pack folder. Never merge a rejoin checkpoint into partially changed evidence and regenerate fingerprints just to force a pass.
