---
title: "Step 4: Advanced - Use MCP to Analyze Instrumentation Quality (Optional)"
weight: 64
---

One powerful capability of Honeycomb MCP is analyzing instrumentation patterns across your services. Let's use Kiro CLI to examine our instrumentation quality.

**Ask Kiro CLI to analyze instrumentation:**

```
Query Honeycomb to show me what attributes are being captured on the gen_ai.bedrock.chat spans. Are we following OpenTelemetry GenAI semantic conventions v1.0?
```

Kiro CLI will:
1. Query for recent `gen_ai.bedrock.chat` spans
2. List all attributes being captured
3. Compare against OpenTelemetry v1.0 specifications
4. Identify any missing recommended attributes

**Expected insights:**
```
> Perfect! Now let me also check for any additional GenAI attributes that might be present by searching for all gen_ai.* fields:
Running tool find_columns with the param (from mcp server: honeycomb)
 ⋮  {
 ⋮    "dataset_slug": "otel-ai-chatbot-backend",
 ⋮    "environment_slug": "otel-ai-chatbot-backend",
 ⋮    "input": "gen_ai"
 ⋮  }
 - Completed in 1.20s

> ## GenAI Bedrock Chat Spans - OpenTelemetry Semantic Conventions Analysis

Based on the Honeycomb data, here are the GenAI attributes being captured on the Bedrock chat spans:

### ✅ Compliant GenAI Attributes (Following OTel GenAI v1.0):

| Attribute | Value Example | OTel v1.0 Status |
|-----------|---------------|------------------|
| gen_ai.system | aws.bedrock | ✅ Required |
| gen_ai.operation.name | chat | ✅ Required |
| gen_ai.request.model | anthropic.claude-3-5-sonnet-20240620-v1:0 | ✅ Required |
| gen_ai.request.max_tokens | 1000 | ✅ Optional |
| gen_ai.request.temperature | 0.70 | ✅ Optional |
| gen_ai.usage.input_tokens | 1242 | ✅ Optional |
| gen_ai.usage.output_tokens | 976 | ✅ Optional |
| gen_ai.response.finish_reasons | ["end_turn"] | ✅ Optional |

### 🔍 Additional Context Attributes:
- aws.request.id - AWS-specific request tracking
- cloud.region - us-west-2
- rpc.method - Converse (Bedrock API method)
- rpc.service - BedrockRuntime
- http.status_code - 200

### 📊 Compliance Assessment:

🎉 EXCELLENT COMPLIANCE - Your implementation is fully compliant with OpenTelemetry GenAI Semantic Conventions v1.0:

✅ All Required Attributes Present:
- gen_ai.system ✓
- gen_ai.operation.name ✓  
- gen_ai.request.model ✓

✅ Rich Optional Attributes:
- Token usage tracking (input/output)
- Request parameters (temperature, max_tokens)
- Response metadata (finish_reasons)

✅ Proper Values:
- System correctly identified as aws.bedrock
- Operation properly set as chat
- Model names follow proper format
- Finish reasons properly formatted as array

### 🏆 Best Practices Observed:
1. Complete token tracking for cost/usage monitoring
2. Request parameter capture for debugging/optimization
3. Response metadata for understanding model behavior
4. AWS-specific enrichment with request IDs and regions

Your GenAI instrumentation is exemplary and follows OpenTelemetry standards perfectly! 🚀
```

**Follow-up prompt to improve instrumentation:**

```
Based on the Honeycomb data, can you suggest improvements to our llmTracing.js to add the missing recommended attributes like temperature and max_tokens?
```

Kiro CLI will:
1. Review current `llmTracing.js` implementation
2. Identify where to add missing attributes
3. Propose code changes with proper v1.0 naming
4. Ensure changes follow best practices

::alert[**MCP Superpower**: This workflow demonstrates using observability data to drive instrumentation improvements. The AI agent learns from what's actually being captured in production and suggests enhancements based on standards and patterns it discovers.]{type="success"}
