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

dir_path = os.path.dirname(os.path.realpath(__file__))

class LLKEventsBot(Bot):

    def __init__(self):
        super().__init__(description="Bot created by Oto#2494", command_prefix=PREFIX, owner_id=271992863175344130,intents=intents)

        print('Loading embed data...')
        try:
            with open(f'{dir_path}/db/embed_id.json', 'r+') as f:
                try:
                    self.embed_data = json.load(f)
                    if self.embed_data:
                        self.embed_id = self.embed_data['eventEmbed']['id']
                except:
                    self.embed_data = {"eventEmbed":{
                        "id": None                    }}
                    self.embed_id = self.embed_data['eventEmbed']['id']
                    json.dump(self.embed_data, f, indent=4)
        except:
            with open(f'{dir_path}/db/embed_id.json', 'w+'):
                self.embed_data = {"eventEmbed":{
                    "id": self.bot.embed_id
                }}
                self.embed_id = self.embed_data['eventEmbed']['id']
                json.dump(self.embed_data, f, indent=4)

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
            with open(f'{dir_path}/db/roles.json', 'w+') as f:
                self.perms_data = {"permissions":{
                    "admins": [],
                    "mods": [],
                    "hosts": []
                }}
                self.perms = self.perms_data['permissions']
                json.dump(self.perms_data, f, indent=4)

        print('Loading roles DB...')
        self.conn = sqlite3.connect(f'{dir_path}/db/events.db')
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
