import discord
from discord.ext import commands
import os

def is_admin(ctx, bot):
    if ctx.channel.permissions_for(ctx.author).administrator:
        return True
    for adminRole in bot.perms['admins']:
        if discord.utils.get(ctx.author.roles, id=adminRole):
            return True
    return False

def is_mod(ctx, bot):
    for modRole in bot.perms['mods']:
        if discord.utils.get(ctx.author.roles, id=modRole):
            return True
    return False

def is_host(ctx, bot):
    for hostRole in bot.perms['hosts']:
        if discord.utils.get(ctx.author.roles, id=hostRole):
            return True
    return False
