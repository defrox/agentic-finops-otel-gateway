import pytest
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
import telemetry.otel_middleware as mw


def test_vllm_cost_calculation_and_span_attributes():
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    mw.tracer = provider.get_tracer("test.finops.gateway")

    result = mw.trace_llm_call(
        tenant_id="risk-analytics",
        model="vllm-llama3-70b",
        prompt_tokens=1000,
        completion_tokens=1000,
    )

    assert result["model"] == "vllm-llama3-70b"
    assert result["cost_usd"] == pytest.approx(0.0016, rel=1e-6)

    spans = exporter.get_finished_spans()
    assert len(spans) == 1
    attrs = dict(spans[0].attributes)
    assert attrs["finops.tenant_id"] == "risk-analytics"
    assert attrs["llm.tokens.total"] == 2000
    assert attrs["finops.cost_usd"] == pytest.approx(0.0016, rel=1e-6)


def test_cloud_fallback_pricing():
    result = mw.trace_llm_call(
        tenant_id="core-platform",
        model="gpt-4o",
        prompt_tokens=500,
        completion_tokens=500,
    )
    assert result["cost_usd"] == pytest.approx(0.005, rel=1e-6)
