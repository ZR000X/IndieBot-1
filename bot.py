import discord
from discord.ext import commands

# inf contains the bot token, which is excluded from this repo
import inf

from time import time, sleep
from asyncio import get_event_loop, gather, all_tasks

bot = commands.Bot(command_prefix='.')
bot_id = 844015565243940864


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Active"))


@bot.event
async def on_message(message):
    author = message.author
    channel = message.channel
    raw = message.content.split(" ")
    for e in range(len(raw)):
        raw[e] = raw[e].lower()

    if raw[0] == "ping":
        await channel.send("pong")


print("Initializing")
loop = get_event_loop()
loop.run_until_complete(bot.start(inf.TOKEN))
print("Bot loop complete.")
