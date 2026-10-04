# Approved Research Notes for the C177 Agent

These notes define the agent's evidence boundary in Lab 1. The agent may organise and paraphrase them but must not claim that its own memory is a source. Trainers should recheck current official documentation before delivery.

## Course outline

- Tertiary Courses, **AI Agents for Stock Trading (C177)**: https://www.tertiarycourses.com.sg/ai-agents-for-stock-trading.html
  - One beginner day.
  - Topic 1 covers AI trading agents, idea research, structured hypotheses, reliable market data, and data quality.
  - Topic 2 covers rule definition, backtesting, audit, risk sizing, paper trades, and verify-then-trust checkpoints.

## AI agents and human control

- OpenAI, **OpenAI Agents SDK**: https://openai.github.io/openai-agents-python/
  - Agents combine instructions, tools, guardrails, and a managed loop.
  - Function tools wrap Python functions with generated schemas and validation.
  - Structured output can use Pydantic models.
- NIST, **AI Risk Management Framework 1.0**: https://doi.org/10.6028/NIST.AI.100-1
- NIST, **Generative AI Profile**: https://doi.org/10.6028/NIST.AI.600-1
  - Testing, evaluation, verification, validation, documentation, and clear human-AI responsibilities support trustworthy use.

## Market data and paper trading

- Alpaca, **About Market Data API**: https://docs.alpaca.markets/us/docs/about-market-data-api
- Alpaca, **Historical Stock Data**: https://docs.alpaca.markets/us/docs/historical-stock-data-1
  - The free IEX feed is a single-exchange feed useful for initial application testing.
  - SIP consolidates eligible activity across US exchanges and has broader market coverage.
- Alpaca-py, **Stock historical data client and requests**: https://alpaca.markets/sdks/python/api_reference/data/stock/historical.html and https://alpaca.markets/sdks/python/api_reference/data/stock/requests.html
  - `StockHistoricalDataClient.get_stock_bars()` uses a `StockBarsRequest` with symbol, dates, timeframe, adjustment, and feed.
- Alpaca, **Paper Trading**: https://docs.alpaca.markets/us/docs/paper-trading
  - Paper trading is a simulation and may omit market impact, information leakage, latency slippage, queue position, price improvement, regulatory fees, and dividends.

## Backtesting and risk

- QuantConnect, **Slippage - Key Concepts**: https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts
  - Slippage is the difference between expected and actual fill price; models improve backtest realism.
- QuantConnect, **Backtesting**: https://www.quantconnect.com/docs/v2/cloud-platform/backtesting
  - A backtest simulates a trading algorithm on historical data; past results do not guarantee future results.
- CME Group, **Proper Position Size**: https://www.cmegroup.com/education/courses/trade-and-risk-management/proper-position-size
  - Position size depends on the stop location and the amount or fraction of the account the trader is willing to risk.
