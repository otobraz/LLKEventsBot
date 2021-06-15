import discord
from discord.ext import commands
import os


def is_admin(ctx):
    if ctx.channel.permissions_for(ctx.author).administrator:
        return True
    for adminRole in ctx.bot.perms['admins']:
        if discord.utils.get(ctx.author.roles, id=adminRole):
            return True
    return False

def admin_check():
    def predicate(ctx):
        return is_admin(ctx)
    return commands.check(predicate)

def is_mod(ctx):
    for modRole in ctx.bot.perms['mods']:
        if discord.utils.get(ctx.author.roles, id=modRole):
            return True
    return False

def mod_check():
    def predicate(ctx):
        return is_mod(ctx)
    return commands.check(predicate)

def is_host(ctx):
    for hostRole in ctx.bot.perms['hosts']:
        if discord.utils.get(ctx.author.roles, id=hostRole):
            return True
    return False

def host_check():
    def predicate(ctx):
        return is_host(ctx)
    return commands.check(predicate)

def blue_embed(title='', description=''):
    return discord.Embed(
        title = title,
        description = description,
        color=discord.Color(int('0047A0', 16))
    )

def red_embed(title='', description=''):
    return discord.Embed(
        title = title,
        description = description,
        color=discord.Color(int('CD2E3A', 16))
    )
