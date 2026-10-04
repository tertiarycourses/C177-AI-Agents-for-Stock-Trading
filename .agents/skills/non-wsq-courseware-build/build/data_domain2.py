"""Connected labs for Topic 2 of AI Agents for Stock Trading (C177)."""

DOMAIN2 = [
    dict(
        num=3,
        topic=2,
        title="Backtest the Rules and Audit the Evidence",
        objective="LO4: run a causal deterministic backtest, compare a benchmark and holdout, stress stated assumptions, and record an auditable research decision",
        goal="Produce a reproducible causal backtest with benchmark, holdout, friction and parameter sensitivities, plus aligned deterministic, agent, and human audit decisions.",
        duration="65 minutes",
        desc=(
            "Verify the accepted hypothesis and market-data fingerprints, run the fixed 20/50-day crossover engine with a one-bar signal shift and declared frictions, then inspect trades, development and out-of-sample metrics, benchmark results, drawdown, and sensitivity checks. "
            "The agent receives only read-only report tools and drafts a review that the human auditor must reconcile with deterministic checks."
        ),
        build=(
            "C177-trading-agent-pack/03-backtest-audit/ containing strategy_spec.json, signal_sample.csv, trades.csv, equity_curve.csv, equity_curve.png, backtest_metrics.json, sensitivity_report.json, audit_log.md, backtest_agent_review.json, run_manifest.json, and fingerprints.json"
        ),
        services="pandas, NumPy, Matplotlib, deterministic C177 backtest engine, OpenAI Agents SDK read-only artifact review, Markdown editor",
        prerequisites=[
            "Lab 1 and Lab 2 fingerprints verify and the deterministic market-data status is READY_FOR_BACKTEST.",
            "The CSV hash matches both market_data_contract.json and data_quality_report.json.",
            "The hypothesis remains version 1.0; parameter or date changes require a separately documented version rather than an overwrite.",
            "The learner understands that historical and out-of-sample results do not guarantee future behaviour.",
        ],
        steps=[
            (
                "Create the Lab 3 folder and verify both upstream checkpoints. Stop on any mismatch instead of accepting a stale or edited input.",
                "python labs/resources/workspace.py mkdir C177-trading-agent-pack/03-backtest-audit\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --verify C177-trading-agent-pack/02-market-data/fingerprints.json",
            ),
            (
                "Run the deterministic engine from the frozen specification and accepted CSV. Do not ask the model to calculate returns, drawdown, Sharpe ratio, trades, or quantity.",
                "python labs/resources/backtest_and_audit.py --hypothesis C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --data C177-trading-agent-pack/02-market-data/spy_daily.csv --quality-report C177-trading-agent-pack/02-market-data/data_quality_report.json --output-dir C177-trading-agent-pack/03-backtest-audit",
            ),
            (
                "Inspect signal_sample.csv around at least one crossover. Confirm the raw signal is computed from completed bars, position_used is shifted by one row, and the same row's return never receives an unshifted signal.",
                "python labs/resources/inspect_signal_timing.py C177-trading-agent-pack/03-backtest-audit/signal_sample.csv",
            ),
            (
                "Read backtest_metrics.json as a system. Compare full, development, and out-of-sample strategy metrics with buy-and-hold; record trade count, total return, annualised return, volatility, Sharpe ratio, maximum drawdown, turnover, and benchmark gap.",
                "python -m json.tool C177-trading-agent-pack/03-backtest-audit/backtest_metrics.json",
            ),
            (
                "Open equity_curve.png and trades.csv. Find the largest drawdown period and inspect at least two entry-exit sequences; confirm the trade rows reconcile with changes in the position column.",
                "python labs/resources/workspace.py locate C177-trading-agent-pack/03-backtest-audit/equity_curve.png C177-trading-agent-pack/03-backtest-audit/trades.csv",
            ),
            (
                "Inspect sensitivity_report.json. Compare the declared friction case with zero and higher friction, then compare nearby 15/50 and 25/50 windows without selecting a new winner during this run.",
                "python -m json.tool C177-trading-agent-pack/03-backtest-audit/sensitivity_report.json",
            ),
            (
                "Complete the human audit log. Record leakage check, data lineage, trial count, benchmark, split date, cost assumptions, parameter stability, limitations, and a CONTINUE_RESEARCH, HOLD, or REVISE decision with reasons.",
                "python labs/resources/workspace.py copy labs/resources/backtest_audit_starter.md C177-trading-agent-pack/03-backtest-audit/audit_log.md\npython labs/resources/workspace.py locate C177-trading-agent-pack/03-backtest-audit/audit_log.md",
            ),
            (
                "Run the agent in read-only backtest-review mode. It must cite report paths and values, preserve the deterministic status, and name limitations instead of recommending a trade.",
                "python labs/resources/trading_research_agent.py review-backtest --mode agent --pack C177-trading-agent-pack --output C177-trading-agent-pack/03-backtest-audit/backtest_agent_review.json --manifest C177-trading-agent-pack/03-backtest-audit/agent_review_manifest.json",
            ),
            (
                "Reconcile human, agent, and deterministic decisions. A disagreement is documented; it is never resolved by rewriting metrics. Lab 4 is enabled only when the deterministic checks allow CONTINUE_RESEARCH and the human audit agrees.",
                "python labs/resources/compare_review.py --report C177-trading-agent-pack/03-backtest-audit/backtest_metrics.json --review C177-trading-agent-pack/03-backtest-audit/backtest_agent_review.json --human C177-trading-agent-pack/03-backtest-audit/audit_log.md",
            ),
            (
                "Freeze and verify the Lab 3 checkpoint. The audit decision permits only a bounded paper exercise; it is not a statement of expected return or suitability for live capital.",
                "python labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --output C177-trading-agent-pack/03-backtest-audit/fingerprints.json\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --verify C177-trading-agent-pack/03-backtest-audit/fingerprints.json",
            ),
        ],
        deck_steps=[
            "Verify frozen inputs and run the deterministic causal engine.",
            "Inspect signal timing, trades, segments, benchmark, and drawdown.",
            "Stress friction and nearby parameters without choosing a new winner.",
            "Reconcile deterministic, agent, and human audit decisions.",
        ],
        deck_verify="Show causal timing evidence, an out-of-sample benchmark comparison, visible sensitivity cases, and a signed research decision.",
        test=(
            "The run manifest must show matching hypothesis and data fingerprints. signal_sample.csv must demonstrate a one-row position shift. backtest_metrics.json must contain full, development, out_of_sample, and benchmark sections plus deterministic_status. "
            "sensitivity_report.json must include at least three friction cases and the 15/50, 20/50, and 25/50 parameter cases. compare_review.py must report the deterministic, agent, and human decisions explicitly. All Lab 3 fingerprints must verify."
        ),
        checkpoint=(
            "Keep the verified 03-backtest-audit folder. Lab 4 reads the accepted audit decision and latest data reference, calculates a bounded quantity, generates a dry-run ticket, and submits only after the explicit human paper-approval gate."
        ),
        troubleshooting=[
            ("The engine reports an input fingerprint mismatch", "Restore the exact frozen file or create a new version and rerun its upstream gate. Do not edit the manifest to match a changed file."),
            ("The signal-timing inspection shows the position was not shifted", "Stop the run, inspect the position_used construction, and rerun from a clean output folder. Any metrics from the biased run are invalid."),
            ("Out-of-sample evidence or friction sensitivity is weak", "Record HOLD or REVISE. Preserve the result; do not tune on the same holdout and then relabel it as untouched evidence."),
        ],
        challenge="Add a walk-forward report with at least three chronological windows while preserving the original v1.0 run and trial log; explain what the extra windows reveal and what they still cannot prove.",
        reflection="Which audit check changed your interpretation of the headline return most, and why?",
    ),
    dict(
        num=4,
        topic=2,
        title="Size Risk, Approve, and Verify a Paper Trade",
        objective="LO5 and LO6: calculate a bounded quantity, generate and review a paper-order ticket, apply the human gate, submit only to simulation, and verify or roll back the result",
        goal="Produce a bounded risk calculation and human-approved paper-order record whose ticket, receipt or clear error, reconciliation, rollback, secret scan, and fingerprints are verifiable.",
        duration="70 minutes",
        desc=(
            "Use the accepted research evidence to calculate quantity from a human-set paper risk budget, stop distance, exposure ceiling, buying power, and hard course cap. "
            "Generate a dry-run ticket, let the agent perform a read-only evidence review, obtain explicit human approval, submit through an Alpaca TradingClient constructed with paper=True, reconcile the receipt, and close with a secret-free final manifest."
        ),
        build=(
            "C177-trading-agent-pack/04-paper-trade/ containing risk_calculation.json, paper_order_ticket.json, ticket_agent_review.json, human_approval.md, submission_attempt.json, a paper receipt or structured error, reconciliation_log.md, rollback_record.md, final_manifest.json, and fingerprints.json"
        ),
        services="Alpaca TradingClient in paper mode, deterministic C177 risk and order guardrails, OpenAI Agents SDK read-only ticket review, paper dashboard, text editor",
        prerequisites=[
            "Lab 3 fingerprints verify, deterministic_status permits CONTINUE_RESEARCH, and the human audit explicitly permits only a bounded paper exercise.",
            "ALPACA_PAPER_ONLY=true and paper-account keys are present locally; no live credentials are available to the course script.",
            "The reviewer understands that a stop reference and paper fill do not guarantee a live loss bound or future performance.",
            "The paper account is suitable for the exercise and the course allowlist contains only SPY.",
        ],
        steps=[
            (
                "Create the Lab 4 folder and verify the Lab 3 checkpoint. Read the audit decision and stop immediately unless both the deterministic and human records permit a paper-only exercise.",
                "python labs/resources/workspace.py mkdir C177-trading-agent-pack/04-paper-trade\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/03-backtest-audit --verify C177-trading-agent-pack/03-backtest-audit/fingerprints.json\npython labs/resources/paper_trade.py check-gate --pack C177-trading-agent-pack",
            ),
            (
                "Generate the deterministic risk calculation and dry-run ticket. Use 0.50% paper-account risk, a 2% stop-distance exercise, a 10% exposure cap, and the course hard cap of 20 shares unless the trainer supplies smaller limits.",
                "python labs/resources/paper_trade.py prepare --pack C177-trading-agent-pack --risk-fraction 0.005 --stop-percent 0.02 --max-exposure-fraction 0.10 --hard-max-qty 20",
            ),
            (
                "Recompute the quantity manually from the displayed paper equity, entry reference, stop reference, risk budget, per-share risk, exposure cap, buying-power cap, and hard cap. Record the smallest active bound in human_approval.md.",
                "python labs/resources/workspace.py copy labs/resources/human_approval_starter.md C177-trading-agent-pack/04-paper-trade/human_approval.md\npython -m json.tool C177-trading-agent-pack/04-paper-trade/risk_calculation.json",
            ),
            (
                "Inspect paper_order_ticket.json. Confirm environment PAPER, symbol SPY, side BUY, positive quantity no greater than 20, order type MARKET, time in force DAY, unique client_order_id, evidence fingerprints, and submission_enabled false.",
                "python -m json.tool C177-trading-agent-pack/04-paper-trade/paper_order_ticket.json",
            ),
            (
                "Run the agent in read-only ticket-review mode. It may cite evidence and missing conditions; it cannot change quantity, enable submission, enter approval, call Alpaca, or recommend live use.",
                "python labs/resources/trading_research_agent.py review-ticket --mode agent --pack C177-trading-agent-pack --output C177-trading-agent-pack/04-paper-trade/ticket_agent_review.json --manifest C177-trading-agent-pack/04-paper-trade/agent_review_manifest.json",
            ),
            (
                "Complete the human review. Enter reviewer initials, UTC time, paper environment, exact quantity, active cap, evidence decision, and APPROVE_PAPER_EXERCISE or HOLD. Do not store an API key or the command approval token in this file.",
                "python labs/resources/workspace.py locate C177-trading-agent-pack/04-paper-trade/human_approval.md",
            ),
            (
                "Preview the exact request without submitting. The output must say DRY_RUN, show the paper endpoint, and refuse if any gate is missing.",
                "python labs/resources/paper_trade.py submit --pack C177-trading-agent-pack --dry-run",
            ),
            (
                "After the reviewer authorises the exercise, submit once with the exact ephemeral approval token. The script constructs TradingClient(..., paper=True), verifies the paper account, uses the saved client_order_id, and writes the receipt without secrets.",
                "python labs/resources/paper_trade.py submit --pack C177-trading-agent-pack --approve C177-PAPER-APPROVED",
            ),
            (
                "Verify the returned order through the API and paper dashboard. Record order ID, client order ID, symbol, side, quantity, status, submitted time, and any fill information in the receipt and reconciliation log.",
                "python labs/resources/paper_trade.py verify --pack C177-trading-agent-pack",
            ),
            (
                "Test idempotency by rerunning the dry run. It must find the existing client_order_id or receipt and refuse to create a duplicate submission.",
                "python labs/resources/paper_trade.py submit --pack C177-trading-agent-pack --dry-run",
            ),
            (
                "If the exercise order remains open, request cancellation and let the script poll for a bounded time until the API confirms a terminal state. A still-open status remains on HOLD. If it filled, inspect or close the exercise position under trainer direction, then rerun rollback with --confirm-position-reviewed so the resolved state is explicit.",
                "python labs/resources/paper_trade.py rollback --pack C177-trading-agent-pack",
            ),
            (
                "Build the final manifest, scan for secret-shaped strings, freeze the folder, and verify every artifact. Any secret hit must be removed and the affected paper key rotated before sharing.",
                "python labs/resources/finalise_pack.py C177-trading-agent-pack\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/04-paper-trade --output C177-trading-agent-pack/04-paper-trade/fingerprints.json\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/04-paper-trade --verify C177-trading-agent-pack/04-paper-trade/fingerprints.json",
            ),
        ],
        deck_steps=[
            "Generate a bounded quantity and dry-run paper ticket.",
            "Recompute the active cap and complete human review.",
            "Submit once to the hard-wired paper client with a unique ID.",
            "Verify, reconcile, roll back, scan secrets, and freeze evidence.",
        ],
        deck_verify="Show a bounded calculation, human-approved PAPER ticket, reconciled paper receipt, rollback state, secret-free manifest, and verified fingerprints.",
        test=(
            "risk_calculation.json must show every formula input and the final quantity as the minimum applicable cap. paper_order_ticket.json must show environment PAPER, symbol SPY, quantity at most 20, submission_enabled false before approval, and a unique client_order_id. "
            "submission_attempt.json must exist before a real API call. paper_order_receipt.json must reconcile the same client order ID, or paper_submission_error.json plus reconciliation_log.md must confirm that no order exists without fabricating success. rollback_record.md must show Resolved YES. final_manifest.json must report secret_hits 0, no release defects, and verified checkpoints from all four labs."
        ),
        checkpoint=(
            "Retain the complete C177-trading-agent-pack as a paper-only research record. Rerun all six gates whenever the hypothesis, prompt, model, source, feed, data, code, risk limit, account, or provider changes."
        ),
        troubleshooting=[
            ("The gate checker refuses to prepare a ticket", "Read the exact missing decision or fingerprint path. Restore and verify the upstream evidence; never edit the checker or ticket to bypass the gate."),
            ("The submit command reports an uncertain timeout", "Do not submit again. The saved submission_attempt.json contains the client_order_id. Run verify; it queries that exact ID and records a receipt, CONFIRMED_NO_ORDER result, or unresolved reconciliation before any further action."),
            ("A secret scan reports a possible key", "Stop sharing, remove the value from every artifact and git history if needed, rotate the affected paper key, then rerun the scan and fingerprints."),
        ],
        challenge="Add a trainer-approved limit-order dry-run path with a maximum ticket age, price-deviation check, and cancellation timeout while preserving the paper-only endpoint and human gate.",
        reflection="Which control would still protect the paper account if the model produced a confident but incorrect recommendation?",
    ),
]
