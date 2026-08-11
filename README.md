<div align="center">

# AI Agents for Trading

[![Course](https://img.shields.io/badge/Course-C177-1f6feb?style=for-the-badge)](https://www.tertiarycourses.com.sg/ai-agents-for-trading.html)
[![Agents SDK](https://img.shields.io/badge/Agent-OpenAI_Agents_SDK-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.github.io/openai-agents-python/)
[![Market Data](https://img.shields.io/badge/Market_Data-Alpaca-fbbf24?style=for-the-badge)](https://docs.alpaca.markets/us/docs/about-market-data-api)
[![Execution](https://img.shields.io/badge/Execution-Paper_Only-34d399?style=for-the-badge)](#safety-boundary)
[![Labs](https://img.shields.io/badge/Connected_Labs-4-7c3aed?style=for-the-badge)](#lab-activities)

**Aligned courseware and connected Python labs for directing a bounded AI agent through hypothesis design, market-data validation, causal backtesting, evidence audit, risk sizing, and a human-approved paper trade.**

[Course Page](https://www.tertiarycourses.com.sg/ai-agents-for-trading.html) · [Learner Guide](LG-AI%20Agents%20for%20Trading%20%28C177%29.md) · [Report Bug](https://github.com/tertiarycourses/C177-AI-Agents-for-Trading/issues) · [Request Improvement](https://github.com/tertiarycourses/C177-AI-Agents-for-Trading/issues)

</div>

> [!NOTE]
> These are the official courseware and hands-on lab materials for **AI Agents for Trading**.
> **Course Code:** `C177` · **Duration:** 1 day / 7.5 instructional hours · by Tertiary Courses / Tertiary Infotech
> **Course page:** https://www.tertiarycourses.com.sg/ai-agents-for-trading.html

---

## Lab Activities

**Lab 1 - Research an Idea and Freeze a Testable Hypothesis** · Run a bounded tool-using agent, separate evidence from assumptions, validate the HYPER structure, and freeze a cited SPY 20/50-day research specification.

**Lab 2 - Fetch Market Data and Prove It Is Fit for Purpose** · Retrieve authorised daily bars under an explicit provider/feed contract, run deterministic lineage and OHLCV gates, and compare the agent's review with the controlling quality report.

**Lab 3 - Backtest the Rules and Audit the Evidence** · Apply a one-bar signal shift, declared frictions, a buy-and-hold benchmark, a chronological holdout, and sensitivity cases; then reconcile deterministic, agent, and human decisions.

**Lab 4 - Size Risk, Approve, and Verify a Paper Trade** · Calculate the smallest bounded quantity, review a dry-run ticket, apply an explicit human gate, submit once to the hard-wired paper client, reconcile the receipt, and record rollback.

---

## About

This repository contains the complete, aligned learning package for **AI Agents for Trading** (`C177`) by Tertiary Courses / Tertiary Infotech: trainer slides, learner slides, Learner Guide, Lesson Plan, detailed Markdown labs, source notes, and executable Python resources.

The course treats an AI trading agent as a controlled research system rather than an autonomous money manager. The model may organise evidence, choose among narrow read-only tools, and explain structured observations. Deterministic Python owns schemas, data checks, fingerprints, signals, returns, friction, metrics, risk quantity, and submission limits. A human owns every consequential decision.

All four labs use one fictional **Northstar SPY Research Pack**. Learners build one `C177-trading-agent-pack`, so each verified output becomes an input to the next lab. The deliberately simple moving-average rule keeps attention on the real course skills: testability, market-data lineage, causal timing, auditability, risk limits, paper operations, and the verify-then-trust habit.

### What you'll learn

| # | Activity | Core concepts |
|---|---|---|
| **1** | **HYPER Hypothesis** | Bounded agency, evidence hierarchy, structured output, falsifiability, version freeze |
| **2** | **Quality Market Data** | Feed coverage, timestamps, adjustments, schema, OHLCV consistency, provenance, fingerprint |
| **3** | **Backtest and Audit** | One-bar shift, benchmark, holdout, drawdown, friction, overfitting, sensitivity, research decision |
| **4** | **Controlled Paper Trade** | Risk budget, stop distance, exposure cap, human approval, idempotency, receipt, rollback |

> **Full walkthrough:** start with the generated root Learner Guide. Slides, the formatted Learner Guide, and the Lesson Plan are in [`courseware/`](courseware/); the executable activity sequence is in [`labs/`](labs/).

---

## Tool Stack

| Category | Technology or resource |
|---|---|
| **Agent runtime** | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) with structured Pydantic output and narrow function tools |
| **Current model default** | `gpt-5.6-sol`, configurable with `OPENAI_MODEL`; recheck official model guidance before delivery |
| **Market data** | [Alpaca-py](https://alpaca.markets/sdks/python/) historical stock client with an explicit IEX feed contract |
| **Paper operations** | Alpaca `TradingClient(..., paper=True)`; SPY allowlist, quantity cap, dry run, approval token, unique client order ID |
| **Quantitative core** | Python 3.11+, pandas, NumPy, Matplotlib |
| **Evidence** | JSON schemas, CSVs, Markdown logs, SHA-256 fingerprints, metrics, sensitivity reports, charts, and paper receipts |
| **Courseware** | PowerPoint/PDF slides, Learner Guide, Lesson Plan, Markdown labs, and locally imported single-source build skill |

---

## Architecture

```text
DEFINE
  Lab 1  Scenario + approved sources
          -> read-only research agent
          -> structured HYPER hypothesis
          -> human resolution + schema + fingerprints

VALIDATE
  Lab 2  Frozen hypothesis
          -> Alpaca historical-data tool
          -> data contract + OHLCV gates + CSV fingerprint
          -> read-only agent review compared with deterministic status

BACKTEST
  Lab 3  Accepted CSV + frozen rules
          -> one-bar shift + friction + benchmark + holdout
          -> trades + metrics + chart + sensitivity
          -> deterministic decision + agent review + human audit

CONTROL
  Lab 4  Accepted audit + latest data reference
          -> risk budget / stop / exposure / buying-power / hard caps
          -> dry-run PAPER ticket -> human approval
          -> submit once -> verify -> reconcile -> rollback

CONNECTED EVIDENCE
  01 hypothesis -> 02 market data -> 03 backtest audit -> 04 paper record
```

---

## Safety Boundary

- Educational research only; no return, suitability, or performance promise.
- No live-order mode, live endpoint flag, or live-credential instructions.
- `TradingClient` is constructed with `paper=True` in the only submission path.
- SPY is the only allowed symbol and the course hard cap is 20 shares.
- Submission is disabled by default and needs a reviewed ticket plus an ephemeral human approval token.
- A unique client order ID is reconciled before any retry.
- Secrets remain in the ignored local `.env` file and the final pack is scanned for secret-shaped strings.
- Historical results and paper fills do not guarantee live execution or future behaviour.

---

## Project Structure

```text
C177-AI-Agents-for-Trading/
├── README.md
├── LG-AI Agents for Trading (C177).md
├── .agents/skills/non-wsq-courseware-build/
│   └── build/                         # one source for PPT, LG, LP, and labs
├── courseware/
│   ├── AI Agents for Trading (C177)-v1.0.pptx
│   ├── AI Agents for Trading (C177)-v1.0.pdf
│   ├── LG-AI Agents for Trading (C177).docx
│   ├── LG-AI Agents for Trading (C177).pdf
│   ├── LP-AI Agents for Trading (C177).docx
│   └── LP-AI Agents for Trading (C177).pdf
├── labs/
│   ├── README.md
│   ├── lab-01-research-an-idea-and-freeze-a-testable-hypothesis.md
│   ├── lab-02-fetch-market-data-and-prove-it-is-fit-for-purpose.md
│   ├── lab-03-backtest-the-rules-and-audit-the-evidence.md
│   ├── lab-04-size-risk-approve-and-verify-a-paper-trade.md
│   └── resources/                     # scripts, starters, sources, and verified synthetic rejoin checkpoints
└── reference/
    └── SOURCES.md
```

---

## Getting Started

### Prerequisites

- A Windows or Mac laptop with Python 3.11 or newer, Visual Studio Code or Google Colab, and a modern browser
- An OpenAI API key or trainer-provided approved equivalent for the agent runs
- An Alpaca Paper Only account and paper API keys
- Internet access for authorised API calls and current official documentation

Keep every credential in the ignored local `.env` file. Never paste a key into a prompt, notebook, screenshot, generated artifact, or repository file.

### 1. Clone the repository

```bash
git clone https://github.com/tertiarycourses/C177-AI-Agents-for-Trading.git
cd C177-AI-Agents-for-Trading
```

### 2. Create the lab environment

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux:       source .venv/bin/activate
python -m pip install -r labs/resources/requirements.txt
```

Copy `labs/resources/.env.example` to `.env`, replace placeholders locally, keep `ALPACA_PAPER_ONLY=true`, and run:

```bash
python labs/resources/preflight.py --require all
```

### 3. Start with the Learner Guide

Open **LG-AI Agents for Trading (C177).md** for the concept chapters, preparation guidance, and complete connected activity instructions.

### 4. Complete the labs in order

1. Read [`labs/README.md`](labs/README.md).
2. Create a local folder named `C177-trading-agent-pack`.
3. Complete Labs 1 to 4 in sequence.
4. Stop whenever a deterministic gate reports `HOLD`.
5. Use the labelled synthetic path only to rejoin or test software; do not describe it as market evidence.
6. Keep all execution paper-only.

If an upstream credential or API issue blocks the sequence, use the exact copy-and-verify commands in [`labs/resources/rejoin/README.md`](labs/resources/rejoin/README.md). Those checkpoints restore the learning workflow with visibly labelled synthetic data; they do not replace the authorised-real-data objective.

---

## Contributing

Contributions, corrections, and improvements are welcome:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-improvement`.
3. Commit your changes: `git commit -m "Add my improvement"`.
4. Push the branch: `git push origin feature/my-improvement`.
5. Open a pull request.

Found a bug or have an idea? Open an [issue](https://github.com/tertiarycourses/C177-AI-Agents-for-Trading/issues).

---

## License

This material is provided for **educational use** as part of **AI Agents for Trading (C177)**. © Tertiary Infotech Pte. Ltd. All rights reserved.

---

## Developed By

**Tertiary Infotech Pte. Ltd.** - [Tertiary Courses](https://www.tertiarycourses.com.sg)

Course: [AI Agents for Trading (C177)](https://www.tertiarycourses.com.sg/ai-agents-for-trading.html)

## Acknowledgements

- OpenAI for the lightweight Agents SDK, structured output, and function-tool patterns used in the bounded research agent
- Alpaca for the official Python SDK, historical market-data interface, and global paper-only account environment
- NIST, CME Group, and QuantConnect for the risk, verification, sizing, and backtest-realism guidance referenced in the course concepts
- The requested Agentic AI Automation with n8n repository for the README, navigation, and progressive-lab presentation pattern

---

<div align="center">

**If this helped you build a more evidence-led trading research workflow, star the repository.**

Powered by [Tertiary Infotech Academy Pte Ltd](https://www.tertiaryinfotech.com/)

[Course Page](https://www.tertiarycourses.com.sg/ai-agents-for-trading.html) · [Learner Guide](LG-AI%20Agents%20for%20Trading%20%28C177%29.md)

</div>
