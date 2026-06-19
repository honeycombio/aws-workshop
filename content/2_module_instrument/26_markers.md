---
title: "Step 6: Best Practice - Deployment Markers (Optional)"
weight: 46
---

Honeycomb supports **markers** to annotate your telemetry data with deployment events. This helps correlate performance changes with code deployments.

To create a marker when deploying:

```bash
# After a successful deployment
HONEYCOMB_API_KEY="your-api-key"
DATASET="otel-ai-chatbot-dev"

curl https://api.honeycomb.io/1/markers/$DATASET \
  -X POST \
  -H "X-Honeycomb-Team: $HONEYCOMB_API_KEY" \
  -d '{
    "message": "Deployed v1.2.3 - Improved LLM instrumentation",
    "type": "deploy",
    "url": "https://github.com/your-repo/commit/abc123"
  }'
```

Markers appear as vertical lines in your Honeycomb graphs, making it easy to see if latency increased or errors spiked after a deployment.

::alert[**CI/CD Integration**: Add marker creation to your CI/CD pipeline so every deployment is automatically annotated in Honeycomb. This is invaluable for incident response and performance regression analysis.]{type="info"}