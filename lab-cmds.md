# Honeycomb + AWS Workshop — Validation Guide

A shared technical reference for the Honeycomb + AWS workshop currently in build. Captures the validated technical path, observed gotchas, and open design questions. Intended audience: Honeycomb and AWS engineering partners co-authoring the workshop.

## Overview

The workshop teaches SREs how to investigate production issues across AWS infrastructure and Honeycomb observability data, using both manual exploration and AI-augmented agents. Attendees deploy a real microservices application on EKS, instrument it for Honeycomb, layer in AI-driven investigation (AWS DevOps Agent + Honeycomb MCP), then build and instrument their own AI agent with OpenTelemetry and explore it live in Honeycomb's Agent Timeline.

## Workshop arc

| # | Module | Outcome | Status |
|---|---|---|---|
| 1 | Deploy otel-demo + configure collector for Honeycomb | Working microservices app sending traces to Honeycomb | ✅ Validated |
| 2 | Investigate in Honeycomb with organic data | BubbleUp / trace / Canvas walkthrough on real latency story | ✅ Validated |
| 3 | Provision AWS DevOps Agent + connect Honeycomb MCP | AI-augmented investigation across AWS infra + Honeycomb traces | ✅ Validated |
| 4 | Build + instrument a Strands agent, explore it in Agent Timeline | Fully-populated Agent Timeline from ~60 lines of attendee-readable code | ✅ Validated 2026-07-16 |

> Workshop is a 4-module arc as of 2026-07-16. A humans-vs-DevOps-Agent race module (flagd chaos toggle) is **parked** as a potential bonus, pending timing with a live audience — design notes preserved in the open items and Appendix A.

## Current validation context

- **Region**: dev validation in `us-west-2`. Workshop-final region (`us-east-1` vs `us-west-2`) still open.
- **Provisioning**: dev uses `eksctl` for speed; workshop-final will be CloudFormation invoked by Workshop Studio at account-vending time. Attendees will only run `aws eks update-kubeconfig`.
- **Honeycomb account**: free-tier signup per attendee. Honeycomb Intelligence (required for MCP) is available on free-tier.

---

## Module 1 — Deploy otel-demo + Honeycomb collector

### Purpose

Stand up the OpenTelemetry Demo ("telescope shop") on EKS, then configure its bundled OpenTelemetry Collector to export traces to a Honeycomb free-tier environment. By the end, attendees have a real microservices app emitting real GenAI-instrumented telemetry to Honeycomb.

### Prereqs in CloudShell

CloudShell ships with `aws` CLI and `kubectl`. Install `eksctl` and `helm` if missing:

```bash
# eksctl
curl --silent --location "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version

# helm (skip if already installed)
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

> **Workshop Studio translation**: this install step disappears for attendees. CFN provisions the cluster directly; attendees only need `aws` and `kubectl`, both already in CloudShell.

### Provision the EKS cluster

Demo chart requires K8s 1.24+ and ~6 GB free RAM. One `m5.xlarge` (16 GB) node is sufficient. Provisioning takes ~15 min.

```bash
eksctl create cluster \
  --name otel-demo \
  --region us-west-2 \
  --nodes 1 \
  --node-type m5.xlarge \
  --managed
