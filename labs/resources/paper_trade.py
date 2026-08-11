"""Risk sizing and hard-wired Alpaca paper-order workflow for C177.

There is deliberately no live-mode option. The trading client is always created
with paper=True, SPY is the only allowed symbol, and every consequential command
re-verifies immutable checkpoints, exact ticket evidence, and complete reviews.
"""

from __future__ import annotations

import argparse
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from course_common import (
    is_placeholder,
    pydantic_dump,
    read_json,
    require_checkpoint,
    sha256_file,
    utc_now,
    write_json,
)
from review_validation import validate_backtest_audit, validate_paper_approval


ALLOWED_SYMBOLS = {"SPY"}
APPROVAL_TOKEN = "C177-PAPER-APPROVED"
OPEN_STATUSES = {
    "new",
    "accepted",
    "pending_new",
    "partially_filled",
    "accepted_for_bidding",
    "stopped",
}
TERMINAL_STATUSES = {"filled", "canceled", "expired", "rejected", "replaced", "suspended", "calculated", "done_for_day"}


def _normalise_status(value: object) -> str:
    return str(value or "unknown").lower().split(".")[-1]


def _verified_manifests(pack: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for folder in ("01-hypothesis", "02-market-data", "03-backtest-audit"):
        manifest = require_checkpoint(pack / folder, folder)
        hashes[folder] = sha256_file(manifest)
    return hashes


def check_gate(pack: Path) -> dict:
    manifest_hashes = _verified_manifests(pack)
    metrics_path = pack / "03-backtest-audit" / "backtest_metrics.json"
    metrics = read_json(metrics_path)
    deterministic = metrics.get("deterministic_status")
    audit_path = pack / "03-backtest-audit" / "audit_log.md"
    human, audit_errors = validate_backtest_audit(audit_path, pack)
    if audit_errors:
        raise SystemExit("HOLD_GATE: incomplete human backtest audit: " + "; ".join(audit_errors))
    if deterministic != "CONTINUE_RESEARCH" or human != "CONTINUE_RESEARCH":
        raise SystemExit(
            f"HOLD_GATE: deterministic={deterministic}; human={human}; both must equal CONTINUE_RESEARCH"
        )
    data = read_json(pack / "02-market-data" / "data_quality_report.json")
    if data.get("status") != "READY_FOR_BACKTEST":
        raise SystemExit("HOLD_GATE: market data is not READY_FOR_BACKTEST")
    print("CHECKPOINTS_VERIFIED: Labs 1-3")
    print("PAPER_EXERCISE_GATE_READY")
    return {
        "deterministic": deterministic,
        "human": human,
        "metrics": metrics,
        "manifest_hashes": manifest_hashes,
    }


def _paper_credentials() -> tuple[str, str]:
    if os.getenv("ALPACA_PAPER_ONLY", "").strip().lower() != "true":
        raise SystemExit("HOLD_PAPER: ALPACA_PAPER_ONLY must equal true")
    key = os.getenv("ALPACA_API_KEY")
    secret = os.getenv("ALPACA_SECRET_KEY")
    if is_placeholder(key) or is_placeholder(secret):
        raise SystemExit("HOLD_PAPER: paper credentials are missing or placeholders")
    return str(key), str(secret)


def _paper_client():
    key, secret = _paper_credentials()
    from alpaca.trading.client import TradingClient

    return TradingClient(key, secret, paper=True)


def prepare(args, pack: Path) -> None:
    gate = check_gate(pack)
    frame_path = pack / "02-market-data" / "spy_daily.csv"
    import pandas as pd

    frame = pd.read_csv(frame_path)
    entry = float(frame.iloc[-1]["close"])
    if entry <= 0:
        raise SystemExit("HOLD_PAPER: invalid entry reference")

    if args.paper_equity is not None:
        equity = float(args.paper_equity)
        buying_power = equity
        account_source = "trainer-supplied offline paper value"
    else:
        account = _paper_client().get_account()
        account_payload = pydantic_dump(account)
        equity = float(account_payload.get("equity") or account_payload.get("cash") or 0)
        buying_power = float(account_payload.get("buying_power") or equity)
        account_source = "Alpaca paper account"
    if equity <= 0 or buying_power <= 0:
        raise SystemExit("HOLD_PAPER: paper equity and buying power must be positive")

    if not (0 < args.risk_fraction <= 0.005):
        raise SystemExit("HOLD_PAPER: risk fraction must be positive and no greater than 0.005")
    if not (0 < args.stop_percent <= 0.02):
        raise SystemExit("HOLD_PAPER: stop percent must be positive and no greater than 0.02")
    if not (0 < args.max_exposure_fraction <= 0.10):
        raise SystemExit("HOLD_PAPER: exposure fraction must be positive and no greater than 0.10")
    if not (1 <= args.hard_max_qty <= 20):
        raise SystemExit("HOLD_PAPER: hard maximum quantity must be between 1 and 20")

    stop = entry * (1.0 - args.stop_percent)
    per_share_risk = entry - stop
    risk_budget = equity * args.risk_fraction
    raw_risk_qty = math.floor(risk_budget / per_share_risk)
    exposure_qty = math.floor((equity * args.max_exposure_fraction) / entry)
    buying_power_qty = math.floor(buying_power / entry)
    final_qty = min(raw_risk_qty, exposure_qty, buying_power_qty, args.hard_max_qty)
    if final_qty <= 0:
        raise SystemExit("HOLD_PAPER: calculated quantity is not positive")

    output = pack / "04-paper-trade"
    output.mkdir(parents=True, exist_ok=True)
    calculation = {
        "course_code": "C177",
        "created_at_utc": utc_now(),
        "environment": "PAPER",
        "account_source": account_source,
        "paper_equity": equity,
        "paper_buying_power": buying_power,
        "entry_reference": entry,
        "stop_reference": stop,
        "stop_percent": args.stop_percent,
        "risk_fraction": args.risk_fraction,
        "risk_budget": risk_budget,
        "per_share_risk": per_share_risk,
        "raw_risk_quantity": raw_risk_qty,
        "max_exposure_fraction": args.max_exposure_fraction,
        "exposure_cap_quantity": exposure_qty,
        "buying_power_cap_quantity": buying_power_qty,
        "hard_max_quantity": args.hard_max_qty,
        "final_quantity": final_qty,
        "formula": "min(floor(equity*risk_fraction/(entry-stop)), floor(equity*exposure_fraction/entry), floor(buying_power/entry), hard_max_qty)",
        "limitations": [
            "A stop reference does not guarantee a fill or loss bound.",
            "The latest accepted historical close is a planning reference, not a live executable price.",
            "This quantity is for a bounded paper exercise only.",
        ],
    }
    calculation_path = output / "risk_calculation.json"
    write_json(calculation_path, calculation)
    id_seed = sha256_file(calculation_path)[:8]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    client_order_id = f"C177-{stamp}-{id_seed}"
    ticket = {
        "course_code": "C177",
        "created_at_utc": utc_now(),
        "environment": "PAPER",
        "symbol": "SPY",
        "side": "BUY",
        "quantity": final_qty,
        "order_type": "MARKET",
        "time_in_force": "DAY",
        "entry_reference": entry,
        "stop_reference": stop,
        "client_order_id": client_order_id,
        "submission_enabled": False,
        "human_approval_required": True,
        "live_endpoint_permitted": False,
        "evidence": {
            "risk_calculation_sha256": sha256_file(calculation_path),
            "hypothesis_fingerprints_sha256": gate["manifest_hashes"]["01-hypothesis"],
            "market_data_fingerprints_sha256": gate["manifest_hashes"]["02-market-data"],
            "backtest_fingerprints_sha256": gate["manifest_hashes"]["03-backtest-audit"],
            "deterministic_decision": gate["deterministic"],
            "human_backtest_decision": gate["human"],
        },
    }
    write_json(output / "paper_order_ticket.json", ticket)
    print("PAPER_TICKET_PREPARED")
    print(f"quantity={final_qty}")
    print(f"client_order_id={client_order_id}")


def _validate_ticket_evidence(pack: Path, ticket: dict, calculation: dict) -> None:
    hashes = _verified_manifests(pack)
    evidence = ticket.get("evidence", {})
    expected = {
        "hypothesis_fingerprints_sha256": hashes["01-hypothesis"],
        "market_data_fingerprints_sha256": hashes["02-market-data"],
        "backtest_fingerprints_sha256": hashes["03-backtest-audit"],
        "risk_calculation_sha256": sha256_file(pack / "04-paper-trade" / "risk_calculation.json"),
    }
    defects = [key for key, value in expected.items() if evidence.get(key) != value]
    if evidence.get("deterministic_decision") != "CONTINUE_RESEARCH":
        defects.append("deterministic_decision")
    if evidence.get("human_backtest_decision") != "CONTINUE_RESEARCH":
        defects.append("human_backtest_decision")
    if int(ticket.get("quantity", 0)) != int(calculation.get("final_quantity", 0)):
        defects.append("quantity")
    if defects:
        raise SystemExit("HOLD_PAPER: ticket evidence changed or does not reconcile: " + ", ".join(defects))


def _review_ready(pack: Path, ticket: dict, calculation: dict) -> None:
    review = read_json(pack / "04-paper-trade" / "ticket_agent_review.json")
    if review.get("controlling_status") != "READY_FOR_HUMAN_REVIEW" or review.get("recommendation") != "READY_FOR_HUMAN_REVIEW":
        raise SystemExit("HOLD_PAPER: agent ticket review is not READY_FOR_HUMAN_REVIEW")
    human, errors = validate_paper_approval(
        pack / "04-paper-trade" / "human_approval.md", ticket, calculation
    )
    if errors:
        raise SystemExit("HOLD_PAPER: incomplete human paper review: " + "; ".join(errors))
    if human != "APPROVE_PAPER_EXERCISE":
        raise SystemExit(f"HOLD_PAPER: human paper decision is {human}")


def _validate_ticket_boundary(ticket: dict) -> int:
    required = {
        "environment": "PAPER",
        "symbol": "SPY",
        "side": "BUY",
        "order_type": "MARKET",
        "time_in_force": "DAY",
        "submission_enabled": False,
        "human_approval_required": True,
        "live_endpoint_permitted": False,
    }
    defects = [key for key, expected in required.items() if ticket.get(key) != expected]
    quantity = int(ticket.get("quantity", 0))
    if quantity <= 0 or quantity > 20:
        defects.append("quantity")
    if not str(ticket.get("client_order_id", "")).startswith("C177-"):
        defects.append("client_order_id")
    if defects:
        raise SystemExit("HOLD_PAPER: invalid ticket boundary: " + ", ".join(defects))
    return quantity


def _receipt_from_order(order: dict, ticket: dict) -> dict:
    receipt = {
        "course_code": "C177",
        "environment": "PAPER",
        "verified_at_utc": utc_now(),
        "order_id": str(order.get("id")),
        "client_order_id": order.get("client_order_id"),
        "symbol": order.get("symbol"),
        "side": str(order.get("side")),
        "quantity": str(order.get("qty")),
        "status": str(order.get("status")),
        "submitted_at": str(order.get("submitted_at")),
        "filled_at": str(order.get("filled_at")) if order.get("filled_at") else None,
        "filled_qty": str(order.get("filled_qty")) if order.get("filled_qty") is not None else None,
        "filled_avg_price": str(order.get("filled_avg_price")) if order.get("filled_avg_price") is not None else None,
        "paper_simulation_only": True,
        "ticket_sha256": sha256_file(ticket["_path"]),
    }
    if receipt["client_order_id"] != ticket["client_order_id"]:
        raise SystemExit("HOLD_PAPER: returned client_order_id does not match the ticket")
    if receipt["symbol"] != ticket["symbol"] or int(float(receipt["quantity"])) != int(ticket["quantity"]):
        raise SystemExit("HOLD_PAPER: returned symbol or quantity does not match the ticket")
    return receipt


def _write_reconciliation(pack: Path, receipt: dict, source: str) -> None:
    log = pack / "04-paper-trade" / "reconciliation_log.md"
    log.write_text(
        "# C177 Paper Reconciliation Log\n\n"
        f"- Verified at UTC: {receipt['verified_at_utc']}\n"
        "- Environment: PAPER\n"
        "- Reconciliation status: CONFIRMED\n"
        "- Order found: YES\n"
        f"- Lookup source: {source}\n"
        f"- Order ID: {receipt['order_id']}\n"
        f"- Client order ID: {receipt['client_order_id']}\n"
        f"- Status: {receipt['status']}\n"
        "- Interpretation: simulator evidence only; not a live fill or performance claim.\n",
        encoding="utf-8",
        newline="\n",
    )


def submit(args, pack: Path) -> None:
    check_gate(pack)
    ticket_path = pack / "04-paper-trade" / "paper_order_ticket.json"
    calculation = read_json(pack / "04-paper-trade" / "risk_calculation.json")
    ticket = read_json(ticket_path)
    ticket["_path"] = ticket_path
    _validate_ticket_evidence(pack, ticket, calculation)
    _review_ready(pack, ticket, calculation)
    quantity = _validate_ticket_boundary(ticket)
    receipt_path = pack / "04-paper-trade" / "paper_order_receipt.json"
    attempt_path = pack / "04-paper-trade" / "submission_attempt.json"
    if receipt_path.exists():
        existing = read_json(receipt_path)
        raise SystemExit(
            f"HOLD_DUPLICATE: receipt already exists for client_order_id={existing.get('client_order_id')}"
        )
    if attempt_path.exists():
        existing = read_json(attempt_path)
        raise SystemExit(
            f"HOLD_DUPLICATE: submission state already exists for client_order_id={existing.get('client_order_id')}; run verify"
        )

    print("ENVIRONMENT=PAPER")
    print(f"symbol={ticket['symbol']}; side={ticket['side']}; quantity={quantity}")
    print(f"client_order_id={ticket['client_order_id']}")
    if args.dry_run:
        print("DRY_RUN: no order submitted; paper client would be constructed with paper=True")
        return
    if args.approve != APPROVAL_TOKEN:
        raise SystemExit("HOLD_PAPER: exact ephemeral approval token is required")

    attempt = {
        "course_code": "C177",
        "environment": "PAPER",
        "state": "SUBMITTING",
        "started_at_utc": utc_now(),
        "client_order_id": ticket["client_order_id"],
        "ticket_sha256": sha256_file(ticket_path),
        "paper_simulation_only": True,
    }
    write_json(attempt_path, attempt)
    client = _paper_client()
    account = pydantic_dump(client.get_account())
    if _normalise_status(account.get("status")) != "active":
        attempt.update({"state": "HOLD_ACCOUNT", "finished_at_utc": utc_now()})
        write_json(attempt_path, attempt)
        raise SystemExit(f"HOLD_PAPER: paper account status is {account.get('status')}")
    from alpaca.trading.enums import OrderSide, TimeInForce
    from alpaca.trading.requests import MarketOrderRequest

    request = MarketOrderRequest(
        symbol=ticket["symbol"],
        qty=quantity,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
        client_order_id=ticket["client_order_id"],
    )
    try:
        order = pydantic_dump(client.submit_order(order_data=request))
    except Exception as exc:
        attempt.update(
            {
                "state": "UNCERTAIN_SUBMISSION",
                "finished_at_utc": utc_now(),
                "error_type": type(exc).__name__,
            }
        )
        write_json(attempt_path, attempt)
        write_json(
            pack / "04-paper-trade" / "paper_submission_error.json",
            {
                "course_code": "C177",
                "environment": "PAPER",
                "occurred_at_utc": utc_now(),
                "client_order_id": ticket["client_order_id"],
                "error_type": type(exc).__name__,
                "message": "The paper API call did not return a confirmed order. Query the saved client order ID before any retry.",
                "resolved": False,
            },
        )
        raise SystemExit("HOLD_UNCERTAIN_SUBMISSION: saved client_order_id; run verify before any retry")
    receipt = _receipt_from_order(order, ticket)
    write_json(receipt_path, receipt)
    attempt.update({"state": "RECEIPT_WRITTEN", "finished_at_utc": utc_now(), "order_id": receipt["order_id"]})
    write_json(attempt_path, attempt)
    print(f"PAPER_ORDER_RECEIPT_WRITTEN: {receipt_path}")


def verify(pack: Path) -> None:
    check_gate(pack)
    ticket_path = pack / "04-paper-trade" / "paper_order_ticket.json"
    ticket = read_json(ticket_path)
    ticket["_path"] = ticket_path
    calculation = read_json(pack / "04-paper-trade" / "risk_calculation.json")
    _validate_ticket_evidence(pack, ticket, calculation)
    _review_ready(pack, ticket, calculation)
    _validate_ticket_boundary(ticket)
    receipt_path = pack / "04-paper-trade" / "paper_order_receipt.json"
    attempt_path = pack / "04-paper-trade" / "submission_attempt.json"
    client = _paper_client()
    try:
        if receipt_path.exists():
            existing = read_json(receipt_path)
            order = pydantic_dump(client.get_order_by_id(existing["order_id"]))
            source = "order_id"
        else:
            if not attempt_path.exists():
                raise SystemExit("HOLD_RECONCILIATION: no submission attempt exists")
            attempt = read_json(attempt_path)
            if attempt.get("client_order_id") != ticket["client_order_id"]:
                raise SystemExit("HOLD_RECONCILIATION: pending client order ID differs from the ticket")
            order = pydantic_dump(client.get_order_by_client_id(ticket["client_order_id"]))
            source = "client_order_id"
    except SystemExit:
        raise
    except Exception as exc:
        log = pack / "04-paper-trade" / "reconciliation_log.md"
        status_code = getattr(exc, "status_code", None)
        if status_code == 404:
            log.write_text(
                "# C177 Paper Reconciliation Log\n\n"
                f"- Verified at UTC: {utc_now()}\n- Environment: PAPER\n"
                "- Reconciliation status: CONFIRMED_NO_ORDER\n- Order found: NO\n"
                f"- Client order ID: {ticket['client_order_id']}\n"
                "- Interpretation: the paper API confirmed that no order exists for the saved client order ID; do not retry without a newly reviewed ticket.\n",
                encoding="utf-8",
                newline="\n",
            )
            error_path = pack / "04-paper-trade" / "paper_submission_error.json"
            error = read_json(error_path) if error_path.exists() else {
                "course_code": "C177",
                "environment": "PAPER",
                "client_order_id": ticket["client_order_id"],
                "error_type": type(exc).__name__,
            }
            error.update({"resolved": True, "resolution": "CONFIRMED_NO_ORDER", "resolved_at_utc": utc_now()})
            write_json(error_path, error)
            attempt = read_json(attempt_path)
            attempt.update({"state": "RECONCILED_NO_ORDER", "finished_at_utc": utc_now()})
            write_json(attempt_path, attempt)
            print("PAPER_ORDER_RECONCILED: no order found for saved client_order_id")
            return
        log.write_text(
            "# C177 Paper Reconciliation Log\n\n"
            f"- Verified at UTC: {utc_now()}\n- Environment: PAPER\n"
            "- Reconciliation status: UNRESOLVED\n- Order found: UNKNOWN\n"
            f"- Client order ID: {ticket['client_order_id']}\n- Error type: {type(exc).__name__}\n"
            "- Next action: inspect the paper dashboard; do not submit again.\n",
            encoding="utf-8",
            newline="\n",
        )
        raise SystemExit("HOLD_RECONCILIATION: API lookup did not resolve the saved client order ID")
    receipt = _receipt_from_order(order, ticket)
    write_json(receipt_path, receipt)
    _write_reconciliation(pack, receipt, source)
    error_path = pack / "04-paper-trade" / "paper_submission_error.json"
    if error_path.exists():
        error = read_json(error_path)
        error.update({"resolved": True, "resolved_at_utc": utc_now(), "order_id": receipt["order_id"]})
        write_json(error_path, error)
    if attempt_path.exists():
        attempt = read_json(attempt_path)
        attempt.update({"state": "RECONCILED", "finished_at_utc": utc_now(), "order_id": receipt["order_id"]})
        write_json(attempt_path, attempt)
    print(f"PAPER_ORDER_VERIFIED: status={receipt['status']}")


def rollback(args, pack: Path) -> None:
    receipt_path = pack / "04-paper-trade" / "paper_order_receipt.json"
    attempt_path = pack / "04-paper-trade" / "submission_attempt.json"
    record_path = pack / "04-paper-trade" / "rollback_record.md"
    if not receipt_path.exists() and attempt_path.exists():
        verify(pack)
    if not receipt_path.exists():
        if attempt_path.exists() and read_json(attempt_path).get("state") == "RECONCILED_NO_ORDER":
            record_path.write_text(
                "# C177 Rollback Record\n\n"
                f"- UTC time: {utc_now()}\n- Environment: PAPER\n- Resolved: YES\n"
                "- Final state: CONFIRMED_NO_ORDER\n"
                "- Action: The saved client order ID was reconciled through the paper API and no order existed to cancel.\n",
                encoding="utf-8",
                newline="\n",
            )
            print("ROLLBACK_RECORDED: confirmed no order")
            return
        record_path.write_text(
            "# C177 Rollback Record\n\n"
            f"- UTC time: {utc_now()}\n- Environment: PAPER\n- Resolved: NO\n"
            "- Final state: NO_CONFIRMED_SUBMISSION\n"
            "- Action: No receipt exists. Finalisation remains on HOLD until a saved submission attempt is reconciled.\n",
            encoding="utf-8",
            newline="\n",
        )
        print("HOLD_ROLLBACK: no reconciled receipt")
        return
    receipt = read_json(receipt_path)
    client = _paper_client()
    order = pydantic_dump(client.get_order_by_id(receipt["order_id"]))
    before = _normalise_status(order.get("status"))
    action = "No automatic cancellation was needed."
    if before in OPEN_STATUSES:
        client.cancel_order_by_id(receipt["order_id"])
        action = "Cancellation requested for the open paper order."
        deadline = time.monotonic() + max(1, min(int(args.poll_seconds), 30))
        while True:
            order = pydantic_dump(client.get_order_by_id(receipt["order_id"]))
            observed = _normalise_status(order.get("status"))
            if observed not in OPEN_STATUSES or time.monotonic() >= deadline:
                break
            time.sleep(min(1.0, max(0.0, deadline - time.monotonic())))
    after = _normalise_status(order.get("status"))
    filled = after == "filled"
    terminal = after in TERMINAL_STATUSES
    resolved = terminal and (not filled or bool(args.confirm_position_reviewed))
    record_path.write_text(
        "# C177 Rollback Record\n\n"
        f"- UTC time: {utc_now()}\n- Environment: PAPER\n- Order ID: {receipt['order_id']}\n"
        f"- Status before: {before}\n- Action: {action}\n- Status after: {after}\n"
        f"- Paper position reviewed: {'YES' if args.confirm_position_reviewed else 'NO'}\n"
        f"- Resolved: {'YES' if resolved else 'NO'}\n"
        f"- Final state: {'RECONCILED_' + after.upper() if resolved else 'HOLD_' + after.upper()}\n"
        "- Interpretation: simulator evidence only; not a live fill or performance claim.\n",
        encoding="utf-8",
        newline="\n",
    )
    if not resolved:
        if after in OPEN_STATUSES:
            raise SystemExit("HOLD_ROLLBACK: cancellation is not yet terminal; verify the paper order and rerun rollback")
        raise SystemExit("HOLD_ROLLBACK: confirm the paper position state, then rerun with --confirm-position-reviewed")
    print(f"ROLLBACK_RECORDED: status_after={after}")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    gate = sub.add_parser("check-gate")
    gate.add_argument("--pack", required=True)
    prepare_parser = sub.add_parser("prepare")
    prepare_parser.add_argument("--pack", required=True)
    prepare_parser.add_argument("--risk-fraction", type=float, required=True)
    prepare_parser.add_argument("--stop-percent", type=float, required=True)
    prepare_parser.add_argument("--max-exposure-fraction", type=float, required=True)
    prepare_parser.add_argument("--hard-max-qty", type=int, required=True)
    prepare_parser.add_argument("--paper-equity", type=float, help="Trainer-only offline rejoin value")
    submit_parser = sub.add_parser("submit")
    submit_parser.add_argument("--pack", required=True)
    submit_parser.add_argument("--dry-run", action="store_true")
    submit_parser.add_argument("--approve")
    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--pack", required=True)
    rollback_parser = sub.add_parser("rollback")
    rollback_parser.add_argument("--pack", required=True)
    rollback_parser.add_argument("--confirm-position-reviewed", action="store_true")
    rollback_parser.add_argument("--poll-seconds", type=int, default=10, help="Bounded wait for a terminal paper-order state (1-30 seconds)")
    args = parser.parse_args()
    pack = Path(args.pack).resolve()
    if args.action == "check-gate":
        check_gate(pack)
    elif args.action == "prepare":
        prepare(args, pack)
    elif args.action == "submit":
        submit(args, pack)
    elif args.action == "verify":
        verify(pack)
    else:
        rollback(args, pack)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
