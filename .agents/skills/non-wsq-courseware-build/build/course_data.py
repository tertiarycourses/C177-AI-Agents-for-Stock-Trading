"""Single source of truth for AI Agents for Stock Trading (C177)."""

# ------------------------------------------------------------------ metadata
TITLE = "AI Agents for Stock Trading (C177)"
SHORT_TITLE = "AI Agents for Stock Trading (C177)"
COURSE_CODE = "C177"
VERSION = "v1.1"
VERSION_DATE = "4 October 2026"
ORG = "Tertiary Infotech Academy Pte Ltd"
UEN = "UEN: 201200696W"
TRAINER = "Course Trainer"
TRAINER_CERT = "Applied AI, quantitative research, and automation practitioner"
TRAINER_DELIVERS = "bounded AI agents, market-data validation, strategy research, backtesting, risk controls, and paper trading"
DAYS = 1
MODE = "Instructor-led, concept-first learning with connected Python labs"

# The advertised 7.5 instructional hours are delivered within an 8-hour
# scheduled day. Two 15-minute tea breaks are included; lunch is excluded.
DAY_MINUTES = 480
INSTRUCTIONAL_HOURS = 7.5
CLOCK_HOURS = 8
DAILY_TIMING = "9:00 am - 6:00 pm (1-hour lunch; two 15-minute tea breaks)"
CONNECTED_PRACTICE = "Four labs build one bounded Northstar SPY research pack from hypothesis to controlled paper evidence."
DARK_THEME = False

REJOIN_PATH = [
    (
        "Before Lab 2",
        "Copy labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis into your pack, verify fingerprints.json, and confirm the SPY long-only 20/50-day rule plus zero unresolved fields before fetching data.",
    ),
    (
        "Before Lab 3",
        "Copy labs/resources/rejoin/C177-trading-agent-pack/01-hypothesis and 02-market-data into your pack, verify both manifests, and confirm the data is visibly labelled synthetic and READY_FOR_BACKTEST before the backtest exercise.",
    ),
    (
        "Before Lab 4",
        "Copy all three folders from labs/resources/rejoin/C177-trading-agent-pack into your pack, verify every manifest, rerun compare_review.py, and inspect the benchmark, holdout, costs, drawdown, and CONTINUE_RESEARCH decision before producing a ticket.",
    ),
]

ICE_BREAKER = [
    "Your name and one trading-research task that you would like an AI agent to help with.",
    "One trading decision or action you would never allow an AI model to perform without human review.",
    "One source of evidence you would require before trusting a trading claim.",
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Explain how a bounded AI trading agent combines a model, instructions, tools, state, evidence, guardrails, and human control without becoming an autonomous money manager.",
    "LO2: Research a trading idea with an AI agent and convert it into a structured, falsifiable hypothesis with explicit rules, assumptions, evidence, and rejection criteria.",
    "LO3: Connect the agent workflow to an authorised market-data source and validate coverage, timestamps, corporate-action adjustments, completeness, consistency, and freshness before use.",
    "LO4: Define deterministic trading rules, run an honest backtest, compare a benchmark, and audit data leakage, friction assumptions, overfitting, and out-of-sample behaviour.",
    "LO5: Calculate a bounded position size from account risk and stop distance, then prepare an auditable paper-order ticket with pre-trade limits and human approval evidence.",
    "LO6: Place and verify a paper-only trade through a controlled agent workflow while applying verify-then-trust checkpoints, logs, stop conditions, and rollback procedures.",
]
LO_TITLES = [
    "Bounded Agent",
    "Testable Hypothesis",
    "Quality Market Data",
    "Backtest and Audit",
    "Risk-Sized Ticket",
    "Controlled Paper Trade",
]

