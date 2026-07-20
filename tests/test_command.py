from __future__ import annotations

import unittest

from mezo_model_server.command import build_vllm_command, redact_command
from mezo_model_server.config import Settings
from tests.test_config import BASE_ENV


class CommandTests(unittest.TestCase):
    def test_builds_qwen_tool_calling_command(self) -> None:
        settings = Settings.from_env(BASE_ENV)
        command = build_vllm_command(settings)
        self.assertEqual(command[:3], ["vllm", "serve", "Qwen/Qwen3-Coder-Next"])
        self.assertIn("--enable-auto-tool-choice", command)
        self.assertEqual(command[command.index("--tool-call-parser") + 1], "qwen3_coder")
        self.assertEqual(command[command.index("--max-model-len") + 1], "32768")
        self.assertIn("--disable-log-requests", command)

    def test_redaction_hides_api_key(self) -> None:
        settings = Settings.from_env(BASE_ENV)
        safe_command = redact_command(build_vllm_command(settings))
        self.assertNotIn("x" * 32, safe_command)
        self.assertEqual(safe_command[safe_command.index("--api-key") + 1], "<redacted>")
