"""Create the final C177 manifest only after every evidence gate resolves."""

from __future__ import annotations

import argparse
from pathlib import Path

from course_common import checkpoint_errors, read_json, scan_secret_hits, sha256_file, utc_now, write_json
from review_validation import field, validate_backtest_audit, validate_paper_approval


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack")
    args = parser.parse_args()
    pack = Path(args.pack).resolve()
    lab4 = pack / "04-paper-trade"
    lab4.mkdir(parents=True, exist_ok=True)
    hits = scan_secret_hits(pack)
    defects: list[str] = []
    checkpoints = {}
    for folder in ("01-hypothesis", "02-market-data", "03-backtest-audit"):
        root = pack / folder
        manifest = root / "fingerprints.json"
        errors = checkpoint_errors(root)
        if errors:
            defects.extend(f"{folder}: {error}" for error in errors)
        checkpoints[folder] = {
            "manifest": manifest.relative_to(pack).as_posix(),
            "manifest_sha256": sha256_file(manifest) if manifest.exists() else None,
            "verified": not errors,
        }

    audit_decision, audit_errors = validate_backtest_audit(
        pack / "03-backtest-audit" / "audit_log.md", pack
    )
    defects.extend(f"human audit: {error}" for error in audit_errors)
    ticket_path = lab4 / "paper_order_ticket.json"
    calculation_path = lab4 / "risk_calculation.json"
    review_path = lab4 / "ticket_agent_review.json"
    approval_path = lab4 / "human_approval.md"
    for required in (ticket_path, calculation_path, review_path, approval_path):
        if not required.is_file():
            defects.append(f"missing Lab 4 gate file: {required.name}")

    approval_decision = "MISSING"
    if ticket_path.is_file() and calculation_path.is_file() and approval_path.is_file():
        ticket = read_json(ticket_path)
        calculation = read_json(calculation_path)
        approval_decision, approval_errors = validate_paper_approval(approval_path, ticket, calculation)
        defects.extend(f"human paper review: {error}" for error in approval_errors)
        evidence = ticket.get("evidence", {})
        current = {
            "hypothesis_fingerprints_sha256": checkpoints["01-hypothesis"]["manifest_sha256"],
            "market_data_fingerprints_sha256": checkpoints["02-market-data"]["manifest_sha256"],
            "backtest_fingerprints_sha256": checkpoints["03-backtest-audit"]["manifest_sha256"],
            "risk_calculation_sha256": sha256_file(calculation_path),
        }
        for key, expected in current.items():
            if evidence.get(key) != expected:
                defects.append(f"ticket evidence hash mismatch: {key}")
    if review_path.is_file():
        review = read_json(review_path)
        if review.get("controlling_status") != "READY_FOR_HUMAN_REVIEW" or review.get("recommendation") != "READY_FOR_HUMAN_REVIEW":
            defects.append("agent ticket review is not READY_FOR_HUMAN_REVIEW")

    receipt = lab4 / "paper_order_receipt.json"
    error = lab4 / "paper_submission_error.json"
    attempt = lab4 / "submission_attempt.json"
    reconciliation = lab4 / "reconciliation_log.md"
    rollback = lab4 / "rollback_record.md"
    reconciliation_status = field(reconciliation.read_text(encoding="utf-8"), "Reconciliation status") if reconciliation.exists() else "MISSING"
    rollback_resolved = field(rollback.read_text(encoding="utf-8"), "Resolved") if rollback.exists() else "MISSING"
    attempt_state = read_json(attempt).get("state") if attempt.exists() else "MISSING"
    receipt_ok = receipt.exists() and reconciliation_status == "CONFIRMED" and attempt_state == "RECONCILED"
    error_ok = False
    if error.exists():
        error_payload = read_json(error)
        error_ok = (
            error_payload.get("resolved") is True
            and error_payload.get("resolution") == "CONFIRMED_NO_ORDER"
            and reconciliation_status == "CONFIRMED_NO_ORDER"
            and attempt_state == "RECONCILED_NO_ORDER"
        )
    if not (receipt_ok or error_ok):
        defects.append("execution evidence is neither a reconciled paper receipt nor a confirmed-no-order error")
    if rollback_resolved != "YES":
        defects.append("rollback state is not resolved")
    if audit_decision != "CONTINUE_RESEARCH":
        defects.append("human audit does not permit continued paper research")
    if approval_decision != "APPROVE_PAPER_EXERCISE":
        defects.append("human paper review does not approve the bounded exercise")
    if hits:
        defects.append(f"secret scan found {len(hits)} hit(s)")

    payload = {
        "course_code": "C177",
        "created_at_utc": utc_now(),
        "scope": "bounded educational research and paper-only execution evidence",
        "checkpoints": checkpoints,
        "human_audit_decision": audit_decision,
        "human_paper_decision": approval_decision,
        "paper_receipt_present": receipt.exists(),
        "paper_receipt_sha256": sha256_file(receipt) if receipt.exists() else None,
        "paper_error_present": error.exists(),
        "paper_error_sha256": sha256_file(error) if error.exists() else None,
        "reconciliation_status": reconciliation_status,
        "rollback_resolved": rollback_resolved,
        "secret_hits": len(hits),
        "secret_hit_locations": hits,
        "live_order_path_present": False,
        "release_defects": defects,
        "final_status": "PACK_READY" if not defects else "HOLD_FINAL_PACK",
        "limitations": [
            "The pack is an educational record, not financial advice.",
            "Historical results and paper fills do not guarantee live behaviour or future performance.",
            "Any change to a source, model, prompt, rule, dataset, code file, limit, account, or provider requires the relevant gates to be rerun.",
        ],
    }
    write_json(lab4 / "final_manifest.json", payload)
    print(f"secret_hits={len(hits)}")
    for defect in defects:
        print(f"release_defect={defect}")
    print(payload["final_status"])
    return 0 if payload["final_status"] == "PACK_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
