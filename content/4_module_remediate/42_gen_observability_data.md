---
title: "Step 2: Generate Fresh Observability Data"
weight: 62
---

Before we can use Kiro CLI to query Honeycomb, we need to generate some recent telemetry data by using the AI Chatbot application.

**Why generate fresh data?**
- Kiro CLI will query data from the "last hour" in the next steps
- Fresh data ensures we have meaningful metrics to analyze
- Multiple requests will generate varied latency patterns for analysis

**Instructions:**

1. **Access the AI Chatbot application:**
   - Get the Application Load Balancer URL from your Pulumi stack outputs:
     ```bash
     pulumi stack output albUrl
     ```
   - Open the URL in your web browser

2. **Generate 5-10 chat requests** by asking varied questions about OpenTelemetry:

   **Example questions to ask:**
   - "How do I configure OpenTelemetry to export traces to Honeycomb?"
   - "What are the steps to instrument a Node.js application with OpenTelemetry?"
   - "How can I create custom spans in my Node.js application?"
   - "What is the difference between manual and automatic instrumentation in OpenTelemetry?"
   - "How can I instrument React web applications with OpenTelemetry?"
   - "Tell me about Honeycomb and Pulumi"

3. **What's happening behind the scenes:**
   - Each chat request triggers multiple spans:
     - HTTP request spans (GET, POST)
     - Vector search operations (OpenSearch)
     - LLM inference calls (AWS Bedrock)
     - Embedding generation
   - OpenTelemetry automatically exports these traces to Honeycomb
   - Traces include latency, status codes, and custom attributes

4. **Wait 1-2 minutes** for traces to propagate to Honeycomb before proceeding to the next step.

::alert[**Pro Tip**: Vary your questions to generate different response patterns. This will give you more interesting data to analyze when querying with Kiro CLI in the next steps!]{type="info"}
