---
title: "Step 8: Migrate from CloudWatch Alarms to Honeycomb Triggers"
weight: 508
---

Traditional AWS deployments use CloudWatch Alarms for alerting. Let's see how to migrate these to Honeycomb Triggers, which work across both application traces and infrastructure metrics.

### Example: ECS CPU Alarm → Honeycomb Trigger

**What the CloudWatch Alarm looked like:**

```typescript
// Traditional CloudWatch Alarm (Pulumi)
const ecsCpuAlarm = new aws.cloudwatch.MetricAlarm("ecs-high-cpu", {
    comparisonOperator: "GreaterThanThreshold",
    evaluationPeriods: 2,
    metricName: "CPUUtilization",
    namespace: "AWS/ECS",
    period: 300,
    statistic: "Average",
    threshold: 80,
    dimensions: {
        ClusterName: cluster.name,
        ServiceName: service.name,
    },
    alarmActions: [snsTopicArn],
});
```

**Honeycomb Trigger equivalent:**

1. In Honeycomb, switch to the `cloudwatch-metrics` dataset

2. Go to **Triggers** → **New Trigger**

3. Configure the trigger:
   - **Name**: ECS High CPU Alert
   - **Query**:
     - **VISUALIZE**: `AVG(AWS/ECS/CPUUtilization.avg)`
     - **WHERE**: `metric_stream_name` EXISTS
     - **GROUP BY**: None (or `ClusterName`, `ServiceName` for per-service alerting)
   - **Threshold**: Alert when `AVG(AWS/ECS/CPUUtilization.avg)` > 80
   - **Evaluation Window**: 5 minutes (equivalent to 2 periods of 300s)
   - **Notification**: Email, Slack, PagerDuty, or webhook

4. Click **Create Trigger**

**Why this is better:**
- ✅ **Unified interface**: Same tool for application AND infrastructure alerts
- ✅ **Rich context**: Click through from alert to query with full BubbleUp capabilities
- ✅ **High-cardinality**: Alert on specific tasks, services, or custom dimensions
- ✅ **Correlation ready**: Immediately correlate with application traces in the same tool

### Example: Application Latency Alert

For application-level alerting:

1. Switch to your application dataset (`otel-ai-chatbot-dev`)

2. Create a new trigger:
   - **Name**: High P95 Latency
   - **Query**:
     - **VISUALIZE**: `P95(duration_ms)`
     - **WHERE**: `name` = `chat.request`
   - **Threshold**: Alert when P95 > 500ms
   - **Evaluation Window**: 5 minutes
   - **Notification**: Email or Slack webhook

3. Click **Create Trigger**

### Module 4 Pattern: Redis Cache Alarms

In Module 4, when AI agents propose adding Redis caching, they also create CloudWatch alarms for:
- Redis CPU utilization
- Redis memory utilization
- Redis eviction rate
- Cache hit rate

These alarms can be migrated to Honeycomb Triggers following the same pattern:
- Query CloudWatch metrics in the `cloudwatch-metrics` dataset
- Set thresholds based on your SLOs
- Benefit from Honeycomb's BubbleUp to identify which specific cache nodes or keys are problematic

::alert[**Infrastructure as Code**: In a production environment, you'd define these triggers in Pulumi using Honeycomb's API. This ensures your alerting is version-controlled alongside your infrastructure. We'll show an example of this in the next step.]{type="info"}

### Step 8a: Creating Honeycomb Triggers as Code (Advanced)

For production environments, you'll want to define triggers as infrastructure-as-code. Here's how to create Honeycomb Triggers using Pulumi's Command provider:

**Example Pulumi code for an ECS CPU trigger:**

```typescript
import * as command from "@pulumi/command";

// Create a Honeycomb Trigger for ECS High CPU
const ecsCpuTrigger = new command.local.Command("honeycomb-ecs-cpu-trigger", {
    create: pulumi.interpolate`curl -X POST https://api.honeycomb.io/1/triggers \
        -H "X-Honeycomb-Team: ${config.requireSecret("honeycombApiKey")}" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "ECS High CPU Alert",
            "dataset_slug": "cloudwatch-metrics",
            "query": {
                "calculations": [{
                    "op": "AVG",
                    "column": "AWS/ECS/CPUUtilization.avg"
                }],
                "filters": [{
                    "column": "metric_stream_name",
                    "op": "exists"
                }],
                "time_range": 300
            },
            "threshold": {
                "op": "gt",
                "value": 80
            },
            "alert_type": "on_change",
            "recipients": [{
                "type": "email",
                "target": "ops-team@example.com"
            }]
        }'`,
    update: pulumi.interpolate`echo "Trigger already exists"`,
    delete: pulumi.interpolate`echo "Trigger deletion would go here"`,
});
```

**For Redis cache alarms (Module 4 pattern):**

```typescript
// Redis CPU utilization trigger
const redisCpuTrigger = new command.local.Command("honeycomb-redis-cpu-trigger", {
    create: pulumi.interpolate`curl -X POST https://api.honeycomb.io/1/triggers \
        -H "X-Honeycomb-Team: ${config.requireSecret("honeycombApiKey")}" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Redis High CPU",
            "dataset_slug": "cloudwatch-metrics",
            "query": {
                "calculations": [{
                    "op": "AVG",
                    "column": "AWS/ElastiCache/CPUUtilization.avg"
                }],
                "filters": [{
                    "column": "CacheClusterId",
                    "op": "exists"
                }],
                "time_range": 300
            },
            "threshold": {
                "op": "gt",
                "value": 75
            },
            "alert_type": "on_change"
        }'`,
});

// Redis eviction rate trigger
const redisEvictionTrigger = new command.local.Command("honeycomb-redis-eviction-trigger", {
    create: pulumi.interpolate`curl -X POST https://api.honeycomb.io/1/triggers \
        -H "X-Honeycomb-Team: ${config.requireSecret("honeycombApiKey")}" \
        -H "Content-Type: application/json" \
        -d '{
            "name": "Redis High Evictions",
            "dataset_slug": "cloudwatch-metrics",
            "query": {
                "calculations": [{
                    "op": "SUM",
                    "column": "AWS/ElastiCache/Evictions.sum"
                }],
                "filters": [{
                    "column": "CacheClusterId",
                    "op": "exists"
                }],
                "time_range": 300
            },
            "threshold": {
                "op": "gt",
                "value": 100
            },
            "alert_type": "on_change"
        }'`,
});
```

**Benefits of Triggers as Code:**
- ✅ **Version Control**: All alerting rules tracked in git
- ✅ **Review Process**: Trigger changes go through PR review
- ✅ **Reproducible**: Spin up new environments with identical alerting
- ✅ **Automated**: Deploy triggers alongside infrastructure changes
- ✅ **Auditable**: Full history of who changed what and when

::alert[**Production Tip**: Use a dedicated Honeycomb Configuration API key (not an Ingest key) for creating triggers. Store it in Pulumi ESC or AWS Secrets Manager just like other sensitive configuration.]{type="warning"}