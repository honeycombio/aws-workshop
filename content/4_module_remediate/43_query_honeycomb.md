---
title: "Step 3: Query Honeycomb Data"
weight: 63
---

Now let's use Kiro CLI to query the observability data we collected in Module 3.

1. Ask Kiro CLI about recent application performance:
   ```
   Using the Honeycomb MCP server, show me the P95 latency for successful chat requests (status code 200) in the last hour for the otel-ai-chatbot-backend dataset
   ```

   Kiro CLI will:
   - Connect to Honeycomb MCP server
   - Construct appropriate Honeycomb query (filtering for HTTP 200 responses)
   - Execute query and return results
   - Format results in a readable way

   Expected output:
   ```
   ...
   > Perfect! Now I can see the actual HTTP spans for the /api/chat endpoint. I can see spans with http.target of /api/chat and duration_ms values. Let me query the P95 latency 
   for successful chat requests using the correct field:
   Running tool run_query with the param (from mcp server: honeycomb)
   ⋮  {
   ⋮    "dataset_slug": "otel-ai-chatbot-backend",
   ⋮    "environment_slug": "otel-ai-chatbot-backend",
   ⋮    "query_spec": "{\n  \"calculations\": [\n    {\n      \"op\": \"P95\",\n      \"column\": \"duration_ms\"\n    },\n    {\n      \"op\": \"COUNT\"\n    },\n    {\n      \"op\": \"AVG\",\n      \"column\": \"duration_ms\"\n    },\n    {\n      \"op\": \"P50\",\n      \"column\": \"duration_ms\"\n    }\n  ],\n  \"filters\": [\n    {\n      \"column\": \"meta.signal_type\",\n      \"op\": \"=\",\n      \"value\": \"trace\"\n    },\n    {\n      \"column\": \"http.target\",\n      \"op\": \"=\",\n      \"value\": \"/api/chat\"\n    },\n    {\n      \"column\": \"http.status_code\",\n      \"op\": \"=\",\n      \"value\": 200\n    }\n  ],\n  \"time_range\": 3600\n}"
   ⋮  }
   ⠋ Thinking... - Completed in 0.564s
   ...
   > Excellent! Here are the P95 latency results for successful chat requests (status code 200) in the last hour for the otel-ai-chatbot-backend dataset:

   ## Chat Request Latency Metrics (Last Hour)
   
   - **P95 Latency**: 28,736.69 ms (~28.7 seconds)
   - **P50 Latency**: 22,473.32 ms (~22.5 seconds)
   - **Average Latency**: 21,446.78 ms (~21.4 seconds)
   - **Request Count**: 17 successful requests
   
   ### Key Observations:
   
   1. High Latency: The chat requests are taking quite a long time (20+ seconds), which is typical for AI chatbot applications that involve:
      - Vector database searches (OpenSearch)
      - LLM API calls (Bedrock/Claude)
      - Context retrieval and processing
   
      2. Consistent Performance: The P50 and average are close, suggesting relatively consistent response times with some outliers pushing the P95 higher.
   
      3. Active Usage: 17 successful chat requests in the last hour shows the application is being actively used.
   
   The high latency is expected for this type of AI application that performs RAG (Retrieval-Augmented Generation) with multiple API calls to AWS Bedrock and OpenSearch vector
   database queries.
   ```

