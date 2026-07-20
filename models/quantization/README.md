# Quantization profiles

Start with the official BF16 weights when the GPU topology can support them. Use a reviewed quantized checkpoint only after measuring coding quality, tool-call validity, latency, and memory on the actual endpoint.

Supported launcher values are `fp8`, `awq`, `gptq`, and `bitsandbytes`, but the value alone does not convert the official model. `MODEL_ID` must point to a checkpoint compatible with the selected quantization mode.

Never silently switch a production endpoint from the pinned official weights to an unrelated community quantization.
