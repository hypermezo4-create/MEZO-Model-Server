ARG VLLM_IMAGE=vllm/vllm-openai:v0.15.0
FROM ${VLLM_IMAGE}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/opt/mezo/src

WORKDIR /opt/mezo
COPY src ./src
COPY models ./models
COPY scripts ./scripts
COPY AGENTS.md SECURITY.md README.md ./

RUN mkdir -p /models && chmod 0755 /models

EXPOSE 8000
ENTRYPOINT ["python", "-m", "mezo_model_server.launcher"]
