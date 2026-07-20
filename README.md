# Honeycomb + AWS Workshop

Observe and debug modern systems — from microservices to AI agents.

A hands-on workshop where you deploy the OpenTelemetry Demo on Amazon EKS, wire it to Honeycomb, investigate real latency yourself and with the AWS DevOps Agent (before and after connecting Honeycomb MCP), then build and instrument your own AWS Strands agent and explore it in Honeycomb's Agent Timeline.

**Start here → [guide.md](guide.md)**

## What's in this repo

| Path | What it is |
|---|---|
| [guide.md](guide.md) | The full workshop guide — four modules, start to finish |
| `artifacts/honeycomb-values.yaml` | Collector override adding the Honeycomb exporter (Module 1) |
| `artifacts/agent.py` | The Strands workshop agent (Module 4) |
| `artifacts/module-5-baseline-naked-investigation.md` | Verbatim DevOps Agent investigation, before MCP (Module 3) |
| `artifacts/module-5-augmented-mcp-investigation.md` | Verbatim DevOps Agent investigation, with Honeycomb MCP (Module 3) |
| `img/` | Screenshots referenced by the guide |

## Prerequisites

An AWS account with CloudShell access and permissions for EKS, IAM, Bedrock, and AWS DevOps Agent, plus a [free Honeycomb account](https://www.honeycomb.io/signup). Details in the guide.

## Getting started

```bash
cd ~
git clone https://github.com/honeycombio/aws-workshop.git
```

Then open [guide.md](guide.md) and begin with Module 1.
