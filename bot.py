# bot.py
import os
import sqlite3
import json

import datetime

from dotenv import load_dotenv

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from cogs.utils import helper as h

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PREFIX = os.getenv('BOT_PREFIX')

dir_path = os.path.dirname(os.path.realpath(__file__))

extensions = ['cogs.general', 'cogs.events', 'cogs.moderation']

class LLKEventsBot(Bot):

    def __init__(self):
        super().__init__(
            description="Bot created by Oto#2494",
            command_prefix=PREFIX,
            owner_id=271992863175344130,
            intents=intents,
            help_command=None
        )
        print('\nLoading embed data...')
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
        if not os.path.exists('logs'):
            os.makedirs('logs')

        print('\nLoading extensions...')
        for extension in extensions:
            print(f'Loading {extension}')
            bot.load_extension(extension)

        await bot.change_presence(activity=discord.Game(f'{PREFIX}help'))

        print(f'\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    # async def on_message(self, msg):
    #     if msg.author.bot:
    #         return

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f'I have no permission to do that')
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'You have no permission to use this command')
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You forgot to inform the following parameter: {error.param}')
        else:
            d = datetime.datetime.now()
            with open(f'logs/{d.year}-{d.month}-{d.day}.log', 'a', encoding='utf8') as f:
                # f.write(f'''-------------\n{d.hour}:{d.minute}:{d.second}.{d.microsecond}\n{type(error)}\n{error}\n-------------\n\n'''')
                f.write(
                    '-------------\n'
                    f'{d.hour}:{d.minute}:{d.second}.{d.microsecond}\n'
                    f'Command: {ctx.message.content}\n'
                    f'Author: {ctx.author}\n'
                    f'Exception: {type(error)}\n'
                    f'Description: {error}\n'
                    '-------------\n\n'
                )
            await ctx.send(f'It seems something went wrong:```{error}```')
            return


bot = LLKEventsBot()
bot.run(TOKEN)
