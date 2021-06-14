import discord
from discord.ext import commands
from .utils import helper as h
import json

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Sets a role as an adminr role
    @commands.command(aliases=['setadminrole', 'sar'])
    async def set_admin_role(self, ctx, *, role):
        if (h.is_admin(ctx, self.bot) or h.is_mod(ctx, self.bot)):
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
        else:
            await ctx.send('You have no permission to use this command')

    # Sets a role as a mod role
    @commands.command(aliases=['setmodrole', 'smr'])
    async def set_mod_role(self, ctx, *, role):
        if (h.is_admin(ctx, self.bot) or h.is_mod(ctx, self.bot)):
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
        else:
            await ctx.send('You have no permission to use this command')

    # Sets a role as a host role
    @commands.command(aliases=['sethostrole', 'shr'])
    async def set_host_role(self, ctx, *, role):
        if (h.is_admin(ctx, self.bot) or h.is_mod(ctx, self.bot)):
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
        else:
            await ctx.send('You have no permission to use this command')

    # Unsets an admin role
    @commands.command(aliases=['unsetadminrole', 'unsetar'])
    async def unset_admin_role(self, ctx, *, role):
        if (h.is_admin(ctx, self.bot) or h.is_mod(ctx, self.bot)):
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
        else:
            await ctx.send('You have no permission to use this command')

    # Unsets a mod role
    @commands.command(aliases=['unsetmodrole', 'unsetmr'])
    async def unset_mod_role(self, ctx, *, role):
        if (h.is_admin(ctx, self.bot) or h.is_mod(ctx, self.bot)):
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
        else:
            await ctx.send('You have no permission to use this command')

    # Unsets a host role
    @commands.command(aliases=['unsethostrole', 'unsethr'])
    async def unset_host_role(self, ctx, *, role):
        if (h.is_admin(ctx, self.bot) or h.is_mod(ctx, self.bot)):
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
        else:
            await ctx.send('You have no permission to use this command')




def setup(bot):
    bot.add_cog(Moderation(bot))
