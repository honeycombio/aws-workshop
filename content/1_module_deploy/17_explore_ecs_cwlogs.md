---
title: "Step 7: Explore ECS and CloudWatch Logs"
weight: 37
---

AWS CLI commands require credentials from your Pulumi ESC environment. Use `pulumi env run` to execute commands with OIDC-based credentials.

1. View ECS service status:
   ```bash
   CLUSTER_NAME=$(pulumi stack output ecsClusterName)

   # Get the service ARN
   SERVICE_ARN=$(pulumi env run honeycomb-pulumi-workshop/ws -i -- \
     aws ecs list-services --cluster $CLUSTER_NAME --query 'serviceArns[0]' --output text)

   # Extract service name from ARN
   SERVICE_NAME=$(echo $SERVICE_ARN | awk -F'/' '{print $NF}')

   # Describe the service
   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws ecs describe-services \
     --cluster $CLUSTER_NAME \
     --services $SERVICE_NAME \
     --query 'services[0].{Status:status,RunningCount:runningCount,DesiredCount:desiredCount}'
   ```

   Expected output:
   ```json
   {
       "Status": "ACTIVE",
       "RunningCount": 1,
       "DesiredCount": 1
   }
   ```

2. View application logs in CloudWatch:
   ```bash
   # Find the log group name (has Pulumi-generated suffix)
   LOG_GROUP=$(pulumi env run honeycomb-pulumi-workshop/ws -i -- \
     aws logs describe-log-groups --log-group-name-prefix otel-ai-chatbot-logs \
     --query 'logGroups[0].logGroupName' --output text)

   # Tail the logs
   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws logs tail $LOG_GROUP --follow
   ```

   Press `Ctrl+C` to stop tailing logs.

::alert[**Why `pulumi env run`?** AWS CLI commands need credentials. The `pulumi env run honeycomb-pulumi-workshop/ws -i --` wrapper executes commands with OIDC-based AWS credentials from your ESC environment, which are dynamically generated and short-lived (1 hour).]{type="info"}

3. Check all Pulumi outputs:
   ```bash
   pulumi stack output
   ```

   This shows:
   - Application URL
   - ECS cluster and service names
   - OpenSearch endpoint
   - ECR repository URL