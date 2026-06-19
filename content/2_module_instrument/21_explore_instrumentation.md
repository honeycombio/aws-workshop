---
title: "Step 1: Explore and Understand Instrumentation"
weight: 41
---

## Explore the Existing Instrumentation

The `ai-workshop` application already has complete OpenTelemetry instrumentation. Let's examine how it works.

1. **Navigate to the server directory**:
   ```bash
   cd /workshop/ai-workshop/server
   ls -la
   ```

   Key files:
   - `instrumentation.js` - Entry point for tracing
   - `config/tracing.js` - OpenTelemetry SDK configuration
   - `utils/llmTracing.js` - Custom LLM tracing utilities
   - `index.js` - Server entry point (imports instrumentation FIRST)

2. **Examine the instrumentation entry point**:
   ```bash
   cat instrumentation.js
   ```

   ```javascript
   /**
    * OpenTelemetry Instrumentation Entry Point
    *
    * This file MUST be imported before any other application code
    * to ensure proper auto-instrumentation of libraries.
    */
   import { initializeTracing } from './config/tracing.js';

   // Initialize tracing immediately
   initializeTracing();
   ```

   **Key Insight**: Instrumentation is initialized **before** any other imports. This ensures auto-instrumentation captures all operations.

3. **Best Practice - High-Cardinality Attributes**:

   When instrumenting your application, Honeycomb excels at handling **high-cardinality data**—attributes with many unique values that traditional monitoring tools struggle with. The application includes attributes like:

   - `user.id` or `session.id` - Unique per user/session
   - `request.id` - Unique per request
   - `gen_ai.request.model` - Specific model version used
   - `deployment.environment` - Environment identifier

   ::alert[**Honeycomb Advantage**: Unlike traditional metrics systems that require pre-aggregation, Honeycomb stores raw event data with all high-cardinality attributes intact. This allows you to ask questions like "Show me all requests from user X where token usage exceeded Y" without pre-defining these queries.]{type="success"}

4. **Review the tracing configuration**:
   ```bash
   cat config/tracing.js | head -60
   ```

   This file configures:
   - **OTLP Exporters** for traces and logs
   - **Resource attributes** (service name, version, environment)
   - **Auto-instrumentations** for Express, HTTP, AWS SDK
   - **Winston instrumentation** for log correlation
   - **Honeycomb-specific configuration**

5. **Examine custom LLM tracing utilities**:
   ```bash
   cat utils/llmTracing.js | head -95
   ```

   The `traceLLMCall()` function wraps Bedrock API calls with:
   - **GenAI semantic conventions v1.0**: `gen_ai.system`, `gen_ai.operation.name`, `gen_ai.request.model`
   - **Token usage tracking**: `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`
   - **Error handling**: Proper span status, exception recording, and `error.type` attribute
   - **Response metadata**: `gen_ai.response.id`, `gen_ai.response.finish_reasons`

::alert[**Production Pattern**: Custom instrumentation captures business-specific metrics (token usage, model performance) that auto-instrumentation can't infer. This is critical for cost monitoring and SLO tracking.]{type="success"}

## Understand Auto-Instrumentation

The application uses `getNodeAutoInstrumentations()` to automatically instrument popular libraries:

**What's instrumented automatically:**
- ✅ **Express.js**: HTTP request/response spans with route information
- ✅ **HTTP/HTTPS**: Outbound HTTP client calls (to Bedrock, OpenSearch)
- ✅ **AWS SDK**: All AWS service calls (Bedrock InvokeModel, OpenSearch queries)
- ✅ **Winston**: Log correlation with trace and span IDs

**Example trace structure** you'll see:
```
POST /api/chat (Express auto-instrumentation)
├─ gen_ai.bedrock.chat (Custom GenAI instrumentation)
│  └─ AWS Bedrock InvokeModel (AWS SDK auto-instrumentation)
├─ db.vector.search (Custom RAG instrumentation)
│  └─ HTTPS POST OpenSearch (HTTP auto-instrumentation)
└─ Response
```

Each span automatically includes:
- **Timing**: Duration, start/end timestamps
- **Context**: Trace ID, span ID, parent span ID
- **Attributes**: HTTP method, status code, URL, etc.
- **Resource**: Service name, version, deployment environment