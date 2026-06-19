---
title: Using Your Own AWS Account
weight: 22
---

::alert[The role used to bootstrap the account will require sufficient permissions to provision the resources above.]{type="info"}

## Option 1: Download and execute the CFN script

Download Cloud Formation Template :link[**here**.]{href=":assetUrl{path="../static/infrastructure/vscode_server.yaml"}" action=download} to automatically provision AWS instrustructure identical to AWS Event. Use AWS CLI or *AWS Management Console -> Cloud Formation -> Create Stack* and select the option *Upload a template file*. 

You will need to provider a stack name. You can leave the rest parameters as is.

::alert[Note the deployment takes 20-30 minutes. Time for a little break and coffee! Feel free to explore the content and Coder termonilogy and continue with hands-on when deployment completed!]{type="warning"}

## Option 2: Use your local IDE 

If you have access to an AWS account with sufficient permissions to configure OIDC, IAM roles and to deploy resources, you can use your local IDE and setup. The following tools are needed and need to be installed and configured as well:

- [Docker](https://www.docker.com/)
- [Kiro CLI](https://kiro.dev/docs/cli/installation/)
- [Pulumi CLI](https://www.pulumi.com/docs/get-started/download-install/)
- [Pulumi ESC CLI](https://www.pulumi.com/docs/esc/cli/download-install/)
- [NVM and Node.js](https://github.com/nvm-sh/nvm)
- Ensure Pulumi and NVM are added to PATH in .bashrc (already done by install scripts, but ensure it's there)
```bash
    echo 'export PATH=$PATH:$HOME/.pulumi/bin' >> /home/<user>/.bashrc
```

- Get [the demo app from GitHub](https://github.com/dirien/ai-workshop)

::alert[If you are running this workshop on your own AWS account, remember to delete all resources by following the [Cleanup instructions](/5_conclusion/52_cleanup.html) to avoid unnecessary charges.]{type="warning"}