# ------------------------------------------------------------------ topics
TOPICS = [
    dict(
        num=1,
        code="01",
        title="From Trading Idea to Quality Market Data",
        subtitle="AI trading agents | research evidence | structured hypotheses | market-data connections | data-quality gates",
        concepts=[
            ("Bounded agency", "The model may research and recommend, but deterministic tools calculate, controls constrain, and a person owns consequential decisions."),
            ("Falsifiable hypothesis", "A useful idea states the asset, data, signal, entry, exit, horizon, benchmark, costs, risks, and rejection rule before testing."),
            ("Evidence chain", "Every material claim links to a source, timestamp, tool result, assumption, or named owner instead of model confidence."),
            ("Market-data contract", "The workflow records provider, feed, symbol, timezone, session, adjustment, interval, coverage, and intended use."),
            ("Quality gates", "Schema, chronology, uniqueness, completeness, OHLC consistency, volume, freshness, and corporate actions are checked before analysis."),
            ("Human control", "The agent stops when evidence is missing, conflicts remain, data quality is weak, or an action exceeds paper-only authority."),
        ],
        teaching=[
            dict(
                title="Chatbot, Workflow, Agent, or Autopilot?",
                kind="compare",
                kicker="TOPIC 01 - CHOOSE THE RIGHT CONTROL MODEL",
                left_title="Bounded research system",
                right_title="Unsafe autopilot claim",
                left=[
                    "Chat explains; workflow follows fixed rules",
                    "Agent chooses among narrow read-only tools",
                    "Code calculates and validates deterministically",
                    "A person approves any paper order",
                ],
                right=[
                    "Model invents or changes trading rules mid-run",
                    "One fluent answer is treated as evidence",
                    "Keys or live-order endpoints are exposed",
                    "No stop condition, audit trail, or owner exists",
                ],
                paragraphs=[
                    "A chatbot responds to a message. A fixed workflow follows a known route. An AI agent adds a goal-directed loop in which a model can choose among explicitly described tools, observe their results, and decide what to do next. In this course, that flexibility is limited to research, interpretation, and routing. Market-data validation, backtest calculations, position sizing, and order constraints remain deterministic Python functions.",
                    "An AI trading agent is not an autonomous portfolio manager. It can organise evidence, propose a hypothesis, call approved read-only tools, and explain results. It cannot guarantee a return, invent missing data, loosen a risk limit, or place a live order. Consequential actions remain behind a visible human gate, and the supplied execution code is hard-wired to the paper environment.",
                ],
            ),
            dict(
                title="Seven Building Blocks of a Bounded Trading Agent",
                kind="tiles",
                kicker="TOPIC 01 - AGENT ANATOMY",
                visual=[
                    ("Goal", "Turn one idea into a traceable research pack, not a buy or sell promise."),
                    ("Model", "Interprets questions, plans tool use, and drafts explanations; it is not the numeric authority."),
                    ("Instructions", "Define evidence, output schema, paper-only boundary, stop rules, and escalation."),
                    ("Tools", "Read market data, validate it, run a backtest, size risk, and prepare or submit a paper ticket."),
                    ("State", "Versioned JSON, CSV, and logs carry verified facts between labs."),
                    ("Guardrails", "Allowlisted symbols, bounded dates, quantity caps, paper endpoint, dry run, and approval phrase."),
                    ("Human owner", "Reviews exceptions, approves the paper ticket, and decides whether research continues."),
                ],
                paragraphs=[
                    "A production-minded agent is a system of responsibilities rather than a clever prompt. The goal defines the finish line. Instructions tell the model what evidence it may use and when it must stop. Tools expose narrow capabilities with typed inputs. State preserves verified facts. Guardrails enforce limits outside the model. A human owner resolves ambiguity and authorises the paper-order step.",
                    "Weakness in one block propagates. If the market-data tool does not report its feed, the agent cannot judge coverage. If the hypothesis omits a rejection rule, a disappointing result can be rationalised after the fact. If the approval gate is only prose inside the prompt, the model can ignore it. Each block therefore produces observable evidence that another person can inspect.",
                ],
            ),
            dict(
                title="The Research Agent Loop",
                kind="flow",
                kicker="TOPIC 01 - OBSERVE BEFORE YOU CONTINUE",
                visual=["Receive a bounded research goal", "Plan the next evidence need", "Call one approved tool", "Inspect the observation", "Verify, stop, or continue"],
                paragraphs=[
                    "The loop begins with a bounded goal such as evaluating a 20/50-day moving-average idea on SPY daily bars. The agent identifies the next missing piece of evidence, calls a tool, reads the returned observation, and checks it against explicit acceptance criteria. Completion is not simply a final paragraph; it is a set of files whose required fields and checks can be verified.",
                    "A tool error, empty dataset, conflicting source, failed quality gate, or exceeded iteration limit ends the loop safely. The agent records what happened and asks the named owner to resolve the gap. This stop behaviour is a core capability, not a weakness: continuing with guessed inputs would make every later result look precise while remaining unsupported.",
                ],
            ),
            dict(
                title="A Trading Idea Is Not Yet a Hypothesis",
                kind="compare",
                kicker="TOPIC 01 - MAKE THE CLAIM TESTABLE",
                left_title="Vague idea",
                right_title="Structured hypothesis",
                left=[
                    "Buy when momentum looks strong",
                    "Use a good stock and recent data",
                    "Exit when conditions change",
                    "The strategy should beat the market",
                ],
                right=[
                    "SPY daily adjusted bars, fixed date range",
                    "20-day SMA crosses above 50-day SMA after close",
                    "Long next session; exit on opposite cross",
                    "Compare with buy-and-hold after stated frictions",
                ],
                paragraphs=[
                    "A trading idea is a narrative about why a pattern might exist. A hypothesis turns that narrative into a proposition that historical data can challenge. It names the instrument, bar interval, signal timing, execution assumption, entry, exit, sizing, benchmark, costs, test window, and outcome that would weaken the idea.",
                    "The specification must be frozen before the backtest. Otherwise the researcher can change the lookback, date range, asset, or exit rule after seeing results. That is hidden optimisation. A versioned hypothesis file makes changes visible: version 1.0 is tested as written; a later version requires a stated reason and a fresh out-of-sample check.",
                ],
            ),
            dict(
                title="The HYPER Hypothesis Contract",
                kind="tiles",
                kicker="TOPIC 01 - ONE CONTRACT FOR AGENT AND HUMAN",
                visual=[
                    ("H - Hypothesis", "One falsifiable sentence and the market rationale it is intended to test."),
                    ("Y - Yardstick", "Benchmark, metrics, minimum sample, and rejection criteria defined in advance."),
                    ("P - Parameters", "Asset, interval, lookbacks, entry, exit, position state, and date range."),
                    ("E - Evidence", "Source URLs, market-data contract, assumptions, and OWNER_TO_VERIFY items."),
                    ("R - Risks", "Look-ahead, overfitting, costs, liquidity, regime change, model error, and operational failure."),
                ],
                paragraphs=[
                    "HYPER is the shared contract used throughout the course. The Hypothesis makes the claim falsifiable. The Yardstick says what will count as useful evidence. Parameters remove ambiguity from the rules. Evidence records sources and data lineage. Risks make failure modes visible before the results create attachment to the idea.",
                    "The contract is intentionally machine-readable and human-readable. JSON gives the tools stable fields; the research log explains judgments and sources. The agent may help draft both, but a schema validator checks the structure and a person confirms any field marked OWNER_TO_VERIFY.",
                ],
            ),
            dict(
                title="Research Evidence: Stronger and Weaker Uses",
                kind="compare",
                kicker="TOPIC 01 - SOURCE DISCIPLINE",
                left_title="Stronger evidence practice",
                right_title="Weaker evidence practice",
                left=[
                    "Exchange, regulator, provider, or official SDK documentation",
                    "Direct dataset metadata and timestamped tool output",
                    "Independent source used to cross-check a material claim",
                    "Citation, access date, scope, and limitation recorded",
                ],
                right=[
                    "Uncited model memory or confident prose",
                    "Screenshot with no source, time, or feed",
                    "Promotional performance claim treated as proof",
                    "Later edits that overwrite the original reasoning",
                ],
                paragraphs=[
                    "The agent can accelerate discovery and summarisation, but the evidence remains external to the model. Official documentation establishes what an API or simulator actually provides. Dataset metadata shows the feed, time range, and adjustment choice. A second source can reveal a coverage difference or implementation assumption that one provider does not emphasise.",
                    "Every source has scope. Alpaca's free IEX feed is useful for initial testing but represents one exchange rather than the full consolidated US market. A daily-bar research exercise may tolerate that scope if it is recorded. A claim about precise executable prices or liquidity would require more complete quote and venue coverage.",
                ],
            ),
            dict(
                title="An Agent Output Needs a Contract",
                kind="tiles",
                kicker="TOPIC 01 - STRUCTURED BEFORE FLUENT",
                visual=[
                    ("Claim", "What is being proposed, in one falsifiable sentence."),
                    ("Known evidence", "Source-backed facts and exact tool observations."),
                    ("Assumptions", "Choices that shape the result but are not measured facts."),
                    ("Unknowns", "Missing or conflicting items labelled OWNER_TO_VERIFY."),
                    ("Next tool", "The single approved action needed to reduce uncertainty."),
                    ("Stop reason", "Why the run cannot safely continue, when applicable."),
                ],
                paragraphs=[
                    "Free-form prose hides missing fields. A structured output contract requires the agent to separate evidence from assumptions, identify unknowns, name the next tool, and explain why it has stopped. This makes the output easier to validate and prevents a polished summary from concealing a weak evidence chain.",
                    "The course agent writes versioned JSON plus a Markdown log. A schema validator rejects missing keys and wrong types. Deterministic tools consume only the validated fields they need; they do not scrape a narrative response for parameters. This separation reduces ambiguity and makes a later rerun reproducible.",
                ],
            ),
            dict(
                title="What a Daily OHLCV Bar Represents",
                kind="tiles",
                kicker="TOPIC 01 - MARKET DATA ANATOMY",
                visual=[
                    ("Timestamp", "The labelled interval and timezone; it must match the intended trading session."),
                    ("Open", "First eligible trade price represented by the bar's aggregation rules."),
                    ("High", "Highest represented trade price; it should not be below open or close."),
                    ("Low", "Lowest represented trade price; it should not be above open or close."),
                    ("Close", "Final represented trade price; adjusted and raw closes answer different questions."),
                    ("Volume", "Aggregated eligible share volume; feed coverage affects the observed value."),
                ],
                paragraphs=[
                    "A bar is an aggregation, not the market itself. Provider rules determine which trades are eligible, how sessions are separated, which timezone labels the interval, and whether corporate actions alter historical prices. A strategy that acts after the daily close must not use information that would only have been known during or after the next bar.",
                    "Basic consistency checks catch impossible rows: high must be at least the maximum of open and close; low must be at most their minimum; price and volume must be non-negative; timestamps must be ordered and unique. These checks do not prove the data is complete, but failing one is enough to stop the workflow.",
                ],
            ),
            dict(
                title="Feed Coverage Changes What You Observe",
                kind="compare",
                kicker="TOPIC 01 - IEX AND CONSOLIDATED COVERAGE",
                left_title="Single-exchange feed",
                right_title="Consolidated feed",
                left=[
                    "Lower-cost access and useful for initial app testing",
                    "Only trades and quotes from the named venue",
                    "Volume and intraday prices may differ from the wider market",
                    "Scope must be recorded in the data contract",
                ],
                right=[
                    "Combines eligible activity across US exchanges",
                    "Broader price, quote, and volume representation",
                    "May require a paid entitlement or provider plan",
                    "Still requires timezone, session, and adjustment checks",
                ],
                paragraphs=[
                    "The source name is not a minor metadata field. Alpaca documents that its free IEX feed covers a single exchange, while its SIP feed consolidates activity from US exchanges. Two valid feeds can therefore produce different bars, volumes, and simulated fills. The learner records the feed explicitly and does not compare results as if the inputs were identical.",
                    "Fit-for-purpose depends on the question. Daily educational research may begin on the free feed, provided the limitation is disclosed. A high-frequency, liquidity-sensitive, or executable-price claim needs broader and more granular data. The agent can explain the trade-off, but the data owner decides whether coverage is sufficient.",
                ],
            ),
            dict(
                title="Time, Session, and Signal Availability",
                kind="compare",
                kicker="TOPIC 01 - PREVENT ACCIDENTAL FUTURE KNOWLEDGE",
                left_title="Known at decision time",
                right_title="Known only later",
                left=[
                    "Completed bars with unambiguous timezone",
                    "Signal computed after the bar closes",
                    "Order scheduled for the next eligible session",
                    "Calendar and session assumptions recorded",
                ],
                right=[
                    "Current bar's final close before it occurs",
                    "Next session open used to decide today's signal",
                    "Revised data silently substituted after the run",
                    "Mixed local, exchange, and UTC dates",
                ],
                paragraphs=[
                    "A timestamp is meaningful only with a timezone and session rule. Daily US equity bars are associated with an exchange session, while an API may return UTC timestamps. Converting to local display time without preserving the original zone can shift a bar to the wrong calendar date.",
                    "The course strategy computes a crossover from completed daily bars and assumes a next-session execution. Signals are shifted before returns are applied in the backtest. This simple discipline prevents the strategy from receiving the same close that it is supposedly deciding before that close existed.",
                ],
            ),
            dict(
                title="Corporate Actions and Adjusted Prices",
                kind="tiles",
                kicker="TOPIC 01 - KEEP THE SERIES ECONOMICALLY CONSISTENT",
                visual=[
                    ("Split", "Share count and quoted price change mechanically; an unadjusted series can show a false crash."),
                    ("Dividend", "Cash distribution affects total return even when the price series alone does not show it."),
                    ("Adjustment mode", "Raw, split-adjusted, or fully adjusted data must be named in the contract."),
                    ("Benchmark consistency", "Strategy and benchmark must use comparable return and adjustment assumptions."),
                    ("Point-in-time concern", "Current symbol mappings and revised histories can leak later knowledge into old dates."),
                    ("Verification", "Inspect provider metadata and a known event before accepting the series."),
                ],
                paragraphs=[
                    "Corporate actions can break a price series if they are ignored. A stock split changes price and shares without creating an equivalent economic loss. Cash dividends contribute to total return. Providers offer adjustment parameters so researchers can choose a consistent series, but the choice must match the strategy and benchmark definition.",
                    "Adjusted data is not automatically free from bias. Symbol changes, delistings, and point-in-time membership can still affect a historical universe. This course uses one liquid ETF to keep the beginner exercise bounded, while explicitly teaching why a later multi-asset study needs survivorship-aware constituents and corporate-action records.",
                ],
            ),
            dict(
                title="The Market-Data Contract",
                kind="tiles",
                kicker="TOPIC 01 - RECORD LINEAGE BEFORE VALUES",
                visual=[
                    ("Provider and endpoint", "Who supplied the data and which documented route returned it."),
                    ("Feed and entitlement", "IEX, SIP, delayed, or another feed plus the account's access scope."),
                    ("Instrument", "Symbol, asset type, venue context, and currency."),
                    ("Time definition", "Interval, start, end, timezone, session, and as-of date."),
                    ("Transformations", "Adjustment, filtering, resampling, missing-value handling, and version."),
                    ("Intended use", "Educational daily-bar research, not a live executable-price guarantee."),
                ],
                paragraphs=[
                    "The data contract is the label attached to every dataset. Without it, a CSV of prices cannot be reproduced or judged. The contract records the provider, endpoint, feed, instrument, interval, date range, timezone, session, adjustment mode, transformations, retrieval time, and intended use.",
                    "The contract travels with the data into the backtest and audit. If a field changes, the dataset receives a new fingerprint and the old backtest is no longer assumed to apply. This lineage rule is more important than the agent's summary because it connects each result to the actual bytes and assumptions used.",
                ],
            ),
            dict(
                title="Eight Data-Quality Gates",
                kind="flow",
                kicker="TOPIC 01 - STOP EARLY WHEN THE INPUT IS WEAK",
                visual=["Schema and types", "Ordered unique timestamps", "Coverage and gaps", "OHLCV consistency", "Freshness and provenance"],
                paragraphs=[
                    "The validator checks eight categories: required columns and numeric types; ordered unique timestamps; expected date coverage; missing values; OHLC consistency; non-negative volume; freshness relative to the requested end; and a complete provider contract with a file fingerprint. The slide compresses these into five visual stages, while the report records every individual check.",
                    "A failed critical gate produces HOLD_DATA and prevents the agent from calling the backtest tool. A warning may be acceptable only when its scope is explained and the owner records a decision. For example, a weekend is not a gap in daily equity sessions, while a missing expected trading day needs investigation.",
                ],
            ),
            dict(
                title="Worked Example: Freeze the SPY Research Pack",
                kind="flow",
                kicker="TOPIC 01 - FROM CLAIM TO VERIFIED INPUT",
                visual=["Draft HYPER v1.0", "Human resolves unknowns", "Fetch SPY daily bars", "Run eight quality gates", "Freeze files and fingerprints"],
                paragraphs=[
                    "The course scenario tests whether a long-only 20-day versus 50-day simple-moving-average crossover on SPY has useful out-of-sample evidence after stated friction assumptions. The hypothesis does not say the strategy will make money. It says exactly what will be measured and which findings would cause the research owner to hold or revise the idea.",
                    "Lab 1 creates the hypothesis and research log. Lab 2 fetches and validates data, then records a SHA-256 fingerprint. The accepted files become immutable inputs to Lab 3. If the hypothesis or data changes, the learner creates a new version instead of overwriting the evidence chain.",
                ],
            ),
        ],
    ),
    dict(
        num=2,
        code="02",
        title="The Six-Step Trading Workflow and Staying in Control",
        subtitle="rule specification | honest backtesting | audit checks | risk sizing | paper orders | verify-then-trust checkpoints",
        concepts=[
            ("Rules before results", "Entry, exit, timing, sizing, costs, benchmark, and rejection criteria are frozen before the engine runs."),
            ("Deterministic core", "Code owns calculations and enforcement; the model interprets, organises evidence, and explains uncertainty."),
            ("Backtest realism", "Signals are shifted, data is split, and fees, spread, slippage, fills, and benchmark assumptions are visible."),
            ("Risk budget", "Quantity follows a capped account-risk budget and stop distance, never a model's confidence score."),
            ("Paper-only execution", "The supplied client uses the paper endpoint, a symbol allowlist, dry run, quantity cap, and explicit approval token."),
            ("Verify then trust", "Every stage produces checks, logs, fingerprints, a decision, and a safe rejoin point."),
        ],
        teaching=[
            dict(
                title="The Six-Step Controlled Trading Workflow",
                kind="flow",
                kicker="TOPIC 02 - THE COURSE SPINE",
                visual=["1 Define rules", "2 Acquire and validate data", "3 Backtest", "4 Audit", "5 Size risk", "6 Paper trade and verify"],
                paragraphs=[
                    "The workflow separates research from execution. First, freeze deterministic rules. Second, acquire data and stop if its contract or quality is inadequate. Third, run the backtest exactly as specified. Fourth, audit leakage, frictions, stability, and the benchmark. Fifth, calculate a position size from a fixed risk budget. Sixth, place a paper-only order after human approval and verify the returned receipt.",
                    "The AI agent helps route the work and explain each artifact, but it cannot skip a gate. A HOLD decision ends the current path and records the reason. This state machine prevents a weak backtest from becoming a position-size calculation simply because the conversation continued.",
                ],
            ),
            dict(
                title="Rule Specification: Remove Every Hidden Choice",
                kind="tiles",
                kicker="TOPIC 02 - FREEZE BEFORE TESTING",
                visual=[
                    ("Universe", "One named asset or a point-in-time selection rule."),
                    ("Signal", "Exact formula, lookback, bar interval, and data field."),
                    ("Timing", "When the signal becomes known and when the order is assumed to execute."),
                    ("Entry and exit", "Conditions, position state, and conflict resolution."),
                    ("Sizing", "Fixed rule independent of model enthusiasm."),
                    ("Friction", "Fees, spread or slippage, and fill assumptions."),
                    ("Benchmark", "A comparable alternative such as buy-and-hold."),
                    ("Decision", "Predeclared evidence for CONTINUE, HOLD, or REVISE."),
                ],
                paragraphs=[
                    "A backtest cannot resolve an ambiguous rule. 'Buy on momentum' leaves the lookback, threshold, timing, order type, and exit undefined. Every unspecified choice becomes an opportunity to tune after seeing the result. The strategy specification removes those hidden degrees of freedom.",
                    "For C177, the signal is a 20-day simple moving average crossing the 50-day average on completed adjusted daily closes. The position is either zero or one. The signal is shifted one bar before returns are applied. A buy-and-hold series over the same accepted dates provides the benchmark.",
                ],
            ),
            dict(
                title="Look-Ahead Bias: The One-Bar Test",
                kind="compare",
                kicker="TOPIC 02 - USE ONLY INFORMATION AVAILABLE THEN",
                left_title="Biased implementation",
                right_title="Causal implementation",
                left=[
                    "Today's close creates today's signal",
                    "Today's signal receives today's close-to-close return",
                    "Final high or low is used before the bar completes",
                    "Future revisions influence an earlier decision",
                ],
                right=[
                    "Completed bar creates the signal after close",
                    "Signal is shifted before the next return is applied",
                    "Execution timing is written in the rule contract",
                    "Inputs and code versions are fingerprinted",
                ],
                paragraphs=[
                    "Look-ahead bias occurs when a simulated decision uses information that was not yet available. In vectorised code, a single missing shift can give the strategy today's full return after computing the signal from today's close. The equity curve may look smooth because the backtest is quietly seeing the future.",
                    "The course engine makes the timing explicit. It computes the position from completed bars, shifts that position by one row, and only then multiplies it by the next period's return. The learner inspects a small table around one crossover to confirm which timestamp supplies the signal and which timestamp receives the return.",
                ],
            ),
            dict(
                title="Backtest Engine: Inputs to Evidence",
                kind="flow",
                kicker="TOPIC 02 - DETERMINISTIC CORE",
                visual=["Load frozen spec and data", "Create lagged signals", "Apply returns and frictions", "Build trades and equity curves", "Write metrics, plots, and fingerprints"],
                paragraphs=[
                    "The deterministic engine loads only a schema-valid strategy specification and a dataset whose fingerprint matches the accepted quality report. It computes moving averages, creates entry and exit transitions, shifts positions, applies friction on turnover, and generates both strategy and benchmark equity curves.",
                    "Outputs include metrics JSON, trades CSV, an equity-curve image, and an audit log template. These artifacts are more important than a single headline return. They let a reviewer reproduce the run, inspect individual trades, compare segments, and identify whether a claimed improvement comes from rule logic or a changed assumption.",
                ],
            ),
            dict(
                title="Development Window and Out-of-Sample Window",
                kind="compare",
                kicker="TOPIC 02 - SEPARATE DESIGN FROM REVIEW",
                left_title="Development segment",
                right_title="Out-of-sample segment",
                left=[
                    "Used to implement and debug the fixed rule",
                    "Can reveal obvious data or code errors",
                    "Results may influence design choices",
                    "Must not be presented as untouched evidence",
                ],
                right=[
                    "Held back until the specification is frozen",
                    "Used once for a cleaner generalisation check",
                    "Compared with benchmark and decision criteria",
                    "Poor evidence leads to HOLD, not repeated tuning",
                ],
                paragraphs=[
                    "If the same period is used to invent, tune, and judge a strategy, the result reflects both the market and the researcher's choices. A chronological split gives earlier data to development and later data to out-of-sample review. It does not eliminate overfitting, but it makes the research path more honest.",
                    "The learner records the split date before running the engine. Changes inspired by the out-of-sample result create a new hypothesis version and require a new untouched period or a more rigorous walk-forward design. Repeatedly checking the same holdout turns it into another development sample.",
                ],
            ),
            dict(
                title="Read Metrics as a System, Not a Score",
                kind="tiles",
                kicker="TOPIC 02 - MULTIPLE VIEWS OF PERFORMANCE",
                visual=[
                    ("Total return", "Growth over the window; it depends strongly on start and end dates."),
                    ("Annualised return", "Compounded rate normalised for time; unstable with short samples."),
                    ("Volatility", "Dispersion of returns, not a complete measure of loss risk."),
                    ("Sharpe ratio", "Excess return per unit of volatility under stated assumptions."),
                    ("Maximum drawdown", "Largest peak-to-trough decline in the simulated equity curve."),
                    ("Turnover", "How often exposure changes; it drives friction sensitivity."),
                    ("Trade count", "A tiny sample cannot support a stable hit-rate story."),
                    ("Benchmark gap", "Strategy result minus a comparable passive alternative."),
                ],
                paragraphs=[
                    "No single metric establishes a good strategy. Return without drawdown hides the path. Sharpe ratio compresses assumptions about distribution and volatility. Hit rate can be high while losses are much larger than gains. A small number of trades makes every summary unstable.",
                    "The course report presents development, out-of-sample, and full-window metrics beside buy-and-hold. Learners explain what each metric captures, what it omits, and how costs or date choices affect it. The decision is based on a predeclared bundle of evidence rather than whichever number looks most favourable.",
                ],
            ),
            dict(
                title="Frictionless Results and More Realistic Results",
                kind="compare",
                kicker="TOPIC 02 - MODEL THE COST OF ACTING",
                left_title="Frictionless simplification",
                right_title="Declared reality assumptions",
                left=[
                    "Every order fills immediately at the chosen bar price",
                    "No spread, fee, slippage, latency, or market impact",
                    "Unlimited liquidity at any quantity",
                    "Useful only as an upper-bound diagnostic",
                ],
                right=[
                    "Turnover incurs stated fee and slippage basis points",
                    "Execution timing and price field are explicit",
                    "Paper limitations and liquidity are disclosed",
                    "Sensitivity cases show how conclusions change",
                ],
                paragraphs=[
                    "Real orders may fill at prices different from a backtest assumption. QuantConnect describes slippage as the difference between expected and actual fill price and provides models to improve realism. Fees, spread, latency, volume, order type, and market impact also affect the path from signal to fill.",
                    "A beginner backtest cannot model every microstructure effect, so the honest choice is to expose a simple friction assumption and test sensitivity. If a small increase in costs erases the result, the evidence is fragile. The report does not hide this behind a single optimised number.",
                ],
            ),
            dict(
                title="Overfitting Red Flags",
                kind="tiles",
                kicker="TOPIC 02 - WHEN THE STORY FITS THE SAMPLE TOO WELL",
                visual=[
                    ("Many trials", "Dozens of unreported variants make the best result look rarer than it is."),
                    ("Tiny sample", "Few trades or one market regime cannot support a stable conclusion."),
                    ("Sharp optimum", "Only one exact parameter works while nearby values collapse."),
                    ("No benchmark", "A complex strategy may merely reproduce market exposure."),
                    ("Hidden exclusions", "Changing assets or dates after inspection creates selection bias."),
                    ("Holdout erosion", "Repeatedly tuning on the same out-of-sample period destroys its role."),
                ],
                paragraphs=[
                    "Overfitting is not only a machine-learning problem. Every choice of asset, date range, indicator, threshold, cost, and exit rule can adapt to noise. Reporting only the best run hides the number of opportunities the researcher had to find it.",
                    "The audit records versions, trials, and rejected ideas. It checks nearby parameters for gross instability, but does not use that check to select a new winner during the same run. The correct response to weak out-of-sample evidence is often HOLD and more disciplined research, not another immediate tweak.",
                ],
            ),
            dict(
                title="The Backtest Audit Trail",
                kind="flow",
                kicker="TOPIC 02 - VERIFY THE RESULT BEFORE INTERPRETING IT",
                visual=["Recompute fingerprints", "Inspect signal timing", "Compare benchmark and segments", "Stress friction and parameters", "Record CONTINUE, HOLD, or REVISE"],
                paragraphs=[
                    "The audit begins by verifying that the strategy, data, and code inputs match the recorded fingerprints. It then inspects rows around a signal change, compares development and out-of-sample segments, checks trade count and drawdown, and reruns declared friction and nearby-parameter cases.",
                    "The final decision includes a reason, owner, timestamp, unresolved limitations, and next permissible action. CONTINUE means the research may proceed to a bounded paper-order exercise; it does not mean the strategy is profitable or suitable for live capital. HOLD stops the execution path until the named evidence gap is resolved.",
                ],
            ),
            dict(
                title="Model Work and Deterministic Work",
                kind="compare",
                kicker="TOPIC 02 - SEPARATE LANGUAGE FROM AUTHORITY",
                left_title="AI model may",
                right_title="Code or human must",
                left=[
                    "Summarise sources and organise a hypothesis draft",
                    "Choose the next approved read-only tool",
                    "Explain metrics and surface uncertainty",
                    "Draft a HOLD or CONTINUE rationale for review",
                ],
                right=[
                    "Validate schema, timestamps, prices, and fingerprints",
                    "Compute signals, returns, costs, and position size",
                    "Enforce paper endpoint, allowlist, caps, and dry run",
                    "Approve the ticket and own the decision",
                ],
                paragraphs=[
                    "Language models are useful at interpretation and synthesis. They are not reliable enforcement layers and should not be trusted to perform precise financial calculations from prose. The course tools return structured observations; the model explains them without rewriting the numbers.",
                    "Controls that protect money, secrets, identity, or auditability live outside the prompt. The paper client ignores any request to use a live endpoint. Quantity is capped by code. The symbol must be allowlisted. Submission remains disabled unless a human supplies the exact approval token after reviewing the generated ticket.",
                ],
            ),
            dict(
                title="Position Size Comes from Risk Budget and Stop Distance",
                kind="tiles",
                kicker="TOPIC 02 - CALCULATE BEFORE YOU ORDER",
                visual=[
                    ("Account equity", "The paper account value used only for the exercise."),
                    ("Risk fraction", "A small predeclared fraction chosen by the human owner, not the agent."),
                    ("Risk budget", "Account equity multiplied by risk fraction."),
                    ("Per-share risk", "Absolute difference between planned entry and protective stop."),
                    ("Risk quantity", "Floor of risk budget divided by per-share risk."),
                    ("Exposure cap", "A second ceiling based on maximum position value and available buying power."),
                ],
                paragraphs=[
                    "CME's educational guidance links position size to two inputs: where the stop is placed and how much of the account the trader is willing to risk. The course formula is quantity = floor(risk budget / per-share risk), then the result is capped by maximum position value and a hard course quantity limit.",
                    "A stop order cannot guarantee the planned loss because markets can gap and fills can slip. The calculation is therefore a planning bound, not a promise. The paper ticket records entry reference, stop reference, timestamp, risk fraction, exposure cap, final quantity, and every cap that changed the raw result.",
                ],
            ),
            dict(
                title="Worked Position-Size Example",
                kind="flow",
                kicker="TOPIC 02 - TRACE EVERY NUMBER",
                visual=["Paper equity = $100,000", "Risk fraction = 0.50%", "Entry $500; stop $490", "Raw quantity = floor($500 / $10) = 50", "Apply exposure and course caps"],
                paragraphs=[
                    "With paper equity of $100,000 and a 0.50% risk fraction, the risk budget is $500. If the planned entry reference is $500 and the stop reference is $490, per-share risk is $10 and the raw risk quantity is 50 shares. A 10% exposure cap also permits at most 20 shares at a $500 reference price, so the final quantity becomes 20.",
                    "The example shows why risk and exposure are different. The stop distance controls the planned loss per share, while the exposure cap limits how much account value is concentrated in one symbol. The smallest applicable bound wins, and the ticket records which bound was active.",
                ],
            ),
            dict(
                title="The Pre-Trade Paper Ticket",
                kind="tiles",
                kicker="TOPIC 02 - REVIEW BEFORE SUBMISSION",
                visual=[
                    ("Instrument", "Allowlisted symbol, asset type, side, and paper environment."),
                    ("Evidence", "Accepted hypothesis, data, backtest, audit decision, and fingerprints."),
                    ("Quantity", "Risk calculation, exposure cap, buying-power check, and hard maximum."),
                    ("Order", "Type, time in force, reference price, and paper endpoint."),
                    ("Limits", "No live route, no secret in logs, no unsupported symbol, no blank approval."),
                    ("Owner", "Reviewer, approval time, approval token, and reason for the exercise."),
                ],
                paragraphs=[
                    "The ticket is a proposal, not an order. It consolidates the exact symbol, side, quantity, order type, time in force, reference price, environment, evidence fingerprints, and active caps. A person can review one artifact instead of reconstructing the decision from a chat transcript.",
                    "The supplied tool generates the ticket in dry-run mode by default. It refuses live mode, non-allowlisted symbols, non-positive or excessive quantities, stale tickets, missing audit decisions, and missing approval. The agent may explain a refusal but cannot override it.",
                ],
            ),
            dict(
                title="Paper Trading Is Useful and Incomplete",
                kind="compare",
                kicker="TOPIC 02 - SIMULATION IS NOT LIVE EVIDENCE",
                left_title="What paper trading exercises",
                right_title="What it may not reproduce",
                left=[
                    "Authentication, request schema, account checks, and order lifecycle",
                    "Real-time data handling and software error paths",
                    "Logging, approval, idempotency, and receipt verification",
                    "Operational rehearsal without risking capital",
                ],
                right=[
                    "Market impact, information leakage, or latency slippage",
                    "Queue position and realistic available liquidity",
                    "All fees, dividends, price improvement, or live behaviour",
                    "Future profitability or suitability for real money",
                ],
                paragraphs=[
                    "Alpaca describes paper trading as a real-time simulation and explicitly lists differences from live trading, including market impact, information leakage, latency slippage, queue position, price improvement, regulatory fees, and dividends. A paper fill is therefore evidence that the software path worked under simulator assumptions, not that a live order would receive the same result.",
                    "The course stays paper-only. Learners verify that the returned account and order belong to the paper environment, save the order identifier and status, and then cancel an open exercise order when appropriate. No live credentials, endpoints, or live-order instructions are included.",
                ],
            ),
            dict(
                title="Human Gate and Safe Submission",
                kind="flow",
                kicker="TOPIC 02 - CONTROL THE CONSEQUENTIAL STEP",
                visual=["Generate dry-run ticket", "Review evidence and limits", "Human enters exact approval token", "Submit to paper endpoint", "Verify receipt or stop"],
                paragraphs=[
                    "The human gate occurs after the deterministic ticket exists. The reviewer checks the paper environment, symbol, quantity, side, order type, active risk cap, accepted audit decision, and absence of secrets. Only then is the exact approval token added to a local command that is not stored in the repository.",
                    "Submission uses a unique client order ID so a retry can be reconciled rather than blindly duplicated. If the network response is uncertain, the tool queries by client order ID before attempting anything else. The safe response to ambiguity is to stop and inspect the paper dashboard.",
                ],
            ),
            dict(
                title="Verify-Then-Trust Checkpoints",
                kind="tiles",
                kicker="TOPIC 02 - EVIDENCE AT EVERY BOUNDARY",
                visual=[
                    ("Hypothesis gate", "Schema valid, assumptions separated, unknowns owned, version frozen."),
                    ("Data gate", "Contract complete, quality checks recorded, fingerprint accepted."),
                    ("Backtest gate", "Timing causal, benchmark present, segments and frictions reported."),
                    ("Audit gate", "Leakage, trials, stability, limitations, and decision documented."),
                    ("Risk gate", "Quantity recomputed from approved inputs and bounded by caps."),
                    ("Execution gate", "Paper endpoint, human approval, unique ID, receipt, and reconciliation."),
                ],
                paragraphs=[
                    "Verify-then-trust is a habit of requiring observable evidence before the next capability is enabled. It does not mean verifying once and trusting forever. Model, prompt, code, data, account, or provider changes can invalidate prior evidence and require a rerun.",
                    "NIST's AI risk guidance emphasises testing, evaluation, verification, validation, documentation, and clear human-AI roles. The course turns those ideas into six concrete gates. Each gate has a file, a check, an owner, a decision, and a rejoin checkpoint so a learner can recover without inventing missing state.",
                ],
            ),
            dict(
                title="Failure, Pause, Reconcile, and Roll Back",
                kind="tiles",
                kicker="TOPIC 02 - OPERATE FOR THE ERROR PATH",
                visual=[
                    ("Tool failure", "Record the error; do not fabricate a result or continue from stale state."),
                    ("Data drift", "Freeze the new dataset separately and rerun quality and backtest evidence."),
                    ("Duplicate risk", "Query the client order ID before retrying a timed-out request."),
                    ("Unexpected fill", "Stop the workflow, inspect the paper account, and preserve the receipt."),
                    ("Model change", "Rerun stable prompts and tool-choice checks before accepting explanations."),
                    ("Rollback", "Cancel open paper orders, disable submission, and restore the last verified version."),
                ],
                paragraphs=[
                    "A reliable workflow is designed around failure paths. APIs time out, providers revise data, credentials expire, models change, and simulated orders can behave unexpectedly. The agent must expose the uncertainty and stop instead of smoothing it into a confident narrative.",
                    "Rollback is practical because each lab produces versioned files. The operator can disable submission, cancel an open paper order, restore the last verified specification and code, and rerun from a known checkpoint. Logs and fingerprints show exactly which state was active when the issue occurred.",
                ],
            ),
        ],
    ),
]

