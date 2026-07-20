from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from typing import Any


def _request(url: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    encoded = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(  # noqa: S310
        url,
        data=encoded,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=180) as response:  # noqa: S310
        body: Any = json.loads(response.read().decode("utf-8"))
    if not isinstance(body, dict):
        raise RuntimeError("endpoint returned a non-object response")
    return body


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
        "messages": [{"role": "user", "content": "Return exactly the word READY."}],
        "temperature": 0,
        "max_tokens": 16,
    }
    try:
        response = _request(f"{args.base_url.rstrip('/')}/chat/completions", args.api_key, payload)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"smoke test failed with HTTP {exc.code}") from exc
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        raise SystemExit("smoke test response has no choices")
    print("smoke test passed")


if __name__ == "__main__":
    main()
