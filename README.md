# MEZO Model Server

Self-hosted GPU model serving for the MEZO coding-agent platform. This repository owns Qwen inference, vLLM launch policy, RunPod deployment, authentication, health checks, model pinning, smoke tests, and performance evaluation. It does not receive GitHub credentials and cannot modify repositories.

## Production model

- Model: `Qwen/Qwen3-Coder-Next`
- Serving engine: `vLLM >= 0.15.0`
- API: OpenAI-compatible `/v1/chat/completions` and `/v1/models`
- Tool parser: `qwen3_coder`
- Default context: `32768` tokens
- Model revision: pinned in `models/registry.json`

The model supports a native context of 262,144 tokens, but the initial production profile deliberately uses 32K to reduce KV-cache pressure and improve concurrency. Raise it only after GPU-specific benchmarks pass.

## Architecture

```text
MEZO-AI-Control-Plane
         |
         | Bearer token + OpenAI API
         v
RunPod GPU / Dedicated GPU Pod
         |
  MEZO launcher policy
         |
       vLLM
         |
 Qwen3-Coder-Next
```

## Repository map

```text
src/mezo_model_server/   Environment validation and deterministic vLLM launcher
models/                  Pinned model and deployment profiles
runpod/                  Pod and Serverless entrypoints
benchmarks/               Latency, throughput, tool-call, and long-context checks
scripts/                  Smoke tests and model verification
tests/                    Configuration and command regression tests
.github/workflows/        CI, image build, image scan, and manual benchmark gates
```

## Safety boundaries

- No GitHub, Fly, database, Telegram, or repository-write credentials are accepted.
- The endpoint requires an API key in production.
- Tool calls are generated as structured proposals only; tools execute in the Control Plane sandbox.
- Model revisions and serving image versions are pinned.
- Secrets are never printed by diagnostics.
- The server exposes only inference, health, metrics, and model-discovery endpoints.

## Quick validation without a GPU

```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests scripts benchmarks runpod
PYTHONPATH=src python -m mezo_model_server.launcher --print-command
```

## Direct GPU Pod

```bash
cp .env.example .env
# Add MODEL_API_KEY, HF_TOKEN, and GPU-specific parallelism.
docker compose up --build
```

Health checks:

```text
GET /health
GET /v1/models
GET /metrics
```

Example request:

```bash
curl "$MODEL_BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $MODEL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-coder-primary",
    "messages": [{"role": "user", "content": "Review this patch for a race condition."}],
    "temperature": 0.2,
    "max_tokens": 2048
  }'
```

## Tool calling

The launcher enables automatic tool selection and the official `qwen3_coder` parser. The Control Plane supplies JSON schemas for tools. This server never executes the requested tools.

## RunPod

Two deployment modes are included:

1. Dedicated Pod: stable latency, persistent model cache, recommended for continuous use.
2. Serverless worker: scales down when idle but has cold-start and large-model download considerations.

See `runpod/README.md` and `runpod/endpoint-config.example.json`.

## Required secrets

```text
MODEL_API_KEY
HF_TOKEN
```

The Control Plane stores `MODEL_API_KEY` as `QWEN_API_KEY` and calls the endpoint through `QWEN_BASE_URL`.

## Important environment values

```text
MODEL_ID=Qwen/Qwen3-Coder-Next
MODEL_REVISION=<pinned Hugging Face revision>
SERVED_MODEL_NAME=qwen-coder-primary
MAX_MODEL_LEN=32768
TENSOR_PARALLEL_SIZE=2
GPU_MEMORY_UTILIZATION=0.90
MAX_NUM_SEQS=2
TOOL_CALL_PARSER=qwen3_coder
```

## Deployment gate

Before production deployment:

1. Build and scan the image.
2. Verify the model revision.
3. Start the endpoint and pass `/health` and `/v1/models`.
4. Pass tool-call smoke tests.
5. Run latency and throughput benchmarks on the target GPU.
6. Record GPU type, quantization, max context, concurrency, tokens/second, and peak memory.
7. Connect the endpoint to `MEZO-AI-Control-Plane` only after the API key is configured.

## Integration boundary

- `MEZO-AI-Control-Plane` owns orchestration, repository access, tools, approvals, and evidence.
- `MEZO-Agent-Skills` owns engineering rules and review gates.
- This repository owns only model inference and GPU-serving reliability.

## License

No open-source license has been granted. All rights are reserved unless the repository owner adds a license explicitly.
