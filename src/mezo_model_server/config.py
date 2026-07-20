from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from mezo_model_server.errors import ConfigurationError


def _parse_bool(value: str, *, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"{name} must be true or false")


def _parse_int(value: str, *, name: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc


def _parse_float(value: str, *, name: str) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a number") from exc


@dataclass(frozen=True, slots=True)
class Settings:
    environment: str
    model_id: str
    model_revision: str
    served_model_name: str
    host: str
    port: int
    api_key: str
    hf_token: str
    max_model_len: int
    tensor_parallel_size: int
    pipeline_parallel_size: int
    gpu_memory_utilization: float
    max_num_seqs: int
    dtype: str
    quantization: str
    tool_call_parser: str
    enable_prefix_caching: bool
    enable_chunked_prefill: bool
    trust_remote_code: bool
    enforce_eager: bool
    disable_log_requests: bool
    download_dir: str
    uvicorn_log_level: str

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        env = os.environ if environ is None else environ
        settings = cls(
            environment=env.get("ENVIRONMENT", "development").strip().lower(),
            model_id=env.get("MODEL_ID", "Qwen/Qwen3-Coder-Next").strip(),
            model_revision=env.get("MODEL_REVISION", "").strip(),
            served_model_name=env.get("SERVED_MODEL_NAME", "qwen-coder-primary").strip(),
            host=env.get("MODEL_HOST", "0.0.0.0").strip(),  # noqa: S104
            port=_parse_int(env.get("MODEL_PORT", "8000"), name="MODEL_PORT"),
            api_key=env.get("MODEL_API_KEY", "").strip(),
            hf_token=env.get("HF_TOKEN", "").strip(),
            max_model_len=_parse_int(env.get("MAX_MODEL_LEN", "32768"), name="MAX_MODEL_LEN"),
            tensor_parallel_size=_parse_int(
                env.get("TENSOR_PARALLEL_SIZE", "1"), name="TENSOR_PARALLEL_SIZE"
            ),
            pipeline_parallel_size=_parse_int(
                env.get("PIPELINE_PARALLEL_SIZE", "1"), name="PIPELINE_PARALLEL_SIZE"
            ),
            gpu_memory_utilization=_parse_float(
                env.get("GPU_MEMORY_UTILIZATION", "0.90"), name="GPU_MEMORY_UTILIZATION"
            ),
            max_num_seqs=_parse_int(env.get("MAX_NUM_SEQS", "2"), name="MAX_NUM_SEQS"),
            dtype=env.get("DTYPE", "auto").strip().lower(),
            quantization=env.get("QUANTIZATION", "").strip().lower(),
            tool_call_parser=env.get("TOOL_CALL_PARSER", "qwen3_coder").strip(),
            enable_prefix_caching=_parse_bool(
                env.get("ENABLE_PREFIX_CACHING", "true"), name="ENABLE_PREFIX_CACHING"
            ),
            enable_chunked_prefill=_parse_bool(
                env.get("ENABLE_CHUNKED_PREFILL", "true"), name="ENABLE_CHUNKED_PREFILL"
            ),
            trust_remote_code=_parse_bool(
                env.get("TRUST_REMOTE_CODE", "false"), name="TRUST_REMOTE_CODE"
            ),
            enforce_eager=_parse_bool(env.get("ENFORCE_EAGER", "false"), name="ENFORCE_EAGER"),
            disable_log_requests=_parse_bool(
                env.get("DISABLE_LOG_REQUESTS", "true"), name="DISABLE_LOG_REQUESTS"
            ),
            download_dir=env.get("DOWNLOAD_DIR", "/models").strip(),
            uvicorn_log_level=env.get("UVICORN_LOG_LEVEL", "info").strip().lower(),
        )
        settings.validate()
        return settings

    def validate(self) -> None:
        if not self.model_id:
            raise ConfigurationError("MODEL_ID is required")
        if not self.served_model_name:
            raise ConfigurationError("SERVED_MODEL_NAME is required")
        if not 1 <= self.port <= 65535:
            raise ConfigurationError("MODEL_PORT must be between 1 and 65535")
        if not 2048 <= self.max_model_len <= 262_144:
            raise ConfigurationError("MAX_MODEL_LEN must be between 2048 and 262144")
        if self.tensor_parallel_size < 1 or self.pipeline_parallel_size < 1:
            raise ConfigurationError("parallel sizes must be at least 1")
        if not 0.50 <= self.gpu_memory_utilization <= 0.98:
            raise ConfigurationError("GPU_MEMORY_UTILIZATION must be between 0.50 and 0.98")
        if not 1 <= self.max_num_seqs <= 256:
            raise ConfigurationError("MAX_NUM_SEQS must be between 1 and 256")
        if self.quantization not in {"", "awq", "gptq", "fp8", "bitsandbytes"}:
            raise ConfigurationError("unsupported QUANTIZATION value")
        if self.tool_call_parser != "qwen3_coder":
            raise ConfigurationError("Qwen3-Coder-Next requires TOOL_CALL_PARSER=qwen3_coder")
        if self.environment == "production" and len(self.api_key) < 32:
            raise ConfigurationError("production MODEL_API_KEY must contain at least 32 characters")
        if self.environment == "production" and not self.model_revision:
            raise ConfigurationError("production MODEL_REVISION must be pinned")
        if self.trust_remote_code and self.environment == "production":
            raise ConfigurationError("TRUST_REMOTE_CODE is forbidden in production")
