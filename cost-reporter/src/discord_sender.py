import os

import boto3
import discord
import io
import aiohttp

def get_webhook() -> str:
    ssm = boto3.client("ssm")

    return ssm.get_parameter(
        Name=os.environ["DISCORD_WEBHOOK_PARAMETER"],
        WithDecryption=True
    )["Parameter"]["Value"]


async def send_image(filename: str):
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(get_webhook(), session=session)
        await webhook.send("Cost Report", file=discord.File(fp=filename))
