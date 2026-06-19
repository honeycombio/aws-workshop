---
title: "Step 5: Explore Log Correlation"
weight: 45
---

One powerful feature of OpenTelemetry is **log-trace correlation**. Winston logs are automatically correlated with traces.

1. **View logs with trace context**:
   ```bash
   cd /workshop/ai-workshop/pulumi
   # Find the log group name (has Pulumi-generated suffix)
   LOG_GROUP=$(pulumi env run honeycomb-pulumi-workshop/ws -i -- \
     aws logs describe-log-groups --log-group-name-prefix otel-ai-chatbot-logs \
     --query 'logGroups[0].logGroupName' --output text)

   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws logs tail \
     $LOG_GROUP \
     --since 5m \
     --filter-pattern "api chat"
   ```

   You'll see logs like:
   ```json
   {
     "message": "Incoming request: POST /api/chat",
     "level": "info",
     "trace_id": "7f8c9d2e1a3b4c5d6e7f8g9h0i1j2k3l",
     "span_id": "a1b2c3d4e5f6g7h8",
     "timestamp": "2024-01-15T10:30:45.123Z"
   }
   ```

2. **In Honeycomb**, click on a log event and you'll see:
   - **Trace ID**: Links directly to the associated trace
   - **Span ID**: Links to the specific span where the log occurred
   - **Service context**: Automatic enrichment with service name, version, environment

This correlation allows you to:
- Navigate from log → trace
- Navigate from trace → logs
- Understand the full context of any event