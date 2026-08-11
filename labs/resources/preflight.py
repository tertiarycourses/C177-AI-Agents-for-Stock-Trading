"""Check C177 lab dependencies without revealing credential values."""

from __future__ import annotations

import argparse
import importlib
import os
import platform
import sys

from course_common import is_placeholder


PACKAGES = {
    "agents": "openai-agents",
    "alpaca": "alpaca-py",
    "pandas": "pandas",
    "numpy": "numpy",
    "matplotlib": "matplotlib",
    "dotenv": "python-dotenv",
    "pydantic": "pydantic",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require", choices=["openai", "alpaca", "all"])
    args = parser.parse_args()

    failures: list[str] = []
    print(f"Python: {platform.python_version()} ({sys.executable})")
    if sys.version_info < (3, 11):
        failures.append("Python 3.11 or newer is required")

    for module_name, package_name in PACKAGES.items():
        try:
            importlib.import_module(module_name)
            print(f"PACKAGE_READY: {package_name}")
        except Exception as exc:  # show type only; dependency messages can be noisy
            failures.append(f"{package_name} import failed ({type(exc).__name__})")

    openai_ready = not is_placeholder(os.getenv("OPENAI_API_KEY"))
    alpaca_ready = not is_placeholder(os.getenv("ALPACA_API_KEY")) and not is_placeholder(
        os.getenv("ALPACA_SECRET_KEY")
    )
    paper_only = os.getenv("ALPACA_PAPER_ONLY", "").strip().lower() == "true"

    print(f"OPENAI_CREDENTIAL_PRESENT: {str(openai_ready).lower()}")
    print(f"ALPACA_CREDENTIALS_PRESENT: {str(alpaca_ready).lower()}")
    print(f"ALPACA_PAPER_ONLY: {str(paper_only).lower()}")

    if args.require in {"openai", "all"} and not openai_ready:
        failures.append("OPENAI_API_KEY is missing or still a placeholder")
    if args.require in {"alpaca", "all"} and not alpaca_ready:
        failures.append("Alpaca paper credentials are missing or still placeholders")
    if args.require in {"alpaca", "all"} and not paper_only:
        failures.append("ALPACA_PAPER_ONLY must equal true")

    if failures:
        print("HOLD_PREFLIGHT")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("READY_PREFLIGHT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
