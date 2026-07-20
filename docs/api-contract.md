# API contract

The dedicated endpoint follows vLLM's OpenAI-compatible API. The MEZO Control Plane uses:

- `GET /health`
- `GET /v1/models`
- `POST /v1/chat/completions`
- `GET /metrics`

Requests use `Authorization: Bearer <MODEL_API_KEY>`. The served model alias is `qwen-coder-primary`.

Tool definitions are OpenAI function-tool JSON schemas. The response may contain `message.tool_calls`; this service returns them unchanged and never executes them.
