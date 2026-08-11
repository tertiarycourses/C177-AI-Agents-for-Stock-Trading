"""Validate the fixed C177 HYPER hypothesis and report exact defects."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from course_common import find_unresolved, read_json, utc_now, write_json
from review_validation import field, unresolved, valid_utc
from trading_research_agent import HypothesisSpec


EXPECTED = {
    "course_code": "C177",
    "version": "1.0",
    "status": "FROZEN_FOR_DATA",
    "symbol": "SPY",
    "bar_interval": "1Day",
    "data_start": "2018-01-01",
    "data_end": "2025-12-31",
    "adjustment": "all",
    "feed": "iex",
    "timezone": "America/New_York",
    "fast_window": 20,
    "slow_window": 50,
    "position_state": "long_only_0_or_1",
    "friction_bps": 5.0,
    "split_date": "2023-01-01",
    "paper_only": True,
    "live_order_requested": False,
}


REQUIRED_EVIDENCE_ROWS = {
    "Course scope",
    "Agent design",
    "Market-data feed",
    "Paper limitations",
    "Position sizing",
}


def _section(text: str, title: str) -> str:
    match = re.search(
        rf"(?ims)^##\s+{re.escape(title)}[ \t]*$\n(.*?)(?=^##\s+|\Z)", text
    )
    return match.group(1) if match else ""


def validate_research_log(path: Path) -> tuple[list[str], list[dict[str, object]]]:
    if not path.is_file():
        return [f"missing research log: {path}"], [{"line": 0, "marker": "MISSING_RESEARCH_LOG"}]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    markers: list[dict[str, object]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        for marker in ("OWNER_TO_VERIFY", "SOURCE_NEEDED", "MODEL_GUESS"):
            if marker in line:
                markers.append({"line": number, "marker": marker})
    for label in ("Scenario", "Human owner", "Reviewer", "Paper-only boundary"):
        if unresolved(field(text, label)):
            errors.append(f"{label} is unresolved")

    questions = {
        int(match.group(1)): match.group(2).strip()
        for match in re.finditer(r"(?m)^\s*([1-3])\.[ \t]+(.+?)[ \t]*$", _section(text, "Questions the evidence must answer"))
    }
    for number in (1, 2, 3):
        if number not in questions or unresolved(questions[number]):
            errors.append(f"Evidence question {number} is unresolved")

    evidence_rows: dict[str, list[str]] = {}
    for line in _section(text, "Evidence table").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        columns = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(columns) == 6 and columns[0] in REQUIRED_EVIDENCE_ROWS:
            evidence_rows[columns[0]] = columns
    for name in sorted(REQUIRED_EVIDENCE_ROWS):
        columns = evidence_rows.get(name)
        if not columns:
            errors.append(f"Missing evidence row: {name}")
            continue
        _, url, accessed, scope, limitation, owner_decision = columns
        if not re.fullmatch(r"https?://\S+", url):
            errors.append(f"Evidence URL is invalid: {name}")
        try:
            date.fromisoformat(accessed)
        except ValueError:
            errors.append(f"Evidence access date is invalid: {name}")
        for label, value in (("scope", scope), ("limitation", limitation), ("owner decision", owner_decision)):
            if unresolved(value):
                errors.append(f"Evidence {label} is unresolved: {name}")

    assumptions = [
        match.group(1).strip()
        for match in re.finditer(r"(?m)^\s*-[ \t]+(.+?)[ \t]*$", _section(text, "Assumptions"))
    ]
    if not assumptions or any(unresolved(value) for value in assumptions):
        errors.append("Assumptions section needs at least one resolved statement")

    resolution_rows: list[list[str]] = []
    for line in _section(text, "Unknowns and resolutions").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        columns = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(columns) == 4 and columns[0] not in {"Unknown", "---"} and not set(columns[0]) <= {"-", ":"}:
            resolution_rows.append(columns)
    if not resolution_rows:
        errors.append("Unknowns and resolutions needs at least one completed row")
    for index, columns in enumerate(resolution_rows, start=1):
        if any(unresolved(value) for value in columns):
            errors.append(f"Unknown-resolution row {index} is incomplete")

    version_rows: list[list[str]] = []
    for line in _section(text, "Version log").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        columns = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(columns) == 5 and columns[0] == "1.0":
            version_rows.append(columns)
    if len(version_rows) != 1:
        errors.append("Version log needs exactly one completed v1.0 row")
    else:
        version, stamp, change, reason, owner = version_rows[0]
        if not valid_utc(stamp):
            errors.append("Version log timestamp must be ISO-8601 UTC")
        for label, value in (("change", change), ("reason", reason), ("owner", owner)):
            if unresolved(value):
                errors.append(f"Version log {label} is unresolved")
    errors.extend(f"unresolved marker {item['marker']} on line {item['line']}" for item in markers)
    return errors, markers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("hypothesis")
    parser.add_argument("--compare")
    parser.add_argument("--report")
    parser.add_argument("--research-log")
    parser.add_argument("--require-frozen", action="store_true")
    args = parser.parse_args()

    path = Path(args.hypothesis)
    raw = read_json(path)
    errors: list[str] = []
    try:
        HypothesisSpec.model_validate(raw)
        schema_valid = True
    except ValidationError as exc:
        schema_valid = False
        errors.extend(
            f"{'.'.join(str(part) for part in item['loc'])}: {item['msg']}" for item in exc.errors()
        )

    mismatches = {
        key: {"expected": expected, "actual": raw.get(key)}
        for key, expected in EXPECTED.items()
        if raw.get(key) != expected
    }
    unresolved = find_unresolved(raw)
    log_unresolved: list[dict[str, object]] = []
    research_log_errors: list[str] = []
    if args.research_log:
        log_path = Path(args.research_log)
        research_log_errors, log_unresolved = validate_research_log(log_path)
    elif args.require_frozen:
        research_log_errors = ["--research-log is required with --require-frozen"]
    if args.compare:
        comparison = read_json(args.compare)
        comparison_mismatches = {
            key: {"template": comparison.get(key), "actual": raw.get(key)}
            for key in EXPECTED
            if comparison.get(key) != raw.get(key)
        }
    else:
        comparison_mismatches = {}

    frozen = schema_valid and not mismatches and not unresolved and not research_log_errors
    report = {
        "course_code": "C177",
        "checked_at_utc": utc_now(),
        "hypothesis_file": path.as_posix(),
        "schema_valid": schema_valid,
        "schema_errors": errors,
        "fixed_field_mismatches": mismatches,
        "comparison_mismatches": comparison_mismatches,
        "unresolved_count": len(unresolved),
        "unresolved_paths": unresolved,
        "research_log_checked": bool(args.research_log),
        "research_log_unresolved_count": len(log_unresolved),
        "research_log_unresolved": log_unresolved,
        "research_log_valid": bool(args.research_log) and not research_log_errors,
        "research_log_errors": research_log_errors,
        "live_order_requested": raw.get("live_order_requested"),
        "status": raw.get("status"),
        "frozen_for_data": frozen,
    }
    if args.report:
        write_json(args.report, report)
    print(f"schema_valid={str(schema_valid).lower()}")
    print(f"unresolved_count={len(unresolved)}")
    print(f"research_log_unresolved_count={len(log_unresolved)}")
    print(f"research_log_error_count={len(research_log_errors)}")
    for error in research_log_errors:
        print(f"research_log_error={error}")
    print(f"fixed_field_mismatches={len(mismatches)}")
    print(f"status={raw.get('status')}")
    print("FROZEN_FOR_DATA" if frozen else "HOLD_HYPOTHESIS")

    if args.require_frozen and not frozen:
        return 1
    return 0 if schema_valid and not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
