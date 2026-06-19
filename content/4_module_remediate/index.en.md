---
title: "Module 4: AI-Powered Remediation"
weight: 60
---

In this module, you'll experience the future of infrastructure management: **AI agents that reason over observability data and propose infrastructure fixes**. You'll configure your IDE with MCP (Model Context Protocol) servers for Honeycomb and Pulumi, then use Pulumi Neo to automatically generate infrastructure code changes based on the performance issues you discovered in Module 3.

## Module Overview

**Duration:** 30 minutes

**Objectives:**
- Understand MCP (Model Context Protocol) and its role in agentic workflows
- Configure Honeycomb MCP server in Kiro CLI
- Configure Pulumi MCP server in Kiro CLI
- Use Kiro CLI to query observability data from Honeycomb
- Ask AI agent to diagnose the performance bottleneck
- Use Pulumi Neo to generate infrastructure code fix
- Review and apply the fix (human-in-the-loop)
- Verify the fix resolves the performance issue

## What is MCP?

**Model Context Protocol (MCP)** is an open protocol that standardizes how AI assistants connect to data sources and tools. Instead of building custom integrations for each LLM and each service, MCP provides a universal interface.

**MCP enables AI agents to:**
- Query external data sources (Honeycomb traces, Pulumi state)
- Execute actions (deploy infrastructure, run queries)
- Access contextual information in real-time

**In this workshop:**
- **Honeycomb MCP Server**: Lets Kiro CLI query your observability data
- **Pulumi MCP Server**: Lets Kiro CLI inspect infrastructure and invoke Pulumi Neo
- **Kiro CLI**: AI assistant that understands MCP protocol (you can also use other AI IDEs like Cursor, Windsurf, or AI CLIs like Zed)

::alert[**Why This Matters**: With MCP, your AI assistant can go beyond simple chat responses. It can actively reason over live data and propose concrete actions. This is the foundation of **agentic workflows** where AI systems can autonomously (with human oversight) operate infrastructure.]{type="info"}