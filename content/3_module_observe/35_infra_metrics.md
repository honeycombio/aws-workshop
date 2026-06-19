---
title: "Step 5: Correlate with Infrastructure Metrics in Honeycomb"
weight: 505
---

Now let's correlate application performance with infrastructure resource utilization. Thanks to CloudWatch Metric Streams, ECS metrics are automatically flowing into Honeycomb!

### Query ECS Metrics in the cloudwatch-metrics Dataset

1. **Switch to the `cloudwatch-metrics` dataset** in Honeycomb
   - Click the dataset dropdown in the top-left corner
   - Select `cloudwatch-metrics`
   - This dataset contains all ECS and Container Insights metrics streamed from CloudWatch

2. **Explore available metrics first**:

   In the `cloudwatch-metrics` dataset, click the "Columns" icon to see available fields. CloudWatch metrics come in with suffixes like:
   - `AWS/ECS/CPUUtilization.avg` - Average value
   - `AWS/ECS/CPUUtilization.max` - Maximum value
   - `AWS/ECS/CPUUtilization.min` - Minimum value

3. **Query ECS CPU Utilization**:
   - **VISUALIZE**: `AVG(AWS/ECS/CPUUtilization.avg)`, `MAX(AWS/ECS/CPUUtilization.max)`
   - **WHERE**: `metric_stream_name` EXISTS
   - **GROUP BY**: `time` (5-minute buckets)
   - **Time Range**: Last 1 hour

   **Expected Results**:
   ```
   Time Window    AVG(CPU)    MAX(CPU)
   ----------------------------------------
   10:00-10:05    62%         78%
   10:05-10:10    68%         85%
   10:10-10:15    71%         91%  ← High!
   10:15-10:20    65%         88%
   ```

4. **Query ECS Memory Utilization**:
   - **VISUALIZE**: `AVG(AWS/ECS/MemoryUtilization.avg)`, `MAX(AWS/ECS/MemoryUtilization.max)`
   - **WHERE**: `metric_stream_name` EXISTS
   - **GROUP BY**: `time` (5-minute buckets)
   - **Time Range**: Last 1 hour

   **Expected Results**:
   ```
   Time Window    AVG(Memory)    MAX(Memory)
   ----------------------------------------
   10:00-10:05    76%            79%
   10:05-10:10    78%            82%
   10:10-10:15    77%            81%
   ```

   ::alert[**Metric Naming**: CloudWatch metrics arrive in OpenTelemetry format with the full namespace path (e.g., `AWS/ECS/CPUUtilization`) and aggregation suffixes (`.avg`, `.max`, `.min`). Use `.avg` for typical queries and `.max` to find peak values.]{type="info"}

5. **Correlate with Application Latency**:

   Now switch back to your application dataset (`otel-ai-chatbot-dev` or `otel-ai-chatbot-ws`) and create a parallel query:
   - **VISUALIZE**: `P95(duration_ms)`
   - **WHERE**: `name` = `chat.request`
   - **GROUP BY**: `time` (5-minute buckets)
   - **Time Range**: Last 1 hour (same as infrastructure queries)

   **Compare the patterns**:
   - Notice how P95 latency spikes correlate with CPU utilization spikes
   - When CPU hits 85-90%, latency increases significantly
   - This confirms CPU constraint is affecting application performance

::alert[**Honeycomb Power Move**: Open two browser tabs side-by-side—one with the `cloudwatch-metrics` dataset showing CPU/memory, another with your app dataset showing latency. Use the same time range to visually correlate spikes. In production, you can create a Board with graphs from both datasets for unified monitoring.]{type="success"}

### Using BubbleUp to Find Hot Services

Want to see which specific ECS services or clusters are having resource issues?

1. **In the `cloudwatch-metrics` dataset**, create a query:
   - **VISUALIZE**: `HEATMAP(AWS/ECS/CPUUtilization.max)`
   - **WHERE**: `metric_stream_name` EXISTS
   - **Time Range**: Last 1 hour

2. **Click BubbleUp** on the highest CPU bucket (rightmost columns)

3. **BubbleUp will analyze** and show you:
   - Which CloudWatch dimension values (cluster, service) have the highest CPU
   - Whether specific services are consistently hot
   - If the issue is widespread across the cluster or isolated to certain services

   ::alert[**Pro Tip**: CloudWatch dimensions become fields in Honeycomb. Look for fields like `ClusterName`, `ServiceName`, or `TaskDefinitionFamily` to GROUP BY and narrow down which specific resources are constrained.]{type="success"}

**Analysis**: The ECS task is undersized (0.5 vCPU, 1GB RAM). Under load, CPU consistently hits 85-91%, which causes:
- Increased application latency due to CPU contention
- Bedrock calls appear slower (processes queue for CPU time)
- All operations slow down proportionally

**Root Cause Confirmed**: Infrastructure constraint (undersized ECS task) is the primary bottleneck, not the external services (Bedrock, OpenSearch).

::alert[**Why This Matters**: By querying CloudWatch metrics directly in Honeycomb, you eliminated context switching to the AWS console. You used the same query interface, BubbleUp, and correlation techniques across both infrastructure and application data. This is the power of unified observability.]{type="info"}