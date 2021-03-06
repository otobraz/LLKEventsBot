import discord
from discord.ext import commands

import sqlite3
import json

import asyncio

from .utils import helper as h

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['add'])
    @commands.check_any(h.admin_check(), h.mod_check(), h.host_check())
    async def add_activity(self, ctx,*, activity_name):
        '''*Creates a new event. You will be prompted to inform a brief description of the event and proficiency level it is aimed at.*

        Example: `!add_activity Speaking Practice`'''
        guild = ctx.guild
        sent = await ctx.send('Briefly describe the event: ')
        try:
            message = await self.bot.wait_for(
                'message', timeout=180,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            if message:
                details = message.content
                await sent.delete()
                await message.delete()
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send('Cancelling request...', delete_after=3)
            return

        sent = await ctx.send('What\'s the target level: ')
        try:
            message = await self.bot.wait_for(
                'message', timeout=60,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            target = message.content
            await sent.delete()
            await message.delete()
        except asyncio.TimeoutError:
            await sent.delete()
            await ctx.send('Cancelling request...', delete_after=3)
            return

        # EVENT EMBED
        # embed = discord.Embed(title=activity_name)
        # # embed.add_field(name='Description', value = f'{description}',inline=False)
        # # embed.add_field(name='Target', value = f'{target}',inline=False)
        # embed.description = f'**Host:** {ctx.author.mention} \n **Description:** {details} \n **Target:** {target}\n\n'
        # await ctx.send(embed=embed)

        role = await guild.create_role(name=activity_name)

        # SQLITE3
        self.bot.cursor.execute(
            f'INSERT into events(event_id, user_id, description, target) values(?, ?, ?, ?)',
            (role.id, ctx.author.id, details, target)
        )
        self.bot.conn.commit()

        # JSON
        # self.events[activity_name] = {
        #     'role_id': role.id,
        #     'host_id': ctx.author.id,
        #     'description': details,
        #     'target': target
        # }
        # with open('db/_events.json', 'w') as f:
        #     json.dump(self.events, f, indent=4)

        await self.update_description(self, guild, self.bot.embed_id)
        await ctx.send(f'The event `{role.name}` was created with success')

    @commands.command(aliases=['del'])
    @commands.check_any(h.admin_check(), h.mod_check(), h.host_check())
    async def del_activity(self, ctx, *, activity_name):
        '''*Removes an event. You can only remove an event you have created.*

        Example: `!del_activity Speaking Practice`'''
        role = discord.utils.get(ctx.guild.roles,name=activity_name)

        # SQLITE
        self.bot.cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
        event = self.bot.cursor.fetchall()
        if event[0][1] == ctx.author.id:
            await role.delete()
            self.bot.cursor.execute('DELETE FROM events WHERE event_id = ?', (str(role.id),))
            self.bot.conn.commit()
            await self.update_description(self, ctx.guild, self.bot.embed_id)
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
    @commands.check_any(h.admin_check() or h.mod_check())
    async def create_embed(self, ctx, channel=None):
        '''*Posts embed with list of ongoing activities in the channel informed.*

        Example: `create_embed #channel`
        '''
        embed = h.red_embed(
            title='LLK Events',
            description=f'''
                *Use **{self.bot.command_prefix}nt<event_name>** to toggle whether you want to receive notifications pertaining to <event_name>.*\n
            '''
        )
        events = self.bot.cursor.execute('SELECT * FROM events').fetchall()

        # SQLITE3
        for e in events:
            event = ctx.guild.get_role(int(e[0]))
            host = ctx.guild.get_member(int(e[1]))
            # embed.add_field(name=f'Event: {event.name}', value = f'Description: Event hosted by {host.mention}')
            embed.description += f'{event.mention}({e[3]}) hosted by {host.mention} \n ```{e[2]}``` \n'
            # # i++;

        # # JSON
        # for k, v in self.events.items():
        #     print(k,v)
        #     host = ctx.guild.get_member(v['host_id'])
        #     description += f"**Event:** {k} \n **Host:** {host.mention} \n **Description:** {v['description']}\n **Target:** {v['target']} \n\n"
        # self.data['eventEmbed']['id'] = self.embed_id
        # with open('db/_config.json', 'w') as f:
        #     json.dump(self.data, f, indent=4)
        if channel:
            sent = await discord.utils.get(ctx.guild.text_channels,mention=channel).send(embed=embed)
        else:
            sent = await ctx.send(embed=embed)
        self.bot.embed_id = sent.id
        self.bot.embed_data = {"eventEmbed":{"id": self.bot.embed_id}}
        with open('db/embed_id.json', 'w') as f:
            json.dump(self.bot.embed_data, f, indent=4)

    @commands.command(aliases=['notifyme', 'notify', 'ntf', 'nt'], case_insensitive=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def notify_me(self, ctx, *, role):
        '''Toggles event role so members get notifications about the events

        Example: `notify_me Speaking Practice`
        '''
        role = discord.utils.get(ctx.guild.roles,name=role)
        self.bot.cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
        if self.bot.cursor.fetchall():
            try:
                if role in ctx.author.roles:
                    await ctx.author.remove_roles(role)
                    await ctx.send(f'{ctx.author.mention}, you won\'t get notifications about {role.name} anymore')
                else:
                    await ctx.author.add_roles(role)
                    await ctx.send(f'{ctx.author.mention}, you will get notifications about {role.name} from now on')
            except discord.errors.Forbidden:
                await ctx.send(embed = h.blue_embed(
                    'Oops...',
                    f'''
                        I have permission to `Manage Roles`, but it seems {role.mention} is above my highest role.
                    '''
                ))
        else:
            await ctx.send(f'The given event doesn\'t exist')

    async def update_description(self, ctx, guild, msgID):
        if not msgID:
            return
        message = await discord.utils.get(guild.text_channels, name='bot').fetch_message(msgID)
        embed = message.embeds[0]
        embed.description=f'''
            *Use **{self.bot.command_prefix}<event_name>** so you get notifications pertaining to <event_name>.*\n
        '''
        self.bot.cursor.execute('SELECT * FROM events')
        events = self.bot.cursor.fetchall()
        for e in events:
            # print(f'{e}\n\n')
            event = guild.get_role(int(e[0]))
            host = guild.get_member(int(e[1]))
            # embed.add_field(name=f'Event: {event.name}', value = f'Description: Event hosted by {host.mention}'
            embed.description += f'{event.mention}({e[3]}) hosted by {host.mention} \n ```{e[2]}``` \n'
            # i++;

        await message.edit(embed=embed)

    # @commands.command(aliases=['addrole'], case_insensitive=True)
    # async def add_role(self, ctx, *, role):
    #     role = discord.utils.get(ctx.guild.roles,name=role)
    #     if role:
    #         self.bot.cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
    #         event = self.bot.cursor.fetchall()
    #         if event:
    #             await ctx.author.add_roles(role)
    #             await ctx.send(f'Role added')
    #         # else:
    #         #     await ctx.send(f'You have no permission to add this role')
    #     else:
    #         await ctx.send(f'The given role doesn\'t exist')
    #
    # @commands.command(aliases=['removerole'])
    # async def remove_role(self, ctx, *, role):
    #     role = discord.utils.get(ctx.guild.roles,name=role)
    #     if role:
    #         self.bot.cursor.execute('SELECT * FROM events WHERE event_id = ?', (str(role.id),))
    #         event = self.bot.cursor.fetchall()
    #         if event:
    #             await ctx.author.remove_roles(role)
    #             await ctx.send(f'Role removed')
    #         # else:
    #         #     await ctx.send(f'You have no permission to remove this role')
    #     else:
    #         await ctx.send(f'The given role doesn\'t exist')

def setup(bot):
    bot.add_cog(Events(bot))
