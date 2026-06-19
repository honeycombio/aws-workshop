---
title: "Step 5: Initialize, Preview and Deploy Pulumi Stack"
weight: 35
---

## Initialize Pulumi program

1. Navigate to the Pulumi directory:
   ```bash
   cd pulumi
   ```

2. Install Pulumi dependencies:
   ```bash
   pulumi install
   ```

3. Initialize a new stack:
   ```bash
   pulumi stack init ws
   ```

   The repository includes a `Pulumi.ws.yaml` file that pre-configures the stack to use your ESC environment:
   ```yaml
   environment:
     - honeycomb-pulumi-workshop/ws
   ```

   When you run `pulumi stack init ws`, Pulumi automatically reads this configuration file and associates the stack with your `honeycomb-pulumi-workshop/ws` ESC environment. This means all secrets, AWS credentials, and configuration values are automatically available to your infrastructure code.

   ::alert[**Stack Configuration**: The `Pulumi.ws.yaml` file is stack-specific configuration. Each stack (dev, staging, prod, ws) can reference different ESC environments, allowing you to manage multiple deployment environments with different credentials and settings.]{type="info"}

## Preview the Infrastructure

Before deploying, preview what Pulumi will create:

```bash
pulumi preview
```

Review the output. You should see Pulumi plans to create approximately:
- 50+ resources including VPC, subnets, security groups, ECS cluster, OpenSearch domain, ALB, etc.
- Docker image build steps
- IAM roles and policies

::alert[**Preview Benefits**: Pulumi's preview shows exactly what will change before any resources are created. This is similar to `terraform plan` but with full programming language support.]{type="info"}

## Deploy the Infrastructure

Now deploy the complete stack:

```bash
pulumi up --yes
```

**What happens during deployment:**

1. **ECR Repository** is created (~30 seconds)
2. **Docker Image** is built from Dockerfile (~3-5 minutes)
   - Installs Node.js dependencies
   - Builds React frontend
   - Creates production container
3. **Docker Image** is pushed to ECR (~1-2 minutes)
4. **VPC and Networking** resources are created (~2-3 minutes)
5. **Security Groups** are configured
6. **OpenSearch Domain** is provisioned (~10-15 minutes) ⏱️
7. **ECS Cluster and Service** are created (~2-3 minutes)
8. **Application Load Balancer** is configured (~2-3 minutes)
9. **CloudWatch Logs** and IAM roles are set up

**Total deployment time: ~15-20 minutes** (mostly waiting for OpenSearch domain creation)

::alert[**Coffee Break Time**: The OpenSearch domain creation takes 10-15 minutes. This is a good time to grab coffee or review the architecture diagram!]{type="info"}

## Verify the Deployment

Once the deployment completes, verify everything is working:

1. Get the application URL:
   ```bash
   pulumi stack output albUrl
   ```

   Copy this URL (e.g., `http://otel-ai-chatbot-alb-1234567.us-east-1.elb.amazonaws.com`)

2. Check the health endpoint:
   ```bash
   curl $(pulumi stack output albUrl)/api/health
   ```

   Expected output:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-11-10T22:11:53.771Z",
     "environment": "production",
     "availableProviders": [
       "bedrock"
     ]
   }
   ```

3. Open the application URL in your browser. You should see the chatbot interface.

4. Try asking a test question (it won't work yet because we haven't ingested documentation):
   - "What is OpenTelemetry?"
   - You'll get a response but without RAG context