```

eksctl writes kubeconfig automatically. Verify:

```bash
kubectl get nodes
```

> **CFN bridge**: `eksctl create cluster ... --dry-run > cluster.yaml` produces an eksctl config that maps closely to the CFN it would have applied — useful as a scaffold for the Workshop Studio template.

### Install the OTel Demo via Helm

```bash
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm repo update
helm install my-otel-demo open-telemetry/opentelemetry-demo
kubectl get pods -w   # Ctrl-C once all pods are Running
```

The bundled load generator (locustfile) starts producing realistic traffic immediately. No extra step needed for trace volume.

### Access the application

CloudShell does **not** support port preview. Use a LoadBalancer (also realistic for the workshop attendee experience):

```bash
kubectl patch svc frontend-proxy -p '{"spec":{"type":"LoadBalancer"}}'
kubectl get svc frontend-proxy -w   # wait for EXTERNAL-IP
```

ELB cost: ~$0.025/hr. Delete the service or the cluster after validation.

### Configure the collector to export to Honeycomb

#### Inspect the running collector first

Names drift across chart versions — never hardcode.

```bash
kubectl get configmap | grep -i otel                       # find configmap name
kubectl get deploy,ds,sts -A | grep -i otel                # find workload (Deployment vs DaemonSet)
kubectl get configmap <name> -o jsonpath='{.metadata.labels}' | tr ',' '\n'
kubectl get configmap <name> -o yaml | grep -A 60 "pipelines:"
```

**Observed in current chart**: configmap `otel-collector-agent`, workload `daemonset.apps/otel-collector-agent`, subchart key `opentelemetry-collector`. Pipeline exporters:
- traces: `otlp/jaeger`, `debug`, `spanmetrics`
- metrics: `otlphttp/prometheus`, `debug`
- logs: `opensearch`, `debug`

#### Create the Honeycomb credentials secret

In Honeycomb: sign up free-tier, go to **Environment Settings → API Keys**, create an ingest key. Then:

```bash
export HONEYCOMB_API_KEY="<your-ingest-key>"
kubectl create secret generic honeycomb-credentials \
  --from-literal=HONEYCOMB_API_KEY="$HONEYCOMB_API_KEY"
```

#### Apply the values override

Save as `~/honeycomb-values.yaml`. Honeycomb is added as an **additional** exporter so existing Jaeger/Grafana/OpenSearch pipelines keep working.

```yaml
opentelemetry-collector:
  extraEnvsFrom:
    - secretRef:
        name: honeycomb-credentials
  config:
    exporters:
      otlp/honeycomb:
        endpoint: "api.honeycomb.io:443"
        headers:
          "x-honeycomb-team": "${env:HONEYCOMB_API_KEY}"
    service:
      pipelines:
        traces:
          exporters: [otlp/jaeger, debug, spanmetrics, otlp/honeycomb]
        metrics:
          exporters: [otlphttp/prometheus, debug, otlp/honeycomb]
        logs:
          exporters: [opensearch, debug, otlp/honeycomb]
