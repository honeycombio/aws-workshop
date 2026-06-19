---
title: "Module 2: Configure Observability"
weight: 40
---

In this module, you'll explore the OpenTelemetry instrumentation that's already built into the GenAI application and configure it to send telemetry data to Honeycomb. This demonstrates a **production-ready pattern** where observability is a first-class citizen from day one, not bolted on later.

## Module Overview

**Duration:** 15 minutes

**Objectives:**
- Understand the existing OpenTelemetry instrumentation architecture
- Review auto-instrumentation and custom tracing for GenAI workloads
- Verify Honeycomb configuration in the deployed application
- Generate traffic and confirm telemetry is flowing to Honeycomb
- Explore the trace structure and GenAI-specific attributes

## Key Concept: Observability From Day One

Unlike traditional approaches where instrumentation is added after deployment, this application demonstrates **observability-first architecture**:

✅ OpenTelemetry instrumentation exists **before** the first deployment

✅ Traces, logs, and metrics are **built into** the application architecture

✅ Configuration is **declarative** via environment variables

✅ GenAI-specific semantics follow **emerging standards**

::alert[**Philosophy**: In production systems, observability should be non-negotiable infrastructure, just like logging and error handling. This workshop shows how to build it in from the start.]{type="info"}
