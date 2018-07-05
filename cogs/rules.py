import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from sys import argv

class Rules:
    """
    Discord rules!
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def simple_embed(self, text, title="", color=discord.Color.default()):
        embed = discord.Embed(title=title, color=color)
        embed.description = text
        await self.bot.say("", embed=embed)

    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def wazne(self):
        """Zasady."""
        await self.simple_embed("Kanał #main służy tylko do rozmów z obcokrajowcami. Nie wykorzystuj go do gadania z Polakami, od tego masz #glowny. Za nieprzestrzeganie tej zasady grozi permanentna blokada.", title="NAJWAŻNIEJSZA ZASADA")

    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def zakazy(self):
        """Zasady."""
        await self.simple_embed("DRUKUJĘ ZAKAZY...\n\n-Korzystania z botów bez zgody administracji (wpisywanie jakichkolwiek komend jest ściśle zakazane)\n"
                                    "-Obrażania innych, chyba że obie strony wiedzą, że jest to w formie żartu\n"
                                    "-Rozpoczynania bezcelowych kłótni i innych gównoburz\n"
                                    "-Reklamowania czegokolwiek bez zgody administracji (serwerów, kanałów, aukcji, CZEGOKOLWIEK!!!)\n"
                                    "-Podszywania się pod administrację (ban z miejsca, chyba osoba pod którą się podszywasz wyraża taką zgodę)\n"
                                    "-Spamowania (tekstowo i głosowo)\n"
                                    "-Proszenia o rangę\n"
                                    "-Tworzenia multikont\n"
                                    "-Oznaczania @Hubert Moszka na kanałach publicznych (bez sensownego powodu)", title="Na serwerze obowiązuje zakaz:")

    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def nakazy(self):
        """Zasady."""
        await self.simple_embed("DRUKUJĘ NAKAZY...\n\n-Wyrażaj się kulturalnie\n"
                                    "-Staraj się możliwie najbardziej uściślać wypowiedź w jednej wiadomości\n"
                                    "-Dbaj o jakość swojego mikrofonu, jeżeli wiesz że jest słaba, postaraj się wyciszać lub ustawić mówienie pod przyciskiem\n"
                                    "-Nick powinien posiadać litery (nie ustawiać samych emotek i liczb)", title="Nakazy")
									
    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def postanowienia(self):
        """Zasady."""
        await self.simple_embed("DRUKUJĘ POSTANOWIENIA...\n\n-Pisz zdania w formie jednej wiadomości. Nie rozdzielaj każdego słowa enterem w swoich wypowiedziach.\n"
                                    "-Jeżeli chcesz się pochwalić swoim dziełem to dodaj do niego odpowiednią licencję (warunki wykorzystywania), inaczej zezwalasz na wykorzystywanie go na warunkach CC-0 (domeny publicznej)\n"
                                    "-O wymiarze kary decyduje administracja (więcej w rodzaje kar)\n"
                                    "-Zastrzegamy sobie możliwość nałożenia kary nawet, gdy wykroczenie nie jest uściślone w powyższym regulaminie, jeżeli według nich użytkownik na to zasługuje.\n"
                                    "-Sprawdź #announcements aby brać udział w konkursach i dostawać odpowiednie serwerowe rangi", title="Ogólne postanowienia")


    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def prohibited(self):
        """Zasady."""
        await self.simple_embed("PRINTING LIST OF PROHIBITED THINGS...\n\n- Using bots without the consent of the administration (entering any commands is strictly prohibited\n"
                                    "- Insulting others, unless both sides know that this is in the form of a \n"
                                    "- Starting pointless disputes among other participants in the \n"
                                    "- Advertising anything without the consent of the administration (servers, channels, listings, ANYTHING \n"
                                    "- Impersonate administration (ban from the place, unless the person is impersonating under which expresses such consent)\n"
                                    "- Spaming on voice and text chat\n"
                                    "- Asking for a rank\n"
                                    "- Making multiaccounts\n"
                                    "- Marking @Hubert Moszka on public channels (without a good reason)", title="On this server is prohibited:")

    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def ordered(self):
        """Zasady."""
        await self.simple_embed("PRINTING LIST OF ORDERED THINGS\n\n- Express yourself culturally\n"
                                    "- Try to make the statement as precise as possible in one message\n"
                                    "- Take care of the quality of your microphone, if you know it is weak, try to mute or set push-to-speak option\n"
                                    "- Nick should have letters (do not set only emoticons and numbers)", title="It is ordered:")

    @commands.command(hidden=True)
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.channel)
    async def provisions(self):
        """Zasady."""
        await self.simple_embed("PRINTING LIST OF PROVISIONED THINGS\n\n- Write sentences in the form of one message. Try not to write many messages one under the other.\n"
                                    "- If you want to show off your work, add the appropriate license (usage conditions), otherwise you allow it to be used on CC-0 (public domain)\n"
                                    "- The size of the penalty is decided by the administration (more in types of penalties)\n"
                                    "- We reserve the right to impose a penalty even if the offense is not specified in the above regulations, if according to them, the user deserves it.\n"
                                    "- Check #announcements to participate in contests and get the right server rank", title="General provisions:")

def setup(bot):
    bot.add_cog(Rules(bot))