2. Ask for more specific analysis:
   ```
   Using the Honeycomb MCP, break down the latency by span name for successful requests. Which operation is the slowest?
   ```

   Expected output:
   ```
   > I'll break down the latency by span name to identify which operation is the slowest for successful chat requests.
   Running tool run_query with the param (from mcp server: honeycomb)
   ⋮  {
   ⋮    "dataset_slug": "otel-ai-chatbot-backend",
   ⋮    "environment_slug": "otel-ai-chatbot-backend",
   ⋮    "query_spec": "{\n  \"calculations\": [\n    {\n      \"op\": \"P95\",\n      \"column\": \"duration_ms\"\n    },\n    {\n      \"op\": \"COUNT\"\n    },\n    {\n      \"op\": \"AVG\",\n      \"column\": \"duration_ms\"\n    },\n    {\n      \"op\": \"P50\",\n      \"column\": \"duration_ms\"\n    }\n  ],\n  \"breakdowns\": [\"name\"],\n  \"filters\": [\n    {\n      \"column\": \"meta.signal_type\",\n      \"op\": \"=\",\n      \"value\": \"trace\"\n    },\n    {\n      \"column\": \"http.status_code\",\n      \"op\": \"=\",\n      \"value\": 200\n    }\n  ],\n  \"orders\": [\n    {\n      \"op\": \"P95\",\n      \"column\": \"duration_ms\",\n      \"order\": \"descending\"\n    }\n  ],\n  \"time_range\": 3600,\n  \"limit\": 15\n}"
   ⋮  }
   - Completed in 0.641s
   
   > Perfect! Here's the latency breakdown by span name for successful requests, ordered by P95 latency:
   
   ## Latency Breakdown by Operation (Slowest to Fastest)
   
   ### 1. Claude LLM Calls - SLOWEST 🐌
   - **Span**: chat anthropic.claude-3-5-sonnet-20240620-v1:0
   - **P95**: 28,592.62 ms (~28.6 seconds)
   - **P50**: 22,320.78 ms (~22.3 seconds)
   - **Average**: 21,279.58 ms (~21.3 seconds)
   - **Count**: 17 requests
   
   ### 2. HTTP POST Requests (Chat Endpoints)
   - **Span**: POST
   - **P95**: 26,586.46 ms (~26.6 seconds)
   - **P50**: 15,191.53 ms (~15.2 seconds)
   - **Average**: 10,736.46 ms (~10.7 seconds)
   - **Count**: 34 requests
   
   ### 3. HTTP GET Requests
   - **Span**: GET
   - **P95**: 204.84 ms (~0.2 seconds)
   - **P50**: 3.51 ms
   - **Average**: 18.87 ms
   - **Count**: 14 requests
   
   ### 4. Bedrock Embedding Calls
   - **Span**: BedrockRuntime.InvokeModel
   - **P95**: 179.22 ms (~0.18 seconds)
   - **P50**: 122.93 ms
   - **Average**: 128.11 ms
   - **Count**: 17 requests
   
   ### 5. HTTP HEAD Requests - FASTEST ⚡
   - **Span**: HEAD
   - **P95**: 130.23 ms
   - **P50**: 130.23 ms
   - **Average**: 66.39 ms
   - **Count**: 2 requests
   
   ## Key Findings:
   
   🔴 Bottleneck Identified: The Claude LLM API calls are by far the slowest operation, taking ~28.6 seconds at P95. This accounts for the majority of the total request latency.
   
   Performance Hierarchy:
   1. Claude LLM (~28.6s) - The primary bottleneck
      2. Bedrock Embeddings (~0.18s) - Fast and efficient
      3. HTTP operations (<0.2s) - Very fast
   
   The Claude LLM calls dominate the total request time, which is expected for AI chatbot applications where the language model generation is the most computationally intensive
   operation.
   ```

3. Check for errors:
   ```
   Query Honeycomb for any errors in the last hour.
   ```

   Expected output:
   ```
   - Completed in 0.138s

   > ## ✅ No Errors Found in the Last Hour

   Based on my analysis of the Honeycomb data for the otel-ai-chatbot-backend dataset, there are no errors in the last hour:
   
   ### Error Analysis Results:
   
   1. No Error Flags: No events with error = true
   2. No HTTP Errors: No 4xx or 5xx status codes
   3. No Exceptions: No exception messages or stack traces
   4. No Error Logs: No error or warning severity levels

   ### What I Found Instead:
   
   Healthy Status Indicators:
   - **430 info logs** - Normal informational logging
   - **356 debug logs** - Debug-level logging (healthy)
   - **81 HTTP 200 responses** - Successful requests
   - **1 HTTP 304 response** - Not Modified (normal caching behavior)
   
   ### Summary:
   The application appears to be running smoothly with no errors in the past hour. All HTTP requests are returning successful status codes (200/304), and the logging shows only
   normal info and debug level messages with no error or warning entries.

   This indicates the otel-ai-chatbot-backend is operating in a healthy state! 🎉
   ```

::alert[**Natural Language Queries**: Notice you don't need to learn Honeycomb's query syntax. Kiro CLI translates your natural language request into proper Honeycomb queries using the MCP server.]{type="success"}
