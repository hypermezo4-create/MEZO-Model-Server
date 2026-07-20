from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mezo_model_server.errors import ConfigurationError


@dataclass(frozen=True, slots=True)
class ModelProfile:
    name: str
    model_id: str
    revision: str
    engine: str
    minimum_engine_version: str
    served_model_name: str
    max_context: int
    default_context: int
    tool_call_parser: str


def load_profile(path: Path, profile_name: str) -> ModelProfile:
    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("models"), dict):
        raise ConfigurationError("registry must contain an object named models")
    models = raw["models"]
    profile = models.get(profile_name)
    if not isinstance(profile, dict):
        raise ConfigurationError(f"unknown model profile: {profile_name}")
    required = {
        "model_id",
        "revision",
        "engine",
        "minimum_engine_version",
        "served_model_name",
        "max_context",
        "default_context",
        "tool_call_parser",
    }
    missing = sorted(required - profile.keys())
    if missing:
        raise ConfigurationError(f"model profile missing keys: {', '.join(missing)}")
    return ModelProfile(name=profile_name, **{key: profile[key] for key in required})
