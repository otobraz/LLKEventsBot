import discord
from discord.ext import commands
from .utils import helper as h
import json

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Sets a role as an admin role
    @commands.command(aliases=['setadminrole', 'sar'])
    @commands.check_any(h.admin_check())
    async def set_admin_role(self, ctx, *, role):
        '''*Sets an existing role as an admin role*.

        Example: `set_admin_role Admin`'''
        try:
            aRole = discord.utils.get(ctx.guild.roles,id=int(role))
        except:
            aRole = discord.utils.get(ctx.guild.roles,name=role)
        if aRole:
            if aRole.id not in self.bot.perms_data['permissions']['admins']:
                self.bot.perms_data['permissions']['admins'].append(aRole.id)
                self.bot.perms = self.bot.perms_data
                with open('db/roles.json', 'w') as f:
                    json.dump(self.bot.perms_data, f, indent=4)
                    await ctx.send(f'{aRole.name} has been set as an admin role')
            else:
                await ctx.send(f'{aRole.name} is already an admin role')

    # Sets a role as a mod role
    @commands.command(aliases=['setmodrole', 'smr'])
    @commands.check_any(h.admin_check(), h.mod_check())
    async def set_mod_role(self, ctx, *, role):
        '''*Sets an existing role as a mod role*.

        Example: `set_mod_role Moderator`'''
        try:
            mRole = discord.utils.get(ctx.guild.roles,id=int(role))
        except:
            mRole = discord.utils.get(ctx.guild.roles,name=role)
        if mRole:
            if mRole.id not in self.bot.perms_data['permissions']['mods']:
                self.bot.perms_data['permissions']['mods'].append(mRole.id)
                self.bot.perms = self.bot.perms_data
                with open('db/roles.json', 'w') as f:
                    json.dump(self.bot.perms_data, f, indent=4)
                    await ctx.send(f'{mRole.name} has been set as a mod role')
            else:
                await ctx.send(f'{mRole.name} is already a mod role')

    # Sets a role as a host role
    @commands.command(aliases=['sethostrole', 'shr'])
    @commands.check_any(h.admin_check(), h.mod_check())
    async def set_host_role(self, ctx, *, role):
        '''*Sets an existing role as a host role.*

        Example: `set_host_role Activity Host`'''
        try:
            hRole = discord.utils.get(ctx.guild.roles,id=int(role))
        except:
            hRole = discord.utils.get(ctx.guild.roles,name=role)
        if hRole:
            if hRole.id not in self.bot.perms_data['permissions']['hosts']:
                self.bot.perms_data['permissions']['hosts'].append(hRole.id)
                self.bot.perms = self.bot.perms_data
                with open('db/roles.json', 'w') as f:
                    json.dump(self.bot.perms_data, f, indent=4)
                    await ctx.send(f'{hRole.name} has been set as a host role')
            else:
                await ctx.send(f'{hRole.name} is already a host role')

    # Unsets an admin role
    @commands.command(aliases=['unsetadminrole', 'unsetar'])
    @commands.check_any(h.admin_check())
    async def unset_admin_role(self, ctx, *, role):
        '''*Unsets an existing admin role.*

        Example: `unset_admin_role Admin`'''
        try:
            aRole = discord.utils.get(ctx.guild.roles,id=int(role))
        except:
            aRole = discord.utils.get(ctx.guild.roles,name=role)
        if aRole:
            if aRole.id in self.bot.perms_data['permissions']['admins']:
                self.bot.perms_data['permissions']['admins'].remove(aRole.id)
                self.bot.perms = self.bot.perms_data
                with open('db/roles.json', 'w') as f:
                    json.dump(self.bot.perms_data, f, indent=4)
                    await ctx.send(f'{aRole.name} has been unset as an admin role')
            else:
                await ctx.send(f'{aRole.name} is not an admin role')

    # Unsets a mod role
    @commands.command(aliases=['unsetmodrole', 'unsetmr'])
    @commands.check_any(h.admin_check(), h.mod_check())
    async def unset_mod_role(self, ctx, *, role):
        '''*Unsets an existing mod role.*

        Example: `unset_mod_role Moderator`'''
        try:
            mRole = discord.utils.get(ctx.guild.roles,id=int(role))
        except:
            mRole = discord.utils.get(ctx.guild.roles,name=role)
        if mRole:
            if mRole.id in self.bot.perms_data['permissions']['mods']:
                self.bot.perms_data['permissions']['mods'].remove(mRole.id)
                self.bot.perms = self.bot.perms_data
                with open('db/roles.json', 'w') as f:
                    json.dump(self.bot.perms_data, f, indent=4)
                    await ctx.send(f'{mRole.name} has been unset as a mod role')
            else:
                await ctx.send(f'{mRole.name} is not a mod role')

    # Unsets a host role
    @commands.command(aliases=['unsethostrole', 'unsethr'])
    @commands.check_any(h.admin_check(), h.mod_check())
    async def unset_host_role(self, ctx, *, role):
        '''*Unsets an existing host role.*

        Example: `unset_host_role Activity Host`'''
        try:
            hRole = discord.utils.get(ctx.guild.roles,id=int(role))
        except:
            hRole = discord.utils.get(ctx.guild.roles,name=role)
        if hRole:
            if hRole.id in self.bot.perms_data['permissions']['hosts']:
                self.bot.perms_data['permissions']['hosts'].remove(hRole.id)
                self.bot.perms = self.bot.perms_data
                with open('db/roles.json', 'w') as f:
                    json.dump(self.bot.perms_data, f, indent=4)
                    await ctx.send(f'{hRole.name} has been unset as a host role')
            else:
                await ctx.send(f'{hRole.name} is not a host role')

def setup(bot):
    bot.add_cog(Moderation(bot))
