---
title: "Step 3: Configure Pulumi ESC Environment"
weight: 33
---

Pulumi ESC (Environments, Secrets, and Configuration) provides secure secrets management. We'll create an ESC environment to store all sensitive configuration.

## Configure OpenID Connect for AWS account

Before creating the workshop environment, you need to configure AWS OIDC authentication. We will do it but running Cloud Formation (CFN) template which creates the identity provider and configures the IAM role with trust policy. To learn more you can check [Pulumi documentation](https://www.pulumi.com/docs/esc/environments/configuring-oidc/aws/).

:image[CloudFormation Upload Template]{src="/static/images/pulumi/cfn-upload-template.png" width=600}

::alert[**What is OIDC?** OpenID Connect (OIDC) allows Pulumi ESC to assume AWS IAM roles without storing long-lived credentials. This is a **security best practice** - credentials are dynamically generated and expire after 1 hour.]{type="note"}

1. Download Cloud Formation Template :link[**here**]{href=":assetUrl{path="../static/infrastructure/pulumi-oidc.yaml"}" action=download} to automatically provision the identity provider and the IAM role

2. Make sure you logged in to event's provided AWS Account. Navigate to [CFN console](https://us-west-2.console.aws.amazon.com/cloudformation/home?region=us-west-2#/stacks/create), select **Upload a template file**, and choose the downloaded file. Click **Next**

3. Enter any stack name, for example `pulumi-oidc`, and enter your Pulumi organization name you created earlier in *PulumiOrgName* parameter. Other parameters are optional and you can leave it as is. Click **Next**

:image[Pulumi OIDC CFN Parameters]{src="/static/images/pulumi/pulumi-oidc-setup-cfn.png" width=600}

4. Scroll down and check *I acknowledge that AWS CloudFormation might create IAM resources with custom names* box at ther bottom of the page, click **Next** and then **Submit** on the next page. 

5. It takes a minute to provision. Navigate to **Outputs** and copy **RoleArn**. You will need it for next step.


## Create Workshop-Specific ESC Environment

Now create the workshop-specific environment that imports the AWS credentials:

1. In Pulumi Cloud, navigate to **ESC** → **Environments**

   You'll see the Environments page. Initially, it will be empty:

   :image[Environments Page]{src="/static/images/pulumi/environments-page.png" width=750}

2. Click **Create Environment**

   In the dialog, fill in the following:
   - **Project name**: `honeycomb-pulumi-workshop` (creates a new project for organizing your environments)
   - **Environment name**: `ws` (short for "workshop")

   :image[Create Environment Form]{src="/static/images/pulumi/create-environment-form.png" width=750}

   ::alert[**Environment Naming**: The full environment name will be `honeycomb-pulumi-workshop/ws`. This format follows the pattern `project-name/environment-name`, allowing you to organize multiple environments under the same project.]{type="info"}

3. Click **Create Environment** to create the environment

4. Add the following YAML configuration. Replace `roleArn` with the RoleArn output value from OIDC setup. Replace `honeycombApiKey` value with your Ingest API token created at Honeycomb setup step.

```yaml
values:
  aws:
    login:
      fn::open::aws-login:
        oidc:
          duration: 1h
          roleArn: <pulumi-oidc-assigned-role>
          sessionName: pulumi-environments-session
  app:
    opensearchMasterPassword:
      fn::secret: YourStrongPassword123!
    opensearchMasterUser: admin
    honeycombApiKey: <honeycomb-api-key>
  pulumiConfig:
    opensearchMasterPassword: ${app.opensearchMasterPassword}
    opensearchMasterUser: ${app.opensearchMasterUser}
    anthropic-api-key: test
    dockerBuildCloudBuilder: cloud-dirien-pulumi-test
    honeycombApiKey: ${app.honeycombApiKey}
  environmentVariables:
    AWS_ACCESS_KEY_ID: ${aws.login.accessKeyId}
    AWS_SECRET_ACCESS_KEY: ${aws.login.secretAccessKey}
    AWS_SESSION_TOKEN: ${aws.login.sessionToken}
```

   After entering the configuration, the Monaco editor will show the YAML on the left side and the resolved preview on the right side:

   :image[Environment Configuration Saved]{src="/static/images/pulumi/environment-configuration-saved.png" width=750}

   ::alert[**Security Note**: The `fn::secret` encryption will happen automatically when you save. Your secrets will be encrypted and stored securely by Pulumi ESC.]{type="info"}

5. Click **Save**

6. **Test your ESC environment** from the VS Code terminal:

   ```bash
   pulumi env get honeycomb-pulumi-workshop/ws
   ```

   This should show your environment configuration (secrets will be hidden).

7. **Verify AWS credentials** work:

   ```bash
   pulumi env run honeycomb-pulumi-workshop/ws -i -- aws sts get-caller-identity
   ```

   Expected output:
   ```json
   {
       "UserId": "<GENERATED_KEY>:pulumi-environments-session",
       "Account": "123456789012",
       "Arn": "arn:aws:sts::123456789012:assumed-role/pulumi-workshop-oidc/pulumi-environments-session"
   }
   ```

   ::alert[**OIDC Authentication**: The ARN shows an assumed role, not a direct IAM user. This confirms that OIDC authentication is working correctly, with temporary credentials generated dynamically.]{type="info"}

::alert[**Troubleshooting**: If `aws sts get-caller-identity` fails, ensure the AWS OIDC configuration is correct in your ESC environment.]{type="warning"}