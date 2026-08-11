"""Strict Markdown gate validation for the C177 human review records."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from course_common import sha256_file


UNRESOLVED = ("OWNER_TO_VERIFY", "SOURCE_NEEDED", "MODEL_GUESS", "<", "VERIFY")


def field(text: str, label: str) -> str:
    match = re.search(rf"(?im)^[ \t]*(?:-[ \t]*)?{re.escape(label)}:[ \t]*(.*?)[ \t]*$", text)
    return match.group(1).strip().strip("`") if match else ""


def unresolved(value: str) -> bool:
    return not value.strip() or any(marker in value for marker in UNRESOLVED)


def valid_utc(value: str) -> bool:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() == timezone.utc.utcoffset(parsed)


def _sha(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))


AUDIT_CHECKS = {
    "Frozen v1.0 rules used",
    "Data status READY_FOR_BACKTEST",
    "Position shifted one bar",
    "No impossible OHLCV rows",
    "Buy-and-hold benchmark present",
    "Development and out-of-sample sections present",
    "Zero, 5, and 10 bps friction cases present",
    "15/50, 20/50, and 25/50 stability cases present",
    "Trial count recorded",
    "Limitations recorded",
}


def validate_backtest_audit(path: str | Path, pack: str | Path) -> tuple[str, list[str]]:
    review_path = Path(path)
    if not review_path.is_file():
        return "MISSING", [f"missing human audit: {review_path}"]
    text = review_path.read_text(encoding="utf-8")
    base = Path(pack).resolve()
    errors: list[str] = []
    initials = field(text, "Auditor initials")
    stamp = field(text, "UTC time")
    hypothesis_hash = field(text, "Hypothesis SHA-256")
    market_hash = field(text, "Market-data CSV SHA-256")
    code_version = field(text, "Code or repository commit")
    if unresolved(initials):
        errors.append("Auditor initials is unresolved")
    if not valid_utc(stamp):
        errors.append("UTC time must be an ISO-8601 UTC timestamp")
    expected_hypothesis = sha256_file(base / "01-hypothesis" / "hypothesis_spec.json")
    expected_market = sha256_file(base / "02-market-data" / "spy_daily.csv")
    if not _sha(hypothesis_hash) or hypothesis_hash != expected_hypothesis:
        errors.append("Hypothesis SHA-256 does not match the frozen input")
    if not _sha(market_hash) or market_hash != expected_market:
        errors.append("Market-data CSV SHA-256 does not match the accepted input")
    if unresolved(code_version):
        errors.append("Code or repository commit is unresolved")

    seen: set[str] = set()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        columns = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(columns) != 4 or columns[0] not in AUDIT_CHECKS:
            continue
        name, evidence, result, note = columns
        seen.add(name)
        if unresolved(evidence):
            errors.append(f"Audit evidence is unresolved: {name}")
        if result != "PASS":
            errors.append(f"Audit result must be PASS: {name}")
        if unresolved(note):
            errors.append(f"Auditor note is unresolved: {name}")
    for name in sorted(AUDIT_CHECKS - seen):
        errors.append(f"Missing audit check row: {name}")

    for label in (
        "Evidence that supports continued paper research",
        "Evidence that weakens the hypothesis",
        "What the backtest cannot establish",
        "Agent-review disagreements",
        "Reason",
        "Next permissible action",
    ):
        if unresolved(field(text, label)):
            errors.append(f"{label} is unresolved")
    owner = field(text, "Owner and UTC time")
    if unresolved(owner) or not re.search(r"\d{4}-\d{2}-\d{2}T[^\s]+(?:Z|\+00:00)", owner):
        errors.append("Owner and UTC time is unresolved or not UTC")
    decision = field(text, "Decision") or "MISSING"
    if decision not in {"CONTINUE_RESEARCH", "HOLD", "REVISE"}:
        errors.append("Decision is not an allowed audit value")
    return decision, errors


def _as_float(value: str, label: str, errors: list[str]) -> float | None:
    try:
        return float(value)
    except ValueError:
        errors.append(f"{label} is not numeric")
        return None


def validate_paper_approval(
    path: str | Path,
    ticket: dict[str, Any],
    calculation: dict[str, Any],
) -> tuple[str, list[str]]:
    review_path = Path(path)
    if not review_path.is_file():
        return "MISSING", [f"missing human paper review: {review_path}"]
    text = review_path.read_text(encoding="utf-8")
    errors: list[str] = []
    values = {
        label: field(text, label)
        for label in (
            "Reviewer initials",
            "UTC time",
            "Environment confirmed",
            "Symbol",
            "Side",
            "Quantity",
            "Entry reference",
            "Stop reference",
            "Risk fraction",
            "Active quantity cap",
            "Deterministic research decision",
            "Agent ticket review",
            "Hypothesis manifest SHA-256",
            "Market-data manifest SHA-256",
            "Backtest manifest SHA-256",
            "Evidence fingerprints verified",
            "Paper dashboard open",
            "Reason",
        )
    }
    for label, value in values.items():
        if unresolved(value):
            errors.append(f"{label} is unresolved")
    if not valid_utc(values["UTC time"]):
        errors.append("UTC time must be an ISO-8601 UTC timestamp")
    expected_text = {
        "Environment confirmed": "PAPER",
        "Symbol": str(ticket.get("symbol")),
        "Side": str(ticket.get("side")),
        "Deterministic research decision": "CONTINUE_RESEARCH",
        "Agent ticket review": "READY_FOR_HUMAN_REVIEW",
        "Evidence fingerprints verified": "YES",
        "Paper dashboard open": "YES",
    }
    for label, expected in expected_text.items():
        if values[label] != expected:
            errors.append(f"{label} must equal {expected}")
    try:
        if int(values["Quantity"]) != int(ticket.get("quantity", 0)):
            errors.append("Quantity does not match the ticket")
    except ValueError:
        errors.append("Quantity is not an integer")
    for label, expected in (
        ("Entry reference", calculation.get("entry_reference")),
        ("Stop reference", calculation.get("stop_reference")),
        ("Risk fraction", calculation.get("risk_fraction")),
    ):
        observed = _as_float(values[label], label, errors)
        if observed is not None and (expected is None or abs(observed - float(expected)) > 1e-8):
            errors.append(f"{label} does not match the risk calculation")
    caps = {
        "raw_risk_quantity": int(calculation.get("raw_risk_quantity", 0)),
        "exposure_cap_quantity": int(calculation.get("exposure_cap_quantity", 0)),
        "buying_power_cap_quantity": int(calculation.get("buying_power_cap_quantity", 0)),
        "hard_max_quantity": int(calculation.get("hard_max_quantity", 0)),
    }
    active_name, active_value = min(caps.items(), key=lambda item: item[1])
    if values["Active quantity cap"] != f"{active_name}={active_value}":
        errors.append(f"Active quantity cap must equal {active_name}={active_value}")
    evidence = ticket.get("evidence", {})
    hash_fields = {
        "Hypothesis manifest SHA-256": "hypothesis_fingerprints_sha256",
        "Market-data manifest SHA-256": "market_data_fingerprints_sha256",
        "Backtest manifest SHA-256": "backtest_fingerprints_sha256",
    }
    for label, key in hash_fields.items():
        if not _sha(values[label]) or values[label] != evidence.get(key):
            errors.append(f"{label} does not match the ticket")
    decision = field(text, "Decision") or "MISSING"
    if decision not in {"APPROVE_PAPER_EXERCISE", "HOLD"}:
        errors.append("Decision is not an allowed paper-review value")
    return decision, errors
