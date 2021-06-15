import discord
from discord.ext import commands

from .utils import helper as h

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.command(aliases=['roll_dice'])
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        '''*Simulates rolling dice.*

        Example: roll 3 6'''
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))

    @commands.command(aliases=['hi'])
    async def hello(self, ctx, *, member: discord.Member = None):
        '*Says hello.*'
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar')
        self._last_member = member

    @commands.command()
    async def help(self, ctx, *, command=None):
        '''*Shows help information about the commands.*

        Example: `help` | `help <command>`
        '''
        if command:
            cmd = self.bot.get_command(command)
            embed = h.blue_embed(
                f'{self.bot.command_prefix}{cmd.name}',
                cmd.help
            )
            if cmd.aliases:
                footer = f'Aliases: {self.bot.command_prefix}{cmd.aliases[0]}'
                for i in range(1, len(cmd.aliases)):
                    footer += f', {self.bot.command_prefix}{cmd.aliases[i]}'
                embed.set_footer(text=footer)
            await ctx.send(embed=embed)
        else:
            commands = f'Help info for {self.bot.user.mention}. Use `{self.bot.command_prefix}help <command>` for specifc help.'
            for cog in self.bot.cogs:
                commands += f'\n\n**{cog}**\n|'
                for cmd in self.bot.get_cog(cog).get_commands():
                    commands += f' `{cmd.qualified_name}` |'
            await ctx.send(embed = h.red_embed(
                'Help Information',
                commands
            ))

def setup(bot):
    bot.add_cog(General(bot))
