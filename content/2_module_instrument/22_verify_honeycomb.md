---
title: "Step 2: Verify Honeycomb Configuration"
weight: 42
---

The Pulumi infrastructure already configured the ECS task with Honeycomb environment variables. Let's verify:

1. **Check the ECS task definition**:
   ```bash
   cd /workshop/ai-workshop/pulumi
   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws ecs describe-task-definition \
     --task-definition $(pulumi stack output ecsTaskDefinitionArn | cut -d'/' -f2) \
     --query 'taskDefinition.containerDefinitions[0].environment[?name==`OTEL_SERVICE_NAME` || name==`OTEL_EXPORTER_OTLP_ENDPOINT` || name==`HONEYCOMB_DATASET`]'
   ```

   Expected output:
   ```json
   [
       {
           "name": "HONEYCOMB_DATASET",
           "value": "otel-ai-chatbot-dev"
       },
       {
           "name": "OTEL_EXPORTER_OTLP_ENDPOINT",
           "value": "https://api.honeycomb.io"
       },
       {
           "name": "OTEL_SERVICE_NAME",
           "value": "otel-ai-chatbot-backend"
       }
   ]
   ```

2. **Verify secrets are configured**:
   ```bash
   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws ecs describe-task-definition \
     --task-definition $(pulumi stack output ecsTaskDefinitionArn | cut -d'/' -f2) \
     --query 'taskDefinition.containerDefinitions[0].secrets[?name==`HONEYCOMB_API_KEY` || name==`OTEL_EXPORTER_OTLP_HEADERS`]'
   ```

   Expected output:
   ```json
   [
       {
           "name": "HONEYCOMB_API_KEY",
           "valueFrom": "arn:aws:secretsmanager:...secret:HONEYCOMB_API_KEY::"
       },
       {
           "name": "OTEL_EXPORTER_OTLP_HEADERS",
           "valueFrom": "arn:aws:secretsmanager:...secret:OTEL_EXPORTER_OTLP_HEADERS::"
       }
   ]
   ```

::alert[**Configuration via Environment**: OpenTelemetry's SDK reads configuration from environment variables, making it cloud-native and easy to configure without code changes.]{type="info"}