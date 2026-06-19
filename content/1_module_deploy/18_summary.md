---
title: "Module Summary"
weight: 38
---

Congratulations! You've successfully:

- ✅ Set up Pulumi Cloud and Pulumi ESC for secure configuration management
- ✅ Deployed a complete GenAI application stack to AWS using Infrastructure as Code
- ✅ Configured ECS Fargate with automated Docker builds
- ✅ Provisioned Amazon OpenSearch with k-NN for vector search
- ✅ Set up Application Load Balancer for production traffic
- ✅ Ingested OpenTelemetry documentation for RAG capabilities
- ✅ Verified the application is running and responding to queries

## What's Next?

In **Module 2**, you'll instrument this application with OpenTelemetry to collect detailed telemetry data and send it to Honeycomb for observability.

---

## Troubleshooting

### Deployment Fails with "Docker daemon not running"

**Solution**: Start Docker daemon:
```bash
sudo systemctl start docker
```

### OpenSearch Domain Creation Timeout

**Symptom**: Deployment stuck on OpenSearch for >20 minutes

**Solution**: OpenSearch domains can take 10-20 minutes. If it exceeds 25 minutes, check AWS Console for errors:
```bash
pulumi env run honeycomb-pulumi-workshop/ws -i -- aws opensearch describe-domain --domain-name otel-ai-chatbot-ws
```

### ECS Tasks Failing Health Checks

**Solution**: Check CloudWatch Logs for application errors:
```bash
# Find the log group name (has Pulumi-generated suffix)
LOG_GROUP=$(pulumi env run honeycomb-pulumi-workshop/ws -i -- \
  aws logs describe-log-groups --log-group-name-prefix otel-ai-chatbot-logs \
  --query 'logGroups[0].logGroupName' --output text)

pulumi env run honeycomb-pulumi-workshop/ws -i -- aws logs tail $LOG_GROUP --since 10m
```

Common issues:
- OpenSearch not accessible (check security group rules)
- AWS Bedrock not enabled in region (verify in AWS Console)
- Environment variables not set correctly (review ECS task definition)

### Application Returns 503 Errors

**Solution**: Verify ECS service has running tasks:
```bash
pulumi env run honeycomb-pulumi-workshop/ws -i -- aws ecs list-tasks --cluster $(pulumi stack output ecsClusterName)
```

If no tasks are running, check ECS service events for deployment failures.

---

## Additional Resources

- [Pulumi AWS Documentation](https://www.pulumi.com/docs/clouds/aws/)
- [Pulumi ESC Documentation](https://www.pulumi.com/docs/pulumi-cloud/esc/)
- [Amazon ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [Amazon OpenSearch k-NN Documentation](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html)
