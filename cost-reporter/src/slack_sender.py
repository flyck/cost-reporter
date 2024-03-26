import os

import boto3
import slack


def get_token() -> str:
    return os.environ["SLACK_TOKEN"]


def send_image(filename: str, slack_channel: str) -> None:
    slacker = slack.WebClient(token=get_token())
    slacker.files_upload(channels=slack_channel, file=filename, title="Cost report")
