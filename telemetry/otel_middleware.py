from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("agentic.finops.gateway")

MODEL_PRICING_PER_1K = {
    "gpt-4o": 0.005,
    "vllm-llama3-70b": 0.0008,
}

def trace_llm_call(tenant_id: str, model: str, prompt_tokens: int, completion_tokens: int) -> dict:
    total_tokens = prompt_tokens + completion_tokens
    estimated_cost = (total_tokens / 1000) * MODEL_PRICING_PER_1K.get(model, 0.001)

    with tracer.start_as_current_span("llm.inference.request") as span:
        span.set_attribute("finops.tenant_id", tenant_id)
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.tokens.total", total_tokens)
        span.set_attribute("finops.cost_usd", round(estimated_cost, 6))
        return {"model": model, "cost_usd": round(estimated_cost, 6)}

if __name__ == "__main__":
    print(trace_llm_call("finance-squad", "vllm-llama3-70b", 1200, 450))
