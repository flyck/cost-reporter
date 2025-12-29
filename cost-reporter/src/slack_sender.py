import os

import boto3
from slack_sdk import WebClient


def get_token() -> str:
    ssm = boto3.client("ssm")

    return ssm.get_parameter(
        Name=os.environ["SLACK_TOKEN_PARAMETER"],
        WithDecryption=True
    )["Parameter"]["Value"]


def send_image(filename: str, channel_id: str) -> None:
    slacker = WebClient(token=get_token())
    slacker.files_upload_v2(
        channel=channel_id,
        file=filename,
        title="Cost report"
    )
