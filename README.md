# Cost Reporter

![Python](https://img.shields.io/badge/python-3.12-blue.svg)

An AWS lambda, which sends a daily cost and trend report graph to slack. It helps with one of the three [**FinOps**](https://www.linkedin.com/company/finops-foundation/) phases: `Inform`. It can send you a report **every day** / **only when cost increases** / **only when cost breached a threshold** depending on your [configuration](template.yaml).

Helpful to keep an eye in new projects when the architecture changes quickly, but also for existing projects if you want to keep a close eye on cost.

Example:
![](assets/Figure_1.png)


## Configuration

The following settings can be configured:
- `Title`: The title for the cost report (i.e.: "Project: XYZ")
- `Days`: The days to report (i.e. 10)
- `MinDailyCost`: The minimal daily cost required to trigger a report in $ (i.e. 10)
- `OnlyNotifyOnIncrease`: Whether to send a report only when the cost increased from yesterday to today
- `TargetChannel`: The target Slack channel ID (e.g., "C1234567890")

## How to deploy

Prerequisites:
- Have the [AWS SAM
  CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) installed

### 1) Create a Slack App and Get Bot Token

This lambda uses Slack's Web API to upload files, which requires a bot token (not a webhook):

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) and click **Create New App** → **From scratch**
2. Give it a name (e.g., "Cost Reporter") and select your workspace
3. Under **OAuth & Permissions**, scroll to **Scopes** and add these **Bot Token Scopes**:
   - `chat:write` - Send messages
   - `files:write` - Upload files
4. Scroll up and click **Install to Workspace**, then **Allow**
5. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

For more details, see the [Slack API documentation](https://api.slack.com/authentication/basics).

### 2) Store the Slack Token in AWS SSM Parameter Store

```bash
aws ssm put-parameter --name /cost-reporter/slack-token --value "xoxb-your-slack-token-here" --type SecureString
```

### 3) Get Your Slack Channel ID

You'll need the channel ID (not the channel name) for the target channel:

1. Open Slack in your browser or desktop app
2. Navigate to the channel where you want reports sent
3. Click the channel name at the top
4. Scroll down in the channel details panel
5. Copy the **Channel ID** at the bottom (e.g., `C1234567890`)

Alternatively, right-click the channel name → **View channel details** → scroll to bottom for the Channel ID.

This ID will be necessary during the sam guided deployment.

### 4) Deploy the lambda

```bash
sam build --use-container
sam deploy --guided
```
