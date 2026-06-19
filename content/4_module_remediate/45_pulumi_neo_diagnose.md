---
title: "Step 5: Use Pulumi Neo to Diagnose the Issue"
weight: 65
---

Now let's use **Pulumi Neo** (via Kiro CLI) to analyze the infrastructure and application based on our Honeycomb findings.

1. Provide Honeycomb findings to Pulumi Neo:
   ```
   Using the Pulumi MCP server, ask Pulumi Neo to analyze stack "otel-ai-chatbot-infra/ws" with these Honeycomb findings.
   ```

   Kiro CLI will:
   - Connect to Pulumi MCP server
   - Invoke Pulumi Neo for stack analysis
   - Neo inspects infrastructure state (ECS, Bedrock config)
   - Neo analyzes application code structure
   - Neo correlates infrastructure with observed latency patterns
   - Neo provides root cause analysis

   Expected response (Neo's comprehensive analysis):

   ::alert[Head over to the Pulumi Cloud Console to see the detailed analysis Neo has generated for the `otel-ai-chatbot-infra/ws` stack.]{type="info"}
   ~~~
   ⠋ Thinking...
   Running tool neo-bridge with the param (from mcp server: pulumi)
   ⋮  {
   ⋮    "taskId": "03eb1822-dbae-447e-85e8-2560af65bad2"
   ⋮  }
   ⠋ Thinking... - Completed in 2.341s
   
   > Pulumi Neo has completed its analysis of the otel-ai-chatbot-infra/ws-2 stack based on your Honeycomb findings. Here's the comprehensive analysis:
   
   ## Key Infrastructure Bottlenecks Identified:
   
   ### **Critical Issues:**
   1. Severely undersized ECS tasks - Only 512 CPU/1024 MB for LLM workloads
   2. No auto-scaling - Single task handling all traffic
   3. Target group timeout too short - 5s timeout vs 20+ second LLM responses
   4. Network bottleneck - Single NAT gateway, no VPC endpoints for Bedrock
   5. OpenSearch not HA - Single AZ deployment
   
   ### **Root Cause:**
   While the 28.7s P95 latency is primarily due to LLM inference time (19-24s), infrastructure constraints are compounding the problem by causing resource contention and network
   delays.
   
   ## **Priority 1 Fixes (Immediate Impact):**
   
   1. Increase ECS resources: 512→2048 CPU, 1024→4096 MB memory
   2. Add VPC endpoint for Bedrock - Eliminates NAT gateway latency
   3. Fix ALB timeouts - Increase to 120s for long LLM responses
   4. Enable auto-scaling - 2-10 tasks with CPU/request-based scaling
   
   ## **Expected Results:**
   - **Latency reduction**: From 28.7s to ~20-22s (removing infrastructure overhead)
   - **Better resilience**: Handle traffic spikes without degradation
   - **Cost optimization**: VPC endpoint saves NAT costs while improving performance
   
   The analysis shows that while LLM inference is the primary bottleneck, infrastructure optimizations can reduce overall latency by 20-30% and significantly improve system
   reliability during peak periods.
   
   Would you like me to help implement any of these infrastructure optimizations?
   ~~~

::alert[**Neo's Power**: Notice how Neo analyzed the entire stack - infrastructure state, application code structure, and correlated with Honeycomb metrics - to provide a comprehensive diagnosis. It correctly identified this as an application-level issue, not infrastructure.]{type="success"}
