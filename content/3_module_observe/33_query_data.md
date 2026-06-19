---
title: "Step 3: Query Data with Honeycomb"
weight: 503
---

Honeycomb's power comes from its ability to slice and dice high-cardinality data. Unlike traditional metrics systems that require pre-aggregation, Honeycomb stores raw events and lets you ask arbitrary questions. This is the difference between **observability** (exploring unknowns) and **monitoring** (tracking known metrics).

::alert[**Honeycomb Philosophy**: Ask "WHY is this happening?" not just "WHAT is happening?" Traditional dashboards show you WHAT (CPU is high), but Honeycomb helps you understand WHY (which users, which endpoints, which code paths).]{type="info"}

### Query 1: Average Latency by Operation

1. In Honeycomb, click **New Query**

2. Set up the query:
   - **VISUALIZE**: `P50(duration_ms)`, `P95(duration_ms)`, `P99(duration_ms)`
   - **GROUP BY**: `name` (span name)
   - **WHERE**: `name` EXISTS (to filter out empty span names)
   - **Time Range**: Last 1 hour

3. Click **Run Query**

**Expected Results:**
```
Span Name                    P50    P95    P99
-------------------------------------------------
gen_ai.bedrock.chat         200ms  350ms  500ms
db.vector.search            100ms  180ms  250ms
chat.request                320ms  550ms  750ms
POST /api/chat              315ms  545ms  745ms
```

**Insights:**
- Bedrock calls have highest latency
- Vector search is moderately slow
- Some P99 latencies exceed 500ms (poor user experience)

**Best Practice - LIMIT for High Cardinality**: When grouping by high-cardinality fields (like `user.id` or `request.id`), always add a `LIMIT` clause to avoid overwhelming result tables. For example:
- **LIMIT 20**: Show top 20 slowest users
- **ORDER BY**: `P95(duration_ms)` DESC to see worst offenders first

### Query 2: Token Usage Analysis

1. Create a new query:
   - **VISUALIZE**: `SUM(gen_ai.usage.input_tokens)`, `SUM(gen_ai.usage.output_tokens)`
   - **WHERE**: `gen_ai.request.model` exists
   - **GROUP BY**: `time` (heatmap or line chart)
   - **Time Range**: Last 1 hour

2. **Run Query**

**Expected Results:**
- Input tokens: ~500-800 per request (RAG context + user question)
- Output tokens: ~200-400 per response
- Total: ~700-1200 tokens per request

