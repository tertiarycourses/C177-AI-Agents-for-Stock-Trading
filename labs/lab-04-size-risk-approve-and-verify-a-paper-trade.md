# Lab 4 — Size Risk, Approve, and Verify a Paper Trade

- **Course:** AI Agents for Stock Trading (C177)
- **Version:** v1.1 (4 October 2026)
- **Topic 2:** The Six-Step Trading Workflow and Staying in Control
- **Maps to:** LO5 and LO6: calculate a bounded quantity, generate and review a paper-order ticket, apply the human gate, submit only to simulation, and verify or roll back the result
- **Tools:** Alpaca TradingClient in paper mode, deterministic C177 risk and order guardrails, OpenAI Agents SDK read-only ticket review, paper dashboard, text editor

**Duration:** 70 minutes

---

## Goal

Produce a bounded risk calculation and human-approved paper-order record whose ticket, receipt or clear error, reconciliation, rollback, secret scan, and fingerprints are verifiable.

## What You Will Do

Use the accepted research evidence to calculate quantity from a human-set paper risk budget, stop distance, exposure ceiling, buying power, and hard course cap. Generate a dry-run ticket, let the agent perform a read-only evidence review, obtain explicit human approval, submit through an Alpaca TradingClient constructed with paper=True, reconcile the receipt, and close with a secret-free final manifest.

## What You Will Build

C177-trading-agent-pack/04-paper-trade/ containing risk_calculation.json, paper_order_ticket.json, ticket_agent_review.json, human_approval.md, submission_attempt.json, a paper receipt or structured error, reconciliation_log.md, rollback_record.md, final_manifest.json, and fingerprints.json

## Prerequisites

- Lab 3 fingerprints verify, deterministic_status permits CONTINUE_RESEARCH, and the human audit explicitly permits only a bounded paper exercise.
- ALPACA_PAPER_ONLY=true and paper-account keys are present locally; no live credentials are available to the course script.
- The reviewer understands that a stop reference and paper fill do not guarantee a live loss bound or future performance.
- The paper account is suitable for the exercise and the course allowlist contains only SPY.

> **Rejoin path.** If a prerequisite artifact is missing, use the Rejoin Path in [the labs index](README.md), reconstruct the named checkpoint, and verify it before continuing.

> **Data note.** Use only authorised accounts, placeholder or synthetic inputs, and paper-trading credentials. This course does not provide financial advice and includes no live-order path.

## Steps

**1. Create the Lab 4 folder and verify the Lab 3 checkpoint. Read the audit decision and stop immediately unless both the deterministic and human records permit a paper-only exercise.**

```text
python labs/resources/workspace.py mkdir C177-trading-agent-pack/04-paper-trade
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --verify C177-trading-agent-pack/03-backtest-audit/fingerprints.json
python labs/resources/paper_trade.py check-gate --pack C177-trading-agent-pack
```

**2. Generate the deterministic risk calculation and dry-run ticket. Use 0.50% paper-account risk, a 2% stop-distance exercise, a 10% exposure cap, and the course hard cap of 20 shares unless the trainer supplies smaller limits.**

```text
python labs/resources/paper_trade.py prepare --pack C177-trading-agent-pack --risk-fraction 0.005 --stop-percent 0.02 --max-exposure-fraction 0.10 --hard-max-qty 20
```

**3. Recompute the quantity manually from the displayed paper equity, entry reference, stop reference, risk budget, per-share risk, exposure cap, buying-power cap, and hard cap. Record the smallest active bound in human_approval.md.**

```text
python labs/resources/workspace.py copy labs/resources/human_approval_starter.md C177-trading-agent-pack/04-paper-trade/human_approval.md
python -m json.tool C177-trading-agent-pack/04-paper-trade/risk_calculation.json
```

**4. Inspect paper_order_ticket.json. Confirm environment PAPER, symbol SPY, side BUY, positive quantity no greater than 20, order type MARKET, time in force DAY, unique client_order_id, evidence fingerprints, and submission_enabled false.**

```text
python -m json.tool C177-trading-agent-pack/04-paper-trade/paper_order_ticket.json
```

**5. Run the agent in read-only ticket-review mode. It may cite evidence and missing conditions; it cannot change quantity, enable submission, enter approval, call Alpaca, or recommend live use.**

