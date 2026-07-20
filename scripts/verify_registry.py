from __future__ import annotations

import argparse
from pathlib import Path

from mezo_model_server.registry import load_profile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=Path("models/registry.json"))
    parser.add_argument("--profile", default="qwen-coder-primary")
    args = parser.parse_args()
    profile = load_profile(args.registry, args.profile)
    if profile.default_context > profile.max_context:
        raise SystemExit("default context exceeds model maximum")
    if profile.engine != "vllm":
        raise SystemExit("primary profile must use vLLM")
    print(f"verified {profile.name} at revision {profile.revision}")


if __name__ == "__main__":
    main()