# ------------------------------------------------------------------ day theme and schedule
DAY_THEMES = {1: "From Evidence-Led Research to a Controlled Paper Trade"}


def SCHEDULE(lab_titles):
    return {
        1: (
            DAY_THEMES[1],
            [
                ("9:00", "9:20", 20, "admin", "Welcome, safety boundary, course outcomes, and connected scenario"),
                ("9:20", "10:05", 45, "topic", "Topic 1 - AI trading agents, research evidence, and structured hypotheses"),
                ("10:05", "10:20", 15, "break", "Tea break"),
                ("10:20", "11:10", 50, "lab", "Hands-on: " + lab_titles([1])),
                ("11:10", "11:45", 35, "topic", "Topic 1 - market-data contracts, feed coverage, adjustments, and quality gates"),
                ("11:45", "12:45", 60, "lab", "Hands-on: " + lab_titles([2])),
                ("12:45", "13:45", 60, "lunch", "Lunch break"),
                ("13:45", "14:45", 60, "topic", "Topic 2 - rule specification, backtesting, realism, and audit"),
                ("14:45", "15:00", 15, "break", "Tea break"),
                ("15:00", "16:05", 65, "lab", "Hands-on: " + lab_titles([3])),
                ("16:05", "16:35", 30, "topic", "Topic 2 - risk sizing, paper orders, human gates, and rollback"),
                ("16:35", "17:45", 70, "lab", "Hands-on: " + lab_titles([4])),
                ("17:45", "18:00", 15, "recap", "Verify final evidence pack, next steps, and Q&A"),
            ],
        )
    }


