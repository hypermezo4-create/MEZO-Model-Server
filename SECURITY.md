# Security Policy

Report vulnerabilities privately to the repository owner. Never place tokens, private prompts, proprietary code, exploit payloads, or infrastructure details in public issues.

## Threat boundaries

- Requests from the Control Plane are authenticated but still validated.
- Prompts and tool schemas are data, never executable instructions for the host.
- vLLM is the inference engine; shell and repository tools are not installed as model tools.
- The endpoint must not be exposed publicly without an API key and provider/network controls.
- Model downloads are pinned to an approved revision.

## Secret rules

`MODEL_API_KEY` and `HF_TOKEN` belong in RunPod secrets or another secret manager. Diagnostics must redact them. Never commit `.env`, generated credentials, or endpoint tokens.
