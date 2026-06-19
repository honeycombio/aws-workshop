---
title: "Step 6: Ask Pulumi Neo for Detailed Solution Recommendations"
weight: 66
---

Neo has diagnosed the root cause (application-level LLM latency). Now let's ask for detailed, prioritized recommendations.

1. Request solution recommendations from Pulumi Neo:
   ```
   Based on your diagnosis, ask Pulumi Neo to provide detailed recommendations for Immediate Impact improvements.
   ```

   ::alert[Head over to the Pulumi Cloud Console to see the detailed recommendations Neo has generated for the `otel-ai-chatbot-infra/ws` stack.]{type="info"}
   Expected response (Neo's detailed recommendations):
   ~~~
   ## **Priority 1 Immediate Impact Improvements:**
   
   ### **1. Increase ECS Task Resources**
   - **Change**: 512→2048 CPU, 1024→4096 MB memory
   - **Impact**: 30-40% latency reduction by eliminating CPU throttling
   - **Cost**: +$0.08/hour per task (~$60/month)
   
   ### **2. Add VPC Endpoint for Bedrock**
   - **Change**: Direct VPC connectivity, bypass NAT gateway
   - **Impact**: 50-150ms reduction per Bedrock call
   - **Cost**: +$0.02/hour, saves NAT gateway data costs
   
   ### **3. Fix ALB/Target Group Timeouts**
   - **Change**: ALB idle timeout 60s→120s, optimized health checks
   - **Impact**: Eliminates 502/504 errors for long LLM responses
   - **Cost**: $0
   
   ### **4. Enable Auto-Scaling**
   - **Change**: Min 2 tasks, scale 2-4 based on CPU/memory/requests
   - **Impact**: 20-30% latency reduction through load distribution
   - **Cost**: +$0.08-0.24/hour variable
   
   ## **Expected Results:**
   - **P95 Latency**: 28.7s → 15-18s (40-50% reduction)
   - **Total Cost**: ~$0.12/hr → ~$0.30/hr (+$220/month)
   - **Reliability**: Eliminates timeout errors, adds redundancy
   
   ## **Implementation Steps:**
   1. Apply code changes to index.ts
   2. Run pulumi preview --stack ws-2
   3. Deploy with pulumi up --stack ws-2
   4. Validate with provided monitoring commands
   
   The analysis includes specific Pulumi TypeScript code for all changes, validation steps, and post-deployment monitoring queries for Honeycomb.
   
   Would you like me to help implement any of these specific changes to your infrastructure code?
   ~~~

2. Review Neo's recommendations:
   - ✓ Prioritized by impact (Streaming first = 85% perceived improvement)
   - ✓ Actionable and specific (Exact files and line numbers provided)
   - ✓ Explains trade-offs (Quality vs speed, code vs infrastructure)
   - ✓ Addresses both quick wins (streaming) and long-term improvements
   - ✓ Provides cost implications for each solution
   - ✓ Includes implementation timeline and strategy

::alert[**The Agentic Workflow**: Notice the flow: Honeycomb data → Neo diagnosis (Step 5) → Neo recommendations (Step 6) → Neo code generation (Step 7). This is a complete AI-driven operations loop where the AI agent reasons across observability, infrastructure, and application code to solve problems autonomously with human oversight.]{type="success"}