# ------------------------------------------------------------------ optional deck content
COURSE_OVERVIEW = dict(
    section_title="Course Fundamentals",
    concepts_title="The Evidence-Led Trading Agent",
    concepts=[
        ("Research, not prediction", "The agent turns an idea into testable evidence; it does not promise a market outcome."),
        ("Tools, not hidden arithmetic", "Typed Python tools fetch, validate, backtest, size, and submit only within code-enforced bounds."),
        ("Paper, not live", "Every order path is hard-wired to simulation and remains behind an explicit human gate."),
        ("Artifacts, not chat memory", "Versioned JSON, CSV, Markdown, plots, fingerprints, and receipts form the audit trail."),
    ],
    framework_title="The Six-Step Verify-Then-Trust Workflow",
    framework=[
        ("Define", "Freeze the HYPER hypothesis and deterministic rules."),
        ("Validate", "Accept only fit-for-purpose market data with recorded lineage."),
        ("Backtest", "Use causal timing, visible frictions, a benchmark, and a holdout."),
        ("Audit", "Check leakage, trials, stability, limitations, and decision criteria."),
        ("Size", "Compute quantity from human-set risk and exposure limits."),
        ("Paper trade", "Approve, submit to simulation, reconcile, verify, and roll back."),
    ],
    statement=dict(
        headline="A confident answer is not trading evidence.",
        body="Trust only the parts you can trace to a source, deterministic calculation, recorded decision, or verified paper receipt.",
        kicker="COURSE PRINCIPLE",
    ),
    pillars_title="What You'll Build",
    pillars=[
        ("Research Pack", ["Structured HYPER hypothesis", "Cited research log", "Schema and version checks"]),
        ("Evidence Pack", ["Market-data contract", "Quality report and fingerprint", "Backtest, trades, chart, and audit"]),
        ("Paper-Trade Pack", ["Bounded risk calculation", "Dry-run ticket and approval", "Paper receipt and rollback record"]),
    ],
    arc_title="How Every Lab Progresses",
    arc=["Start from a verified checkpoint.", "Use the agent only within its evidence boundary.", "Run deterministic checks before interpretation.", "Save an observable artifact and fingerprint.", "Stop, resolve, or continue through a named gate."],
)

