import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import asyncio
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=";", intents=intents)

channel_id = 1180258553227903137
sent_videos = set()
sent_videos_file = "sent_videos.txt"

async def read_sent_videos():
    try:
        with open(sent_videos_file, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

async def write_sent_video(video_id):
    with open(sent_videos_file, "a") as file:
        file.write(video_id + "\n")

@bot.command()
async def fight(ctx):
    channel = bot.get_channel(channel_id)

    response = requests.get("https://t.me/s/onlyfighting/random")
    webpage = response.text
    soup = BeautifulSoup(webpage, 'html.parser')

    video_tags = soup.find_all('video')

    sent_videos = await read_sent_videos()

    for i, video_tag in enumerate(video_tags[:3]):
        video_url = video_tag['src']
        video_id = video_tag.get('id') or video_url

        if video_id in sent_videos:
            continue

        sent_videos.add(video_id)
        await write_sent_video(video_id)

        file_name = f"video{i}.mp4"

        response = requests.get(video_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        await channel.send(file=discord.File(file_name))
        os.remove(file_name)

@bot.event
async def on_member_join(member):
    channel_id = 1180244347233501328
    welcome_channel = bot.get_channel(channel_id)

    if welcome_channel:
        welcome_message = (
            f"Welcome to Out of Racks, {member.mention}!\n"
            f"- Check out <#1180258553227903137>\n"
            f"  - Make sure to stay active!\n"
            f"- only real mfs\n"
        )

        embed = discord.Embed(description=welcome_message, color=0xc22bf1)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1071729494391529522/1071744392064421908/image0.gif")
        embed.set_footer(text="Out of Racks Remake")

        await welcome_channel.send(embed=embed)

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
