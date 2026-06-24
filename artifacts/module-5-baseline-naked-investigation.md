# Module 5 — Baseline "Naked" Investigation

**Captured:** 2026-06-24
**Setup:** AWS DevOps Agent in `us-west-2`, Agent Space connected to dev account `272469967381`. Cluster `otel-demo` deployed 2026-06-22, m5.xlarge single node. otel-demo Helm chart installed. Honeycomb MCP **not yet connected**. No additional gap-closing changes (no Container Insights, no kubectl access entry for the agent's IAM role).

**Prompt:** "Investigate latency on frontend-proxy."

**Time to completion:** ~7–8 minutes (full multi-subagent investigation).

**Purpose:** "Before" reference for Module 5's compare/contrast against the MCP-augmented investigation. Used to show attendees what an AWS-native agent can and cannot see at the application layer.

---

## Full investigation summary (verbatim agent output)

# Investigation summary
## Impact
### Latency on frontend-proxy service in otel-demo EKS cluster
The frontend-proxy service in the otel-demo EKS cluster (account 272469967381, us-west-2) is experiencing latency issues. The cluster was deployed on June 22, 2026. The cluster runs on a single m5.xlarge node (i-0657518b481b0a4ef). The exact onset time and magnitude of the latency is not yet quantified.
*Started: 2026-06-22T20:00:00Z*

## Hypotheses

### Memory pressure on single m5.xlarge node running entire otel-demo stack
The otel-demo application typically deploys 10+ microservices (frontend, frontend-proxy, cart, checkout, currency, email, payment, product-catalog, recommendation, shipping, ad, fraud-detection, etc.) plus supporting infrastructure (OpenTelemetry Collector, Jaeger, Kafka, Redis, PostgreSQL). Running all of these on a single m5.xlarge (16 GiB RAM) could easily lead to memory pressure, causing pods to be OOM-killed, throttled, or experience garbage collection pauses. Memory utilization cannot be verified because Container Insights is not enabled and kubectl access is not available. This is the most likely cause given: (1) CPU is only at 31% (suggesting the workload is not CPU-bound but could be memory-bound), (2) EBS queue length is trending upward (could indicate swap activity), (3) the entire demo stack on 16 GiB is a known resource concern.

### Downstream service latency causing frontend-proxy slowness
The frontend-proxy (Envoy) forwards requests to multiple backend services. If any downstream service (e.g., frontend, product-catalog, checkout, recommendation) is slow due to resource constraints, unhealthy pods, or application bugs, the frontend-proxy will reflect that latency to clients. Without distributed traces (X-Ray not configured, Jaeger is in-cluster only) or application logs, we cannot determine which downstream service may be contributing to latency. The very low request count at the ELB (~2 per 5 minutes) suggests either minimal traffic or that requests are taking so long that throughput is severely impacted.

### CPU throttling at pod level due to Kubernetes resource limits
Even though the node shows only 31% CPU utilization overall, individual pods may have restrictive CPU limits configured. Kubernetes enforces CPU limits via CFS (Completely Fair Scheduler) throttling, which can cause significant latency spikes even when the node has available CPU. The frontend-proxy pod or its downstream services could be hitting their CPU limits and being throttled. This is invisible at the EC2 instance level and requires kubectl access or Container Insights to verify (container_cpu_cfs_throttled_periods metric).

## Investigation gaps

- **No Kubernetes API Access — Cannot Inspect Pod State, Logs, or Resource Usage:** kubectl commands to the otel-demo EKS cluster fail with authentication errors ('the server has asked for the client to provide credentials'). The agent's IAM role is not configured as an access entry on the cluster.

- **Container Insights Not Enabled — No Pod-Level Memory or CPU Metrics:** The CloudWatch Agent is not installed on the node (i-0657518b481b0a4ef). No metrics for `node_memory_utilization`, `pod_memory_utilization`, `pod_cpu_utilization`, `container_cpu_cfs_throttled_periods`, etc.

- **No Distributed Traces Available — Cannot Identify Latency Breakdown Across Services:** AWS X-Ray has zero traces for any service in the otel-demo cluster. The ADOT addon is not installed; the OpenTelemetry Collector is likely configured to export traces only to an in-cluster Jaeger instance.

- **No Application Logs in CloudWatch — Cannot Analyze Error Patterns or Response Times:** No CloudWatch log groups exist for the otel-demo application. EKS cluster logging (API server, audit, authenticator, controller manager, scheduler) is fully disabled.

---

## Workshop notes

**The agent's hypotheses are reasonable but wrong.** The actual latency driver is the mock LLM service serving `/api/product-ask-ai-assistant/` — confirmed via Honeycomb BubbleUp before MCP was connected. The agent reaches for infra explanations (memory, CPU, CFS) because it has no visibility into the application layer.

**Three visibility gaps, only one to close in Module 5.** Keep the kubectl + Container Insights gaps in place. Closing only the trace gap with Honeycomb MCP gives the cleanest "before/after" narrative. The other gaps remain as realistic friction attendees can identify with.

**Time-window quirk to handle in Module 5.** The agent treated cluster deployment time (2026-06-22T20:00:00Z) as incident start. For the race, scope investigation windows tightly (e.g., last 30 minutes) so the agent doesn't drown in stale data.

**Best ROI improvement on rerun:** "the latency is concentrated at `/api/product-ask-ai-assistant/` and originates in calls to the in-cluster `llm` service." If Honeycomb MCP yields that conclusion in a comparable time budget, Module 5's payoff lands.
