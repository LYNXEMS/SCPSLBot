import discord


class Patreon:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        server = before.server
        if before.roles == after.roles:
            return
        if discord.utils.get(server.roles,
                             name="Patreon level - Facility Manager") in after.roles and discord.utils.get(server.roles,
                                                                                                           name="Patreon Supporters") not in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles, name="Patreon level - Zone Manager") in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") not in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles, name="Patreon level - Major Scientist") in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") not in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles, name="Patreon level - Scientist") in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") not in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles, name="Patreon level - Janitor") in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") not in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles,
                             name="Patreon level - Facility Manager") not in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles,
                             name="Patreon level - Zone Manager") not in after.roles and discord.utils.get(server.roles,
                                                                                                           name="Patreon Supporters") in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles,
                             name="Patreon level - Major Scientist") not in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles, name="Patreon level - Scientist") not in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        if discord.utils.get(server.roles, name="Patreon level - Janitor") not in after.roles and discord.utils.get(
                server.roles, name="Patreon Supporters") in after.roles:
            await asyncio.sleep(1)
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return


def setup(bot):
    bot.add_cog(Patreon(bot))
