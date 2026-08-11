"""Fetch authorised SPY daily bars or create a labelled synthetic rejoin set, then validate them."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from course_common import is_placeholder, read_json, sha256_file, utc_now, write_json


REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def synthetic_bars(start: str, end: str) -> pd.DataFrame:
    dates = pd.bdate_range(start=start, end=end, tz="UTC")
    rng = np.random.default_rng(177)
    cycle = 0.0009 * np.sin(np.arange(len(dates)) / 45.0)
    shocks = rng.normal(0.00025, 0.0105, len(dates)) + cycle
    close = 250.0 * np.exp(np.cumsum(shocks))
    overnight = rng.normal(0.0, 0.0025, len(dates))
    open_ = close * (1.0 + overnight)
    spread = np.abs(rng.normal(0.006, 0.002, len(dates)))
    high = np.maximum(open_, close) * (1.0 + spread)
    low = np.minimum(open_, close) * (1.0 - spread)
    volume = rng.integers(35_000_000, 140_000_000, len(dates), endpoint=False)
    return pd.DataFrame(
        {
            "timestamp": dates,
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "trade_count": rng.integers(100_000, 600_000, len(dates), endpoint=False),
            "vwap": (open_ + high + low + close) / 4.0,
        }
    )


def alpaca_bars(spec: dict) -> pd.DataFrame:
    key = os.getenv("ALPACA_API_KEY")
    secret = os.getenv("ALPACA_SECRET_KEY")
    if is_placeholder(key) or is_placeholder(secret):
        raise SystemExit("HOLD_DATA: Alpaca paper credentials are missing or placeholders")
    if os.getenv("ALPACA_PAPER_ONLY", "").lower() != "true":
        raise SystemExit("HOLD_DATA: ALPACA_PAPER_ONLY must remain true")

    from alpaca.data.enums import Adjustment, DataFeed
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame

    client = StockHistoricalDataClient(key, secret)
    request = StockBarsRequest(
        symbol_or_symbols=[spec["symbol"]],
        timeframe=TimeFrame.Day,
        start=datetime.fromisoformat(spec["data_start"]).replace(tzinfo=timezone.utc),
        end=(datetime.fromisoformat(spec["data_end"]).replace(tzinfo=timezone.utc) + pd.Timedelta(days=1)),
        adjustment=Adjustment.ALL,
        feed=DataFeed.IEX,
    )
    frame = client.get_stock_bars(request).df.copy()
    if frame.empty:
        raise SystemExit("HOLD_DATA: Alpaca returned no bars")
    if isinstance(frame.index, pd.MultiIndex):
        if "symbol" in frame.index.names:
            frame = frame.xs(spec["symbol"], level="symbol")
        else:
            frame = frame.droplevel(0)
    frame = frame.reset_index()
    if "index" in frame.columns and "timestamp" not in frame.columns:
        frame = frame.rename(columns={"index": "timestamp"})
    for optional in ("trade_count", "vwap"):
        if optional not in frame.columns:
            frame[optional] = np.nan
    return frame[["timestamp", "open", "high", "low", "close", "volume", "trade_count", "vwap"]]


def validate(frame: pd.DataFrame, spec: dict, contract: dict, csv_hash: str) -> dict:
    checks: list[dict] = []

    def add(name: str, ok: bool, critical: bool, details: str) -> None:
        checks.append({"name": name, "ok": bool(ok), "critical": critical, "details": details})

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    add("required_schema", not missing_columns, True, f"missing_columns={missing_columns}")
    timestamps = pd.to_datetime(frame.get("timestamp"), utc=True, errors="coerce")
    duplicate_count = int(timestamps.duplicated().sum())
    missing_required = int(frame[REQUIRED_COLUMNS].isna().sum().sum()) if not missing_columns else -1
    monotonic = bool(timestamps.is_monotonic_increasing)

    numeric = frame[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric, errors="coerce")
    invalid_ohlc = int(
        (
            (numeric["high"] < numeric[["open", "close"]].max(axis=1))
            | (numeric["low"] > numeric[["open", "close"]].min(axis=1))
            | (numeric["high"] < numeric["low"])
            | (numeric[["open", "high", "low", "close"]] <= 0).any(axis=1)
        ).sum()
    )
    negative_volume = int((numeric["volume"] < 0).sum())
    row_count = int(len(frame))
    start_gap = abs((timestamps.min().date() - datetime.fromisoformat(spec["data_start"]).date()).days)
    end_gap = abs((datetime.fromisoformat(spec["data_end"]).date() - timestamps.max().date()).days)
    day_gaps = timestamps.sort_values().diff().dt.total_seconds().div(86400)
    long_gap_count = int((day_gaps > 7).sum())

    add("ordered_timestamps", monotonic, True, f"monotonic_increasing={monotonic}")
    add("unique_timestamps", duplicate_count == 0, True, f"duplicate_timestamps={duplicate_count}")
    add("required_values", missing_required == 0, True, f"missing_required_values={missing_required}")
    add("ohlc_consistency", invalid_ohlc == 0, True, f"invalid_ohlc_rows={invalid_ohlc}")
    add("non_negative_volume", negative_volume == 0, True, f"negative_volume_rows={negative_volume}")
    add("minimum_history", row_count >= 252, True, f"row_count={row_count}")
    add("requested_date_coverage", start_gap <= 10 and end_gap <= 10, True, f"start_gap_days={start_gap}; end_gap_days={end_gap}")
    add("unexpected_long_calendar_gaps", long_gap_count == 0, False, f"gaps_over_7_days={long_gap_count}")
    add(
        "complete_data_contract",
        all(contract.get(key) not in (None, "") for key in ("provider", "endpoint", "feed", "symbol", "interval", "adjustment", "retrieved_at_utc", "intended_use")),
        True,
        "required lineage fields present",
    )
    add("csv_fingerprint", len(csv_hash) == 64, True, f"csv_sha256={csv_hash}")

    critical_failures = [check for check in checks if check["critical"] and not check["ok"]]
    warnings = [check for check in checks if not check["critical"] and not check["ok"]]
    return {
        "course_code": "C177",
        "created_at_utc": utc_now(),
        "status": "READY_FOR_BACKTEST" if not critical_failures else "HOLD_DATA",
        "critical_failures": len(critical_failures),
        "warnings": len(warnings),
        "row_count": row_count,
        "first_timestamp": timestamps.min().isoformat(),
        "last_timestamp": timestamps.max().isoformat(),
        "duplicate_timestamps": duplicate_count,
        "missing_required_values": missing_required,
        "invalid_ohlc_rows": invalid_ohlc,
        "negative_volume_rows": negative_volume,
        "long_calendar_gaps": long_gap_count,
        "csv_sha256": csv_hash,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--source", choices=["alpaca", "synthetic"], required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    spec = read_json(args.hypothesis)
    if spec.get("status") != "FROZEN_FOR_DATA" or spec.get("symbol") != "SPY":
        raise SystemExit("HOLD_DATA: hypothesis is not the frozen C177 SPY specification")
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    if args.source == "alpaca":
        frame = alpaca_bars(spec)
        provider = "Alpaca Market Data API"
        endpoint = "StockHistoricalDataClient.get_stock_bars"
        intended = "Educational SPY daily-bar research using the declared IEX feed; not an executable-price guarantee"
    else:
        frame = synthetic_bars(spec["data_start"], spec["data_end"])
        provider = "C177 deterministic synthetic rejoin generator"
        endpoint = "labs/resources/fetch_validate_data.py::synthetic_bars"
        intended = "Synthetic rejoin and software-verification data only; not real market data and not evidence about SPY performance"

    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True).map(lambda value: value.isoformat())
    frame = frame.sort_values("timestamp").reset_index(drop=True)
    csv_path = output / "spy_daily.csv"
    frame.to_csv(csv_path, index=False, lineterminator="\n")
    csv_hash = sha256_file(csv_path)

    contract = {
        "course_code": "C177",
        "provider": provider,
        "endpoint": endpoint,
        "feed": "iex" if args.source == "alpaca" else "synthetic",
        "entitlement_scope": "Single-exchange IEX coverage" if args.source == "alpaca" else "No market entitlement; generated values",
        "symbol": spec["symbol"],
        "asset_type": spec["asset_type"],
        "currency": "USD",
        "interval": spec["bar_interval"],
        "requested_start": spec["data_start"],
        "requested_end": spec["data_end"],
        "response_timezone": "UTC",
        "exchange_timezone": spec["timezone"],
        "session": "US regular-session daily aggregation as defined by provider" if args.source == "alpaca" else "Synthetic business-day calendar",
        "adjustment": spec["adjustment"] if args.source == "alpaca" else "synthetic series; no corporate actions",
        "retrieved_at_utc": utc_now(),
        "transformations": ["sorted by timestamp", "selected standard OHLCV columns", "timestamp serialised as ISO-8601 UTC"],
        "intended_use": intended,
        "csv_file": csv_path.name,
        "csv_sha256": csv_hash,
    }
    write_json(output / "market_data_contract.json", contract)
    report = validate(frame, spec, contract, csv_hash)
    write_json(output / "data_quality_report.json", report)
    write_json(
        output / "retrieval_manifest.json",
        {
            "course_code": "C177",
            "created_at_utc": utc_now(),
            "source_mode": args.source,
            "hypothesis_file": Path(args.hypothesis).as_posix(),
            "hypothesis_sha256": sha256_file(args.hypothesis),
            "outputs": ["spy_daily.csv", "market_data_contract.json", "data_quality_report.json"],
            "paper_only": True,
        },
    )
    print(f"DATA_STATUS: {report['status']}")
    print(f"rows={report['row_count']}")
    print(f"csv_sha256={csv_hash}")
    return 0 if report["status"] == "READY_FOR_BACKTEST" else 1


if __name__ == "__main__":
    raise SystemExit(main())
