import logging
import os
from typing import Optional

import boto3
import slack


def get_token() -> Optional[str]:
    try:
        ssm = boto3.client("ssm")
        return ssm.get_parameter(
            Name=os.environ["SLACK_TOKEN_PARAMETER"],
            WithDecryption=True
        )["Parameter"]["Value"]
    except Exception as e:
        logging.info(f"Slack token not found: {e}")
        return None


def send_image(filename: str, slack_channel: str, token: str) -> None:
    slacker = slack.WebClient(token=token)
    slacker.files_upload(channels=slack_channel, file=filename, title="Cost report")
