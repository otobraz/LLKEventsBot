# bot.py
import os
import discord
import sqlite3
import json
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('BOT_PREFIX')

class LLKEventsBot(Bot):

    def __init__(self):
        super().__init__(description="Bot created by Oto#2494", command_prefix=PREFIX, owner_id=271992863175344130,intents=intents)

        print('Loading embed data...')
        try:
            with open('db/embed_id.json', 'r+') as f:
                try:
                    self.embed_data = json.load(f)
                    if self.embed_data:
                        self.embed_id = self.embed_data['eventEmbed']['id']
                except Exception as e:
                    print(f'{e}')
        except:
            open('db/embed_id.json', 'w+')

        print('Loading permissions data...')
        try:
            with open('db/roles.json', 'r+') as f:
                try:
                    self.perms_data = json.load(f)
                    if self.perms_data:
                        self.perms = self.perms_data['permissions']
                except Exception as e:
                    print(f'{e}')
        except:
            open('db/roles.json', 'w+')

        print('Loading roles DB...')
        self.conn = sqlite3.connect("db/events.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                event_id STRING NOT NULL,
                user_id STRING NOT NULL,
                description STRING NOT NULL,
                target STRING NOT NULL
            )
        """)

        # print('Loading embed data...')
        # try:
        #     with open('db/embed_id.json', 'r+') as f:
        #         try:
        #             self.embed_data = json.load(f)
        #             if self.embed_data:
        #                 self.embed_id = self.embed_data['eventEmbed']['id']
        #         except Exception as e:
        #             print(f'{e}')
        # except:
        #     open('db/embed_id.json', 'w+')

    async def on_ready(self):
        if not os.path.exists('db'):
            os.makedirs('db')
        bot.load_extension('cogs.events')
        bot.load_extension('cogs.moderation')


bot = LLKEventsBot()
bot.run(TOKEN)
