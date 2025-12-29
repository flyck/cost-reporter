# Cost Reporter

![Python](https://img.shields.io/badge/python-3.12-blue.svg)

An AWS lambda, which sends a daily cost and trend report graph to Slack and/or Discord. It helps with one of the three [**FinOps**](https://www.linkedin.com/company/finops-foundation/) phases: `Inform`. It can send you a report **every day** / **only when cost increases** / **only when cost breached a threshold** depending on your [configuration](template.yaml).

Helpful to keep an eye in new projects when the architecture changes quickly, but also for existing projects if you want to keep a close eye on cost.

Example:
![](assets/Figure_1.png)


## Configuration

The following settings can be configured:
- `Title`: The title for the cost report (i.e.: "Project: XYZ")
- `Days`: The days to report (i.e. 10)
- `MinDailyCost`: The minimal daily cost required to trigger a report in $ (i.e. 10)
- `OnlyNotifyOnIncrease`: Whether to send a report only when the cost increased from yesterday to today

### Slack Configuration
- `SlackTokenParameterName`: SSM Parameter name for the Slack token (default: "/cost-reporter/slack-token")
- `SlackTargetChannel`: The target Slack channel (i.e. "#costoptimization")

### Discord Configuration
- `DiscordWebhookParameterName`: SSM Parameter name for the Discord webhook URL (default: "/cost-reporter/discord-webhook")

## How to deploy

Prerequisites:
- Have the [AWS SAM
  CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed

Deploy the stack:

```bash
sam build --use-container
sam deploy --guided
```

After deployment, configure your notification tokens in AWS Systems Manager Parameter Store:

### For Slack Integration (optional)
Create a Slack bot token (`xoxb-....`) with permissions to write files and send messages to your Slack channel, then store it in the SSM parameter:

```bash
aws ssm put-parameter --name /cost-reporter/slack-token --value "xoxb-your-token-here" --type SecureString
```

### For Discord Integration (optional)
Create a Discord webhook in your channel (Server Settings → Integrations → Webhooks → New Webhook), then store the webhook URL in the SSM parameter:

```bash
aws ssm put-parameter --name /cost-reporter/discord-webhook --value "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL" --type SecureString
```

**Note**: You can configure Slack, Discord, or both. At least one integration should be configured for the lambda to send reports.