```

> Use `api.eu1.honeycomb.io:443` for EU.
> Per-pipeline exporter lists are **replaced** by the merge, not appended — always include the existing exporters alongside `otlp/honeycomb`.

#### Roll out and verify

```bash
helm upgrade my-otel-demo open-telemetry/opentelemetry-demo --values ~/honeycomb-values.yaml
kubectl rollout status daemonset/otel-collector-agent
kubectl logs -l app.kubernetes.io/name=opentelemetry-collector -f --tail=50
```

Look for absence of `401`, `permission denied`, or `connection refused`. New datasets appear in Honeycomb under **Datasets** within ~30 seconds, one per service.

### Observed gotcha — CloudShell paste mangling

Multi-line pastes into CloudShell can mangle whitespace and quotes — hit repeatedly during Module 1 and Module 4 validation; files had to be uploaded from local. Recommended attendee distribution (reordered 2026-07-16):

1. **Git clone of a workshop assets repo** (recommended — one clone delivers every module's files, including the Module 4 agent script; no per-file copy steps).
2. S3 + `aws s3 cp` (Workshop Studio assets bucket — confirm whether it obviates the repo).
3. Heredoc with quoted `'EOF'` (last resort; still paste-dependent).

### Cleanup

```bash
helm uninstall my-otel-demo
eksctl delete cluster --name otel-demo --region us-west-2
```

Verify no orphaned ELB or ENIs in the console — `helm uninstall` removes the patched LoadBalancer service, but worth confirming.

> **Workshop Studio translation**: cluster + collector configuration both become CFN. Attendee experience reduces to running `aws eks update-kubeconfig` and pasting a Honeycomb API key into a pre-staged secret.

---

## Module 2 — Investigate in Honeycomb with organic data

### Purpose

Tour Honeycomb's investigation surfaces — datasets, traces, BubbleUp, Canvas — using the organic latency present in the demo *without toggling any flags*. The demo's `product-reviews` service ships with a self-hosted LLM (`LLM_HOST=llm`, `LLM_MODEL=astronomy-llm`) and OpenAI-compatible API. `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` is set, so GenAI semantic conventions are on out of the box.

### What's organically present

- `/api/product-ask-ai-assistant/` endpoint with P99 ~214ms (sequential 2-LLM-call pattern, compounding variance).
- `/api/recommendations` and `/api/product-reviews` at elevated latency vs. baseline.
- `gen_ai.system`, `gen_ai.request.model`, `gen_ai.response.*` attributes on LLM spans.
- Zero application errors with all flags off.

### Suggested attendee flow

1. Open Honeycomb → look at the auto-created datasets (one per service).
2. Run a default trace query on the `frontend-proxy` dataset.
3. Apply BubbleUp on slow request distributions — confirm `/api/product-ask-ai-assistant/` jumps out as the outlier.
4. Open a representative trace, walk the span tree across services.
5. Use Canvas to build an investigation board around the AI assistant endpoint.

### Workshop Studio translation

Nothing to provision — pure UI exploration.

---

## Module 3 — AWS DevOps Agent + Honeycomb MCP

### Purpose

Provision an AWS DevOps Agent (built on Bedrock AgentCore, GA March 2026), test it against the EKS cluster *without* observability MCP to establish a baseline, then connect Honeycomb MCP to demonstrate the value of trace-data-aware AI investigation.

### Prereqs

- IAM permissions `aidevops:*` and `iam:CreateRole` in the account.
- DevOps Agent GA region (US East N. Virginia, US West Oregon, EU Frankfurt/Ireland, AP Sydney/Tokyo).

### Agent Space setup

1. Console → search "DevOps Agent" → **Create Agent Space**.
2. Wizard: auto-create the service IAM role (one click — recommended).
3. Enable the Web App (separate IAM-authenticated URL).
4. Open the agent UI via **"Operator access"** on the Agent Space page.

### Sanity-check the IAM role

```bash
aws iam list-roles --query 'Roles[?contains(RoleName, `DevOpsAgent`)].RoleName'
aws iam list-attached-role-policies --role-name <role-name>
```

Confirm the role has read access to EKS, CloudWatch Logs, EC2, X-Ray.

### Naked smoke test (before MCP)

Run these prompts in order via the Operator access chat:

1. *"Tell me what's deployed."* — confirms account association + role.
2. *"Describe my EKS cluster `otel-demo`."* — confirms topology read.
3. *"Investigate latency on frontend-proxy."* — kicks off a full investigation.

**Expected outcome**: the agent runs a multi-subagent investigation (~7-8 minutes), correctly rules out infrastructure causes (CPU, memory, network, ELB, EBS), then *names* the four visibility gaps preventing it from reaching application-level conclusions. See `module-5-baseline-naked-investigation.md` for the full verbatim baseline.

### Why MCP matters — observed visibility gaps

The naked investigation surfaces four distinct gaps, each closeable by a different mechanism:

| Gap | Closed by |
|---|---|
| No kubectl access (agent IAM role not in EKS access entries) | EKS access entry |
| No Container Insights / pod-level metrics | CloudWatch Container Insights addon |
| No application logs in CloudWatch | EKS logging enable + CloudWatch agent |
| **No distributed traces** | **Honeycomb MCP** |

For the workshop, **leave the kubectl, Container Insights, and CloudWatch log gaps in place**. Closing *only* the trace gap with MCP gives the cleanest before/after narrative — and keeps the parked humans-vs-agent bonus module viable if timing allows.

### Register Honeycomb MCP

#### In Honeycomb

**Account → Team Settings → API Keys → Create Management API Key**. Scope: Model Context Protocol (Read) + Environments (Read). Copy both the **Key ID** and **Key Secret** — shown only once.

#### In the DevOps Agent console

Agent Space → Capabilities → **MCP Servers → Register MCP Server**.

| Step | Field | Value |
|---|---|---|
| 1 — Server details | URL | `https://mcp.honeycomb.io/mcp` (US) or `https://mcp.eu1.honeycomb.io/mcp` (EU) |
| 1 — Server details | Transport | HTTP / Streamable HTTP |
| 2 — Authorization flow | Method | API key |
| 3 — Authorization config | API Key Name | Friendly label (e.g. `honeycomb-mcp`) |
| 3 — Authorization config | **API Key Header** | `Authorization` — *header name only* |
| 3 — Authorization config | **API Key Value** | `Bearer KEY_ID:SECRET_KEY` — *Bearer prefix here, both halves of the key joined with `:`* |

