import discord
from discord.ext import commands
import re
from sys import argv


class serverlist:
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def on_message(self, message):
        server = message.server
        channel = message.channel
        content = message.content
        author = message.author
        lang = 0
        if channel == discord.utils.get(server.channels, name='serwery'):
            lang = 1
        if can_baypss(message):
            return
        if lang > 0:
            if verify_server_message(message):
                if len(content) > 320:
                    await self.bot.delete_message(message)
                    if lang == 1:
                        await self.bot.send_message(author,  ":x: Człowieku, twoja wiadomość została skasowana z listy serwerów, ponieważ była dłuższa niż 320 znaków.")
                    else:
                        await self.bot.send_message(author, ":x: Human, your message has been deleted from server list, because messages there cannot be longer than 320 characters.")
                else:
                    content = content.replace("https://discord.gg/", "")
                    if "http://" in content or "https://" in content:
                        await self.bot.delete_message(message)
                        if lang == 1:
                            await self.bot.send_message(author,  ":x: Człowieku, twoja wiadomość została skasowana z listy serwerów, ponieważ wiadomości na liście serwerów nie mogą zawierać linków (z wyjątkiem zaproszeń na discorda).")
                        else:
                            await self.bot.send_message(author, ":x: Human, your message has been deleted from server list, because messages there mustn't contain links (excluding discord invites).")
            else:
                await self.bot.delete_message(message)
                if lang == 1:
                    await self.bot.send_message(author, ":x: Człowieku, twoja wiadomość została skasowana z listy serwerów, ponieważ wiadomości na liście serwerów muszą zawierać poprawny adres IP lub nazwę domenową.")
                else:
                    await self.bot.send_message(author, ":x: Human, your message has been deleted from server list, because messages there must contain valid IP address or domain name.")

    async def on_message_edit(self, before, after):
        server = before.server
        channel = before.channel
        content = after.content
        author = before.author
        message = before
        if channel == discord.utils.get(server.channels, name='serwery') or channel == discord.utils.get(
                server.channels, name='serwery-weryfikacje'):
            lang = 1
        if channel == discord.utils.get(server.channels, name='nicku-servers'):
            lang = 2
        if can_baypss(message):
            return
        if lang > 0:
            if verify_server_message(after):
                return
            else:
                await self.bot.delete_message(after)
                if lang == 1:
                    await self.bot.send_message(author, ":x: Człowieku, twoja zmodyfikowana wiadomość przestała spełniac wymagania na kanale #serwery. Nie próbowałeś przypadkiem obejść filtru?")
                else:
                    await self.bot.send_message(author, ":x: Humen, your modified message doesn't meet the requirements on #servers channel. Weren't you trying to bypass the filter?")


def setup(bot):
    bot.add_cog(serverlist(bot))

def can_baypss(msg):
    return msg.channel.permissions_for(msg.author).manage_messages

def verify_server_message(message):
    pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}|(^|\ |\.)[a-zA-Z0-9]+\.[a-zA-Z]{1,3}|[0-9a-f]{0,4}(:[0-9a-f]{0,4}){1,7}:[0-9a-f]{0,4}', re.M)
    if pattern.search(message.content):
        return True
    else:
        return False
