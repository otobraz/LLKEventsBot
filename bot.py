# bot.py
import os
import discord
import sqlite3
from dotenv import load_dotenv
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('BOT_PREFIX')

if not os.path.exists('db'):
    os.makedirs('db')

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    bot.load_extension('cogs.greetings')
    bot.load_extension('cogs.events')
    bot.load_extension('cogs.misc')

bot.run(TOKEN)
