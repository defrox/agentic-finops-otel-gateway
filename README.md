# Agentic FinOps & OpenTelemetry LLM Gateway

[![Kubernetes](https://img.shields.io/badge/kubernetes-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-000000?logo=opentelemetry&logoColor=white)](https://opentelemetry.io/)

Enterprise LLM Inference & FinOps Gateway combining LiteLLM, vLLM routing, and OpenTelemetry per-tenant cost attribution.

## Quickstart
```bash
docker compose up -d
python telemetry/otel_middleware.py
```
