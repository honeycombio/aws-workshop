---
title: "When Your Observability Data Talks Back: AI Agents That Reason Over Infrastructure"
weight: 0
---

Welcome to our AWS workshop

with      :image[Honeycomb Logo]{src="/static/images/honeycomb/honeycomb-transparent-bg.png" width=200}      and      :image[Pulumi Logo]{src="/static/images/pulumi/pulumi-transparent-bg.png" width=200}

## Overview

Most teams treat observability as a one-way street: telemetry flows in, humans interpret it, then context-switch to infrastructure tooling to fix what's broken. But what happens when the agent reading your traces can also modify the infrastructure that produced them?

In this hands-on workshop, you'll build a closed-loop system where AI agents consume OpenTelemetry metrics from Honeycomb, reason about resource constraints or misconfigurations in AWS environments, and propose infrastructure changes via Pulumi's AI agent, Neo.

We'll provision a GenAI workload (an OpenTelemetry AI chatbot) on AWS using Pulumi, instrument it with OpenTelemetry, surface anomalies in Honeycomb, then show an AI agent working in your IDE diagnosing the root cause in real time and generating infrastructure-as-code patches with Neo's help—all with a human-in-the-loop step for full enterprise compliance.

## You'll leave with:

* **Patterns you can adapt to your own infrastructure** to provision an observability solution using the same IaC approach as for other applications and modules
* **Understanding of OpenTelemetry semantic conventions** for AI workloads and how to use Honeycomb to quickly analyze bottlenecks by asking questions of the data
* **Knowledge of Pulumi Neo's capabilities** and use cases it helps to address at scale
* **Practical insight into how agentic AI** can accelerate time-consuming debugging and remediation tasks all the way to PR in your repo

## Who should attend

Perfect for **platform engineers, SREs, and developers** managing cloud-native AI workloads who want to understand agentic workflows beyond chat interfaces.

**Prerequisites:**
- No prior MCP experience required
- Familiarity with Kubernetes, AWS, and basic observability concepts is recommended

**Workshop Details:**
- Duration: 2 hours
- Format: Hands-on interactive session with live coding
- Experience Level: Intermediate