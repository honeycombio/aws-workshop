---
title: "Step 3: Application Logs and Traces"
weight: 43
---

## Check Application Logs for Tracing initialization

1. **View recent CloudWatch logs**:
   ```bash
   cd /workshop/ai-workshop/pulumi
   # Find the log group name (has Pulumi-generated suffix)
   LOG_GROUP=$(pulumi env run honeycomb-pulumi-workshop/ws -i -- \
     aws logs describe-log-groups --log-group-name-prefix otel-ai-chatbot-logs \
     --query 'logGroups[0].logGroupName' --output text)

   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws logs tail \
     $LOG_GROUP \
     --since 1h \
     --filter-pattern "OpenTelemetry"
   ```

   Look for these log lines:
   ```
   [OpenTelemetry] ✨ Tracing and logging initialized
   [OpenTelemetry] 📊 Service: otel-ai-chatbot-backend
   [OpenTelemetry] 🌍 Environment: development
   [OpenTelemetry] 🔗 Endpoint: https://api.honeycomb.io
   [OpenTelemetry] 📝 Logs will be sent to both CloudWatch and Honeycomb
   ```

   If you see these logs, OpenTelemetry is successfully initialized! ✅

2. **If logs don't show initialization**, check for errors:
   ```bash
   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws logs tail \
     $LOG_GROUP \
     --since 1h \
     --filter-pattern "error"
   ```

## Generate Traffic to the Application

Now let's generate some requests to create traces.

1. **Get the application URL**:
   ```bash
   cd /workshop/ai-workshop/pulumi
   ALB_URL=$(pulumi stack output albUrl)
   echo "Application URL: $ALB_URL"
   ```

2. **Send a few chat requests**:
   ```bash
   for i in {1..3}; do
     echo "Request $i:"
     curl -X POST "${ALB_URL}/api/chat" \
       -H "Content-Type: application/json" \
       -d '{"message": "How do I instrument Express.js with OpenTelemetry?"}' \
       -w "\nHTTP Status: %{http_code}, Time: %{time_total}s\n\n"
     sleep 2
   done
   ```

   Expected output:
   ```
   Request 1:
   {"success":true,"response":"To instrument Express.js...","sources":[...]}
   HTTP Status: 200, Time: 2.341s

   Request 2:
   {"success":true,"response":"To instrument Express.js...","sources":[...]}
   HTTP Status: 200, Time: 1.876s
   ```

3. **Check health endpoint** (note: this is excluded from tracing):
   ```bash
   curl "${ALB_URL}/api/health"
   ```

   Expected:
   ```json
   {
     "status": "healthy",
     "timestamp": "2024-01-15T10:30:45.123Z",
     "services": {
       "llm": "bedrock",
       "vectorStore": "opensearch"
     }
   }
   ```

::alert[**Health Check Exclusion**: The `/api/health` endpoint is intentionally excluded from tracing (see `config/tracing.js:79-82`) to avoid noisy telemetry from load balancer health checks.]{type="info"}

## Verify Traces in Honeycomb

1. **Login to Honeycomb**: https://ui.honeycomb.io

2. **Select your dataset**: `otel-ai-chatbot-dev` (or `otel-ai-chatbot-ws` depending on your stack)

3. **View Recent Traces**:
   - You should see traces appearing in real-time
   - Each trace represents one chat request

4. **Click on a trace to examine it**:

   You'll see the trace waterfall showing:
   ```
   POST /api/chat (root span)
   ├─ gen_ai.bedrock.chat (~1.8s)
   │  └─ AWS Bedrock InvokeModel (~1.7s)
   ├─ db.vector.search (~0.3s)
   │  └─ HTTPS POST OpenSearch (~0.2s)
   └─ serialization (~0.05s)
   ```

5. **Examine span attributes**:

   Click on the `gen_ai.bedrock.chat` span to see attributes:
   - `gen_ai.system` = "aws.bedrock"
   - `gen_ai.operation.name` = "chat"
   - `gen_ai.request.model` = "anthropic.claude-3-5-sonnet-20240620-v1:0"
   - `gen_ai.usage.input_tokens` = 652
   - `gen_ai.usage.output_tokens` = 234
   - `gen_ai.response.finish_reasons` = ["stop"]
   - `gen_ai.response.id` = "msg_01ABC..."
   - `server.address` = "bedrock-runtime.us-east-1.amazonaws.com"

::alert[**Success!** You're now seeing production-grade observability data. The application was instrumented from day one, and you only had to configure where to send the data.]{type="success"}