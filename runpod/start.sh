#!/usr/bin/env bash
set -euo pipefail

python -m mezo_model_server.launcher &
VLLM_PID=$!

cleanup() {
  kill -TERM "$VLLM_PID" 2>/dev/null || true
  wait "$VLLM_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

python - <<'PY'
import os
import time
import urllib.error
import urllib.request

port = os.environ.get("MODEL_PORT", "8000")
deadline = time.monotonic() + int(os.environ.get("MODEL_STARTUP_TIMEOUT_SECONDS", "1800"))
url = f"http://127.0.0.1:{port}/health"
while time.monotonic() < deadline:
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                raise SystemExit(0)
    except (urllib.error.URLError, TimeoutError):
        pass
    time.sleep(5)
raise SystemExit("vLLM did not become healthy before startup timeout")
PY

python /opt/mezo/runpod/handler.py
