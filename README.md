# AI Agents for Stock Trading

A hands-on, one-day non-WSQ course that teaches you to direct a bounded AI agent through stock-trading research — from a testable hypothesis and quality market data to an audited backtest, risk sizing and a human-approved paper trade.

| Course detail | Information |
|---|---|
| Course code | `C177` |
| Programme | Non-WSQ |
| Duration | 1 day (7.5 hours) |
| Registration | [View course details and register](https://www.tertiarycourses.com.sg/ai-agents-for-stock-trading.html) |
| Courseware version | v1.1 (4 October 2026) |

---

## About the course

Put an AI agent to work on your stock trading research. The course treats an AI trading agent as a **controlled research system, not an autonomous money manager**: the model organises evidence, chooses among narrow read-only tools and explains structured observations, while deterministic Python owns schemas, data checks, fingerprints, signals, metrics, risk quantity and submission limits — and a human owns every consequential decision.

All four labs use one fictional **Northstar SPY Research Pack**. Learners build one `C177-trading-agent-pack`, so each verified output becomes the input to the next lab, and they practise the verify-then-trust habit at every checkpoint. Execution is **paper-only** throughout.

## Learning outcomes

By the end of the course, you will be able to:

1. Explain how a bounded AI trading agent combines a model, instructions, tools, state, evidence, guardrails and human control without becoming an autonomous money manager.
2. Research a trading idea with an AI agent and convert it into a structured, falsifiable hypothesis with explicit rules, assumptions, evidence and rejection criteria.
3. Connect the agent workflow to an authorised market-data source and validate coverage, timestamps, corporate-action adjustments, completeness, consistency and freshness before use.
4. Define deterministic trading rules, run an honest backtest, compare a benchmark, and audit data leakage, friction assumptions, overfitting and out-of-sample behaviour.
5. Calculate a bounded position size from account risk and stop distance, then prepare an auditable paper-order ticket with pre-trade limits and human approval evidence.
6. Place and verify a paper-only trade through a controlled agent workflow while applying verify-then-trust checkpoints, logs, stop conditions and rollback procedures.

## Topics covered

**Topic 1 — From Trading Idea to Quality Market Data**
- Introduction to AI Agents for Stock Trading
- Researching Trading Ideas with an AI Agent
- Turning Ideas into a Structured, Testable Hypothesis
- Connecting the AI Agent to Reliable Market Data
- Checking Market Data Quality

**Topic 2 — The Six-Step Trading Workflow and Staying in Control**
- Defining Trading Rules with the AI Agent
- Backtesting and Auditing the Strategy
- Risk Sizing and Placing Paper Trades
- Applying the Verify-Then-Trust Habit and Checkpoints

## Labs

Start with the [labs overview](labs/README.md), then complete the labs in order:

1. [Lab 1 — Research an Idea and Freeze a Testable Hypothesis](labs/lab-01-research-an-idea-and-freeze-a-testable-hypothesis.md)
2. [Lab 2 — Fetch Market Data and Prove It Is Fit for Purpose](labs/lab-02-fetch-market-data-and-prove-it-is-fit-for-purpose.md)
3. [Lab 3 — Backtest the Rules and Audit the Evidence](labs/lab-03-backtest-the-rules-and-audit-the-evidence.md)
4. [Lab 4 — Size Risk, Approve, and Verify a Paper Trade](labs/lab-04-size-risk-approve-and-verify-a-paper-trade.md)

Scripts, starters and labelled synthetic rejoin checkpoints are in [`labs/resources/`](labs/resources/). If a credential or API issue blocks the sequence, use the [rejoin guide](labs/resources/rejoin/README.md).

## Course materials

| Material | Files |
|---|---|
| Slide deck | [PowerPoint](courseware/AI%20Agents%20for%20Stock%20Trading%20%28C177%29-v1.1.pptx) · [PDF](courseware/AI%20Agents%20for%20Stock%20Trading%20%28C177%29-v1.1.pdf) |
| Learner Guide | [Word](courseware/LG-AI%20Agents%20for%20Stock%20Trading%20%28C177%29.docx) · [PDF](courseware/LG-AI%20Agents%20for%20Stock%20Trading%20%28C177%29.pdf) · [Markdown](LG-AI%20Agents%20for%20Stock%20Trading%20%28C177%29.md) |
| Lesson Plan | [Word](courseware/LP-AI%20Agents%20for%20Stock%20Trading%20%28C177%29.docx) · [PDF](courseware/LP-AI%20Agents%20for%20Stock%20Trading%20%28C177%29.pdf) |
| Labs | [`labs/`](labs/) |

All courseware is generated from one source (`.agents/skills/non-wsq-courseware-build/build/`), so the deck, Learner Guide, Lesson Plan and labs stay aligned.

### Using the lab environment

You need Python 3.11+, an OpenAI API key (or trainer-provided equivalent) and an Alpaca **paper-only** account.

```bash
git clone https://github.com/tertiarycourses/C177-AI-Agents-for-Trading.git
cd C177-AI-Agents-for-Trading
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1   macOS/Linux: source .venv/bin/activate
python -m pip install -r labs/resources/requirements.txt
python labs/resources/preflight.py --require all
```

Copy `labs/resources/.env.example` to `.env` and keep every credential there — never in a prompt, notebook, screenshot or repository file. Keep `ALPACA_PAPER_ONLY=true`.

### Safety boundary

- Educational research only; no return, suitability or performance promise.
- No live-order mode: the only submission path uses `TradingClient(..., paper=True)`.
- SPY is the only allowed symbol, with a hard cap of 20 shares; submission needs a reviewed ticket plus a human approval token.
- Historical results and paper fills do not guarantee live execution or future behaviour.

## What is published here

This public repository carries the current courseware (slides, Learner Guide, Lesson Plan) and the labs. Superseded courseware versions, source reference material, and any credentials or `.env` files are kept private and are not published.

---

© Tertiary Infotech Academy Pte Ltd. Provided for educational use as part of **AI Agents for Stock Trading (C177)**. All rights reserved.

Developed and delivered by [Tertiary Infotech Academy Pte Ltd](https://www.tertiarycourses.com.sg) — [AI Agents for Stock Trading course page](https://www.tertiarycourses.com.sg/ai-agents-for-stock-trading.html).
