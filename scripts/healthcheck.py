from __future__ import annotations

import os
import urllib.error
import urllib.request


def main() -> None:
    host = os.environ.get("HEALTHCHECK_HOST", "127.0.0.1")
    port = os.environ.get("MODEL_PORT", "8000")
    request = urllib.request.Request(f"http://{host}:{port}/health", method="GET")
    try:
        with urllib.request.urlopen(request, timeout=4) as response:  # noqa: S310
            if response.status != 200:
                raise SystemExit(1)
    except (urllib.error.URLError, TimeoutError):
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
