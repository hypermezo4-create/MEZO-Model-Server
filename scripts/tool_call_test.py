from __future__ import annotations

import argparse
import json
import os
import urllib.request
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default=os.environ.get("MODEL_BASE_URL", "http://127.0.0.1:8000/v1"),
    )
    parser.add_argument("--api-key", default=os.environ.get("MODEL_API_KEY", ""))
    parser.add_argument(
        "--model",
        default=os.environ.get("SERVED_MODEL_NAME", "qwen-coder-primary"),
    )
    args = parser.parse_args()
    if not args.api_key:
        raise SystemExit("MODEL_API_KEY or --api-key is required")

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": "Read README.md using the available tool."}],
        "temperature": 0,
        "max_tokens": 256,
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read a repository file",
                    "parameters": {
                        "type": "object",
                        "properties": {"path": {"type": "string"}},
                        "required": ["path"],
                        "additionalProperties": False,
                    },
                },
            }
        ],
    }
    request = urllib.request.Request(  # noqa: S310
        f"{args.base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {args.api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:  # noqa: S310
        result: Any = json.loads(response.read().decode())
    choices = result.get("choices") if isinstance(result, dict) else None
    message = choices[0].get("message", {}) if isinstance(choices, list) and choices else {}
    tool_calls = message.get("tool_calls") if isinstance(message, dict) else None
    if not isinstance(tool_calls, list) or not tool_calls:
        raise SystemExit("tool-call test failed: no structured tool call")
    print("tool-call test passed")


if __name__ == "__main__":
    main()
