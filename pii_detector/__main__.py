"""Command line interface for pii-detector-fr."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .detector import PIIDetector


def _read_input(text: str | None, file_path: str | None) -> str:
    if text and file_path:
        raise ValueError("Use either --text or --file, not both.")
    if text:
        return text
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    data = sys.stdin.read()
    if not data.strip():
        raise ValueError("No input received. Use --text, --file, or stdin.")
    return data


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pii-detector",
        description="Detect and anonymize French PII from text.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Detect PII and output JSON.")
    scan_parser.add_argument("--text", help="Inline text to scan.")
    scan_parser.add_argument("--file", help="Path of a text file to scan.")
    scan_parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output.",
    )

    anon_parser = subparsers.add_parser("anonymize", help="Return redacted text.")
    anon_parser.add_argument("--text", help="Inline text to anonymize.")
    anon_parser.add_argument("--file", help="Path of a text file to anonymize.")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        input_text = _read_input(args.text, args.file)
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    detector = PIIDetector(language="fr")

    if args.command == "scan":
        payload = [match.to_dict() for match in detector.detect(input_text)]
        if args.pretty:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(payload, ensure_ascii=False))
        return 0

    if args.command == "anonymize":
        print(detector.anonymize(input_text))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
