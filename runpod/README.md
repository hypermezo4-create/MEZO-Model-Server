# RunPod deployment

## Dedicated Pod

Use `Dockerfile` and mount a persistent network volume at `/models`. Expose port 8000 only through RunPod's authenticated proxy or a private network path. Configure `MODEL_API_KEY`, `HF_TOKEN`, and the GPU profile.

Recommended starting profile:

```text
MAX_MODEL_LEN=32768
TENSOR_PARALLEL_SIZE=2
MAX_NUM_SEQS=2
GPU_MEMORY_UTILIZATION=0.90
```

The actual GPU count must match tensor parallelism. Benchmark before increasing context or concurrency.

## Serverless

Use `Dockerfile.runpod`. The container starts vLLM, waits for health, then starts a RunPod handler that accepts only:

```json
{"input": {"path": "chat/completions", "body": {"model": "qwen-coder-primary", "messages": []}}}
```

or:

```json
{"input": {"path": "models"}}
```

The handler does not expose arbitrary URLs or shell commands. Large-model serverless cold starts can be substantial, so keep weights on a network volume or use a dedicated Pod when consistent latency matters.
