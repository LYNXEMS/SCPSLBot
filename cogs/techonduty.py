import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import cooldown
from sys import argv

class TechOnDuty:
    """
    Przydziela role Tech Support/Assigns the Tech Support role
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(hidden=True, pass_context=True)
    async def onduty(self, ctx):
        """Daje ci range Tech Support/Gives you the Tech Support Rank"""
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if discord.utils.get(server.roles, name="Tech Support Off Duty") in author.roles:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="MTF Technical Support"))
            await asyncio.sleep(1)
            await self.bot.remove_roles(author, discord.utils.get(server.roles, name="Tech Support Off Duty"))
            await self.bot.send_message(author, "Human, you are on duty now.")
        elif discord.utils.get(server.roles, name="MTF Technical Support") in author.roles:
            await self.bot.send_message(author, "Human, but you're already on duty right now.")
        else:
            await self.bot.send_message(author, "Human, you don't have access to this command..")

    @commands.command(hidden=True, pass_context=True)
    async def offduty(self, ctx):
        """Zabiera ci range Tech Support/Takes away the Tech Support rank from you"""
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if discord.utils.get(server.roles, name="MTF Technical Support") in author.roles:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="Tech Support Off Duty"))
            await asyncio.sleep(1)
            await self.bot.remove_roles(author, discord.utils.get(server.roles, name="MTF Technical Support"))
            await self.bot.send_message(author, "Human, you are Tech Support Off Duty now.")
        elif discord.utils.get(server.roles, name="Tech Support Off Duty") in author.roles:
            await self.bot.send_message(author, "Human, you are Tech Support Off Duty already.")
        else:
            await self.bot.send_message(author, "Human, you don't have access to this command..")

def setup(bot):
    bot.add_cog(TechOnDuty(bot))
