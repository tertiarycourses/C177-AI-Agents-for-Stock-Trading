"""Bounded OpenAI Agents SDK research agent for the connected C177 labs.

The agent can read only approved course sources or selected structured artifacts.
It has no trading client and cannot submit an order.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from course_common import (
    REPO_ROOT,
    pydantic_dump,
    read_json,
    safe_within,
    sha256_file,
    utc_now,
    write_json,
)


class HypothesisSpec(BaseModel):
    course_code: Literal["C177"] = "C177"
    version: Literal["1.0"] = "1.0"
    status: Literal["FROZEN_FOR_DATA"] = "FROZEN_FOR_DATA"
    title: str
    symbol: Literal["SPY"] = "SPY"
    asset_type: Literal["US ETF"] = "US ETF"
    hypothesis: str
    rationale: str
    benchmark: str
    bar_interval: Literal["1Day"] = "1Day"
    data_start: Literal["2018-01-01"] = "2018-01-01"
    data_end: Literal["2025-12-31"] = "2025-12-31"
    adjustment: Literal["all"] = "all"
    feed: Literal["iex"] = "iex"
    timezone: Literal["America/New_York"] = "America/New_York"
    fast_window: Literal[20] = 20
    slow_window: Literal[50] = 50
    position_state: Literal["long_only_0_or_1"] = "long_only_0_or_1"
    signal_rule: str
    entry_rule: str
    exit_rule: str
    execution_timing: str
    friction_bps: Literal[5.0] = 5.0
    sensitivity_friction_bps: list[float]
    split_date: Literal["2023-01-01"] = "2023-01-01"
    rejection_criteria: list[str] = Field(min_length=4)
    evidence_urls: list[str] = Field(min_length=4)
    assumptions: list[str] = Field(min_length=3)
    unknowns: list[str]
    risks: list[str] = Field(min_length=6)
    human_owner: str
    paper_only: Literal[True] = True
    live_order_requested: Literal[False] = False


class AgentReview(BaseModel):
    course_code: Literal["C177"] = "C177"
    review_type: Literal["data", "backtest", "ticket"]
    controlling_status: str
    recommendation: str
    evidence_citations: list[str] = Field(min_length=3)
    critical_observations: list[str] = Field(min_length=2)
    limitations: list[str] = Field(min_length=2)
    next_allowed_action: str
    human_owner_required: Literal[True] = True
    live_action_permitted: Literal[False] = False


def deterministic_hypothesis() -> HypothesisSpec:
    return HypothesisSpec(
        title="SPY 20/50-Day Moving-Average Crossover Research Hypothesis",
        hypothesis=(
            "On accepted adjusted SPY daily bars, a long-only position held after the 20-day simple moving average "
            "crosses above the 50-day average may show different out-of-sample return and drawdown characteristics "
            "from buy-and-hold after declared friction; the historical test can weaken but cannot prove the idea."
        ),
        rationale=(
            "A transparent trend rule is simple enough to audit for timing, data lineage, costs, and stability while "
            "still exercising the complete agent-led research workflow."
        ),
        benchmark="Buy-and-hold SPY over the same accepted dates and adjustment assumptions",
        sensitivity_friction_bps=[0.0, 5.0, 10.0],
        signal_rule="fast_sma = mean(close, 20); slow_sma = mean(close, 50); raw_signal = 1 when fast_sma > slow_sma else 0",
        entry_rule="Enter long only when raw_signal changes from 0 to 1 after a completed daily bar",
        exit_rule="Exit to cash only when raw_signal changes from 1 to 0 after a completed daily bar",
        execution_timing="Shift raw_signal by one row before applying the next daily close-to-close return",
        rejection_criteria=[
            "Any critical market-data quality gate fails or the accepted CSV fingerprint changes",
            "Signal timing uses current or future information instead of a one-row shift",
            "The benchmark, development segment, or out-of-sample segment is missing",
            "Out-of-sample evidence is too sparse, unstable, or materially weakened by declared friction",
            "Any workflow step requests live credentials, a live endpoint, or autonomous execution",
        ],
        evidence_urls=[
            "https://www.tertiarycourses.com.sg/ai-agents-for-trading.html",
            "https://openai.github.io/openai-agents-python/",
            "https://docs.alpaca.markets/us/docs/historical-stock-data-1",
            "https://docs.alpaca.markets/us/docs/paper-trading",
            "https://www.cmegroup.com/education/courses/trade-and-risk-management/proper-position-size",
            "https://doi.org/10.6028/NIST.AI.100-1",
        ],
        assumptions=[
            "Daily adjusted bars are fit only for the bounded educational research question stated in the data contract",
            "A 5 basis-point charge on each position change is a simplified friction model rather than a live fill forecast",
            "The chronological split beginning 2023-01-01 is frozen before the backtest is inspected",
            "A paper simulator receipt is operational evidence and not evidence of live execution quality or profitability",
        ],
        unknowns=[],
        risks=[
            "Look-ahead bias from applying an unshifted signal",
            "Feed coverage differences between IEX and consolidated data",
            "Corporate-action or timestamp inconsistency",
            "Overfitting through unreported trials or repeated holdout use",
            "Under-modelled fees, spread, slippage, liquidity, and market impact",
            "Regime change and unstable historical relationships",
            "Model fabrication or incorrect interpretation of structured observations",
            "Credential leakage, duplicate submission, or paper/live environment confusion",
        ],
        human_owner="Course Learner, reviewed by Course Trainer",
    )


def _import_agents():
    from agents import Agent, Runner

    try:
        from agents.decorators import tool
    except ImportError:  # compatibility with older SDK releases
        from agents import function_tool as tool
    return Agent, Runner, tool


def _write_manifest(path: str | None, action: str, mode: str, model: str, output: Path, tools: list[str]) -> None:
    if not path:
        return
    write_json(
        path,
        {
            "course_code": "C177",
            "action": action,
            "mode": mode,
            "model": model,
            "created_at_utc": utc_now(),
            "tools_exposed": tools,
            "output_file": output.name,
            "output_sha256": sha256_file(output),
            "paper_only": True,
            "trading_client_exposed": False,
        },
    )


def run_draft(mode: str, output: Path, manifest: str | None) -> None:
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    if mode == "template":
        write_json(output, pydantic_dump(deterministic_hypothesis()))
        _write_manifest(manifest, "draft", mode, "none", output, [])
        print(f"TEMPLATE_WRITTEN: {output}")
        return

    Agent, Runner, tool = _import_agents()

    @tool
    def read_approved_course_source(source_name: str) -> str:
        """Read an approved C177 source. source_name must be scenario_brief or research_sources."""
        mapping = {
            "scenario_brief": REPO_ROOT / "labs" / "resources" / "scenario_brief.md",
            "research_sources": REPO_ROOT / "labs" / "resources" / "research_sources.md",
        }
        if source_name not in mapping:
            return "ERROR: source_name must be scenario_brief or research_sources"
        return mapping[source_name].read_text(encoding="utf-8")

    agent = Agent(
        name="C177 Bounded Trading Research Agent",
        model=model,
        instructions=(
            "You draft a structured educational research hypothesis, not financial advice. "
            "Call read_approved_course_source for BOTH scenario_brief and research_sources before answering. "
            "Preserve every fixed scenario field exactly: SPY, 1Day, 2018-01-01 to 2025-12-31, adjustment all, "
            "feed iex, America/New_York, 20/50 windows, long-only 0-or-1, 5 bps friction, split 2023-01-01, "
            "paper_only true, live_order_requested false. Separate evidence, assumptions, unknowns, risks, and "
            "rejection criteria. Never claim a return, suitability, or certainty. Return only the requested schema."
        ),
        tools=[read_approved_course_source],
        output_type=HypothesisSpec,
    )
    result = Runner.run_sync(agent, "Create C177 hypothesis version 1.0 from the two approved sources.")
    payload = pydantic_dump(result.final_output)
    write_json(output, payload)
    _write_manifest(manifest, "draft", mode, model, output, ["read_approved_course_source"])
    print(f"AGENT_DRAFT_WRITTEN: {output}")


REVIEW_FILES = {
    "review-data": "02-market-data/data_quality_report.json",
    "review-backtest": "03-backtest-audit/backtest_metrics.json",
    "review-ticket": "04-paper-trade/paper_order_ticket.json",
}


def _status_for(action: str, payload: dict) -> tuple[str, str, str]:
    if action == "review-data":
        status = str(payload.get("status", "HOLD_DATA"))
        return "data", status, status
    if action == "review-backtest":
        status = str(payload.get("deterministic_status", "HOLD"))
        return "backtest", status, status
    environment = payload.get("environment")
    status = "READY_FOR_HUMAN_REVIEW" if environment == "PAPER" and payload.get("symbol") == "SPY" else "HOLD"
    return "ticket", status, status


def run_review(action: str, mode: str, pack: Path, output: Path, manifest: str | None) -> None:
    relative = REVIEW_FILES[action]
    report_path = safe_within(pack, relative)
    if not report_path.exists():
        raise SystemExit(f"Required structured artifact not found: {report_path}")
    report = read_json(report_path)
    review_type, controlling, recommendation = _status_for(action, report)
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")

    if mode == "template":
        review = AgentReview(
            review_type=review_type,
            controlling_status=controlling,
            recommendation=recommendation,
            evidence_citations=[f"{relative}::$", f"{relative}::status", f"{relative}::structured_checks"],
            critical_observations=["The deterministic status controls the workflow.", "No numeric value was recalculated by the model."],
            limitations=["Template mode does not call a model.", "The artifact remains bounded to the course scenario."],
            next_allowed_action="Follow the deterministic status and obtain the named human review.",
        )
        write_json(output, pydantic_dump(review))
        _write_manifest(manifest, action, mode, "none", output, [])
        print(f"TEMPLATE_REVIEW_WRITTEN: {output}")
        return

    Agent, Runner, tool = _import_agents()

    @tool
    def read_structured_course_artifact(relative_path: str) -> str:
        """Read the one structured JSON artifact allowed for this review; other paths are refused."""
        if relative_path != relative:
            return f"ERROR: only {relative} is allowed for this review"
        return safe_within(pack, relative_path).read_text(encoding="utf-8")

    agent = Agent(
        name=f"C177 Read-Only {review_type.title()} Reviewer",
        model=model,
        instructions=(
            f"Review only {relative}. Call read_structured_course_artifact before answering. "
            f"The controlling status is the exact deterministic value '{controlling}'. Preserve it as both "
            "controlling_status and recommendation. Cite JSON paths and exact values; do not recalculate, "
            "rewrite, or improve a number. State limitations and a human-owned next action. Never recommend "
            "a live trade, expose credentials, or permit live action. Return only the requested schema."
        ),
        tools=[read_structured_course_artifact],
        output_type=AgentReview,
    )
    result = Runner.run_sync(agent, f"Review {relative} for the C177 verify-then-trust gate.")
    review = result.final_output
    if review.controlling_status != controlling or review.recommendation != controlling:
        raise SystemExit("HOLD_AGENT_REVIEW_CHANGED_CONTROLLING_STATUS")
    write_json(output, pydantic_dump(review))
    _write_manifest(manifest, action, mode, model, output, ["read_structured_course_artifact"])
    print(f"AGENT_REVIEW_WRITTEN: {output}")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)

    draft = sub.add_parser("draft")
    draft.add_argument("--mode", choices=["template", "agent"], required=True)
    draft.add_argument("--output", required=True)
    draft.add_argument("--manifest")

    for action in REVIEW_FILES:
        review = sub.add_parser(action)
        review.add_argument("--mode", choices=["template", "agent"], required=True)
        review.add_argument("--pack", required=True)
        review.add_argument("--output", required=True)
        review.add_argument("--manifest")

    args = parser.parse_args()
    output = Path(args.output)
    if args.action == "draft":
        run_draft(args.mode, output, args.manifest)
    else:
        run_review(args.action, args.mode, Path(args.pack).resolve(), output, args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
