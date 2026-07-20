from __future__ import annotations

import unittest

from mezo_model_server.config import Settings
from mezo_model_server.errors import ConfigurationError

BASE_ENV = {
    "ENVIRONMENT": "production",
    "MODEL_ID": "Qwen/Qwen3-Coder-Next",
    "MODEL_REVISION": "abc123",
    "SERVED_MODEL_NAME": "qwen-coder-primary",
    "MODEL_API_KEY": "x" * 32,
    "MAX_MODEL_LEN": "32768",
    "TENSOR_PARALLEL_SIZE": "2",
    "PIPELINE_PARALLEL_SIZE": "1",
    "GPU_MEMORY_UTILIZATION": "0.90",
    "MAX_NUM_SEQS": "2",
    "TOOL_CALL_PARSER": "qwen3_coder",
}


class SettingsTests(unittest.TestCase):
    def test_production_profile_is_valid(self) -> None:
        settings = Settings.from_env(BASE_ENV)
        self.assertEqual(settings.max_model_len, 32768)
        self.assertEqual(settings.tensor_parallel_size, 2)

    def test_production_requires_long_api_key(self) -> None:
        env = {**BASE_ENV, "MODEL_API_KEY": "short"}
        with self.assertRaisesRegex(ConfigurationError, "at least 32"):
            Settings.from_env(env)

    def test_production_requires_pinned_revision(self) -> None:
        env = {**BASE_ENV, "MODEL_REVISION": ""}
        with self.assertRaisesRegex(ConfigurationError, "must be pinned"):
            Settings.from_env(env)

    def test_remote_code_is_forbidden_in_production(self) -> None:
        env = {**BASE_ENV, "TRUST_REMOTE_CODE": "true"}
        with self.assertRaisesRegex(ConfigurationError, "forbidden"):
            Settings.from_env(env)

    def test_context_cannot_exceed_native_limit(self) -> None:
        env = {**BASE_ENV, "MAX_MODEL_LEN": "262145"}
        with self.assertRaisesRegex(ConfigurationError, "262144"):
            Settings.from_env(env)