### Auth UX gotchas — must be in attendee guide

**The AWS form splits header name from header value, but Honeycomb's docs show the header as a single concatenated string.** Both docs surfaces are lacking; attendees will hit this without explicit guidance.

1. **Header field expects only the header name.** Pasting `Authorization: Bearer xxx` whole will throw "Invalid input".
2. **Key ID and Key Secret must be joined with a colon.** Half-pasted keys produce silent auth failures.
3. **`Bearer ` prefix (with trailing space) goes in the value field.** If the AWS form auto-prepends `Bearer` in future, drop the prefix and use just `KEY_ID:SECRET_KEY`. Verify behavior pre-workshop.
4. **No leading/trailing whitespace or quotes** in either field — silent failure mode.

After saving, smoke test with the prompt *"List available Honeycomb teams and environments"*. A real response confirms auth.

### Augmented smoke test

Re-run the same latency prompt: *"Investigate latency on frontend-proxy."*

**Expected outcome**: the investigation now reaches application-level root cause. Observed in dev:
- Correctly diagnoses the 900K ms outlier as flagd EventStream long-lived gRPC streams (architectural, not request latency).
- Identifies `/api/product-ask-ai-assistant/` as the real tail-latency endpoint with sequential-LLM-call compounding variance (P99 ~214ms).
- Provides per-endpoint percentile breakdowns.
- Zero "cannot determine" gap blocks.

Full verbatim output: `module-5-augmented-mcp-investigation.md`.

### Workshop Studio translation

DevOps Agent setup is Terraform-supported and will be wrapped into the Workshop Studio CFN/IaC blueprint. MCP server registration remains interactive per-attendee (key generation + console paste) — ~5 minutes per attendee. Pre-staging the Honeycomb signup link in the Workshop Studio landing page would shorten the front-of-module setup.

---

## Module 4 — Build + instrument a Strands agent → Agent Timeline

**Status: ✅ validated end-to-end 2026-07-16 (dev account, us-west-2).** Replaces the earlier Kiro and Claude Code designs (decision history and archaeology: `module-4-strands-agent-timeline.md`, `module-4-cc-bedrock-validation.md`).

### Purpose

Attendees run a minimal AWS Strands agent in CloudShell, instrumented with OTel GenAI semantic conventions, exporting OTLP **directly to Honeycomb — no collector, no transform**. Payoff: a fully-populated Agent Timeline (conversation grouping, chat + tool-call spans, complete role-labeled Messages panel) from ~60 lines of code attendees can read top to bottom.

### Why this design

- Strands emits GenAI semconv natively (`invoke_agent` / `chat` / `execute_tool` spans, token + model attributes). The three attributes Agent Timeline requires — `gen_ai.conversation.id`, `gen_ai.agent.name`, `gen_ai.operation.name` — are visible in the agent code itself. That's the teaching moment: instrumentation as three readable lines, not a magic sidecar.
- Honeycomb is OTLP-native, so export is just env vars.
- Bedrock Haiku 4.5 keeps per-attendee cost trivial. Validated inference profile: `us.anthropic.claude-haiku-4-5-20251001-v1:0`. (5-series models are account-gated — do not build on them.)
- Contrast with Module 3 completes the arc: *use* an AWS agent, then *instrument your own*.

