"""Deterministic, causal C177 backtest and audit evidence generator."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from course_common import read_json, sha256_file, utc_now, write_json


def max_drawdown(returns: pd.Series) -> float:
    equity = (1.0 + returns.fillna(0.0)).cumprod()
    drawdown = equity / equity.cummax() - 1.0
    return float(drawdown.min()) if len(drawdown) else 0.0


def metrics(returns: pd.Series, turnover: pd.Series, position: pd.Series) -> dict:
    clean = returns.fillna(0.0)
    periods = int(len(clean))
    total = float((1.0 + clean).prod() - 1.0)
    annual = float((1.0 + total) ** (252.0 / periods) - 1.0) if periods > 0 and total > -1 else -1.0
    vol = float(clean.std(ddof=0) * math.sqrt(252.0)) if periods else 0.0
    sharpe = float(clean.mean() / clean.std(ddof=0) * math.sqrt(252.0)) if periods and clean.std(ddof=0) > 0 else 0.0
    entries = int(((position.diff().fillna(position) > 0)).sum())
    exits = int(((position.diff().fillna(position) < 0)).sum())
    return {
        "periods": periods,
        "total_return": total,
        "annualised_return": annual,
        "annualised_volatility": vol,
        "sharpe_ratio_rf0": sharpe,
        "maximum_drawdown": max_drawdown(clean),
        "turnover_units": float(turnover.fillna(0.0).sum()),
        "entry_count": entries,
        "exit_count": exits,
        "average_exposure": float(position.fillna(0.0).mean()) if periods else 0.0,
    }


def run_strategy(frame: pd.DataFrame, fast: int, slow: int, friction_bps: float) -> pd.DataFrame:
    result = frame.copy()
    result["daily_return"] = result["close"].pct_change().fillna(0.0)
    result["fast_sma"] = result["close"].rolling(fast, min_periods=fast).mean()
    result["slow_sma"] = result["close"].rolling(slow, min_periods=slow).mean()
    result["raw_signal"] = (result["fast_sma"] > result["slow_sma"]).astype(int)
    result.loc[result["slow_sma"].isna(), "raw_signal"] = 0
    result["expected_position"] = result["raw_signal"].shift(1).fillna(0).astype(int)
    result["position_used"] = result["expected_position"]
    result["turnover"] = result["position_used"].diff().abs().fillna(result["position_used"].abs())
    result["friction"] = result["turnover"] * (friction_bps / 10_000.0)
    result["strategy_return"] = result["position_used"] * result["daily_return"] - result["friction"]
    result["benchmark_return"] = result["daily_return"]
    result["strategy_equity"] = (1.0 + result["strategy_return"]).cumprod()
    result["benchmark_equity"] = (1.0 + result["benchmark_return"]).cumprod()
    return result


def section_metrics(result: pd.DataFrame, mask: pd.Series) -> tuple[dict, dict]:
    subset = result.loc[mask]
    strategy = metrics(subset["strategy_return"], subset["turnover"], subset["position_used"])
    benchmark = metrics(subset["benchmark_return"], pd.Series(0.0, index=subset.index), pd.Series(1.0, index=subset.index))
    strategy["benchmark_total_return_gap"] = strategy["total_return"] - benchmark["total_return"]
    return strategy, benchmark


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--quality-report", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    spec = read_json(args.hypothesis)
    quality = read_json(args.quality_report)
    data_hash = sha256_file(args.data)
    if quality.get("status") != "READY_FOR_BACKTEST":
        raise SystemExit("HOLD_BACKTEST: deterministic data status is not READY_FOR_BACKTEST")
    if quality.get("csv_sha256") != data_hash:
        raise SystemExit("HOLD_BACKTEST: CSV fingerprint does not match the accepted quality report")
    if spec.get("status") != "FROZEN_FOR_DATA" or spec.get("live_order_requested") is not False:
        raise SystemExit("HOLD_BACKTEST: hypothesis is not the frozen paper-only C177 specification")

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    frame = pd.read_csv(args.data, parse_dates=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    if len(frame) <= int(spec["slow_window"]):
        raise SystemExit("HOLD_BACKTEST: insufficient rows for the slow moving average")

    result = run_strategy(frame, int(spec["fast_window"]), int(spec["slow_window"]), float(spec["friction_bps"]))
    split = pd.Timestamp(spec["split_date"], tz="UTC")
    timestamps = pd.to_datetime(result["timestamp"], utc=True)
    development_mask = timestamps < split
    oos_mask = timestamps >= split
    full_mask = pd.Series(True, index=result.index)

    full_strategy, full_benchmark = section_metrics(result, full_mask)
    dev_strategy, dev_benchmark = section_metrics(result, development_mask)
    oos_strategy, oos_benchmark = section_metrics(result, oos_mask)

    causal_ok = bool((result["position_used"] == result["raw_signal"].shift(1).fillna(0).astype(int)).all())
    structural_checks = {
        "input_fingerprint_matches": True,
        "one_bar_signal_shift": causal_ok,
        "benchmark_present": True,
        "development_segment_present": int(development_mask.sum()) >= 252,
        "out_of_sample_segment_present": int(oos_mask.sum()) >= 252,
        "declared_friction_applied": float(spec["friction_bps"]) == 5.0,
    }
    continue_research = (
        all(structural_checks.values())
        and oos_strategy["entry_count"] >= 2
        and oos_strategy["maximum_drawdown"] >= -0.40
    )
    deterministic_status = "CONTINUE_RESEARCH" if continue_research else "HOLD"

    metrics_payload = {
        "course_code": "C177",
        "created_at_utc": utc_now(),
        "strategy": "SPY long-only 20/50-day SMA crossover",
        "friction_bps": float(spec["friction_bps"]),
        "split_date": spec["split_date"],
        "deterministic_status": deterministic_status,
        "status_reason": (
            "Structural checks are clean and the bounded out-of-sample evidence is sufficient for a paper-only operational exercise."
            if continue_research
            else "One or more structural, sample-size, or drawdown conditions require a hold."
        ),
        "structural_checks": structural_checks,
        "full": {"strategy": full_strategy, "benchmark": full_benchmark},
        "development": {"strategy": dev_strategy, "benchmark": dev_benchmark},
        "out_of_sample": {"strategy": oos_strategy, "benchmark": oos_benchmark},
        "limitations": [
            "Historical and out-of-sample results do not guarantee future performance.",
            "Daily bars and a basis-point friction model do not reproduce live order-book dynamics.",
            "One liquid ETF and one rule provide an educational workflow, not an investment conclusion.",
            "The free IEX feed has narrower coverage than a consolidated US market feed when that source mode is used.",
        ],
    }
    write_json(output / "backtest_metrics.json", metrics_payload)

    changes = result["position_used"].diff().fillna(result["position_used"])
    event_rows = result.loc[changes.ne(0), ["timestamp", "close", "position_used", "fast_sma", "slow_sma"]].copy()
    event_rows["event"] = np.where(event_rows["position_used"] > 0, "ENTRY", "EXIT")
    event_rows.to_csv(output / "trades.csv", index=False, lineterminator="\n")

    change_indexes = np.flatnonzero(changes.ne(0).to_numpy())
    sample_indexes: set[int] = set()
    for index in change_indexes[:8]:
        sample_indexes.update(i for i in range(max(0, index - 1), min(len(result), index + 2)))
    if not sample_indexes:
        sample_indexes.update(range(min(8, len(result))))
    sample_columns = [
        "timestamp",
        "close",
        "fast_sma",
        "slow_sma",
        "raw_signal",
        "expected_position",
        "position_used",
        "daily_return",
        "strategy_return",
    ]
    result.loc[sorted(sample_indexes), sample_columns].to_csv(
        output / "signal_sample.csv", index=False, lineterminator="\n"
    )
    result[[
        "timestamp",
        "close",
        "raw_signal",
        "position_used",
        "turnover",
        "strategy_return",
        "benchmark_return",
        "strategy_equity",
        "benchmark_equity",
    ]].to_csv(output / "equity_curve.csv", index=False, lineterminator="\n")

    plt.figure(figsize=(10, 5.5))
    plt.plot(timestamps, result["strategy_equity"], label="20/50 strategy after 5 bps turnover friction", linewidth=2)
    plt.plot(timestamps, result["benchmark_equity"], label="Buy-and-hold benchmark", linewidth=1.5)
    plt.axvline(split, color="#7c3aed", linestyle="--", linewidth=1.2, label="Out-of-sample begins")
    plt.title("C177 SPY Research Equity Curves - Educational Backtest")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1 (simulated)")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output / "equity_curve.png", dpi=160)
    plt.close()

    friction_cases = []
    for friction in spec["sensitivity_friction_bps"]:
        case = run_strategy(frame, 20, 50, float(friction))
        case_strategy, _ = section_metrics(case, pd.to_datetime(case["timestamp"], utc=True) >= split)
        friction_cases.append({"friction_bps": float(friction), "out_of_sample": case_strategy})
    parameter_cases = []
    for fast in (15, 20, 25):
        case = run_strategy(frame, fast, 50, float(spec["friction_bps"]))
        case_strategy, _ = section_metrics(case, pd.to_datetime(case["timestamp"], utc=True) >= split)
        parameter_cases.append({"fast_window": fast, "slow_window": 50, "out_of_sample": case_strategy})
    write_json(
        output / "sensitivity_report.json",
        {
            "course_code": "C177",
            "created_at_utc": utc_now(),
            "declared_case": {"fast_window": 20, "slow_window": 50, "friction_bps": 5.0},
            "friction_cases": friction_cases,
            "nearby_parameter_cases": parameter_cases,
            "selection_rule": "Report all cases; do not select a new winner during this frozen v1.0 run.",
        },
    )
    write_json(output / "strategy_spec.json", spec)
    write_json(
        output / "run_manifest.json",
        {
            "course_code": "C177",
            "created_at_utc": utc_now(),
            "hypothesis_sha256": sha256_file(args.hypothesis),
            "data_csv_sha256": data_hash,
            "quality_report_sha256": sha256_file(args.quality_report),
            "engine": "labs/resources/backtest_and_audit.py",
            "one_bar_shift": causal_ok,
            "deterministic_status": deterministic_status,
            "trial_count_this_run": 6,
            "paper_only": True,
        },
    )
    print(f"BACKTEST_STATUS: {deterministic_status}")
    print(f"one_bar_signal_shift={str(causal_ok).lower()}")
    print(f"out_of_sample_entries={oos_strategy['entry_count']}")
    print(f"out_of_sample_maximum_drawdown={oos_strategy['maximum_drawdown']:.6f}")
    return 0 if all(structural_checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
