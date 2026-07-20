# GPU profiles

No GPU profile is considered supported until it passes startup, smoke, tool-call, latency, throughput, and memory checks.

## Initial profile

- Tensor parallelism: 2
- Context: 32K
- Concurrent sequences: 2
- GPU memory utilization target: 90%
- Prefix caching: enabled
- Chunked prefill: enabled

Reduce context or concurrency first if startup or runtime memory fails. Do not hide OOM errors by returning empty or mock output.
