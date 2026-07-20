from __future__ import annotations

import os
from typing import Any

import httpx
import runpod

MODEL_PORT = os.environ.get("MODEL_PORT", "8000")
MODEL_API_KEY = os.environ.get("MODEL_API_KEY", "")
BASE_URL = f"http://127.0.0.1:{MODEL_PORT}/v1"
ALLOWED_PATHS = {"chat/completions", "models"}


async def handler(job: dict[str, Any]) -> dict[str, Any]:
    request = job.get("input")
    if not isinstance(request, dict):
        return {"error": "input must be an object"}
    path = request.get("path", "chat/completions")
    payload = request.get("body", {})
    if path not in ALLOWED_PATHS:
        return {"error": "unsupported path"}
    if not isinstance(payload, dict):
        return {"error": "body must be an object"}

    headers = {"Authorization": f"Bearer {MODEL_API_KEY}"} if MODEL_API_KEY else {}
    method = "GET" if path == "models" else "POST"
    async with httpx.AsyncClient(timeout=600) as client:
        response = await client.request(
            method,
            f"{BASE_URL}/{path}",
            headers=headers,
            json=None if method == "GET" else payload,
        )
    try:
        body: Any = response.json()
    except ValueError:
        body = {"error": "model server returned non-JSON output"}
    return {"status_code": response.status_code, "body": body}


runpod.serverless.start({"handler": handler})
