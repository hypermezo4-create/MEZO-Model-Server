from __future__ import annotations

from mezo_model_server.config import Settings


def build_vllm_command(settings: Settings) -> list[str]:
    command = [
        "vllm",
        "serve",
        settings.model_id,
        "--host",
        settings.host,
        "--port",
        str(settings.port),
        "--served-model-name",
        settings.served_model_name,
        "--max-model-len",
        str(settings.max_model_len),
        "--tensor-parallel-size",
        str(settings.tensor_parallel_size),
        "--pipeline-parallel-size",
        str(settings.pipeline_parallel_size),
        "--gpu-memory-utilization",
        str(settings.gpu_memory_utilization),
        "--max-num-seqs",
        str(settings.max_num_seqs),
        "--dtype",
        settings.dtype,
        "--enable-auto-tool-choice",
        "--tool-call-parser",
        settings.tool_call_parser,
        "--download-dir",
        settings.download_dir,
        "--uvicorn-log-level",
        settings.uvicorn_log_level,
    ]
    if settings.model_revision:
        command.extend(["--revision", settings.model_revision])
    if settings.api_key:
        command.extend(["--api-key", settings.api_key])
    if settings.quantization:
        command.extend(["--quantization", settings.quantization])
    if settings.enable_prefix_caching:
        command.append("--enable-prefix-caching")
    if settings.enable_chunked_prefill:
        command.append("--enable-chunked-prefill")
    if settings.trust_remote_code:
        command.append("--trust-remote-code")
    if settings.enforce_eager:
        command.append("--enforce-eager")
    if settings.disable_log_requests:
        command.append("--disable-log-requests")
    return command


def redact_command(command: list[str]) -> list[str]:
    redacted = command.copy()
    for index, value in enumerate(redacted[:-1]):
        if value == "--api-key":
            redacted[index + 1] = "<redacted>"
    return redacted
