# When Your Observability Data Talks Back: AI Agents That Reason Over Infrastructure

A hands-on AWS workshop exploring how AI agents can bridge the gap between observability and infrastructure management.

## What is this workshop about?

Imagine this: your application is running slow. Your observability tools show you the problem, but fixing it means switching contexts, digging through infrastructure configs, and manually making changes. What if your observability data could talk directly to your infrastructure—and suggest fixes automatically?

This workshop shows you how to build exactly that: a closed-loop system where AI agents read your telemetry data, understand what's wrong, and propose infrastructure changes—all with you staying in control.

## What you'll build

You'll deploy a real AI chatbot application on AWS, instrument it with OpenTelemetry, and watch as AI agents:
- **Analyze performance data** from Honeycomb to spot bottlenecks and misconfigurations
- **Reason about infrastructure problems** in real-time
- **Generate infrastructure code fixes** using Pulumi Neo
- **Create pull requests** ready for your review—with you making the final call

This isn't about replacing humans—it's about giving platform engineers and SREs superpowers to debug and fix issues faster.

## What you'll learn

- **Deploy modern AI workloads** using infrastructure as code with Pulumi
- **Instrument applications** with OpenTelemetry to capture meaningful telemetry
- **Query observability data** in Honeycomb to quickly identify issues
- **Work with AI agents** that can read telemetry, diagnose problems, and suggest fixes
- **Implement human-in-the-loop controls** to maintain governance while accelerating remediation

## Who should attend

This workshop is perfect for:
- **Platform Engineers** managing cloud infrastructure
- **SREs** responsible for reliability and incident response
- **Developers** working with cloud-native applications

**Prerequisites:**
- Basic familiarity with AWS, Kubernetes, and observability concepts
- No AI or machine learning experience required
- No prior MCP (Model Context Protocol) experience required

**Workshop Format:**
- Duration: 2 hours
- Hands-on, interactive session
- Experience level: Intermediate

## Technologies you'll use

- **Pulumi** - Infrastructure as code with AI-powered assistance
- **Honeycomb** - Observability platform for querying telemetry data
- **VS Code with Kiro CLI** - AI coding assistant with infrastructure access
- **AWS** - EKS (Kubernetes), EC2, and supporting services
- **OpenTelemetry** - Industry-standard instrumentation framework

## Getting started

The workshop environment includes a VS Code Server pre-configured with all the tools you need. When you join the workshop, you'll receive access to:
- A fully configured development environment
- An AWS account with workshop infrastructure
- Step-by-step guided instructions

## Preview workshop content locally

Want to preview or contribute to the workshop content? You can run the workshop guide locally:

### On macOS
```bash
cd /path/to/repository
chmod +x static/preview_build  # First time only
./static/preview_build
```

For macOS 15 Sequoia or later, you may need to allow the app in System Settings > Privacy & Security, or control-click the app and choose "Open" from the menu.

## Repository structure

```
.
├── content/                   # Workshop guide markdown files
├── static/                    # Images, scripts, and infrastructure templates
│   └── infrastructure/        # CloudFormation templates for workshop setup
├── contentspec.yaml          # Workshop configuration and metadata
└── README.md                 # This file
```

## Resources

- [Honeycomb on AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-x7qbbi2gqjz2o)
- [Pulumi on AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-dwn22batkhsyg)
