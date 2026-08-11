"""Verify that each displayed C177 position equals the prior bar's raw signal."""

from __future__ import annotations

import argparse

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("signal_sample")
    args = parser.parse_args()
    frame = pd.read_csv(args.signal_sample)
    required = {"timestamp", "raw_signal", "expected_position", "position_used"}
    if not required.issubset(frame.columns):
        print(f"HOLD_SIGNAL_SAMPLE: missing={sorted(required - set(frame.columns))}")
        return 1
    displayed_mismatch = frame["expected_position"].astype(int) != frame["position_used"].astype(int)
    prior_signal = frame["raw_signal"].shift(1)
    independent_rows = prior_signal.notna()
    independent_mismatch = (
        frame.loc[independent_rows, "position_used"].astype(int)
        != prior_signal.loc[independent_rows].astype(int)
    )
    print(frame.to_string(index=False))
    print(f"displayed_rows={len(frame)}")
    print(f"displayed_expected_mismatches={int(displayed_mismatch.sum())}")
    print(f"independent_prior_signal_mismatches={int(independent_mismatch.sum())}")
    causal = not displayed_mismatch.any() and not independent_mismatch.any()
    print("CAUSAL_TIMING_OK" if causal else "HOLD_LOOK_AHEAD_RISK")
    return 0 if causal else 1


if __name__ == "__main__":
    raise SystemExit(main())
