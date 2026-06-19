---
title: "Step 9: Analyze the Root Cause"
weight: 509
---

Based on our investigation, we've identified:

1. **Primary Bottleneck**: Bedrock API calls (P95: 350ms)
2. **Secondary Bottleneck**: OpenSearch vector search (P95: 180ms)
3. **Infrastructure Constraint**: ECS task is CPU-constrained (0.5 vCPU hitting 85-90% utilization)
4. **Cost Impact**: High token usage (~1000 tokens/request)

**Root Cause Hypothesis:**
- The ECS task has insufficient CPU (0.5 vCPU)
- Under load, CPU contention adds overhead to all operations
- This makes already-slow Bedrock calls appear even slower
- Solution: Increase ECS task CPU allocation

**How would we normally fix this?**
1. Update Pulumi code to change CPU from 512 (0.5 vCPU) to 1024 (1 vCPU)
2. Redeploy with `pulumi up`
3. Monitor to verify improvement

But in Module 4, we'll use **AI agents** to propose and apply this fix automatically!

## Step 10: Stop Load Generator

Before moving to the next module, stop the load generator:

```bash
kill $LOAD_PID
# Or if you lost the PID:
pkill -f generate-load.sh
```