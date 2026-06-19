---
title: "Step 7: Request Code Generation and PR"
weight: 67
---

Let's ask Neo to implement the highest-impact solution: **Enable Streaming Responses**.

1. Ask Pulumi Neo to generate code patches and create a PR:
   ```
   Using the git repository github.com/dirien/ai-workshop and the Pulumi MCP server to create now a PR for this solution. Auto approve the plan Neo creates and approve the preview run too.
   ```

   ::alert[Head over to the Pulumi Cloud Console to see the detailed PR creation process Neo is undertaking for the `dirien/ai-workshop` repository.]{type="info"}
   **Note**: Neo will analyze the git repository, generate code patches, and create a Pull Request automatically. You'll be asked to approve the changes before Neo creates the PR.

   Neo's actual response:
   ~~~
   Running tool neo-continue-task with the param (from mcp server: pulumi)
   ⋮  {
   ⋮    "taskId": "e561125c-17b4-4679-88b4-a9e075fdacd6"
   ⋮  }
   - Completed in 0.457s
   
   > Perfect! Pulumi Neo has successfully implemented the Priority 1 performance improvements and is now ready to create the PR. The task shows:
   
   ## **Status Update:**
   - ✅ Infrastructure changes implemented in pulumi/index.ts
   - ✅ TypeScript validation passed
   - ✅ Stack configuration set up for ws-2
   - ⏳ Ready for Pulumi preview (waiting for approval)
   
   ## **Changes Implemented:**
   1. ECS task resources: Increased to 2048 CPU / 4096 MB memory
   2. VPC endpoints: Added for Bedrock, Secrets Manager, CloudWatch Logs
   3. ALB timeout fixes: Configured for long LLM responses
   4. Auto-scaling: Enabled with 2-4 tasks
   5. Node.js optimization: Memory tuning added
   
   The task is now at the final stage - Neo is asking for approval to run pulumi preview to validate the changes before creating the pull request.
   
   Expected Impact: P95 latency reduction from 28.7s to 15-18s (40-50% improvement)
   
   Neo has successfully prepared all the infrastructure improvements and is ready to complete the PR creation process. The task is currently idle and waiting for the final
   approval to proceed with the Pulumi preview and PR creation.
   ~~~

::alert[**Iterative Collaboration**: Don't expect a perfect result on the first try! Working with agentic AI like Kiro is often an iterative process. You may need to answer clarifying questions, provide additional context, or give feedback to refine the solution. This back-and-forth conversation is a feature, not a bug. It helps ensure the AI understands your specific requirements and constraints. Additionally, it is worth checking the Neo task in Pulumi Cloud in case you need to approve any pending actions there.]{type="info"}

::alert[**The Complete Agentic Loop**: Neo just demonstrated end-to-end automation - from observability data to PR creation. It analyzed Honeycomb metrics (Step 4), diagnosed the issue (Step 5), provided recommendations (Step 6), generated code patches, and created a production-ready PR (Step 7). This is AI-powered infrastructure management in action with human-in-the-loop oversight.]{type="success"}

## Review the Pull Request

1. Visit the Pull Request URL provided by Neo:
   ```
   https://github.com/dirien/ai-workshop/pull/XXX
   ```

2. Review the comprehensive PR that Neo created.

::alert[**Human-in-the-Loop**: Notice how Neo created a complete PR with all files, documentation, and clear explanations - but it's waiting for YOUR approval. You maintain full control over what gets deployed to production.]{type="success"}
