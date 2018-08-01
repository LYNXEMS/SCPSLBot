from discord.ext import commands
import discord

class Patreon:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        server = before.server
        patroles = [discord.utils.get(message.server.roles, name="Patreon level - Facility Manager"), discord.utils.get(message.server.roles, name="Patreon level - Zone Manager"), discord.utils.get(message.server.roles, name="Patreon level - Major Scientist"), discord.utils.get(message.server.roles, name="Patreon level - Scientist"), discord.utils.get(message.server.roles, name="Patreon level - Janitor")]
        if len(list(set(after.roles).intersection(patroles))) > 0 and discord.utils.get(message.server.roles, name="Patreon Supporter") not in after.roles:
            await self.bot.add_roles(member, discord.utils.get(server.roles, name="Patreon Supporters"))
        elif len(list(set(after.roles).intersection(patroles))) == 0 and discord.utils.get(message.server.roles, name="Patreon Supporter") in after.roles:
            await self.bot.remove_roles(member, discord.utils.get(server.roles, name="Patreon Supporters"))
        else:
            return
            
def setup(bot):
    bot.add_cog(Patreon(bot))