LAB_SHOTS = {}

# ------------------------------------------------------------------ learner guide content
LG_INTRO = (
    "AI Agents for Stock Trading is a one-day, beginner-level course about disciplined trading research, not automated profit. "
    "You will build a bounded research agent that can organise a hypothesis, call approved Python tools, interpret structured observations, and prepare a paper-order exercise. "
    "Calculations and controls remain deterministic, consequential steps require human approval, and the supplied execution path cannot send a live order."
)
LG_INTRO2 = (
    "All four labs use one SPY daily-bar moving-average scenario and one C177-trading-agent-pack. "
    "Each lab begins from a verified checkpoint and produces versioned JSON, CSV, Markdown, image, or receipt evidence for the next lab. "
    "The strategy is deliberately simple so the course can focus on research quality, data lineage, causal testing, risk limits, paper execution, and the verify-then-trust habit."
)
LG_SETUP = dict(
    needs=[
        "A Windows or Mac laptop with Python 3.11 or newer, Visual Studio Code or Google Colab, and a modern browser.",
        "The C177 repository and permission to create a local C177-trading-agent-pack folder.",
        "An OpenAI API key stored only in a local environment variable for the agent labs, or a trainer-provided approved equivalent.",
        "An Alpaca paper-only account with paper API keys. Never use live-trading credentials in this course.",
        "Internet access for official documentation and authorised API calls; a supplied synthetic checkpoint is available only as a rejoin fallback.",
    ],
    verify_text="Create a virtual environment, install the pinned lab dependencies, copy the example environment file, then run the preflight check. Do not paste keys into chat, code, screenshots, notebooks, or git.",
    verify_code="python -m venv .venv\n# Windows: .\\.venv\\Scripts\\Activate.ps1\n# macOS/Linux: source .venv/bin/activate\npython -m pip install -r labs/resources/requirements.txt\nCopy-Item labs/resources/.env.example .env  # Windows\n# cp labs/resources/.env.example .env       # macOS/Linux\npython labs/resources/preflight.py",
    conventions=[
        "Commands are run from the repository root unless a step says otherwise.",
        "Placeholders such as <OPENAI_API_KEY> and <ALPACA_PAPER_KEY> are replaced only in the local .env file, which git ignores.",
        "The default OpenAI model for this August 2026 build is gpt-5.6-sol; trainers should recheck the official model guide before delivery.",
        "ALPACA_PAPER_ONLY must remain true. The supplied client constructs TradingClient(..., paper=True) and contains no live-mode flag.",
        "All prices, strategy outputs, and paper fills are educational observations rather than recommendations or promises.",
        "If a critical check reports HOLD, stop and follow the troubleshooting or rejoin path before continuing.",
    ],
)
LAB_NOTE = "Use only authorised accounts, placeholder or synthetic inputs, and paper-trading credentials. This course does not provide financial advice and includes no live-order path."