::alert[**Cost Analysis**: With Claude 3.5 Sonnet pricing (~$3 per million input tokens, ~$15 per million output tokens), each request costs approximately $0.003-0.005. At 1000 requests/day, that's $3-5/day just for LLM calls.]{type="warning"}

### Query 3: Error Rate Analysis

1. Create a new query:
   - **VISUALIZE**: `COUNT`
   - **WHERE**: `error` = `true`
   - **GROUP BY**: `name`, `error.message`
   - **Time Range**: Last 1 hour

2. **Run Query**

**Expected Results** (if errors exist):
```
Span Name                  Error Message                    Count
-----------------------------------------------------------------------
db.vector.search           Connection timeout                  3
gen_ai.bedrock.chat        Rate limit exceeded                 1
```

**Insights:**
- Occasional OpenSearch timeouts (resource constraint?)
- Rare Bedrock rate limiting

### Query 4: Slowest Traces with Heatmap

1. Create a new query:
   - **VISUALIZE**: `HEATMAP(duration_ms)`
   - **WHERE**: `name` = `chat.request`
   - **Time Range**: Last 1 hour

2. Click on the slowest bucket in the heatmap (rightmost columns)

3. Honeycomb will show you example traces from that bucket

4. Click on the slowest trace to investigate

**Common causes of slow traces:**
- Cold start (OpenSearch first query)
- Large context size (more tokens → longer Bedrock processing)
- Network latency spikes
- Resource contention (CPU/memory limits)

::alert[**Heatmaps are Interactive**: Unlike static histograms, Honeycomb's heatmaps let you click on any bucket to see actual traces. This turns data exploration into an interactive investigation.]{type="success"}

### Query 5: Using BubbleUp to Find Outliers

**BubbleUp** is Honeycomb's signature feature that answers: "What's different about these slow requests compared to normal ones?" It automatically analyzes all dimensions and highlights statistically significant differences.

1. From your heatmap query above, click **BubbleUp** in the toolbar

2. Select the **slowest bucket** (P99+ traces) as your target

3. BubbleUp will compare these slow traces against all other traces

4. Look for attributes highlighted in **orange/red** - these have the biggest differences

**Example BubbleUp Results:**

```
Attribute                   Slow Traces    Normal Traces    Impact
-----------------------------------------------------------------------
gen_ai.usage.input_tokens   1200           650             🔴 High
db.vector.k                 15             5               🟠 Medium
http.route                  /api/chat      /api/chat       ⚪ None
deployment.environment      production     production      ⚪ None
```

**Insights from BubbleUp:**
- Slow requests have **2x more input tokens** (1200 vs 650)
- Slow requests fetch **3x more vectors** (15 vs 5)
- This explains the latency: larger context → longer LLM processing

**Why BubbleUp Matters:** Without BubbleUp, you'd manually create dozens of queries grouping by each field. BubbleUp does this automatically in seconds, even with millions of high-cardinality combinations.

::alert[**BubbleUp for Incidents**: During production incidents, BubbleUp is your first tool. It instantly shows you what's different about failing requests: specific users? Certain API versions? Particular code paths? Answer these in 30 seconds instead of 30 minutes.]{type="info"}

### Query 6: Using Query Assistant (Natural Language)

Honeycomb's **Query Assistant** uses AI to translate natural language questions into queries. This is perfect for teams new to Honeycomb or for quickly exploring data without remembering query syntax.

1. Click **Query Assistant** (or the sparkle ✨ icon) in the query builder

2. Try asking questions like:

   **Example 1**: "Show me the slowest Bedrock calls in the last hour"

   Query Assistant translates to:
   - VISUALIZE: `P99(duration_ms)`
   - WHERE: `name` = `gen_ai.bedrock.chat`
   - ORDER BY: `P99(duration_ms)` DESC
   - Time Range: Last 1 hour

   **Example 2**: "Which users are consuming the most tokens?"

   First, create a calculated field (see Step 6 for details):
   - **Name**: `gen_ai.usage.total_tokens`
   - **Expression**: `SUM($gen_ai.usage.input_tokens, $gen_ai.usage.output_tokens)`

   Then Query Assistant translates to:
   - VISUALIZE: `SUM(gen_ai.usage.total_tokens)`
   - GROUP BY: `user.id`
   - ORDER BY: `SUM(gen_ai.usage.total_tokens)` DESC
   - LIMIT: 20

   **Example 3**: "Show me all errors from the last 30 minutes"

   Query Assistant translates to:
   - VISUALIZE: `COUNT`
   - WHERE: `error` = `true` OR `otel.status_code` = `ERROR`
   - GROUP BY: `error.message`, `name`
   - Time Range: Last 30 minutes

3. Review the generated query and click **Run Query**

4. Refine the natural language prompt if needed, or edit the query directly

::alert[**Query Assistant Best Practice**: Use natural language to get started, then refine the query manually. This is great for learning Honeycomb's query language and discovering attributes you didn't know existed.]{type="success"}

### Query 7: HAVING Clause for Advanced Filtering

The **HAVING** clause filters on aggregated results, which is essential when working with high-cardinality data.

**Example: Find users with excessive token usage**

First, ensure you've created the `gen_ai.usage.total_tokens` calculated field (from Example 2 above).

Then create a query:
   - **VISUALIZE**: `SUM(gen_ai.usage.total_tokens)`, `COUNT`
   - **GROUP BY**: `user.id`
   - **HAVING**: `SUM(gen_ai.usage.total_tokens)` > 10000
   - **ORDER BY**: `SUM(gen_ai.usage.total_tokens)` DESC
   - **LIMIT**: 20

**Why HAVING is powerful:**
- **WHERE** filters raw events before aggregation: "Show requests where duration > 500ms"
- **HAVING** filters aggregated results: "Show users where total tokens > 10000"

**Use cases:**
- Find users with >100 requests/hour (potential abuse)
- Find endpoints with >5% error rate
- Find models with >$10 in API costs per hour