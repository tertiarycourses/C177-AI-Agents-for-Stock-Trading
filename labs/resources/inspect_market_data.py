"""Print bounded head/tail rows and independent OHLCV checks."""

from __future__ import annotations

import argparse

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--head", type=int, default=3)
    parser.add_argument("--tail", type=int, default=3)
    args = parser.parse_args()
    frame = pd.read_csv(args.csv, parse_dates=["timestamp"])
    invalid = (
        (frame["high"] < frame[["open", "close"]].max(axis=1))
        | (frame["low"] > frame[["open", "close"]].min(axis=1))
        | (frame["high"] < frame["low"])
        | (frame["volume"] < 0)
    )
    print("FIRST_ROWS")
    print(frame.head(args.head).to_string(index=False))
    print("LAST_ROWS")
    print(frame.tail(args.tail).to_string(index=False))
    print(f"ordered={frame['timestamp'].is_monotonic_increasing}")
    print(f"duplicate_timestamps={int(frame['timestamp'].duplicated().sum())}")
    print(f"invalid_ohlcv_rows={int(invalid.sum())}")
    ok = frame["timestamp"].is_monotonic_increasing and not frame["timestamp"].duplicated().any() and not invalid.any()
    print("MARKET_DATA_SPOT_CHECK_OK" if ok else "HOLD_MARKET_DATA_SPOT_CHECK")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
