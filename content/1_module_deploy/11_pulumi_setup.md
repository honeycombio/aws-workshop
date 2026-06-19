---
title: "Step 1: Set Up Pulumi Cloud Account"
weight: 31
---

1. **Create a free Pulumi Cloud account** at https://app.pulumi.com/signup

   You can sign up using:
   - GitHub
   - GitLab
   - Email address

   After signing up, you'll see your organization in the top-left dropdown. You can switch between your organization account and individual account:

   :image[Organization Dropdown]{src="/static/images/pulumi/organization-dropdown.png" width=600}

 2. **Create a workshop-specific organization**: Click on **Create organization** from the dropdown. Enter your organization name (e.g., `honeycomb-pulumi-ai-workshop`), agree to the terms of service, and click **Create organization**:

   ::alert[**Organization Naming**: Choose a descriptive name for your workshop organization. The name becomes part of your Pulumi Cloud URL (e.g., `https://app.pulumi.com/honeycomb-pulumi-ai-<initials>-workshop`). Organization names must be unique across Pulumi Cloud.]{type="info"}

   :image[Create Organization Form]{src="/static/images/pulumi/create-organization-form.png" width=600}

3. **Create a Personal Access Token**:

   Once logged in to Pulumi Cloud:
   - Navigate to https://app.pulumi.com/account/tokens (or click your profile icon → **Personal Access Tokens**)
   - Click **Create token**
   - **Description**: `workshop-token` or `honeycomb-pulumi-workshop`
   - **Expiration**: Leave as default (no expiration) or set to a future date after the workshop
   - Click **Create**
   - **Important**: Copy the token value immediately - you won't be able to see it again!

4. **Login to Pulumi from your VS Code terminal**:

   ```bash
   pulumi login
   ```

   You'll see a prompt like this:
   ```
   Manage your Pulumi stacks by logging in.
   Run `pulumi login --help` for alternative login options.
   Enter your access token from https://app.pulumi.com/account/tokens
       or hit <ENTER> to log in using your browser                   :
   ```

   Paste your access token and press Enter.

5. **Set the default organization**:

   ```bash
   pulumi org set-default <your-organization>
   ```

   This sets your workshop organization as the default for all Pulumi operations, ensuring that new stacks and resources are created under the correct organization.

   Expected output:
   ```
   Default organization set to <your-organization>
   ```

6. **Verify your login**:

   ```bash
   pulumi whoami -v && echo 'Default org:' && pulumi org get-default 
   ```

   Expected output:
   ```
   User: your-username
   Organizations: <your-username>, <your_organization>
   Backend URL: https://api.pulumi.com
   Token type: personal
   Default org:
   <your_organization>
   ```

::alert[**Security Tip**: Pulumi Personal Access Tokens provide access to your infrastructure state and should be treated like passwords. Never commit them to version control or share them in public channels.]{type="warning"}