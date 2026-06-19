---
title: "Module 1: Deploy the GenAI Workload"
weight: 30
---

In this module, you'll deploy a production-ready GenAI application to AWS using Pulumi. The application is an **OpenTelemetry AI Chatbot** that uses RAG (Retrieval Augmented Generation) to help developers with OpenTelemetry integration questions.

## Module Overview

**Duration:** 20 minutes

**Objectives:**
- Set up Pulumi CLI and authenticate with Pulumi Cloud
- Configure Pulumi ESC for secrets management
- Examine the infrastructure code
- Deploy the complete application stack to AWS
- Verify the deployment

## What You'll Deploy

By the end of this module, you'll have a fully functional GenAI chatbot running on AWS with the following components:

- **ECS Fargate** cluster running containerized application
- **Application Load Balancer** routing traffic to frontend and API
- **Amazon OpenSearch Service** for vector storage (RAG)
- **Amazon ECR** repository with automatically built Docker images
- **VPC** with public and private subnets across 2 Availability Zones
- **IAM roles** for secure service-to-service communication
- **CloudWatch Logs** for application logging

::alert[**Architecture Note**: The application uses AWS Bedrock (Claude 3.5 Sonnet) for AI responses and OpenSearch for semantic search over OpenTelemetry documentation. The entire stack is deployed as code using Pulumi TypeScript.]{type="info"}

## Access Your Development Environment

1. Open the **VS Code Server URL** provided by your workshop instructor (or from CloudFormation outputs if self-paced)

2. Enter the **password** when prompted

3. Verify you're in the `/workshop/ai-workshop` directory:
   ```bash
   pwd
   # Should output: /workshop/ai-workshop
   ```
   
4. Verify all required tools are installed:
   ```bash
   pulumi version
   aws --version
   node --version
   docker --version
   ```

Expected output:
- Pulumi: v3.x or later
- AWS CLI: v2.x or later
- Node.js: v18.x or later
- Docker: 20.x or later

5. Explore your workspace

::alert[**Tip**: Double click on in main editor area to create an empty file to temporary store all necessary keys. The following values you will need to collect:]{type="info"}
   ```bash
pulumi org:  
pulumi token: 

honeycomb env: 
honeycomb ingest key: 
honeycomb management key
    key secret:  
    key_id: 
   ```

:image[VSCode project]{src="/static/images/pulumi/vscode-project-structure.png" width=750}
