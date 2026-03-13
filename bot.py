import discord
import os
import random
from discord.ext import tasks
from datetime import time

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1482100223982436525

IMAGE_FOLDER = "images"
POSTED_FILE = "posted.txt"

intents = discord.Intents.default()
client = discord.Client(intents=intents)


def get_posted():
    if not os.path.exists(POSTED_FILE):
        return []
    with open(POSTED_FILE, "r") as f:
        return f.read().splitlines()


def save_posted(image):
    with open(POSTED_FILE, "a") as f:
        f.write(image + "\n")


async def post_image():

    channel = client.get_channel(CHANNEL_ID)

    images = os.listdir(IMAGE_FOLDER)
    posted = get_posted()

    available = [img for img in images if img not in posted]

    if not available:
        print("All images posted")
        return

    image = random.choice(available)

    await channel.send(file=discord.File(f"{IMAGE_FOLDER}/{image}"))

    save_posted(image)

    print("Posted:", image)


@tasks.loop(time=time(hour=20, minute=0))
async def daily_post():
    await post_image()


@client.event
async def on_ready():
    print(f"Bot online: {client.user}")
    daily_post.start()


client.run(TOKEN)