```text
python labs/resources/trading_research_agent.py review-ticket --mode agent --pack C177-trading-agent-pack --output C177-trading-agent-pack/04-paper-trade/ticket_agent_review.json --manifest C177-trading-agent-pack/04-paper-trade/agent_review_manifest.json
```

**6. Complete the human review. Enter reviewer initials, UTC time, paper environment, exact quantity, active cap, evidence decision, and APPROVE_PAPER_EXERCISE or HOLD. Do not store an API key or the command approval token in this file.**

```text
python labs/resources/workspace.py locate C177-trading-agent-pack/04-paper-trade/human_approval.md
```

**7. Preview the exact request without submitting. The output must say DRY_RUN, show the paper endpoint, and refuse if any gate is missing.**

```text
python labs/resources/paper_trade.py submit --pack C177-trading-agent-pack --dry-run
```

**8. After the reviewer authorises the exercise, submit once with the exact ephemeral approval token. The script constructs TradingClient(..., paper=True), verifies the paper account, uses the saved client_order_id, and writes the receipt without secrets.**

```text
python labs/resources/paper_trade.py submit --pack C177-trading-agent-pack --approve C177-PAPER-APPROVED
```

**9. Verify the returned order through the API and paper dashboard. Record order ID, client order ID, symbol, side, quantity, status, submitted time, and any fill information in the receipt and reconciliation log.**

```text
python labs/resources/paper_trade.py verify --pack C177-trading-agent-pack
```

**10. Test idempotency by rerunning the dry run. It must find the existing client_order_id or receipt and refuse to create a duplicate submission.**

```text
python labs/resources/paper_trade.py submit --pack C177-trading-agent-pack --dry-run
```

**11. If the exercise order remains open, request cancellation and let the script poll for a bounded time until the API confirms a terminal state. A still-open status remains on HOLD. If it filled, inspect or close the exercise position under trainer direction, then rerun rollback with --confirm-position-reviewed so the resolved state is explicit.**

```text
python labs/resources/paper_trade.py rollback --pack C177-trading-agent-pack
```

**12. Build the final manifest, scan for secret-shaped strings, freeze the folder, and verify every artifact. Any secret hit must be removed and the affected paper key rotated before sharing.**

```text
python labs/resources/finalise_pack.py C177-trading-agent-pack
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/04-paper-trade --output C177-trading-agent-pack/04-paper-trade/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/04-paper-trade --verify C177-trading-agent-pack/04-paper-trade/fingerprints.json
```

## Test It

risk_calculation.json must show every formula input and the final quantity as the minimum applicable cap. paper_order_ticket.json must show environment PAPER, symbol SPY, quantity at most 20, submission_enabled false before approval, and a unique client_order_id. submission_attempt.json must exist before a real API call. paper_order_receipt.json must reconcile the same client order ID, or paper_submission_error.json plus reconciliation_log.md must confirm that no order exists without fabricating success. rollback_record.md must show Resolved YES. final_manifest.json must report secret_hits 0, no release defects, and verified checkpoints from all four labs.

## Checkpoint for the Next Lab

Retain the complete C177-trading-agent-pack as a paper-only research record. Rerun all six gates whenever the hypothesis, prompt, model, source, feed, data, code, risk limit, account, or provider changes.

## Troubleshooting

- **The gate checker refuses to prepare a ticket:** Read the exact missing decision or fingerprint path. Restore and verify the upstream evidence; never edit the checker or ticket to bypass the gate.
- **The submit command reports an uncertain timeout:** Do not submit again. The saved submission_attempt.json contains the client_order_id. Run verify; it queries that exact ID and records a receipt, CONFIRMED_NO_ORDER result, or unresolved reconciliation before any further action.
- **A secret scan reports a possible key:** Stop sharing, remove the value from every artifact and git history if needed, rotate the affected paper key, then rerun the scan and fingerprints.

## Challenge

Add a trainer-approved limit-order dry-run path with a maximum ticket age, price-deviation check, and cancellation timeout while preserving the paper-only endpoint and human gate.

## Reflection

Which control would still protect the paper account if the model produced a confident but incorrect recommendation?

---

[← Lab 3](lab-03-backtest-the-rules-and-audit-the-evidence.md) · [Labs index →](README.md)
