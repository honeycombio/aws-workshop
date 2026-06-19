---
title: "Cleanup"
weight: 70
---

## Overview

To avoid ongoing AWS charges, it's important to clean up all resources created during this workshop. Follow these steps carefully to ensure complete cleanup.

::alert[**Important**: If you're attending an AWS-hosted workshop event with pre-provisioned accounts, **no cleanup is required**. The workshop organizers will handle resource cleanup automatically after the event.]{type="info"}

::alert[**Self-Paced Learners**: If you're running this workshop on your own AWS account, **you must complete these cleanup steps** to avoid ongoing charges of ~$100-110/month for the application infrastructure.]{type="warning"}

## Estimated Costs if NOT Cleaned Up

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| ECS Fargate | 1 vCPU, 1GB, 24/7 | ~$25 |
| Amazon OpenSearch | t3.small.search, 10GB | ~$40 |
| Application Load Balancer | Basic usage | ~$18 |
| NAT Gateway | Single gateway | ~$32 |
| Amazon ECR | ~10 container images | ~$0.30 |
| CloudWatch Logs | 7-day retention | ~$5 |
| **Total** | | **~$120/month** |

## Cleanup Steps

### Step 1: Destroy Pulumi Stack

Fore more information see [Pulumi documentation](https://www.pulumi.com/docs/iac/get-started/azure/destroy-stack/).

The application infrastructure you deployed via Pulumi can be destroyed in a single command:

```bash
cd /workshop/ai-workshop/pulumi
pulumi destroy --yes
```

This will delete:
- ✓ ECS Service and Tasks
- ✓ Application Load Balancer and Target Groups
- ✓ Amazon OpenSearch Domain (~10-15 minutes to delete)
- ✓ ECR Repository and Container Images
- ✓ VPC, Subnets, NAT Gateway, Internet Gateway
- ✓ Security Groups
- ✓ IAM Roles and Policies
- ✓ CloudWatch Log Groups
- ✓ Secrets Manager secrets

**Expected time: 15-20 minutes** (most time spent waiting for OpenSearch domain deletion)

::alert[**Monitor Progress**: You can monitor deletion progress in the AWS Console by navigating to CloudFormation → Stacks (Pulumi uses CloudFormation under the hood).]{type="info"}

### Step 2: Verify Stack Deletion

After destruction completes, verify the stack is gone:

```bash
pulumi stack ls
```

You should see your `ws` stack with no resources:

```
NAME                                                    LAST UPDATE     RESOURCE COUNT  URL
ws                                                     3 minutes ago   0               https://app.pulumi.com/...
```

### Step 3: Remove Pulumi Stack (Optional)

If you want to completely remove the stack from Pulumi Cloud:

```bash
pulumi stack rm ws --yes
```

::alert[**Warning**: This deletes the stack history and state. Only do this if you're sure you won't need to reference this stack again.]{type="warning"}

### Step 4: Clean Up Honeycomb (Optional)

If you created a Honeycomb account specifically for this workshop:

1. Login to https://ui.honeycomb.io

2. Navigate to **Settings** → **Datasets**

3. Delete the `otel-ai-chatbot` dataset

4. Optionally, delete your Honeycomb account:
   - Go to **Settings** → **Team** → **Delete Team**

::alert[**Note**: Honeycomb has a generous free tier. You may want to keep your account for future observability projects!]{type="info"}

### Step 5: Clean Up Pulumi Cloud (Optional)

If you created a Pulumi Cloud account specifically for this workshop:

1. Login to https://app.pulumi.com

2. Navigate to your organization settings

3. Delete the organization (this removes all stacks, state, and history)

Alternatively, just remove the workshop stack:
- Go to **Stacks** → select your `dev` stack → **Settings** → **Delete Stack**

::alert[**Note**: Pulumi has a generous free tier (3,000 resource operations/month). You may want to keep your account for future IaC projects!]{type="info"}

### Step 8: Clean Up Local Files (Optional)

On your local machine or VS Code Server, remove workshop files:

```bash
cd /workshop
rm -rf ai-workshop
```

This removes:
- Cloned workshop repository
- Node.js dependencies
- Generated Docker images (local cache)
- CloudWatch log data (local cache)

## Verification Checklist

Before concluding cleanup, verify:

- [ ] Pulumi stack destroyed successfully (`pulumi stack ls` shows 0 resources)
- [ ] CloudFormation stacks deleted (EKS + VS Code Server)
- [ ] No ECS clusters remaining with "otel-ai-chatbot" or "demo-aws-cluster" in name
- [ ] No OpenSearch domains remaining with "otel-ai-chatbot" in name
- [ ] No ECR repositories remaining with "otel-ai-chatbot" in name
- [ ] No Application Load Balancers remaining with "otel-ai-chatbot" in name
- [ ] No VPCs tagged with Project=otel-ai-chatbot
- [ ] AWS billing dashboard shows expected cost reduction (check in 24-48 hours)

### Step 9: Remove Cloud Formation Stacks from your own AWS accounts

If you used Cloud Formation templates to provision VS Code with predeployed tools and Pulumi OIDC, navigate to Cloud Formation in AWS Management Console and explicitly remove stacks.

## Troubleshooting Cleanup Issues

### Pulumi Destroy Hangs on OpenSearch Deletion

**Symptom**: `pulumi destroy` is stuck waiting for OpenSearch domain deletion

**Solution**: OpenSearch domain deletion takes 10-15 minutes. If it exceeds 20 minutes:
1. Check AWS Console → OpenSearch Service → Domains
2. Look for domain status (should be "Deleting")
3. If stuck, manually delete via console and then re-run `pulumi destroy`

### "Resource in use" Errors

**Symptom**: Pulumi or CloudFormation reports resources can't be deleted because they're in use

**Common causes and solutions:**

1. **ECS tasks still running**:
   ```bash
   aws ecs update-service --cluster <cluster-name> --service <service-name> --desired-count 0
   aws ecs delete-service --cluster <cluster-name> --service <service-name> --force
   ```

2. **ENIs not detached**:
   - Wait 5 minutes for automatic cleanup
   - Or manually detach via EC2 Console → Network Interfaces

3. **S3 buckets not empty**:
   - Empty the bucket via console or CLI before deletion

### Stack Deletion Fails

**Symptom**: CloudFormation stack deletion fails with errors

**Solution**:
1. Go to AWS Console → CloudFormation → Select the failed stack
2. Click **Events** tab to see error details
3. Manually delete the problematic resource
4. Retry stack deletion

### Unexpected AWS Charges After Cleanup

**Symptom**: You continue to see charges 24-48 hours after cleanup

**Common causes:**
1. **NAT Gateway**: Charged per hour, ensure VPC was deleted
2. **EBS volumes**: Orphaned volumes not deleted with EC2 instances
3. **Elastic IPs**: Unattached EIPs are charged
4. **CloudWatch Logs**: Data storage charges (minimal)

**Solution**: Review AWS Cost Explorer → Filter by service to identify source

## Cost Verification

After cleanup, verify costs are stopping:

1. Go to AWS Console → Billing → Cost Explorer

2. View **Last 7 days** with daily granularity

3. You should see a sharp drop in costs after cleanup day

4. Expected residual costs:
   - $0.01-0.10/day for CloudWatch Logs retention (until 7-day retention expires)
   - $0.00-0.05/day for S3 storage (if any logs were archived)

## Need Help?

If you encounter issues during cleanup:

- **AWS-Hosted Workshop**: Contact your workshop facilitator
- **Self-Paced Learning**:
  - Check [AWS Support](https://console.aws.amazon.com/support/)
  - Pulumi Community Slack: https://slack.pulumi.com
  - Honeycomb Community Slack: https://pollinators.honeycomb.io

## Thank You!

Thank you for participating in this workshop! We hope you gained valuable insights into:
- Building agentic workflows with AI
- OpenTelemetry instrumentation for GenAI workloads
- Using Honeycomb for observability-driven development
- Pulumi for Infrastructure as Code
- Closed-loop systems with human-in-the-loop controls

### Continue Your Learning

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Honeycomb Learning Portal](https://www.honeycomb.io/learn)
- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Stay curious and keep building!** 🚀
