---
title: "Module Summary"
weight: 48
---

Congratulations! You've successfully:

✅ Explored the existing OpenTelemetry instrumentation in the application

✅ Understood auto-instrumentation for Express, HTTP, and AWS SDK

✅ Reviewed custom GenAI tracing with v1.0 semantic conventions

✅ Learned about high-cardinality attributes and why they matter

✅ Verified Honeycomb configuration in the ECS task

✅ Generated traffic and confirmed traces are flowing to Honeycomb

✅ Examined trace structure and GenAI-specific attributes

✅ Understood log-trace correlation

✅ Learned deployment markers for correlating changes with performance

✅ Explored sampling strategies for production deployments

## Key Takeaways

### 1. Observability-Driven Development Culture

Just like you wouldn't deploy without logging or error handling, you shouldn't deploy without observability. Build it in from day one. At Honeycomb, engineers add telemetry as a **core part** of every feature and bug fix, creating a culture where observability is everyone's responsibility.

### 2. High-Cardinality is a Feature, Not a Bug

Traditional monitoring tools force you to aggregate away high-cardinality data (like user IDs, request IDs, model versions). Honeycomb **embraces** high-cardinality, allowing you to ask questions like "Show me all requests from user X where model Y exceeded Z tokens"—without pre-defining these queries.

### 3. Auto-Instrumentation Does the Heavy Lifting

OpenTelemetry's auto-instrumentation captures 80% of telemetry with zero code changes. Custom instrumentation fills the remaining 20% for business-specific metrics like token usage, RAG performance, and agentic workflows.

### 4. Configuration is Declarative

Environment variables control where telemetry goes, making it easy to send data to different backends without code changes (Honeycomb today, Jaeger tomorrow). This is the OpenTelemetry promise: **vendor-neutral instrumentation**.

### 5. GenAI Workloads Need Specialized Observability

Token usage, model selection, and prompt engineering directly impact cost and performance. The OpenTelemetry GenAI semantic conventions (now standardized) ensure consistent instrumentation across providers, making it easy to compare Bedrock vs OpenAI vs Anthropic direct.

### 6. Balance Privacy and Visibility with Sampling

Capture 100% of structured metadata (tokens, model, latency, user ID), but sample sensitive unstructured data like full prompts/responses at 1-10% primarily for **privacy protection**. Always capture 100% on errors for debugging, ensuring PII is redacted first.

### 7. Context Propagation is Automatic

OpenTelemetry automatically propagates trace context across service boundaries (HTTP calls, async operations, AWS SDK calls), giving you end-to-end visibility from API gateway → application → Bedrock → OpenSearch without manual plumbing.

## What's Next?

In **Module 3**, you'll use Honeycomb to analyze the telemetry data you're now collecting, identify performance bottlenecks, and discover resource constraints in the infrastructure.

---

## Additional Resources

- [OpenTelemetry Node.js Documentation](https://opentelemetry.io/docs/instrumentation/js/getting-started/nodejs/)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [Honeycomb OpenTelemetry Setup Guide](https://docs.honeycomb.io/getting-data-in/opentelemetry/)
- [AWS Distro for OpenTelemetry](https://aws-otel.github.io/)
