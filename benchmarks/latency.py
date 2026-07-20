from __future__ import annotations

import argparse
import json
import os
import statistics
import time
import urllib.request


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
    parser.add_argument("--requests", type=int, default=5)
    args = parser.parse_args()
    if not args.api_key:
        raise SystemExit("MODEL_API_KEY is required")

    durations: list[float] = []
    for _ in range(args.requests):
        payload = {
            "model": args.model,
            "messages": [
                {"role": "user", "content": "Write a Python function that adds two integers."}
            ],
            "temperature": 0,
            "max_tokens": 128,
        }
        request = urllib.request.Request(  # noqa: S310
            f"{args.base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {args.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        started = time.perf_counter()
        with urllib.request.urlopen(request, timeout=180) as response:  # noqa: S310
            response.read()
        durations.append(time.perf_counter() - started)

    result = {
        "requests": len(durations),
        "mean_seconds": statistics.mean(durations),
        "median_seconds": statistics.median(durations),
        "max_seconds": max(durations),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
