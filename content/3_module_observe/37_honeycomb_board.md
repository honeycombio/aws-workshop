---
title: "Step 7: Create a Honeycomb Board"
weight: 507
---

Boards in Honeycomb let you create dashboards for ongoing monitoring. Let's create one:

1. In Honeycomb, click **Boards** → **New Board**

2. Name it: "OTel AI Chatbot Performance"

3. Add the following queries as separate graphs:

**Graph 1: Request Latency**
- **VISUALIZE**: `P50(duration_ms)`, `P95(duration_ms)`, `P99(duration_ms)`
- **WHERE**: `name` = `chat.request`
- **Graph Type**: Line chart

**Graph 2: Request Rate**
- **VISUALIZE**: `COUNT`
- **WHERE**: `name` = `chat.request`
- **GROUP BY**: `time` (1-minute buckets)
- **Graph Type**: Line chart

**Graph 3: Error Rate**
- **VISUALIZE**: `COUNT`
- **WHERE**: `error` = `true`
- **GROUP BY**: `error.message`
- **Graph Type**: Bar chart

**Graph 4: Bedrock Token Usage**
- **VISUALIZE**: `SUM(gen_ai.usage.input_tokens)`, `SUM(gen_ai.usage.output_tokens)`
- **WHERE**: `gen_ai.request.model` exists
- **GROUP BY**: `time` (5-minute buckets)
- **Graph Type**: Stacked area chart

**Graph 5: OpenSearch Query Performance**
- **VISUALIZE**: `P95(duration_ms)`
- **WHERE**: `name` = `db.vector.search`
- **GROUP BY**: `db.vector.k` (number of results requested)
- **Graph Type**: Line chart

**Graph 6: Estimated API Costs** (using calculated field)
- **VISUALIZE**: `SUM(cost_per_request_usd)`
- **GROUP BY**: `time` (1-hour buckets)
- **Graph Type**: Line chart

4. Click **Save Board**

::alert[**Dashboards vs. Exploratory Analysis**: Boards are great for monitoring known metrics. But Honeycomb's real power is ad-hoc queries when investigating incidents or exploring new patterns. Always start with exploration, then create boards for recurring questions.]{type="info"}