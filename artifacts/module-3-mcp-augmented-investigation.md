# Module 3 — MCP-Augmented Investigation

**Captured:** 2026-06-24
**Setup:** Identical to the baseline (see `module-3-baseline-investigation.md`) — same dev account, same cluster, same prompt, same time window. **Only change:** Honeycomb MCP server registered in the Agent Space.

**Prompt:** Same as baseline — "Investigate latency on frontend-proxy."

**Purpose:** "After" reference for Module 5. The before/after contrast is the workshop's payoff moment.

---

## Full investigation summary (verbatim agent output)

# Investigation summary
## Impact
### Frontend-proxy latency: extreme outliers from flagd EventStream + moderate tail latency from LLM-backed endpoints
The frontend-proxy service shows two distinct latency patterns: (1) EXTREME outlier latency of 900,322ms (15 min) from flagd EventStream gRPC streaming connections — these are by-design long-lived connections, not user requests; (2) REAL user-facing tail latency: GET P50=3.9ms/P95=22ms/P99=42ms (healthy), POST P50=7.1ms/P95=60ms/P99=146ms (moderate), with slowest endpoint /api/product-ask-ai-assistant at P50=45ms/P95=178ms/P99=214ms due to LLM calls. Zero HTTP 5xx errors observed.
*Started: 2026-06-22T20:34:30Z*

## Root causes

### Extreme outlier latency (900K ms) caused by long-lived flagd EventStream gRPC streaming connections
The MAX latency of 900,322ms (15 minutes) observed on the frontend-proxy is from flagd.evaluation.v1.Service/EventStream — long-lived gRPC streaming connections used for real-time feature flag update notifications. These are architectural by-design patterns, not actual request latency. Evidence: (1) All 70 EventStream spans in 2 hours have P50=600,001ms (exactly 10-minute server timeout), (2) 22/70 spans show error=true with status_message='stream closed due to server-side timeout' and gRPC status code 4 (DEADLINE_EXCEEDED), (3) The 4 slow POST spans through frontend-proxy to flagservice have response_flags=DC (downstream connection termination — client disconnected), (4) 4/9 flagservice egress spans have canceled=true. These streaming connections are expected behavior for feature flag services using server-sent events/gRPC streaming.

### Tail latency (P95=178ms, P99=214ms) driven by high-variance LLM calls in product-ask-ai-assistant endpoint
The highest user-facing latency on the frontend-proxy comes from the /api/product-ask-ai-assistant endpoint, which makes 2 sequential 'chat astronomy-llm' LLM calls per request. The LLM call itself has high latency variance: P50=6.4ms, P95=56.7ms, P99=86.5ms, MAX=115.6ms. Since 2 calls are made per request, the variance compounds: get_ai_assistant_response P50=41.9ms, P95=170.2ms, P99=205.6ms. This is inherent to the LLM inference workload, not an infrastructure issue. The heatmap shows a bimodal distribution with most LLM calls completing in 5-13ms but a significant tail extending to 100+ms. No errors are observed (0% error rate across all upstream clusters). Other endpoints show normal latency: /api/checkout P99=83ms, /api/recommendations P99=51ms, /api/product-reviews P99=47ms.

---

## Workshop notes — what to highlight in the before/after

### Specificity
| Naked | MCP-augmented |
|---|---|
| "Memory pressure most likely" | `GET P99=42ms`, `/api/product-ask-ai-assistant P99=214ms` |
| Three hypotheses, all infra | Two named root causes with span counts and percentile data |
| ~7–8 min, ends in "cannot determine" | Comparable time, ends in actionable findings |

### Noise filtering (the standout finding)
The 900K ms flagd EventStream diagnosis is the most impressive bit and worth dwelling on in the workshop. The agent recognized that 15-min "latency" matching the 10-min server timeout, paired with `DEADLINE_EXCEEDED` and `response_flags=DC`, is an architectural streaming pattern — not a request. This is reasoning the naked agent literally could not do because it had no span-level context.

### Causal chain insight
"2 sequential LLM calls per request → compounding variance" (P99=86.5ms × 2 sequential → P99=214ms endpoint). A lot of human investigators miss compounding effects like this. Teachable moment for the workshop.

### Zero visibility gaps
Naked had four explicit gap blocks (kubectl, Container Insights, X-Ray, CloudWatch logs). MCP-augmented has none — the trace data closes the application-layer gap completely, even though the kubectl/Container Insights gaps remain unaddressed.

### Implication for Module 5 race mechanics
The MCP-augmented agent is *very* sharp. For human attendees to feel competitive, framing should probably be **"different paths to the same place"** rather than "race to root cause first." Suggested human path: use Honeycomb's UI (BubbleUp, traces, Canvas) to find the same `/api/product-ask-ai-assistant/` story the agent finds — then go *deeper* than the agent (which traces, which prompts, which user sessions). The agent provides breadth; humans add depth.

### Recommended layered chaos for the race
The organic latency story is already compelling enough that we might not need a flagd toggle. But layering `llmRateLimitError` adds errors *on the same endpoint* the agent already identified as slow — clean narrative continuity. The agent should pivot from "LLM is slow" to "LLM is slow AND failing", and the failing-LLM story is what attendees can find via BubbleUp on `error=true`.
