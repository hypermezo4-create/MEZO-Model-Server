from __future__ import annotations

import argparse
import json
import os
import sys

from mezo_model_server.command import build_vllm_command, redact_command
from mezo_model_server.config import Settings
from mezo_model_server.errors import ConfigurationError


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate configuration and launch vLLM")
    parser.add_argument(
        "--print-command",
        action="store_true",
        help="Print the redacted deterministic vLLM command without executing it",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Use JSON when printing the command",
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    try:
        settings = Settings.from_env()
    except ConfigurationError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    command = build_vllm_command(settings)
    if args.print_command:
        safe_command = redact_command(command)
        if args.json:
            print(json.dumps(safe_command))
        else:
            print(" ".join(safe_command))
        return

    os.execvp(command[0], command)  # noqa: S606


if __name__ == "__main__":
    main()