### Setup (CloudShell)

CloudShell's default `python3` meets the ≥3.10 requirement (3.13 observed). The `[otel]` extra is required — the base package omits the OTLP exporter and the telemetry bootstrap fails with `ModuleNotFoundError: opentelemetry.exporter...`.

```bash
python3 -m venv ~/strands-venv
source ~/strands-venv/bin/activate
pip install 'strands-agents[otel]'
```

### Agent script

Save as `~/agent.py` — ships in the workshop assets repo, not pasted. Two zero-dependency `@tool` functions produce clean `execute_tool` spans with visible arguments and results; their docstrings become the tool descriptions the model sees. The `trace_attributes` block carries the two identity attributes the Timeline groups on; Strands emits `gen_ai.operation.name` per span automatically.

```python
import uuid
from datetime import datetime, timezone

from strands import Agent, tool
from strands.telemetry import StrandsTelemetry

StrandsTelemetry().setup_otlp_exporter()


@tool
def current_time() -> str:
    """Returns the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


@tool
def word_count(text: str) -> int:
    """Counts the number of words in the provided text."""
    return len(text.split())


session_id = str(uuid.uuid4())

agent = Agent(
    model="us.anthropic.claude-haiku-4-5-20251001-v1:0",
    tools=[current_time, word_count],
    system_prompt="You are a concise workshop assistant. Use your tools when asked about the time or word counts.",
    trace_attributes={
        "gen_ai.conversation.id": session_id,
        "gen_ai.agent.name": "workshop-agent",
    },
)

print(f"conversation id: {session_id}")
while True:
    try:
        user_input = input("\nyou> ")
    except EOFError:
        break
    if user_input.strip().lower() in ("exit", "quit"):
        break
    agent(user_input)
```

### Configure and run

