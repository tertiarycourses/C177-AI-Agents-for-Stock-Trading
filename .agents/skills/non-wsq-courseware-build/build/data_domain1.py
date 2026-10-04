"""Connected labs for Topic 1 of AI Agents for Stock Trading (C177)."""

DOMAIN1 = [
    dict(
        num=1,
        topic=1,
        title="Research an Idea and Freeze a Testable Hypothesis",
        objective="LO1 and LO2: operate a bounded tool-using research agent and convert one trading idea into a cited, structured, falsifiable HYPER hypothesis",
        goal="Produce a schema-valid, cited HYPER hypothesis version 1.0 with zero unresolved fields and a verified fingerprint manifest.",
        duration="50 minutes",
        desc=(
            "Start the connected SPY research scenario by running an OpenAI Agents SDK research agent with read-only course-source tools and structured output. "
            "Separate evidence, assumptions, and unknowns; resolve the required human-owned fields; validate the schema; then freeze version 1.0 with fingerprints before any market data is fetched."
        ),
        build=(
            "C177-trading-agent-pack/01-hypothesis/ containing hypothesis_spec.json, research_log.md, agent_run_manifest.json, validation_report.json, and fingerprints.json for the frozen SPY 20/50-day moving-average hypothesis"
        ),
        services="Python 3.11+, OpenAI Agents SDK, trainer-approved OpenAI API key, Pydantic, scenario brief, approved source notes, text or JSON editor",
        prerequisites=[
            "Create and activate the repository virtual environment, install labs/resources/requirements.txt, and run labs/resources/preflight.py.",
            "Store OPENAI_API_KEY only in the local .env file or process environment; never paste it into a prompt, notebook, screenshot, or repository file.",
            "Read labs/resources/scenario_brief.md and labs/resources/research_sources.md before asking the agent to draft anything.",
            "Create an empty local folder named C177-trading-agent-pack; do not place real brokerage data or live credentials in it.",
        ],
        steps=[
            (
                "Create the Lab 1 output folder and run the preflight check. Continue only when Python and the required packages are ready; an absent OpenAI key must be resolved before the agent run.",
                "python labs/resources/workspace.py mkdir C177-trading-agent-pack/01-hypothesis\npython labs/resources/preflight.py --require openai",
            ),
            (
                "Read the scenario without AI. In research_log.md, record the fixed course scenario, the human owner, the paper-only boundary, and three questions the evidence must answer.",
                "python labs/resources/workspace.py show labs/resources/scenario_brief.md\npython labs/resources/workspace.py copy labs/resources/research_log_starter.md C177-trading-agent-pack/01-hypothesis/research_log.md",
            ),
            (
                "Generate a deterministic template first. This creates the expected field structure without calling a model, so you can distinguish schema problems from agent-output problems.",
                "python labs/resources/trading_research_agent.py draft --mode template --output C177-trading-agent-pack/01-hypothesis/template_hypothesis_spec.json",
            ),
            (
                "Run the bounded research agent. It may call only the supplied read-only source tools and must return the HypothesisSpec structured type; it has no market-data or order tool in this lab.",
                "python labs/resources/trading_research_agent.py draft --mode agent --output C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --manifest C177-trading-agent-pack/01-hypothesis/agent_run_manifest.json",
            ),
            (
                "Compare agent output with the template. Confirm symbol SPY, daily bars, fast window 20, slow window 50, long-only state, next-bar timing, benchmark, fixed date range, adjustment mode, friction, split date, and rejection criteria.",
                "python labs/resources/validate_hypothesis.py C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --compare C177-trading-agent-pack/01-hypothesis/template_hypothesis_spec.json",
            ),
            (
                "Resolve every OWNER_TO_VERIFY item from the scenario and approved sources. Do not silently replace an unknown with a model guess; record the source or human decision in research_log.md.",
                "python labs/resources/workspace.py locate C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json C177-trading-agent-pack/01-hypothesis/research_log.md",
            ),
            (
                "Validate the edited hypothesis and the complete research log. The report must show schema_valid true, unresolved_count 0, research_log_valid true, live_order_requested false, and status FROZEN_FOR_DATA before the next lab.",
                "python labs/resources/validate_hypothesis.py C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --research-log C177-trading-agent-pack/01-hypothesis/research_log.md --report C177-trading-agent-pack/01-hypothesis/validation_report.json",
            ),
            (
                "Audit the evidence table in research_log.md. For each material claim, record a URL, access date, exact scope, and limitation; label agent-written prose as a draft rather than a source.",
                "python labs/resources/workspace.py unresolved C177-trading-agent-pack/01-hypothesis/research_log.md",
            ),
            (
                "Run the strict frozen-state check, then freeze the Lab 1 checkpoint. Hash the hypothesis, log, manifest, and final validation report; the fingerprint file becomes the integrity reference for Lab 2.",
                "python labs/resources/validate_hypothesis.py C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --research-log C177-trading-agent-pack/01-hypothesis/research_log.md --report C177-trading-agent-pack/01-hypothesis/validation_report.json --require-frozen\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --output C177-trading-agent-pack/01-hypothesis/fingerprints.json\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json",
            ),
            (
                "Review the frozen pack with a partner without modifying it. Point to the exact field that defines signal timing, benchmark, friction, out-of-sample split, rejection criteria, paper-only boundary, and human owner; then verify the unchanged manifest again.",
                "python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json",
            ),
        ],
        deck_steps=[
            "Read the scenario and approved evidence boundary.",
            "Run the research agent with structured HYPER output.",
            "Resolve unknowns and validate every required field.",
            "Freeze version 1.0 and record fingerprints.",
        ],
        deck_verify="Show a frozen hypothesis with zero unresolved fields, an evidence log, and matching file fingerprints.",
        test=(
            "Run the final validator and fingerprint command. validation_report.json must contain schema_valid=true, unresolved_count=0, research_log_valid=true, research_log_errors=[], live_order_requested=false, status=FROZEN_FOR_DATA, and the expected SPY 20/50 daily rule fields. "
            "The log validator must confirm scenario, owner, three evidence questions, five complete source rows, assumptions, resolved unknowns, and the v1.0 UTC record. fingerprints.json must list hypothesis_spec.json, research_log.md, agent_run_manifest.json, and validation_report.json. A partner must be able to find the signal timing, benchmark, friction, split date, rejection criteria, paper-only boundary, and owner without reading the chat transcript."
        ),
        checkpoint=(
            "Keep the entire 01-hypothesis folder unchanged. Lab 2 verifies its fingerprints, fetches authorised SPY daily bars under the recorded data contract, and writes a separate 02-market-data checkpoint."
        ),
        troubleshooting=[
            ("The agent run reports a missing or invalid API key", "Stop. Confirm OPENAI_API_KEY exists in the local process or ignored .env file, then rerun preflight. Never print the key or place it in a command argument."),
            ("The agent changes the asset, windows, date range, or paper-only boundary", "Discard the draft, reread the scenario brief, and rerun with the supplied instructions. The model may structure the scenario; it may not redesign it."),
            ("Validation finds unresolved fields", "Open the exact JSON paths listed in validation_report.json, resolve them from an approved source or named human decision, and record that evidence in research_log.md."),
        ],
        challenge="Add a deliberately vague alternative idea to the research log, then write the minimum HYPER fields needed to make it testable without running another backtest.",
        reflection="Which field most effectively prevented a fluent trading story from becoming an untestable claim?",
    ),
    dict(
        num=2,
        topic=1,
        title="Fetch Market Data and Prove It Is Fit for Purpose",
        objective="LO3: connect the workflow to authorised Alpaca market data, record the data contract, run deterministic quality gates, and let the agent interpret only the verified report",
        goal="Produce an authorised SPY daily-bar dataset whose complete data contract, deterministic quality report, agent review, and SHA-256 fingerprint all agree.",
        duration="60 minutes",
        desc=(
            "Verify the frozen hypothesis, connect to Alpaca's historical stock-data client, fetch the declared SPY daily bars, and produce a source contract, CSV, quality report, and fingerprint. "
            "Then give the research agent read-only access to the structured quality report so it can recommend READY_FOR_BACKTEST or HOLD_DATA without changing any numeric observation."
        ),
        build=(
            "C177-trading-agent-pack/02-market-data/ containing spy_daily.csv, market_data_contract.json, data_quality_report.json, data_agent_review.json, retrieval_manifest.json, and fingerprints.json"
        ),
        services="Alpaca Paper Only account, alpaca-py StockHistoricalDataClient, pandas, deterministic quality validator, OpenAI Agents SDK read-only artifact tool",
        prerequisites=[
            "Lab 1 is frozen and C177-trading-agent-pack/01-hypothesis/fingerprints.json still matches its files.",
            "ALPACA_API_KEY and ALPACA_SECRET_KEY are stored only in the ignored .env file; ALPACA_PAPER_ONLY remains true.",
            "The account entitlement and intended feed are understood: the default course request uses the IEX feed and records its single-exchange scope.",
            "Internet access is available. The synthetic generator is a labelled rejoin fallback and must not be described as real market data.",
        ],
        steps=[
            (
                "Create the Lab 2 folder and recheck the Lab 1 fingerprints. Stop if any frozen file changed; restore it or create a documented new version before fetching data.",
                "python labs/resources/workspace.py mkdir C177-trading-agent-pack/02-market-data\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json",
            ),
            (
                "Run preflight for Alpaca credentials. The script checks presence and the paper-only flag without displaying secret values.",
                "python labs/resources/preflight.py --require alpaca",
            ),
            (
                "Fetch the exact symbol, dates, interval, adjustment, and feed from the frozen hypothesis. The tool writes raw observations before any agent is asked to interpret them.",
                "python labs/resources/fetch_validate_data.py --hypothesis C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --source alpaca --output-dir C177-trading-agent-pack/02-market-data",
            ),
            (
                "If the provider is unavailable during class, generate the labelled synthetic rejoin checkpoint in a separate folder. Never rename it to hide its source and do not combine it with the Alpaca run.",
                "python labs/resources/fetch_validate_data.py --hypothesis C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --source synthetic --output-dir C177-trading-agent-pack/02-market-data-rejoin",
            ),
            (
                "Inspect market_data_contract.json. Confirm provider, endpoint, feed, entitlement scope, symbol, interval, start, end, timezone, session, adjustment, retrieved_at_utc, intended_use, and CSV fingerprint.",
                "python -m json.tool C177-trading-agent-pack/02-market-data/market_data_contract.json",
            ),
            (
                "Inspect data_quality_report.json. Resolve every critical failure; distinguish an expected market closure from an unexplained long calendar gap, and record any accepted warning with its owner and scope.",
                "python -m json.tool C177-trading-agent-pack/02-market-data/data_quality_report.json",
            ),
            (
                "Spot-check the first three and last three rows. Verify ordered unique timestamps, numeric OHLCV fields, high at least open and close, low at most open and close, and non-negative volume.",
                "python labs/resources/inspect_market_data.py C177-trading-agent-pack/02-market-data/spy_daily.csv --head 3 --tail 3",
            ),
            (
                "Run the research agent in read-only data-review mode. It must cite check names and values from the quality report and must not invent a price, fill a gap, or rewrite the status.",
                "python labs/resources/trading_research_agent.py review-data --mode agent --pack C177-trading-agent-pack --output C177-trading-agent-pack/02-market-data/data_agent_review.json --manifest C177-trading-agent-pack/02-market-data/agent_review_manifest.json",
            ),
            (
                "Compare the agent review with the deterministic status. If they disagree, the deterministic report controls and the disagreement is recorded as an agent defect.",
                "python labs/resources/compare_review.py --report C177-trading-agent-pack/02-market-data/data_quality_report.json --review C177-trading-agent-pack/02-market-data/data_agent_review.json",
            ),
            (
                "Freeze the Lab 2 checkpoint and verify it immediately. Lab 3 must receive the exact CSV whose hash appears in both the contract and quality report.",
                "python labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --output C177-trading-agent-pack/02-market-data/fingerprints.json\npython labs/resources/fingerprint_pack.py C177-trading-agent-pack/02-market-data --verify C177-trading-agent-pack/02-market-data/fingerprints.json",
            ),
        ],
        deck_steps=[
            "Verify the frozen hypothesis and paper-only credential boundary.",
            "Fetch SPY bars under an explicit provider and feed contract.",
            "Run deterministic schema, chronology, OHLCV, coverage, and freshness gates.",
            "Compare the agent's review with the controlling quality report.",
        ],
        deck_verify="Show READY_FOR_BACKTEST in the deterministic report, a matching CSV fingerprint, and an agent review that cites the same evidence.",
        test=(
            "data_quality_report.json must show status READY_FOR_BACKTEST, critical_failures 0, duplicate_timestamps 0, missing_required_values 0, invalid_ohlc_rows 0, negative_volume_rows 0, and the same csv_sha256 recorded in market_data_contract.json. "
            "compare_review.py must report REVIEW_ALIGNED. fingerprints.json must verify every Lab 2 artifact. If you used the synthetic rejoin folder, the provider and intended_use fields must visibly identify it as synthetic and the real-data objective remains to be completed."
        ),
        checkpoint=(
            "Keep 02-market-data unchanged. Lab 3 verifies the CSV fingerprint, uses only the accepted dataset, and writes backtest outputs to a new 03-backtest-audit folder."
        ),
        troubleshooting=[
            ("The API returns an authentication or entitlement error", "Confirm you used paper-account API keys and the IEX feed. Do not switch to an undocumented endpoint or paste keys into the script. Use the labelled synthetic rejoin path while the trainer resolves access."),
            ("The quality report shows HOLD_DATA", "Open the critical_checks list, correct the source, date, schema, or corrupted file, and rerun from a clean Lab 2 folder. Never edit prices merely to make the gate green."),
            ("The agent calls the data ready while the report says HOLD_DATA", "Keep HOLD_DATA, record an agent-review defect, and rerun the agent after checking the supplied instructions and artifact path."),
        ],
        challenge="Fetch the same bounded date window from a second authorised feed or provider, record a separate contract, and explain why row counts, volume, or prices can differ without declaring either dataset automatically wrong.",
        reflection="Which market-data contract field would be easiest to omit and most damaging to a later interpretation?",
    ),
]
