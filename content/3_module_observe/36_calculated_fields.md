---
title: "Step 6: Advanced Technique - Calculated Fields"
weight: 506
---

**Calculated fields** let you create new fields from existing data using mathematical operations or string manipulation. This is powerful for calculating metrics not captured during instrumentation.

### Essential Calculated Fields for GenAI

In Honeycomb, go to **Dataset Settings** → **Calculated Fields** and create these:

**1. Total Tokens** (required for v1.0 conventions)

   - **Name**: `gen_ai.usage.total_tokens`
   - **Expression**: `SUM($gen_ai.usage.input_tokens, $gen_ai.usage.output_tokens)`
   - **Description**: "Total tokens (input + output) per request"

   **Why needed**: OpenTelemetry GenAI v1.0 only defines `input_tokens` and `output_tokens`. This calculated field lets you query total usage in a single metric.

**2. Cost Per Request**

   - **Name**: `cost_per_request_usd`
   - **Expression**:
     ```
     SUM(
       MUL($gen_ai.usage.input_tokens, 0.000003),
       MUL($gen_ai.usage.output_tokens, 0.000015)
     )
     ```
   - **Description**: "Estimated cost in USD based on Claude 3.5 Sonnet pricing"

**3. Token Throughput**

   - **Name**: `tokens_per_second`
   - **Expression**: `DIV($gen_ai.usage.total_tokens, DIV($duration_ms, 1000))`
   - **Description**: "Tokens processed per second (throughput metric)"

**4. Slow Request Indicator**

   - **Name**: `is_slow_request`
   - **Expression**: `GT($duration_ms, 500)`
   - **Description**: "Boolean flag for requests exceeding 500ms"

Now you can query using these calculated fields:
   - **VISUALIZE**: `SUM(cost_per_request_usd)`
   - **GROUP BY**: `user.id`
   - **ORDER BY**: `SUM(cost_per_request_usd)` DESC
   - **Time Range**: Last 24 hours

::alert[**Calculated Fields Best Practice**: Use calculated fields for calculations you'll query repeatedly. They're computed at query time, so there's no storage overhead, but they save you from repeating complex expressions in every query.]{type="success"}