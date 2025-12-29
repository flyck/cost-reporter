import logging
import os
from typing import Optional

import boto3
import discord


def get_webhook_url() -> Optional[str]:
    try:
        ssm = boto3.client("ssm")
        return ssm.get_parameter(
            Name=os.environ["DISCORD_WEBHOOK_PARAMETER"],
            WithDecryption=True
        )["Parameter"]["Value"]
    except Exception as e:
        logging.info(f"Discord webhook not found: {e}")
        return None


def send_image(filename: str, webhook_url: str, title: str = "Cost report") -> None:
    """Send an image to Discord via webhook

    Args:
        filename: Path to the image file
        webhook_url: Discord webhook URL
        title: Title/message to send with the image
    """
    webhook = discord.SyncWebhook.from_url(webhook_url)

    with open(filename, 'rb') as f:
        webhook.send(content=title, file=discord.File(f, filename='cost_report.png'))