LG_WRAPUP = dict(
    title="Wrap-Up - Your Controlled Trading Research Pack",
    intro="You have moved one deliberately simple trading idea through an auditable chain from hypothesis to market data, backtest, risk calculation, and paper-only order evidence.",
    sections=[
        dict(
            title="What the agent contributed",
            bullets=[
                "Converted a broad idea into a structured draft and exposed unknowns.",
                "Selected approved tools and explained their structured observations.",
                "Maintained a clear separation between claims, evidence, assumptions, and stop reasons.",
            ],
        ),
        dict(
            title="What deterministic controls contributed",
            bullets=[
                "Validated schemas, data quality, fingerprints, signal timing, metrics, and quantity.",
                "Enforced symbol, risk, exposure, quantity, paper-environment, approval, and idempotency limits.",
                "Produced reproducible files that can be reviewed independently of the chat session.",
            ],
        ),
        dict(
            title="What remains uncertain",
            bullets=[
                "Historical and out-of-sample results do not guarantee future performance.",
                "Simple friction assumptions and a paper simulator do not reproduce the live market.",
                "One asset, one rule, and one period are a learning exercise, not an investment conclusion.",
            ],
        ),
    ],
)
LG_NEXT_STEPS = [
    "Re-run the full pack from an empty output folder and compare the new fingerprints and logs.",
    "Replace only one declared parameter, create hypothesis version 1.1, and preserve version 1.0 for comparison.",
    "Add walk-forward windows and broader point-in-time data before considering a multi-asset research claim.",
    "Review OpenAI Agents SDK, Alpaca, NIST, CME, and backtest-engine documentation for changes before each delivery.",
    "Keep every experiment paper-only until an appropriately qualified owner establishes a separate governance, compliance, risk, and operational process.",
]
LG_GLOSSARY = [
    ("AI agent", "A goal-directed system in which a model can choose among approved tools, observe results, and continue or stop within defined limits."),
    ("Backtest", "A simulation that applies fixed rules to historical data under stated timing, cost, and fill assumptions."),
    ("Benchmark", "A comparable reference, such as buy-and-hold, used to interpret whether complexity added evidence."),
    ("Corporate-action adjustment", "A transformation that accounts for events such as splits or dividends in a historical price series."),
    ("Data contract", "Metadata that records a dataset's provider, feed, instrument, interval, dates, timezone, adjustments, transformations, and intended use."),
    ("Drawdown", "A peak-to-trough decline in an equity curve before a new peak is reached."),
    ("Fingerprint", "A cryptographic hash used to identify the exact bytes of an input or output file."),
    ("HYPER", "The course hypothesis contract: Hypothesis, Yardstick, Parameters, Evidence, and Risks."),
    ("Look-ahead bias", "Use of information in a simulated decision before that information would have been available."),
    ("Market-data feed", "A defined source and coverage of trades, quotes, or bars, such as a single venue or consolidated market feed."),
    ("Out-of-sample", "A later period held apart from rule development and used for a cleaner review of generalisation."),
    ("Paper trading", "A simulated order environment that exercises software and operations without routing an order to a live exchange."),
    ("Per-share risk", "The absolute difference between planned entry and stop reference used in the course sizing formula."),
    ("Position sizing", "Calculation of quantity from a human-set risk budget, stop distance, exposure cap, and other limits."),
    ("Slippage", "The difference between the expected order price and the actual fill price."),
    ("Verify-then-trust", "A recurring practice of requiring observable evidence at each boundary before enabling the next capability."),
]

NEXT_STEPS = dict(
    title="Continue with Evidence, Not Automation Pressure",
    items=[
        "Reproduce the same run before changing the idea.",
        "Version every rule, dataset, prompt, code, and decision change.",
        "Increase realism and independent review before increasing autonomy.",
        "Keep execution paper-only throughout the course and personal practice.",
    ],
)
THANK_YOU = dict(
    body="You can now direct a bounded AI agent through a traceable trading research cycle while keeping data, calculation, risk, and execution evidence under human control.",
    kicker="KEEP VERIFYING BEFORE YOU TRUST",
)

# ------------------------------------------------------------------ version history
VERSION_HISTORY = [
    ("1.0", "11 August 2026", "Initial aligned non-WSQ release with two topics, four connected labs, and a paper-only trading workflow.", TRAINER),
    ("1.1", VERSION_DATE, "Course retitled from AI Agents for Trading to AI Agents for Stock Trading.", TRAINER),
]
