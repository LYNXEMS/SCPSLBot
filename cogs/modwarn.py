import discord
import json
import time
from discord.ext import commands
from sys import argv
import asyncio

class ModWarn:
    """
    Warn commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))
		
    async def on_message(self, message):

        if len(message.content) < 2 or message.channel.is_private:
            return
        if discord.utils.get(message.server.members, id='242306234269696000') not in message.mentions:
            return
        server = message.server
        channel = message.channel
        logchannel = discord.utils.get(server.channels, name="warnings")
        try:
            member = message.author
        except IndexError:
            return
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if len(member.roles) != 1:
            return
        if member.id not in warns:
            warns[member.id] = {"warns": []}
        await self.bot.add_roles(member, discord.utils.get(message.server.roles, name="WARNED"))
        warns[member.id]["name"] = member.name + "#" + member.discriminator
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        warns[member.id]["warns"].append({"issuer_id": "BOT", "issuer_name": "BOT", "reason": "PINGING HUBIE", "timestamp": timestamp})
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        msg = "You have benn issued a warn {}.".format(server.name)
        reason = "Pinging Hubert"
        msg += " The reason is: " + reason
        msg += "\n\nPlease read the rules. This is warning number {}.".format(len(warns[member.id]["warns"]))
        warn_count = len(warns[member.id]["warns"])
        if warn_count == 1:
            msg += " __Human, the next warning will kick you automatically.__"
        if warn_count == 2:
            msg += "\n\nHuman, you have been kicked, one more warning and you will get Class D Personel."
        if warn_count >= 3:
            msg += "\n\nHuman, you have gotten 3 warnings. You've been assigned as a Class D Personel now."
        try:
            await self.bot.send_message(member, msg)
        except discord.errors.Forbidden:
            pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
        if warn_count == 2:
            await self.bot.kick(member)
        if warn_count >= 3:
            role = discord.utils.get(message.server.roles, name="Class D - Muted")
            await self.bot.add_roles(member, role)
        await self.bot.send_message(channel, "A human, {} warned for pinging Hubie with {} warns total now".format(member.mention, len(warns[member.id]["warns"])))
        msg = "⚠️ **Warn**:{} was warned for Pinging Hubert with his/her warn total now being {} | {}#{}".format(member.mention, len(warns[member.id]["warns"]), member.name, member.discriminator)
        await self.bot.send_message(logchannel, msg)
        await asyncio.sleep(5)
        await self.bot.remove_roles(member, discord.utils.get(message.server.roles, name="WARNED"))


    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def warn(self, ctx, user, *, reason=""):
        """Warn a user."""
        server = ctx.message.server
        issuer = ctx.message.author
        logchannel = discord.utils.get(server.channels, name="warnings")
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("Please tag an user.")
            return
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if discord.utils.get(ctx.message.server.roles, name="Discord Mod - MTF Nine Tailed Fox") in member.roles or discord.utils.get(ctx.message.server.roles, name="The O5 Council") in member.roles or discord.utils.get(ctx.message.server.roles, name="Admin - MTF Red Right Hand") in member.roles:
            await self.bot.say("PREVENTING STAFF WARNING!")
            return
        if member.id not in warns:
            warns[member.id] = {"warns": []}
        if discord.utils.get(ctx.message.server.roles, name="WARNED") in member.roles:
            await self.bot.say("PREVENTING MULTI WARNING!")
            return
        await self.bot.add_roles(member, discord.utils.get(ctx.message.server.roles, name="WARNED"))
        warns[member.id]["name"] = member.name + "#" + member.discriminator
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        warns[member.id]["warns"].append({"issuer_id": issuer.id, "issuer_name": issuer.name, "reason": reason, "timestamp": timestamp})
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        msg = "You have benn issued a warn {}.".format(server.name)
        if reason != "":
            # much \n
            msg += " The reason is: " + reason
        msg += "\n\nPlease read the rules. This is warning number {}.".format(len(warns[member.id]["warns"]))
        warn_count = len(warns[member.id]["warns"])
        if warn_count == 1:
            msg += " __Human, the next warning will kick you automatically.__"
        if warn_count == 2:
            msg += "\n\nHuman, you have been kicked, one more warning and you will get Class D Personel."
        if warn_count >= 3:
            msg += "\n\nHuman, you have gotten 3 warnings. You've been assigned as a Class D Personel now."
        try:
            await self.bot.send_message(member, msg)
        except discord.errors.Forbidden:
            pass  # don't fail in case user has DMs disabled for this server, or blocked the bot
        if warn_count == 2:
            await self.bot.kick(member)
        if warn_count >= 3:
            role = discord.utils.get(ctx.message.server.roles, name="Class D - Muted")
            await self.bot.add_roles(member, role)
        await self.bot.say("A human, {} warned with {} warns total now".format(member.mention, len(warns[member.id]["warns"])))
        msg = "⚠️ **Warn**: {} warned {} with his/her warn total now being {} | {}#{}".format(issuer.mention, member.mention, len(warns[member.id]["warns"]), member.name, member.discriminator)
        if reason != "":
            # much \n
            msg += "\n✏️ __Reason__: " + reason
        await self.bot.send_message(logchannel, msg + ("\nPlease try to add a reason next, human." if reason == "" else ""))
        await asyncio.sleep(5)
        await self.bot.remove_roles(member, discord.utils.get(ctx.message.server.roles, name="WARNED"))

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def listwarns(self, ctx, user):
        """List warns for a user. Staff only."""
        server = ctx.message.server
        issuer = ctx.message.author
        logchannel = discord.utils.get(server.channels, name="warnings")
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("ERROR, user not tagged.")
            return
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.set_author(name="Warns for {}#{}".format(member.display_name, member.discriminator), icon_url=member.avatar_url)
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        try:
            if len(warns[member.id]["warns"]) == 0:
                embed.description = "None!"
                embed.color = discord.Color.green()
            else:
                for idx, warn in enumerate(warns[member.id]["warns"]):
                    value = ""
                    value += "Reason: " + warn["reason"] + " "
                    # embed.add_field(name="{}: {}".format(key + 1, warn["timestamp"]), value="Issuer: {}\nReason: {}".format(warn["issuer_name"], warn["reason"]))
                    embed.add_field(name="{}: {}".format(idx + 1, warn["timestamp"]), value=value)
        except KeyError:  # if the user is not in the file
            embed.description = "None!"
            embed.color = discord.Color.green()
        await self.bot.say("", embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def listwarnsid(self, ctx, user_id):
        """List warns for a user based on ID. Staff only."""
        server = ctx.message.server
        issuer = ctx.message.author
        logchannel = discord.utils.get(server.channels, name="warnings")
        embed = discord.Embed(color=discord.Color.dark_red())
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        # crappy workaround given how dicts are not ordered
        try:
            embed.set_author(name="Warns for {}".format(warns[user_id]["name"]))
            if len(warns[user_id]["warns"]) == 0:
                embed.description = "None!"
                embed.color = discord.Color.green()
            else:
                for idx, warn in enumerate(warns[user_id]["warns"]):
                    value = ""
                    value += "Reason: " + warn["reason"] + " "
                    # embed.add_field(name="{}: {}".format(key + 1, warn["timestamp"]), value="Issuer: {}\nReason: {}".format(warn["issuer_name"], warn["reason"]))
                    embed.add_field(name="{}: {}".format(idx + 1, warn["timestamp"]), value=value)
        except KeyError:  # if the user is not in the file
            embed.set_author(name="Warns for {}".format(user_id))
            embed.description = "This ID has no registered warns."
            embed.color = discord.Color.green()
        await self.bot.say("", embed=embed)

    @commands.has_permissions(manage_server=True)
    @commands.command(pass_context=True)
    async def copywarns_id2id(self, ctx, user_id1, user_id2):
        """Copy warns from one user ID to another. Overwrites all warns of the target user ID. Staff only."""
        server = ctx.message.server
        logchannel = discord.utils.get(server.channels, name="warnings")
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if user_id1 not in warns:
            await self.bot.say("{} doesn't exist in saved warnings.".format(user_id1))
            return
        warn_count = len(warns[user_id1]["warns"])
        if warn_count == 0:
            await self.bot.say("{} has no warns!".format(warns[user_id1]["name"]))
            return
        warns1 = warns[user_id1]
        if user_id2 not in warns:
            warns[user_id2] = []
        warns2 = warns[user_id2]
        if "name" not in warns2:
            orig_name = ""
            warns2["name"] = "(copied from {})".format(warns1["name"])
        else:
            orig_name = warns2["name"]
            warns2["name"] = "{} (copied from {})".format(warns2["name"], warns1["name"])
        warns2["warns"] = warns1["warns"]
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        await self.bot.say("Human, {} warns were copied from {} to {}!".format(warn_count, user_id1, user_id2))
        msg = "📎 **Copied warns**: {} copied {} warns from {} ({}) to ".format(ctx.message.author.mention, warn_count, warns1["name"], user_id1)
        if orig_name:
            msg += "{} ({})".format(warns2["name"], user_id2)
        else:
            msg += user_id2
        await self.bot.send_message(logchannel, msg)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def delwarn(self, ctx, user, idx: int):
        """Remove a specific warn from a user. Staff only."""
        server = ctx.message.server
        logchannel = discord.utils.get(server.channels, name="warnings")
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("ERROR, user not tagged.")
            return
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if member.id not in warns:
            await self.bot.say("{} has no warns!".format(member.mention))
            return
        warn_count = len(warns[member.id]["warns"])
        if warn_count == 0:
            await self.bot.say("{} has no warns!".format(member.mention))
            return
        if idx > warn_count:
            await self.bot.say("Human, warn index higher than their number - ({})!".format(warn_count))
            return
        if idx < 1:
            await self.bot.say("LESS THAN 1? REALLY HUMAN?!")
            return
        warn = warns[member.id]["warns"][idx - 1]
        embed = discord.Embed(color=discord.Color.dark_red(), title="Warn {} on {}".format(idx, warn["timestamp"]),
                              description="Issuer: {0[issuer_name]}\nReason: {0[reason]}".format(warn))
        del warns[member.id]["warns"][idx - 1]
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        await self.bot.say("Human, one warn has been deleted from {}!".format(member.mention))
        if warn_count == 3:
            await self.bot.say("Removing Class D status if existed!")
            await self.bot.remove_roles(member, discord.utils.get(ctx.message.server.roles, name="Class D - Muted"))
        msg = "🗑 **Warn removed**: {} deleted a warn issued by {} from {} | {}#{}".format(ctx.message.author.mention, idx, member.mention, member.name, member.discriminator)
        await self.bot.send_message(logchannel, msg, embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def delwarnid(self, ctx, user_id, idx: int):
        """Remove a specific warn from a user based on ID. Staff only."""
        server = ctx.message.server
        logchannel = discord.utils.get(server.channels, name="warnings")
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if user_id not in warns:
            await self.bot.say("Human, {} doesn't exist in saved warnings.".format(user_id))
            return
        warn_count = len(warns[user_id]["warns"])
        if warn_count == 0:
            await self.bot.say("Human, {} has no warns!".format(warns[user_id]["name"]))
            return
        if idx > warn_count:
            await self.bot.say("Human, warn index is higher than warn count ({})!".format(warn_count))
            return
        if idx < 1:
            await self.bot.say("LESS THAN 1? REALLY HUMAN?!")
            return
        warn = warns[user_id]["warns"][idx - 1]
        embed = discord.Embed(color=discord.Color.dark_red(), title="Warn {} on {}".format(idx, warn["timestamp"]),
                              description="Issuer: {0[issuer_name]}\nReason: {0[reason]}".format(warn))
        del warns[user_id]["warns"][idx - 1]
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        await self.bot.say("Human, one warn has been deleted from {}".format(warns[user_id]["name"]))
        msg = "🗑 **Deleted warn**: {} removed warn {} from {} ({})".format(ctx.message.author.mention, idx, warns[user_id]["name"], user_id)
        await self.bot.send_message(logchannel, msg, embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def clearwarns(self, ctx, user):
        """Clear all warns for a user. Staff only."""
        server = ctx.message.server
        logchannel = discord.utils.get(server.channels, name="warnings")
        try:
            member = ctx.message.mentions[0]
        except IndexError:
            await self.bot.say("ERROR, user not tagged.")
            return
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if member.id not in warns:
            await self.bot.say("Human, {} has no warns!".format(member.mention))
            return
        warn_count = len(warns[member.id]["warns"])
        if warn_count == 0:
            await self.bot.say("Human, {} has no warns!".format(member.mention))
            return
        warns[member.id]["warns"] = []
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        await self.bot.say("Human, {} no longer has any warns!".format(member.mention))
        if warn_count >= 3:
            await self.bot.say("Removing Class D status if existed!")
            await self.bot.remove_roles(member, discord.utils.get(ctx.message.server.roles, name="Class D - Muted"))
        msg = "🗑 **Cleared warns**: {} cleared {} warns from {} | {}#{}".format(ctx.message.author.mention, warn_count, member.mention, member.name, member.discriminator)
        await self.bot.send_message(logchannel, msg)

    @commands.has_permissions(kick_members=True)
    @commands.command(pass_context=True)
    async def clearwarnsid(self, ctx, user_id):
        """Clear all warns for a user based on ID. Staff only."""
        server = ctx.message.server
        logchannel = discord.utils.get(server.channels, name="warnings")
        with open("data/warnsv2.json", "r") as f:
            warns = json.load(f)
        if user_id not in warns:
            await self.bot.say("Human, {} doesn't exist in saved warnings.".format(user_id))
            return
        warn_count = len(warns[user_id]["warns"])
        if warn_count == 0:
            await self.bot.say("Human, {} has no warns!".format(warns[user_id]["name"]))
            return
        warns[user_id]["warns"] = []
        with open("data/warnsv2.json", "w") as f:
            json.dump(warns, f)
        await self.bot.say("Human, {} no longer has any warns!".format(warns[user_id]["name"]))
        msg = "🗑 **Cleared warns**: {} cleared {} warns from {} ({})".format(ctx.message.author.mention, warn_count, warns[user_id]["name"], user_id)
        await self.bot.send_message(logchannel, msg)

chars = "\\`*_<>#@:~"
def escape_name(name):
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\u200b")  # prevent mentions

def setup(bot):
    bot.add_cog(ModWarn(bot))
