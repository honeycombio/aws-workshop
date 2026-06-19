---
title: "Step 4: Identify the Bottleneck"
weight: 504
---

Let's create a query specifically to identify our bottleneck:

### Query: Breakdown by Service Component

1. Create a new query:
   - **VISUALIZE**: `P95(duration_ms)`
   - **WHERE**: `service.name` = `otel-ai-chatbot`
   - **GROUP BY**: `name`
   - **ORDER BY**: `P95(duration_ms)` DESC
   - **LIMIT**: 10

2. **Run Query**

**Results**:
```
Operation                   P95 Duration
-----------------------------------------
gen_ai.bedrock.chat         350ms  ← SLOWEST
db.vector.search           180ms  ← SECOND SLOWEST
chat.request               545ms  (aggregate)
```

**Conclusion**: The LLM calls to Bedrock are our primary bottleneck.