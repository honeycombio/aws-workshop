---
title: "Step 7: Sampling Strategies and Approaches"
weight: 47
---

## Sampling Strategies for Production

While the workshop captures 100% of traces for demonstration purposes, **production deployments require sampling** to balance cost, privacy, and observability value.

### Understanding Sampling Trade-offs

**Why sample?**
- **Privacy Protection**: Avoid capturing sensitive user data in every trace
- **Cost Management**: Reduce data volume sent to observability backend
- **Performance**: Minimize instrumentation overhead in high-throughput services
- **Compliance**: Meet data retention and privacy regulations (GDPR, CCPA)

**What to always capture (100%):**
- ✅ Structured metadata: tokens, model, latency, user IDs, error types
- ✅ All errors and exceptions (critical for debugging)
- ✅ High-value transactions (user signups, purchases)
- ✅ Trace context for distributed tracing

**What to sample (1-10%):**
- 🔒 Full prompt content (`gen_ai.prompt.*.content`)
- 🔒 Full response content (`gen_ai.completion.*.content`)
- 🔒 PII-containing fields
- 📊 Routine successful operations in high-traffic endpoints

### Sampling Approaches

#### Option 1: Head-Based Sampling (Simple)

Decides at trace start whether to sample. Good for development and testing.

```javascript
// config/tracing.js
import { TraceIdRatioBasedSampler } from '@opentelemetry/sdk-trace-base';

const sdk = new NodeSDK({
  sampler: new TraceIdRatioBasedSampler(0.1), // Sample 10% of traces
  // ... other config
});
```

**Pros**: Simple, deterministic, low overhead
**Cons**: Might miss important error traces if unlucky

#### Option 2: Tail-Based Sampling (Production-Recommended)

Examines complete trace before deciding to sample. Captures ALL errors while sampling successes.

```javascript
// Requires OpenTelemetry Collector
// collector-config.yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      # Always sample errors
      - name: errors-policy
        type: status_code
        status_code: {status_codes: [ERROR]}

      # Always sample slow requests
      - name: slow-traces-policy
        type: latency
        latency: {threshold_ms: 1000}

      # Always sample on specific attributes
      - name: high-value-users
        type: attribute
        attribute: {key: user.tier, values: [premium, enterprise]}

      # Sample 1% of everything else
      - name: probabilistic-policy
        type: probabilistic
        probabilistic: {sampling_percentage: 1}
```

**Pros**: Intelligent sampling, captures all errors, production-grade
**Cons**: Requires Collector, more complex setup

#### Option 3: Content Sampling (Privacy-Focused)

Capture 100% of traces but sample sensitive content within spans.

```javascript
// server/utils/llmTracing.js
const CAPTURE_CONTENT = process.env.OTEL_GENAI_CAPTURE_CONTENT === 'true';
const CONTENT_SAMPLE_RATE = parseFloat(process.env.OTEL_GENAI_CONTENT_SAMPLE_RATE || '0.01');

export async function traceLLMCall(providerName, modelName, systemPrompt, userPrompt, fn, metadata = {}) {
  return tracer.startActiveSpan(
    `gen_ai.${providerName}.chat`,
    { /* ... attributes ... */ },
    async (span) => {
      try {
        const result = await fn();

        // Always capture metadata (100%)
        span.setAttributes({
          'gen_ai.usage.input_tokens': usage.promptTokens,
          'gen_ai.usage.output_tokens': usage.completionTokens,
          'gen_ai.response.id': result.id,
          'gen_ai.response.finish_reasons': [result.stop_reason]
        });

        // Conditionally capture content (1% sample rate)
        if (CAPTURE_CONTENT && (Math.random() < CONTENT_SAMPLE_RATE || span.isErrored())) {
          // Always capture on errors, otherwise sample at 1%
          span.setAttributes({
            'gen_ai.prompt.0.content': redactPII(systemPrompt),
            'gen_ai.prompt.1.content': redactPII(userPrompt),
            'gen_ai.completion.0.content': redactPII(result.content)
          });
        }

        return result;
      } catch (error) {
        // ALWAYS capture prompts on errors for debugging
        if (CAPTURE_CONTENT) {
          span.setAttributes({
            'gen_ai.prompt.0.content': redactPII(systemPrompt),
            'gen_ai.prompt.1.content': redactPII(userPrompt)
          });
        }
        throw error;
      }
    }
  );
}

// Simple PII redaction example
function redactPII(text) {
  return text
    .replace(/\b\d{3}-\d{2}-\d{4}\b/g, '[SSN]')           // SSN
    .replace(/\b[\w\.-]+@[\w\.-]+\.\w+\b/g, '[EMAIL]')    // Email
    .replace(/\b\d{16}\b/g, '[CARD]');                     // Credit card
}
```

**Pros**: Fine-grained control, privacy-first, captures all metadata
**Cons**: Requires code changes, manual PII redaction implementation

### Recommended Strategy for This Workshop

**Development/Testing:**
- ✅ Use head-based sampling at 100% (current implementation)
- ✅ No content capture by default (privacy-safe for workshop)

**Production:**
- ✅ Use tail-based sampling with OpenTelemetry Collector
- ✅ Capture 100% of errors and slow traces
- ✅ Sample 1-5% of successful traces
- ✅ Implement PII redaction for any captured content
- ✅ Use separate datasets for dev (100%) vs. prod (sampled)

::alert[**Workshop Note**: The current implementation captures 100% of traces with no prompt/response content. This is appropriate for the workshop. In production, implement tail-based sampling via OpenTelemetry Collector for optimal cost and privacy balance.]{type="success"}