Set the Honeycomb ingest key first, on its own (same key/pattern as Module 1's `honeycomb-credentials`):

```bash
export HONEYCOMB_API_KEY=<INGEST_KEY>
```

Then the OTel env vars. **`OTEL_SEMCONV_STABILITY_OPT_IN` is load-bearing**: without the `gen_ai_span_attributes_only` token, Strands puts message content in a span event, which the Agent Timeline Messages panel does not render (known limitation) — the timeline populates but conversations appear empty. CloudShell already provides AWS credentials and `AWS_REGION` for Bedrock.

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=https://api.honeycomb.io
export OTEL_EXPORTER_OTLP_HEADERS=x-honeycomb-team=$HONEYCOMB_API_KEY
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_RESOURCE_ATTRIBUTES=service.name=strands-workshop-agent
export OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental,gen_ai_span_attributes_only
```

Then activate and run:

```bash
source ~/strands-venv/bin/activate
python ~/agent.py
```

### Suggested attendee prompts

1. *"What time is it right now?"* — forces a `current_time` tool call.
2. *"How many words are in this sentence: observability makes on-call humane again"* — forces `word_count` with arguments.
3. *"Summarize what tools you have."* — pure chat turn, no tool.

### Explore Agent Timeline (formerly Module 6 — now the payoff of this module)

Open **Agent Timeline** from the main navigation and find the conversation (browse recent conversations, or search by the printed conversation id). Attendee flow:

1. **Conversations view**: the session appears in the list with agent count, tool calls, tokens, and latency — grouped across every turn by the session UUID the script set as `gen_ai.conversation.id`.
2. **Timeline view**: `workshop-agent` lane with one `invoke_agent` span per turn; nested `chat` spans (model name + token counts) and `execute_tool current_time` / `execute_tool word_count` spans.
3. **Gen AI tab on a chat span**: model, parameters, TTFT, token usage — and the **Messages section rendering both user prompts and assistant responses, role-labeled**. Connect it back to the code: this is `gen_ai.input/output.messages` as span attributes.
4. **Gen AI tab on a tool span**: tool name plus arguments and result JSON — connect back to the `@tool` functions.
5. Optionally, drop into the **Traces view** below the timeline to see the same data as a raw span waterfall — reinforces that Agent Timeline is a lens over ordinary OTel traces, not a separate pipeline.

Also verify: a new `strands-workshop-agent` dataset exists in the environment (`service.name` routing, same as Module 1).

### Observed gotchas — must be in attendee guide

1. **`pip install strands-agents` alone breaks at runtime** — the `[otel]` extra is mandatory (`ModuleNotFoundError` on the OTLP exporter import).
2. **The `gen_ai_span_attributes_only` token** in `OTEL_SEMCONV_STABILITY_OPT_IN` is the difference between a populated Messages panel and an empty one.
3. **Ingest key, not management key** — same failure mode as Module 3's key confusion; the OTLP header silently authenticates against ingest only.

### Workshop Studio translation

Nothing new to provision — Bedrock model access/IAM in the vended account is the same dependency Module 3 already carries. The script ships in the assets repo; attendee-side work reduces to venv + pip install + env vars. Pin the `strands-agents` version in the assets repo requirements before the event.

---

## Open items for AWS + Honeycomb collaboration

- [ ] **Region lock**: `us-east-1` (original plan) vs. `us-west-2` (current dev).
- [ ] **Workshop Studio CFN**: translate eksctl-equivalent + DevOps Agent Terraform + Honeycomb pre-staging into the blueprint.
- [ ] **SCPs / IAM boundaries**: confirm the constraints attendee accounts will inherit; emulate them in dev validation account to catch surprises.
- [ ] **Asset distribution**: GitHub repo cloned into CloudShell is now the leading candidate (2026-07-16 — CloudShell paste-mangling makes S3/heredoc worse for multi-line files); confirm against Workshop Studio's assets bucket, stand up the repo, pin `strands-agents` version in it.
- [x] **Module 4**: ~~Kiro path~~ → Strands agent + Agent Timeline (absorbs former Module 6), validated end-to-end 2026-07-16.
- [ ] **Bonus module (PARKED — evaluate after live-audience timing)**: humans-vs-DevOps-Agent race. Preserved design notes from the June validation: reframe as *different paths to the same conclusion* rather than a timed race (the MCP-augmented agent is sharp enough to demoralize); chaos flag `llmRateLimitError` (narrative continuity with the LLM endpoint the agent already flags — pivots "LLM is slow" to "slow AND failing", humans find it via BubbleUp on `error=true`); scope investigation windows tightly (~last 30 min — both validation runs treated cluster-deploy time as incident start).
- [ ] **Auth UX gotcha**: surface to both AWS DevOps Agent docs team and Honeycomb docs team — the split-field vs concatenated-string mismatch is a documented trap.

---

## Helpful links

### Workshop infrastructure (after deploy — replace `<elb-dns>` with `kubectl get svc frontend-proxy` external IP)

- Web store: `http://<elb-dns>:8080/`
- Grafana: `http://<elb-dns>:8080/grafana/`
- Jaeger UI: `http://<elb-dns>:8080/jaeger/ui/`
- Load Generator UI: `http://<elb-dns>:8080/loadgen/`
- Flagd configurator UI: `http://<elb-dns>:8080/feature`

### AWS DevOps Agent

- [Working with DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent.html)
- [Getting Started — Creating an Agent Space](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html)
- [Connecting MCP Servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-capabilities-for-aws-devops-agent-connecting-mcp-servers.html)
- [DevOps Agent IAM Permissions](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html)
- [Getting Started — Terraform](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-getting-started-with-aws-devops-agent-using-terraform.html)
- [Connecting to Privately Hosted Tools (VPC)](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-capabilities-for-aws-devops-agent-connecting-to-privately-hosted-tools.html)
- [AWS Blog — Building an End-to-End Agentic SRE](https://aws.amazon.com/blogs/devops/building-an-end-to-end-agentic-sre-using-aws-devops-agent/)
- [AWS Blog — Diagnose EKS Node Issues with DevOps Agent + Custom MCP](https://aws.amazon.com/blogs/devops/diagnose-eks-node-issues-faster-with-aws-devops-agent-and-custom-mcp/)

### OpenTelemetry Demo

- [Kubernetes Deployment Guide](https://opentelemetry.io/docs/demo/kubernetes-deployment/)
- [otel-demo Helm Chart (source)](https://github.com/open-telemetry/opentelemetry-helm-charts)
- [Demo Architecture](https://opentelemetry.io/docs/demo/architecture/)

### Honeycomb

- [MCP Configuration Guide](https://docs.honeycomb.io/integrations/mcp/configuration-guide)
- [MCP Tools Reference](https://docs.honeycomb.io/integrations/mcp/tools/)
- [Honeycomb Intelligence](https://docs.honeycomb.io/security-compliance/honeycomb-intelligence/)
- [MCP Use Cases & Examples](https://docs.honeycomb.io/integrations/mcp/use-cases/)
- [MCP Troubleshooting](https://docs.honeycomb.io/integrations/mcp/troubleshooting/)

### AWS infrastructure tooling

- [eksctl](https://eksctl.io/)
- [AWS CloudShell](https://console.aws.amazon.com/cloudshell)
- [AWS Workshop Studio (catalog)](https://catalog.workshops.aws/)

### Strands / Agent Timeline (Module 4)

- [AWS Strands Agents SDK](https://strandsagents.com/)
- [Honeycomb — Instrumenting AI Agents](https://docs.honeycomb.io/send-data/use-cases/agents/)
- [Honeycomb — Agent Timeline](https://docs.honeycomb.io/investigate/observe/agent-timeline)
- [storechat reference implementation (Honeycomb DevRel)](https://github.com/honeycombio/devrel-opentelemetry-demo/tree/main/src/storechat)

### Validation artifacts (in this folder)

- `module-5-baseline-naked-investigation.md` — DevOps Agent investigation **before** Honeycomb MCP
- `module-5-augmented-mcp-investigation.md` — DevOps Agent investigation **with** Honeycomb MCP
- `module-4-strands-agent-timeline.md` — Module 4 validation runbook (Strands, validated 2026-07-16)
- `module-4-cc-bedrock-validation.md` — superseded Claude Code path; retained as evidence for feature asks (CC response-text-on-spans; Timeline non-attribute rendering)

---

## Appendix A — flagd flag inventory

Flags shipped by the otel-demo, available via the Flagd configurator UI at `http://<elb-dns>:8080/feature`. All default `off`. Used for chaos engineering and investigation moments.

| Flag | Behavior | Workshop fit |
|---|---|---|
| `adFailure` | Fail ad service | General error investigation |
| `adHighCpu` | High CPU on ad service | Resource saturation |
| `adManualGc` | Trigger GC pauses in ad service | Latency tail story |
| `cartFailure` | Fail cart service | General error investigation |
| `emailMemoryLeak` | Memory leak in email service (variants 1x → 10000x) | Slow-burn investigation |
| `failedReadinessProbe` | Cart readiness probe failure | K8s health investigation |
| `imageSlowLoad` | Slow image loading (5s / 10s) | Frontend latency story |
| `kafkaQueueProblems` | Kafka queue overload + consumer delay | Backpressure / lag story |
| **`llmInaccurateResponse`** | Inaccurate LLM summary for product ID L9ECAV7KIM | Module 3 quality investigation |
| **`llmRateLimitError`** | Intermittent LLM rate-limit errors | **Parked bonus module — leading candidate** |
| `loadGeneratorFloodHomepage` | Flood frontend with requests | Throughput / scaling story |
| `paymentFailure` | Payment service charge failures (10% → 100%) | Error rate investigation |
| `paymentUnreachable` | Payment service unavailable | Hard failure story |
| `productCatalogFailure` | Fail product catalog service | General error investigation |
| `recommendationCacheFailure` | Recommendation cache failure | Memory growth story |
