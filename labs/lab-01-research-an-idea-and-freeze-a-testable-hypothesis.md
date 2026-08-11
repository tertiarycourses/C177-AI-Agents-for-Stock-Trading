# Lab 1 — Research an Idea and Freeze a Testable Hypothesis

- **Course:** AI Agents for Trading (C177)
- **Version:** v1.0 (11 August 2026)
- **Topic 1:** From Trading Idea to Quality Market Data
- **Maps to:** LO1 and LO2: operate a bounded tool-using research agent and convert one trading idea into a cited, structured, falsifiable HYPER hypothesis
- **Tools:** Python 3.11+, OpenAI Agents SDK, trainer-approved OpenAI API key, Pydantic, scenario brief, approved source notes, text or JSON editor

**Duration:** 50 minutes

---

## Goal

Produce a schema-valid, cited HYPER hypothesis version 1.0 with zero unresolved fields and a verified fingerprint manifest.

## What You Will Do

Start the connected SPY research scenario by running an OpenAI Agents SDK research agent with read-only course-source tools and structured output. Separate evidence, assumptions, and unknowns; resolve the required human-owned fields; validate the schema; then freeze version 1.0 with fingerprints before any market data is fetched.

## What You Will Build

C177-trading-agent-pack/01-hypothesis/ containing hypothesis_spec.json, research_log.md, agent_run_manifest.json, validation_report.json, and fingerprints.json for the frozen SPY 20/50-day moving-average hypothesis

## Prerequisites

- Create and activate the repository virtual environment, install labs/resources/requirements.txt, and run labs/resources/preflight.py.
- Store OPENAI_API_KEY only in the local .env file or process environment; never paste it into a prompt, notebook, screenshot, or repository file.
- Read labs/resources/scenario_brief.md and labs/resources/research_sources.md before asking the agent to draft anything.
- Create an empty local folder named C177-trading-agent-pack; do not place real brokerage data or live credentials in it.

> **Data note.** Use only authorised accounts, placeholder or synthetic inputs, and paper-trading credentials. This course does not provide financial advice and includes no live-order path.

## Steps

**1. Create the Lab 1 output folder and run the preflight check. Continue only when Python and the required packages are ready; an absent OpenAI key must be resolved before the agent run.**

```text
python labs/resources/workspace.py mkdir C177-trading-agent-pack/01-hypothesis
python labs/resources/preflight.py --require openai
```

**2. Read the scenario without AI. In research_log.md, record the fixed course scenario, the human owner, the paper-only boundary, and three questions the evidence must answer.**

```text
python labs/resources/workspace.py show labs/resources/scenario_brief.md
python labs/resources/workspace.py copy labs/resources/research_log_starter.md C177-trading-agent-pack/01-hypothesis/research_log.md
```

**3. Generate a deterministic template first. This creates the expected field structure without calling a model, so you can distinguish schema problems from agent-output problems.**

```text
python labs/resources/trading_research_agent.py draft --mode template --output C177-trading-agent-pack/01-hypothesis/template_hypothesis_spec.json
```

**4. Run the bounded research agent. It may call only the supplied read-only source tools and must return the HypothesisSpec structured type; it has no market-data or order tool in this lab.**

```text
python labs/resources/trading_research_agent.py draft --mode agent --output C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --manifest C177-trading-agent-pack/01-hypothesis/agent_run_manifest.json
```

**5. Compare agent output with the template. Confirm symbol SPY, daily bars, fast window 20, slow window 50, long-only state, next-bar timing, benchmark, fixed date range, adjustment mode, friction, split date, and rejection criteria.**

```text
python labs/resources/validate_hypothesis.py C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --compare C177-trading-agent-pack/01-hypothesis/template_hypothesis_spec.json
```

**6. Resolve every OWNER_TO_VERIFY item from the scenario and approved sources. Do not silently replace an unknown with a model guess; record the source or human decision in research_log.md.**

```text
python labs/resources/workspace.py locate C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json C177-trading-agent-pack/01-hypothesis/research_log.md
```

**7. Validate the edited hypothesis and the complete research log. The report must show schema_valid true, unresolved_count 0, research_log_valid true, live_order_requested false, and status FROZEN_FOR_DATA before the next lab.**

```text
python labs/resources/validate_hypothesis.py C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --research-log C177-trading-agent-pack/01-hypothesis/research_log.md --report C177-trading-agent-pack/01-hypothesis/validation_report.json
```

**8. Audit the evidence table in research_log.md. For each material claim, record a URL, access date, exact scope, and limitation; label agent-written prose as a draft rather than a source.**

```text
python labs/resources/workspace.py unresolved C177-trading-agent-pack/01-hypothesis/research_log.md
```

**9. Run the strict frozen-state check, then freeze the Lab 1 checkpoint. Hash the hypothesis, log, manifest, and final validation report; the fingerprint file becomes the integrity reference for Lab 2.**

```text
python labs/resources/validate_hypothesis.py C177-trading-agent-pack/01-hypothesis/hypothesis_spec.json --research-log C177-trading-agent-pack/01-hypothesis/research_log.md --report C177-trading-agent-pack/01-hypothesis/validation_report.json --require-frozen
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --output C177-trading-agent-pack/01-hypothesis/fingerprints.json
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
```

**10. Review the frozen pack with a partner without modifying it. Point to the exact field that defines signal timing, benchmark, friction, out-of-sample split, rejection criteria, paper-only boundary, and human owner; then verify the unchanged manifest again.**

```text
python labs/resources/fingerprint_pack.py C177-trading-agent-pack/01-hypothesis --verify C177-trading-agent-pack/01-hypothesis/fingerprints.json
```

## Test It

Run the final validator and fingerprint command. validation_report.json must contain schema_valid=true, unresolved_count=0, research_log_valid=true, research_log_errors=[], live_order_requested=false, status=FROZEN_FOR_DATA, and the expected SPY 20/50 daily rule fields. The log validator must confirm scenario, owner, three evidence questions, five complete source rows, assumptions, resolved unknowns, and the v1.0 UTC record. fingerprints.json must list hypothesis_spec.json, research_log.md, agent_run_manifest.json, and validation_report.json. A partner must be able to find the signal timing, benchmark, friction, split date, rejection criteria, paper-only boundary, and owner without reading the chat transcript.

## Checkpoint for the Next Lab

Keep the entire 01-hypothesis folder unchanged. Lab 2 verifies its fingerprints, fetches authorised SPY daily bars under the recorded data contract, and writes a separate 02-market-data checkpoint.

## Troubleshooting

- **The agent run reports a missing or invalid API key:** Stop. Confirm OPENAI_API_KEY exists in the local process or ignored .env file, then rerun preflight. Never print the key or place it in a command argument.
- **The agent changes the asset, windows, date range, or paper-only boundary:** Discard the draft, reread the scenario brief, and rerun with the supplied instructions. The model may structure the scenario; it may not redesign it.
- **Validation finds unresolved fields:** Open the exact JSON paths listed in validation_report.json, resolve them from an approved source or named human decision, and record that evidence in research_log.md.

## Challenge

Add a deliberately vague alternative idea to the research log, then write the minimum HYPER fields needed to make it testable without running another backtest.

## Reflection

Which field most effectively prevented a fluent trading story from becoming an untestable claim?

---

[← Labs index](README.md) · [Lab 2 →](lab-02-fetch-market-data-and-prove-it-is-fit-for-purpose.md)
