---
title: "Module Summary"
weight: 510
---

Congratulations! You've successfully:

✅ Generated realistic load on the application

✅ Explored traces in Honeycomb's interface

✅ Used Honeycomb queries to analyze latency patterns

✅ Identified performance bottlenecks (Bedrock calls, OpenSearch queries)

✅ Discovered infrastructure constraints (undersized ECS tasks)

✅ Created a monitoring board for ongoing visibility

✅ Set up alerting for latency degradation

✅ Formulated a hypothesis for remediation

## What's Next?

In **Module 4**, you'll use **Amazon Kiro CLI with MCP servers** to:
1. Query Honeycomb data directly from your IDE
2. Ask an AI agent to diagnose the performance issue
3. Use **Pulumi Neo** to generate infrastructure code changes
4. Review and apply the fix (human-in-the-loop)
5. Verify the improvement

---

## Key Takeaways

### 1. High-Cardinality Data is Your Superpower

Traditional monitoring tools force you to pre-aggregate metrics, losing the ability to ask detailed questions. Honeycomb stores raw trace data with all high-cardinality attributes intact, letting you ask questions like:
- "Show me traces where Bedrock calls exceeded 500ms AND vector search returned <5 results **AND** user_id = 'user_12345'"
- "Which specific model versions have the highest error rate?"
- "Compare performance before/after deploy for users in region 'us-west-2'"

**The Honeycomb Promise**: You can ask questions you didn't know you needed to ask, without pre-defining dashboards or metrics.

### 2. BubbleUp Accelerates Root Cause Analysis

During incidents, BubbleUp automatically identifies what's different about problematic requests by comparing distributions across all dimensions. This turns hours of manual investigation into 30 seconds of automated analysis. It's particularly powerful with high-cardinality data (millions of users, thousands of model versions).

### 3. Observability ≠ Monitoring

**Monitoring**: "Is the system up? Are metrics within thresholds?" (known-knowns)

**Observability**: "Why is this specific request slow? What's different about it?" (unknown-unknowns)

Honeycomb enables **observability-driven development** where you explore first, then create dashboards for known issues.

### 4. Ask "WHY" Questions, Not Just "WHAT" Questions

Traditional tools answer WHAT: "P99 latency is 750ms"

Honeycomb answers WHY: "P99 latency is 750ms **because** requests from premium users fetch 3x more vector results and use larger context windows"

Use BubbleUp, high-cardinality GROUP BY, and HAVING clauses to answer WHY questions.

### 5. Query Assistant Lowers the Learning Curve

Natural language querying with Query Assistant means teams can start asking questions on day one, without mastering query syntax. It's also excellent for discovering attributes you didn't know existed in your data.

### 6. The Three Pillars, Unified

While we focused on **traces** in this module, remember:
- **Traces**: Request flow and latency breakdown (what we used)
- **Metrics**: Aggregated numerical data (CPU, memory from CloudWatch)
- **Logs**: Discrete events (errors, debug info correlated via trace IDs)

OpenTelemetry captures all three, and Honeycomb correlates them automatically through trace context propagation.

### 7. Heatmaps + HAVING + LIMIT = High-Cardinality Mastery

When working with millions of unique values:
- **Heatmaps**: Visualize distributions and identify outliers interactively
- **HAVING**: Filter on aggregated values (e.g., users with >10K tokens)
- **LIMIT**: Show top N results to avoid overwhelming tables
- **ORDER BY**: Sort by the metric that matters (P95, SUM, etc.)

---

## Additional Resources

- [Honeycomb Query Documentation](https://docs.honeycomb.io/working-with-your-data/queries/)
- [Honeycomb Best Practices](https://docs.honeycomb.io/working-with-your-data/best-practices/)
- [OpenTelemetry Trace Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/general/trace/)
- [Charity Majors on Observability](https://www.honeycomb.io/blog/observability-a-manifesto)
