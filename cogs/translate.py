from googletrans import Translator
import discord
from discord.ext import commands
from sys import argv

# Instantiates a client
translator = Translator()

class Translate:
	def __init__(self, bot):
	    self.bot = bot
	    print('Addon "{}" loaded'.format(self.__class__.__name__))
	

	@commands.command()
	async def translate(ctx, *, arg):
		try:
			out = translator.translate(arg, src='en', dest='pl').text
			await ctx.bot.say("TRANSLATING...")
			await ctx.bot.say(out)
		except:
			await ctx.bot.say("Error while translating try remove emoji (Emoji support will be added soon)")

	@commands.command()
	async def tłumacz(ctx, *, arg):
		try:
			out = translator.translate(arg, src='pl', dest='en').text
			await ctx.bot.say("TŁUMACZĘ...")
			await ctx.bot.say(out)
		except:
			await ctx.bot.say("Problem z tłumaczeniem spróbuj usunąć emoji (Wsparcie dla emoji zostanie wkrótce dodane)")
		

def setup(bot):
	bot.add_cog(Translate(bot))