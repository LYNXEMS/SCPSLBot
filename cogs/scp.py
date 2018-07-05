import discord
from discord.ext import commands

class SCP:
    """Look up SCP articles. Warning: Some of them may be too creepy or gruesome."""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def scp(self, num : int):
        """Look up SCP articles. Warning: Some of them may be too creepy or gruesome. Reminder: You must specify a number between 1 and 3999."""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        if (num > 0 and num <= 3999):
            url = "http://www.scp-wiki.net/scp-{:03}".format(num)
            msg = "Click the link to access requested content.\n\nSCP-{}".format(num)
            c = discord.Color.green()
            title = "[DECRYPTED DATA]"
            footer = "079OS v1.42"
            thumb = "https://i.imgur.com/lkRcAxN.jpg"
            em = discord.Embed(description=msg, title=title, url=url, color=c)
            em.set_thumbnail(url=thumb)
            em.set_footer(text=footer)
        else:
            msg = "ERROR. SCP NOT FOUND."
            c = discord.Color.red()
            em = discord.Embed(description=msg, color=c)
            
        await self.bot.say(embed=em)

    @commands.command()
    async def scpj(self, joke : str):
        """Look up SCP-Js. Reminder: Enter the correct name or else the resultant page will be invalid. (Use 001, etc. in case of numbers less than 100.)"""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        msg = "Click the link to access requested content.\n\nSCP-{}-J".format(joke)
        url = "http://www.scp-wiki.net/scp-{}-j".format(joke)
        thumb = "https://i.imgur.com/lkRcAxN.jpg"
        title = "[DECRYPTED DATA]"
        footer = "079OS v1.42"
        em = discord.Embed(description=msg, title=title, url=url, color=discord.Color.green())
        em.set_thumbnail(url=thumb)
        em.set_footer(text=footer)
        await self.bot.say(embed=em)

    @commands.command()
    async def scparc(self, num : int):
        """Look up SCP archives. Warning: Some of them may be too creepy or gruesome. Reminder: You must specify a valid archive number. (13, 48, 51, 89, 91, 112, 132, 138, 157, 186, 232, 234, 244, 252, 257, 338, 356, 361, 400, 406, 503, 515, 517, 578, 728, 744, 776, 784, 837, 922, 987, 1023)"""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        if num in (13, 48, 51, 89, 91, 112, 132, 138, 157, 186, 232, 234, 244, 252, 257, 338, 356, 361, 400, 406, 503, 515, 517, 578, 728, 744, 776, 784, 837, 922, 987, 1023):
            url = "http://www.scp-wiki.net/scp-{:03}-arc".format(num)
            c = discord.Color.green()
            msg = "Click the link to access requested content.\n\nSCP-{}-ARC".format(num)
            title = "[DECRYPTED DATA]"
            footer = "079OS v1.42"
            thumb = "https://i.imgur.com/lkRcAxN.jpg"
            em = discord.Embed(description=msg, title=title, url=url, color=c)
            em.set_thumbnail(url=thumb)
            em.set_footer(text=footer)
        else:
            msg = "ERROR. No archive found."
            c = discord.Color.red()
            em = discord.Embed(description=msg, color=c)

        await self.bot.say(embed=em)

    @commands.command()
    async def scpex(self, num : int):
        """Look up explained SCP articles. Warning: Some of them may be too creepy or gruesome. Reminder: You must specify a valid archive number. (711, 920, 1841, 1851, 1974, 2600, 4023, 8900)"""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        if num in (711, 920, 1841, 1851, 1974, 2600, 4023, 8900):
            url = "http://www.scp-wiki.net/scp-{:03}-ex".format(num)
            c = discord.Color.green()
            msg = "Click the link to access requested content.\n\nSCP-{}-EX".format(num)
            title = "[DECRYPTED DATA]"
            footer = "079OS v1.42"
            thumb = "https://i.imgur.com/lkRcAxN.jpg"
            em = discord.Embed(description=msg, title=title, url=url, color=c)
            em.set_thumbnail(url=thumb)
            em.set_footer(text=footer)
        else:
            msg = "ERROR. Explained SCP not found."
            c = discord.Color.red()
            em = discord.Embed(description=msg, color=c)


        await self.bot.say(embed=em)

    @commands.command()
    async def anomalousitems(self):
        """Look through the log of anomalous items."""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        url = "http://www.scp-wiki.net/log-of-anomalous-items"
        c = discord.Color.green()
        msg = "Click the link to access requested content.\n\nAnomalous Items".format(num)
        title = "[DECRYPTED DATA]"
        footer = "079OS v1.42"
        thumb = "https://i.imgur.com/lkRcAxN.jpg"
        em = discord.Embed(description=msg, title=title, url=url, color=c)
        em.set_thumbnail(url=thumb)
        em.set_footer(text=footer)
        await self.bot.say(embed=em)

    @commands.command()
    async def extranormalevents(self):
        """Look through the log of extranormal events."""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        url = "http://www.scp-wiki.net/log-of-extranormal-events"
        em = discord.Embed(description=msg, color=discord.Color.green())
        c = discord.Color.green()
        msg = "Click the link to access requested content.\n\nExtranormal Events".format(num)
        title = "[DECRYPTED DATA]"
        footer = "079OS v1.42"
        thumb = "https://i.imgur.com/lkRcAxN.jpg"
        em = discord.Embed(description=msg, title=title, url=url, color=c)
        em.set_thumbnail(url=thumb)
        em.set_footer(text=footer)
        await self.bot.say(embed=em)

    @commands.command()
    async def unexplainedlocations(self):
        """Look through the log of unexplained locations."""

        await self.bot.say("Hacking access to foundation Archives... SUCCESS")
        url = "http://www.scp-wiki.net/log-of-unexplained-locations"
        c = discord.Color.green()
        msg = "Click the link to access requested content.\n\nUnexplained Locations".format(num)
        title = "[DECRYPTED DATA]"
        footer = "079OS v1.42"
        thumb = "https://i.imgur.com/lkRcAxN.jpg"
        em = discord.Embed(description=msg, title=title, url=url, color=c)
        em.set_thumbnail(url=thumb)
        em.set_footer(text=footer)
        await self.bot.say(embed=em)


def setup(bot):
    bot.add_cog(SCP(bot))
