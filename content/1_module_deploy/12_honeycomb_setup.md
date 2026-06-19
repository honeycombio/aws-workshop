---
title: "Step 2: Set Up Honeycomb Account"
weight: 32
---

1. **Create a free Honeycomb account** at https://ui.honeycomb.io/signup

   You can sign up using:
   - Email address
   - Google account
   - GitHub account

2. **Create an Ingest API Key**:

   Once logged in to Honeycomb:
   - Navigate to your environment settings

   :image[Environment Settings]{src="/static/images/honeycomb/api_keys.png" width=750}

   - Click **Create Ingest API Key** 
      - **Key Name**: `workshop-otel`
      - Leave **"Can create services/datasets"** enabled. This allows the application to automatically create the `otel-ai-chatbot` dataset when sending telemetry
      - Click **Create**

   :image[Ingest API Key]{src="/static/images/honeycomb/create_ingest_key.png" width=600}
  
   - **Important**: Copy the API key value immediately - you won't be able to see it again!

   Example API key format: `hc[alphanumeric string]`

2. Create an **Managenent API Key** for MCP server. For more documentation check [here](https://docs.honeycomb.io/integrations/mcp/configuration-guide/#setting-up-an-api-key).

   - Navigate to your **Account > Team Settings > API Keys**

   :image[Ingest API Key]{src="/static/images/honeycomb/account_team_settings.png" width=750}

   - Click **Create Management API Key** 
      - **Key Name**: `mcp-integration`
      - Choose 
         - **Environments** scope > **Read-only** 
         - **Model Context Protocol** scope > **Read and write** 
      - Click **Create**
 
   :image[Ingest API Key]{src="/static/images/honeycomb/create_management_key.png" width=600}

   - **Important**: Copy the Key Secret value immediately and click **I've copied key secret!**. Copy **Key ID** as well and save it as the pair.

4. Note your **Environment name**:
   - Look at the top-left of the Honeycomb UI
   - The environment name is usually shown as part of your team name
   - Default environment is often `production` or your team slug
   - You'll see this later when viewing traces

::alert[**API Key Types**: Honeycomb has two types of API keys. **Ingest Keys** are used to send telemetry data (traces, logs, metrics) from your applications. **Configuration Keys** are for managing Honeycomb resources via the API. For this workshop, we only need an Ingest Key.]{type="info"}

::alert[**Security Best Practice**: API keys are immutable after creation for security. Treat Honeycomb API keys like passwords - never commit them to version control or share them publicly. We'll store them securely in Pulumi ESC in the next step.]{type="warning"}

We'll use this API key in the next step to configure Pulumi ESC.