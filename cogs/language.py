import discord
from discord.ext import commands
from sys import argv
import asyncio

class Language:
    """
    CHOOSE YOUR FIGHTER
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.command(pass_context=True)
    async def pl(self, ctx):
        """Join the Polish section"""
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if discord.utils.get(server.roles, name="PL") in author.roles:
            await self.bot.send_message(author, "Masz juz dostep do tej sekcji.")
        else:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="PL"))
            await self.bot.send_message(author, "Dostep do sekcji Polskiej przyznany.")
		
    @commands.command(pass_context=True)
    async def int(self, ctx):
        """Join the International section"""
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if discord.utils.get(server.roles, name="INT") in author.roles:
            await self.bot.send_message(author, "You already have access to this section.")
        else:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="INT"))
            await self.bot.send_message(author, "Access to the International section granted.")

    @commands.command(pass_context=True)
    async def both(self, ctx):
        """Join both Polish and Internation sections"""
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        if discord.utils.get(server.roles, name="INT") in author.roles and discord.utils.get(server.roles, name="PL") in author.roles:
            await self.bot.send_message(author, "You already have access to these sections.")
        elif discord.utils.get(server.roles, name="INT") in author.roles and discord.utils.get(server.roles, name="PL") not in author.roles:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="PL"))
            await self.bot.send_message(author, "Access to the Polish section granted.")
        elif discord.utils.get(server.roles, name="INT") not in author.roles and discord.utils.get(server.roles, name="PL") in author.roles:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="INT"))
            await self.bot.send_message(author, "Access to the International section granted.")
        else:
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="INT"))
            await asyncio.sleep(1)
            await self.bot.add_roles(author, discord.utils.get(server.roles, name="PL"))
            await self.bot.send_message(author, "Access to Polish and International sections granted.")
			
    @commands.command(pass_context=True)
    async def clear(self, ctx):
        """Clear your joined sections"""
        server = ctx.message.server
        author = ctx.message.author
        await self.bot.delete_message(ctx.message)
        await self.bot.remove_roles(author, discord.utils.get(server.roles, name="PL"))
        await asyncio.sleep(1)
        await self.bot.remove_roles(author, discord.utils.get(server.roles, name="INT"))
        await self.bot.send_message(author, "Access to Polish and International sections revoked.")
			
    async def on_message(self, message):
        if message.channel.is_private:
            return
        if message.channel.name != "select-your-language":
            return   
        if message.content == "!pl" or message.content == "!int" or message.content == "!both":
            pass
        else:
            await self.bot.delete_message(message)

# Load the extension
def setup(bot):
    bot.add_cog(Language(bot))
