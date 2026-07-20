from __future__ import annotations

import unittest
from pathlib import Path

from mezo_model_server.registry import load_profile


class RegistryTests(unittest.TestCase):
    def test_primary_profile_is_pinned(self) -> None:
        profile = load_profile(Path("models/registry.json"), "qwen-coder-primary")
        self.assertEqual(profile.engine, "vllm")
        self.assertTrue(profile.revision)
        self.assertEqual(profile.default_context, 32768)
        self.assertEqual(profile.tool_call_parser, "qwen3_coder")
