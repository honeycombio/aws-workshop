---
title: "Step 4: Understand the GenAI Semantic Conventions"
weight: 44
---

The LLM tracing follows OpenTelemetry's **standardized semantic conventions for GenAI** workloads. These conventions were recently finalized as part of OpenTelemetry's official specifications, representing a major milestone for standardizing AI observability across the industry.

| Attribute | Description | Example |
|-----------|-------------|---------|
| `gen_ai.system` | The GenAI system/provider | "bedrock", "openai", "anthropic" |
| `gen_ai.request.model` | Model identifier | "anthropic.claude-3-5-sonnet-20240620-v1:0" |
| `gen_ai.operation.name` | Type of GenAI operation | "completion", "embedding", "chat" |
| `gen_ai.usage.input_tokens` | Input tokens consumed | 652 |
| `gen_ai.usage.output_tokens` | Output tokens generated | 234 |
| `gen_ai.response.finish_reasons` | Completion reason | "stop", "length", "error" |
| `gen_ai.prompt.0.content` | First prompt content (sampling) | "You are a helpful assistant..." |
| `gen_ai.response.id` | Unique response identifier | "msg_01ABC..." |
| `error.type` | Error type if failed | "RateLimitError", "InvalidRequest" |

**Why these attributes matter:**
- **Cost tracking**: Token usage directly correlates to API costs ($3-15 per million tokens)
- **Performance monitoring**: Duration helps identify slow models or API issues
- **Error analysis**: Distinguish between rate limits, timeouts, and invalid requests
- **Model comparison**: Compare performance across different models and versions
- **Prompt engineering**: Analyze which prompts lead to better outcomes (when sampled)
- **User attribution**: Track which users/teams consume the most tokens

::alert[**OpenTelemetry Standard**: As of 2025, GenAI semantic conventions are now part of the official OpenTelemetry specification. This ensures consistent instrumentation across all observability vendors. See https://opentelemetry.io/docs/specs/semconv/gen-ai/ for complete details.]{type="success"}

### Best Practice: Capturing the Right Context

When instrumenting GenAI applications, Honeycomb recommends capturing:

1. **All errors** - Not just LLM API failures, but also:
   - Invalid or malformed responses that cause downstream errors
   - Timeout errors from slow responses
   - Rate limiting and quota exceeded errors

2. **User/team identifiers** - High-cardinality attributes like:
   - `user.id` - Track per-user behavior and costs
   - `team.id` - Analyze usage by team or organization
   - `session.id` - Correlate multiple requests in a conversation

3. **The actual prompt** (with sampling) - For debugging and optimization:
   - Use `gen_ai.prompt.0.content` to capture the system prompt
   - **Privacy consideration**: Sample at ~1% in production to protect sensitive user data
   - Always capture prompts for errors (100% sampling on failures) to aid debugging
   - Consider redacting PII from prompts before sending to observability platforms

4. **RAG context** - If using retrieval-augmented generation:
   - `rag.documents_retrieved` - Number of documents fetched
   - `rag.documents_used` - Number actually included in context
   - `rag.retrieval_latency_ms` - Time spent on vector search

5. **Function/tool calls** - For agentic workflows:
   - `gen_ai.tools_count` - Number of tools available
   - `gen_ai.tool_calls` - Which tools were invoked
   - Each tool call as a child span with its own attributes

::alert[**Privacy vs. Visibility**: While Honeycomb doesn't charge extra for high-cardinality attributes, consider sampling sensitive data like full prompts/responses primarily for **privacy protection**. Capture 100% of metadata (tokens, model, latency, user IDs) but sample full prompt/response content at 1-10% depending on your privacy requirements. Always implement PII redaction for production workloads.]{type="info"}