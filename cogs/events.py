import discord
from discord.ext import commands
import sqlite3
import asyncio
import json
from json.decoder import JSONDecodeError

conn = sqlite3.connect("db/events.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS events (
             event_id STRING NOT NULL,
             user_id STRING NOT NULL,
             description STRING NOT NULL,
             target STRING NOT NULL)
             """)

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.timeout = 10
        self.embed_id = self.data = None;
        try:
            with open('db/embed_id.json', 'r+') as f:
                try:
                    self.data = json.load(f)
                    if self.data:
                        self.embed_id = self.data['eventEmbed'][0]['id']
                except:
                    print(f'Error while opening the file')
        except:
            open('db/embed_id.json', 'w+')

    @commands.command(aliases=['add'])
    @commands.has_role(768529062159056977)
    async def add_activity(self, ctx,*, activity_name):
        guild = ctx.guild
        sent = await ctx.send('Briefly describe the event: ')
        details = ''
        try:
            message = await self.bot.wait_for(
                'message', timeout=int(self.timeout),
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            if message:
                details = message.content
                await sent.delete()
                await message.delete()
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send('Cancelling requent...', delete_after=int(self.timeout))
            return

        sent = await ctx.send('Target: ')
        target = ''
        try:
            message = await self.bot.wait_for(
                'message', timeout=int(self.timeout),
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            target = message.content
            await sent.delete()
            await message.delete()
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send('Cancelling requent...', delete_after=int(self.timeout))
            return

        embed = discord.Embed(title=activity_name)
        # embed.add_field(name='Description', value = f'{description}',inline=False)
        # embed.add_field(name='Target', value = f'{target}',inline=False)
        embed.description = f'**Host:** {ctx.author.mention} \n **Description:** {details} \n **Target:** {target}\n\n'
        await ctx.send(embed=embed)
        role = await guild.create_role(name=activity_name)

        # SQLITE3
        cursor.execute(
            f'INSERT into events(event_id, user_id, description, target) values(?, ?, ?, ?)',
            (role.id, ctx.author.id, details, target)
        )
        conn.commit()

        # JSON
        # self.events[activity_name] = {
        #     'role_id': role.id,
        #     'host_id': ctx.author.id,
        #     'description': details,
        #     'target': target
        # }
        # with open('db/_events.json', 'w') as f:
        #     json.dump(self.events,f)

        await self.update_description(guild, self.embed_id)
        await ctx.send(f'The event `{role.name}` was created with success')

    @commands.command(aliases=['del'])
    @commands.has_role(768529062159056977)
    async def del_activity(self, ctx, *, activity_name):
        role = discord.utils.get(ctx.guild.roles,name=activity_name)

        # SQLITE
        cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
        event = cursor.fetchall()
        if event[0][1] == ctx.author.id:
            await role.delete()
            cursor.execute('DELETE FROM events WHERE event_id = ?', (str(role.id),))
            conn.commit()
            await self.update_description(ctx.guild, self.embed_id)
            await ctx.send(f'The event `{role.name}` was delete with success')
        else:
            await ctx.send(f'You can only delete events you have created')

        # # JSON
        # if self.events[activity_name]['host_id'] == ctx.author.id:
        #     if activity_name in self.events:
        #         del self.events[activity_name]
        #         await role.delete()
        #     for k, v in self.events.items():
        #         print(k,v)
        #     await self.update_description(ctx.guild, self.embed_id)
        #     await ctx.send(f'The event `{role.name}` was delete with success')
        # else:
        #     await ctx.send(f'You can only delete events you have created')

    @commands.command(aliases=['emb'])
    @commands.has_role(768529062159056977)
    async def create_embed(self, ctx):
        embed = discord.Embed(title="LLK Events")
        events = cursor.execute('SELECT * FROM events').fetchall()
        description = ''

        # SQLITE3
        for e in events:
            event = ctx.guild.get_role(int(e[0]))
            host = ctx.guild.get_member(int(e[1]))
            # embed.add_field(name=f'Event: {event.name}', value = f'Description: Event hosted by {host.mention}')
            description += f'**Event:** {event.name} \n **Host:** {host.mention} \n **Description:** {e[2]}\n **Target:** {e[3]} \n\n'
            # # i++;

        # # JSON
        # for k, v in self.events.items():
        #     print(k,v)
        #     host = ctx.guild.get_member(v['host_id'])
        #     description += f"**Event:** {k} \n **Host:** {host.mention} \n **Description:** {v['description']}\n **Target:** {v['target']} \n\n"
        # self.data['eventEmbed']['id'] = self.embed_id
        # with open('db/_config.json', 'w') as f:
        #     json.dump(self.data,f)

        embed.description = description
        sent = await ctx.send(embed=embed)
        self.embed_id = sent.id
        self.data = {"eventEmbed":[{"id": self.embed_id}]};
        with open('db/embed_id.json', 'w') as f:
            json.dump(self.data,f)


    @commands.command(aliases=['addRole'])
    async def add_role(self, ctx, *, role):
        role = discord.utils.get(ctx.guild.roles,name=role)
        if role:
            cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
            event = cursor.fetchall()
            if event:
                await ctx.author.add_roles(role)
                await ctx.send(f'Role added')
            else:
                await ctx.send(f'You have no permission to add this role')
        else:
            await ctx.send(f'The given role doesn\'t exist')

    @commands.command(aliases=['removeRole'])
    async def remove_role(self, ctx, *, role):
        role = discord.utils.get(ctx.guild.roles,name=role)
        if role:
            cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
            event = cursor.fetchall()
            if event:
                await ctx.author.remove_roles(role)
                await ctx.send(f'Role removed')
            else:
                await ctx.send(f'You have no permission to remove this role')
        else:
            await ctx.send(f'The given role doesn\'t exist')

    async def update_description(ctx, guild, msgID):
        if not msgID:
            return;
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        description = ''
        for e in events:
            # print(f'{e}\n\n')
            event = guild.get_role(int(e[0]))
            host = guild.get_member(int(e[1]))
            # embed.add_field(name=f'Event: {event.name}', value = f'Description: Event hosted by {host.mention}'
            description += f'**Event:** {event.name} \n **Host:** {host.mention} \n **Description:** {e[2]}\n **Target:** {e[3]} \n\n'
            # i++;

        textChannel = discord.utils.get(guild.text_channels, name='bot')
        message = await textChannel.fetch_message(msgID)
        embed = message.embeds[0]
        embed.description = description
        await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
