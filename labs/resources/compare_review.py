"""Compare deterministic, agent, and optional human C177 gate decisions."""

from __future__ import annotations

import argparse
from pathlib import Path

from course_common import read_json
from review_validation import validate_backtest_audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--review", required=True)
    parser.add_argument("--human")
    args = parser.parse_args()

    report = read_json(args.report)
    review = read_json(args.review)
    deterministic = str(report.get("deterministic_status", report.get("status", "HOLD")))
    controlling = str(review.get("controlling_status", ""))
    recommendation = str(review.get("recommendation", ""))
    aligned = deterministic == controlling == recommendation
    print(f"deterministic={deterministic}")
    print(f"agent_controlling_status={controlling}")
    print(f"agent_recommendation={recommendation}")

    if args.human:
        pack = Path(args.report).resolve().parent.parent
        human, human_errors = validate_backtest_audit(args.human, pack)
        print(f"human_decision={human}")
        for error in human_errors:
            print(f"human_audit_error={error}")
        aligned = aligned and not human_errors and human == deterministic

    print("REVIEW_ALIGNED" if aligned else "HOLD_REVIEW_DISAGREEMENT")
    return 0 if aligned else 1


if __name__ == "__main__":
    raise SystemExit(main())
