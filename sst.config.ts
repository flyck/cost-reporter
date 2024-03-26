/// <reference path="./.sst/platform/config.d.ts" />

export default $config({
  app(input) {
    return {
      name: "cost-reporter",
      removal: input?.stage === "production" ? "retain" : "remove",
      home: "aws",
    };
  },
  async run() {
    new sst.aws.Function("Reporter", {
      handler: "lambda_function.lambda_handler",
      timeout: "30 seconds",
      bundle: "cost-reporter/dist/",
      environment: {
        TITLE: "Cost Report",
        DAYS: 10,
        MIN_DAILY_COST: 0,
        OnlyNotifyOnIncrease: false,
        // currently SST only supports attaching the secret directly
        SLACK_TOKEN: new sst.Secret("CostReporterSlackToken").value,
        DISCORD_TOKEN: new sst.Secret("CostReporterDiscordToken").value,
      },
      permissions: [
        {
          actions: ["ce:getCostAndUsage"],
          resources: ["*"]
        },
        {
          actions: [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          resources: ["*"]
        }
      ],
      transform: {
        function: (props) => ({ ...props, runtime: "python3.9", })
      }
    });
  },
});
