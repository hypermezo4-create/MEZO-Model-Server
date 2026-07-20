# Benchmark policy

Record results under a dated external artifact or release, not as unverifiable prose. Every result must include:

- image digest and git commit
- model ID and revision
- GPU type and count
- quantization and dtype
- tensor/pipeline parallelism
- maximum context and concurrency
- prompt/output token counts
- latency and tokens per second
- peak GPU memory
- tool-call validity rate

Do not compare profiles with different prompts or output limits as though they were equivalent.
