---
title: "Step 1: Setup IDE with MCP servers"
weight: 61
---

Kiro CLI should be pre-installed in your VS Code Server environment. If you prefer to use a different AI IDE or CLI (such as Cursor, Windsurf, or Zed), you can follow their respective MCP configuration guides.

1. Verify Kiro CLI is installed:
   ```bash
   kiro-cli --version
   ```

2. Login to Kiro CLI. **Make sure to add** *--use-device-flow* flag. Select **Use for Free with Builder ID** option.

   ```bash
   kiro-cli-chat login --use-device-flow
   ```

   Once prompted, follow the authentication link, login or sign up for a free account. Confirm the authentication code, and confirm **Allow access** for Kiro CLI.

3. Verify MCP support is enabled:
   ```bash
   kiro-cli-chat mcp list
   ```

   This will show any currently configured MCP servers. Initially, it is empty.

::alert[**AI Tool Choice**: This workshop uses Kiro CLI for examples, but the MCP protocol is standardized. You can use any MCP-compatible AI assistant (Kiro, Claude Code, Cursor, Windsurf, etc.) with the same MCP servers.]{type="info"}

## Step 2: Add Honeycomb MCP Servers

The Honeycomb MCP server allows to query your observability data directly. We'll use OAuth authentication, which eliminates the need to manage API keys.

Add the Honeycomb MCP server. Replace `<KEY_ID>` and `<SECRET_KEY>` with your Management Key values created earlier during Honeycomb account setup:

   ```bash
   kiro-cli-chat mcp add --name honeycomb --command npx --args "-y,mcp-remote,https://mcp.honeycomb.io/mcp,--header,Authorization: Bearer <KEY_ID>:<SECRET_KEY>"
   ```

::alert[**Documentation**: For detailed Honeycomb MCP configuration, see: https://docs.honeycomb.io/integrations/mcp/configuration-guide/#step-2-add-your-api-key-to-your-agent]{type="info"}

## Step 3: Add Pulumi MCP Server

The Pulumi MCP server allows to inspect infrastructure state and invoke Pulumi Neo for code generation.

Add the Pulumi MCP server:
   ```bash
   kiro-cli-chat mcp add --name pulumi --command npx --args "mcp-remote,https://mcp.ai.pulumi.com/mcp,--header,Authorization: Bearer <PULUMI_TOKEN>,--header,X-Pulumi-Org:<PULUMI_ORG>"
   ```

::alert[**Documentation**: For detailed Pulumi MCP configuration and capabilities, see: https://www.pulumi.com/docs/iac/using-pulumi/mcp-server/]{type="info"}

## Verify MCP servers configuration and authenticate

1. Verify both MCP servers are configured:
   ```bash
   kiro-cli-chat mcp list
   ```

2. Start Kiro CLI chat to initiate authentication:

   ```bash
   kiro-cli-chat
   ```

4. Test the connection by asking questions:
   ```
   What Honeycomb datasets are available?
   ```

   ```
   What Pulumi stacks do I have in my organization?
   ```


::alert[**MCP Architecture**: Current workshop doesn't support OAuth with HTTP type and one-click integration. See Pulumi and Honeycomb documentation if you desire to configure OAuth authentication with your IDE loacally.]{type="warning"}