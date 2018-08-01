import discord


class Patreon:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        server = before.server
        patroles = [discord.utils.get(server.roles, name="Patreon level - Facility Manager"),
                    discord.utils.get(server.roles, name="Patreon level - Zone Manager"),
                    discord.utils.get(server.roles, name="Patreon level - Major Scientist"),
                    discord.utils.get(server.roles, name="Patreon level - Scientist"),
                    discord.utils.get(server.roles, name="Patreon level - Janitor")]
        if before.roles == after.roles:
            return
        elif len(list(set(after.roles).intersection(patroles))) > 0 and discord.utils.get(server.roles, name="Patreon Supporters") not in after.roles:
            await self.bot.add_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        elif len(list(set(after.roles).intersection(patroles))) == 0 and discord.utils.get(server.roles, name="Patreon Supporters") in after.roles:
            await self.bot.remove_roles(before, discord.utils.get(server.roles, name="Patreon Supporters"))
            return
        else:
            return


def setup(bot):
    bot.add_cog(Patreon(bot))
