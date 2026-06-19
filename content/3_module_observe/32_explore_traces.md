---
title: "Step 2: Explore Traces in Honeycomb"
weight: 502
---

1. Open Honeycomb: https://ui.honeycomb.io

2. Select your dataset: `otel-ai-chatbot`

3. You should see a stream of traces in the **Recent Traces** view

4. Click on any trace to see its details:
   - Trace timeline showing all spans
   - Waterfall view of span hierarchy
   - Span attributes and metadata
   - Duration breakdown by span

5. Examine a typical trace structure:
   ```
   chat.request (350ms)
   ├─ POST /api/chat (345ms)
   │  ├─ db.vector.search (120ms)
   │  │  └─ HTTPS POST OpenSearch (115ms)
   │  ├─ gen_ai.bedrock.chat (210ms)
   │  │  └─ AWS Bedrock InvokeModel (205ms)
   │  └─ Response serialization (5ms)
   ```

**Key observations:**
- Most time is spent in Bedrock API calls (~60% of request time)
- OpenSearch vector search is the second slowest operation (~35%)
- Application logic overhead is minimal (~5%)