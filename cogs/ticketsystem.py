import discord
from discord.ext import commands
import json
import os

class ticketSystem:
	def __init__(self, bot):
		self.bot = bot


	if not os.path.exists("data/tickets.json"):
		with open("data/tickets.json", mode='w') as f:
			json.dump({}, f)
	
	if not os.path.exists("data/techsupportstats.json"):
		with open("data/techsupportstats", mode='w') as f:
			json.dump({}, f)

	if not os.path.exists("data/claimedticketids.json"):
		with open("data/claimedticketids.json", mode='w') as f:
			json.dump({}, f)

	@commands.group(pass_context=True)
	async def ticket(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.send_cmd_help(ctx)


	@ticket.command(pass_context=True)
	@commands.cooldown(1, 30, commands.BucketType.user)
	async def send(self, ctx):
		issuer = ctx.message.author
		ticketmessage = ctx.message.content[13:]

		if ticketmessage == "":
			await self.bot.send_message(ctx.message.channel, "Please submit a message")
			return

		with open("data/tickets.json", "r") as f: 
			tickets = json.load(f)

		with open("data/claimedticketids.json", "r") as f:
			ticket_claims = json.load(f)

		if "amount_of_open_tickets" not in tickets:
			tickets["amount_of_open_tickets"] = 0

		ticketnumber = tickets["amount_of_open_tickets"] + 1
		tickets["amount_of_open_tickets"] = ticketnumber

		while ticketnumber in tickets:
			ticketnumber += 1

		ticket_claims[ticketnumber] = "not_claimed"

		tickets[ticketnumber] = {"ticket_data": []}
		tickets[ticketnumber]["ticket_data"].append({"issuer_id": issuer.id, "issuer_name": issuer.name, "ticket_message": ticketmessage})

		await self.bot.say("Please read the FAQ before sending a ticket.(<#468799519811829761> for servers, and <#468799722933714964> for users) If you have read the FAQ, respond to this message with 'Y'. You have 15 seconds to reply. DO NOT send any other messages.")
		msg = await self.bot.wait_for_message(timeout=15, author=issuer)
		if msg is None:
			await self.bot.say("You have ran out of time.")
			return
		if msg.content.upper() != "Y":
			await self.bot.say("You have sent a message that was not 'Y'. Returning.")
			return

		try:
			embed = discord.Embed(name="Ticket nr. {}".format(ticketnumber), description="Ticket nr. {}".format(ticketnumber), color=0xff0000)
			embed.add_field(name="Ticket ID: ", value=ticketnumber, inline=True)
			embed.add_field(name="Issuer Name: ", value=issuer.name, inline=True)
			embed.add_field(name="Issuer ID: ", value=issuer.id, inline=True)
			embed.add_field(name="Ticket Message: ", value=ticketmessage, inline=True)
			channel = discord.utils.get(ctx.message.server.channels, name="tickets")
			await self.bot.send_message(channel, embed=embed)
			await self.bot.say("Thank you for submitting your ticket! It's ID is: {}".format(ticketnumber))
		except discord.errors.HTTPException:
			await self.bot.say("You have exceeded the character limit! The limit is somewhere around 1900(depends on the length of your nickname)")
			return

		with open("data/tickets.json", "w") as f:
			json.dump(tickets, f)

		with open("data/claimedticketids.json", "w") as f:
			json.dump(ticket_claims, f)


	@ticket.command(pass_context=True)
	@commands.has_role("Tech Support")
	async def claim(self, ctx):
		server = ctx.message.server
		claimer = ctx.message.author
		ticket = ctx.message.content[14:]


		if ticket == "":
			await self.bot.say("Please input a ticket id")
			return
	

		with open("data/claimedticketids.json", "r") as f:
			ticket_claims = json.load(f)

		a = open("data/tickets.json").read()
		tickets = json.loads(a)


		if ticket not in ticket_claims:
			await self.bot.say("No ticket with that ID was found")
			return


		if ticket_claims[ticket] != "not_claimed":
			await self.bot.say("This ticket is already claimed.")
			return

		ticket_claims[ticket] = claimer.id
		role = discord.utils.get(server.roles, name="Overseer")
		user = await self.bot.get_user_info(tickets[ticket]["ticket_data"][0][u'issuer_id'])

		
		ticket_perms = discord.PermissionOverwrite(read_messages=True)
		everyone_perms = discord.PermissionOverwrite(read_messages=False)

		techlead = discord.ChannelPermissions(target=role, overwrite=ticket_perms)
		everyone = discord.ChannelPermissions(target=server.default_role, overwrite=everyone_perms)
		ticketuser = discord.ChannelPermissions(target=user, overwrite=ticket_perms)
		claimeruser = discord.ChannelPermissions(target=ctx.message.author, overwrite=ticket_perms)

		await self.bot.create_channel(server, "Ticket Nr. {}".format(ticket), ticketuser, everyone, techlead, claimeruser) 

		with open("data/claimedticketids.json", "w") as f:
			json.dump(ticket_claims, f)

		channel = discord.utils.get(ctx.message.server.channels, name="tickets")
		await self.bot.send_message(channel, claimer.name + " has claimed the ticket nr. " + ticket)

		await self.bot.say("You have claimed the ticket nr. " + ticket)

	@ticket.command(pass_context=True)
	@commands.has_role("Tech Support")
	async def close(self, ctx):
		try:
			closer = ctx.message.author
			ticket = ctx.message.content[14:]

			if ticket == "":
				await self.bot.say("Please input a ticket id")
				return

			with open("data/tickets.json", "r") as f:
				tickets = json.load(f)

			with open("data/claimedticketids.json") as f:
				ticket_claims = json.load(f)

			if ticket not in ticket_claims:
				await self.bot.say("No ticket with that ID was found")
				return

			if ticket_claims[ticket] == "not_claimed":
				await self.bot.say("This ticket hasn't been claimed yet.")
				return

			del tickets[ticket]

			with open("data/tickets.json", "w") as f:
				json.dump(tickets, f)

			with open("data/claimedticketids.json", "w") as f:
				json.dump(ticket_claims, f)

			channel = discord.utils.get(ctx.message.server.channels, name="tickets")
			await self.bot.send_message(channel, closer.name + " has closed the ticket nr. " + ticket)

			await self.bot.say("You have succesfully closed the ticket nr. " + ticket)
		except KeyError:
			await self.bot.say("No ticket with that ID was found")

	@ticket.command(pass_context=True)
	@commands.has_role("Overseer")
	async def approve(self, ctx):

		ticket = ctx.message.content[16:]

		if ticket == "":
			await self.bot.say("Please input a ticket id")
			return

		with open("data/techsupportstats.json", "r") as f:
			techstats = json.load(f)
		with open("data/claimedticketids.json", "r") as f:
			tickets = json.load(f)
		with open("data/tickets.json", "r") as f:
			ticketnumbers = json.load(f)

		claimedtech = tickets[ticket]

		if claimedtech == "not_claimed":
			await self.bot.say("This ticket has not been claimed yet.")
			return

		if claimedtech not in techstats:
			await self.bot.say("This tech support member is not in the statistics. First add him to the statistics file using !ticket addtech, and then approve the ticket.")
			return

		ticketnum = ticketnumbers["amount_of_open_tickets"] - 1
		ticketnumbers["amount_of_open_tickets"] = ticketnum

		techstats[claimedtech] = techstats[claimedtech] + 1

		del tickets[ticket]
		channel = discord.utils.get(ctx.message.server.channels, name="ticket-nr-{}".format(ticket))
		await self.bot.delete_channel(channel)
		await self.bot.send_message(ctx.message.author, "You have approved the ticket. The tech support member will have this ticket added to his/her statistics")

		with open("data/techsupportstats.json", "w") as f:
			json.dump(techstats, f)
		with open("data/claimedticketids.json", "w") as f:
			json.dump(tickets, f)
		with open("data/tickets.json", "w") as f:
			json.dump(ticketnumbers, f)

	@ticket.command(pass_context=True)
	@commands.has_role("Overseer")
	async def deny(self,ctx):
		try:
			ticket = ctx.message.content[13:]
			ticketnumber = ticket
			if ticket == "":
				await self.bot.say("Please supply a ticket id")
				return
			with open("data/claimedticketids.json", "r") as f:
				ticket_data = json.load(f)
			with open("data/tickets.json", "r") as f:
				tickets = json.load(f)
			if ticket_data[ticket] == "not_claimed":
				await self.bot.say("This ticket has not been claimed yet.")
				return
			del ticket_data[ticket]

			ticketnumber = tickets["amount_of_open_tickets"] - 1
			tickets["amount_of_open_tickets"] = ticketnumber

			with open("data/tickets.json", "w") as f:
				json.dump(tickets, f)

			with open("data/claimedticketids.json", "w") as f:
				json.dump(ticket_data, f)
			
			await self.bot.send_message(ctx.message.author, "You have denied the ticket. The tech support member will not have this ticket added to his/her statistics.")
			channel = discord.utils.get(ctx.message.server.channels, name="ticket-nr-{}".format(ticket))
			await self.bot.delete_channel(channel)
		except KeyError:
			await self.bot.say("No ticket with that id was found")
			return

	@ticket.command(pass_context=True)
	@commands.has_role("Tech Support")
	async def info(self,ctx):
		ticket = ctx.message.content[13:]
		if ticket == "":
			await self.bot.say("Please supply a ticket id")
			return
		json_data= open("data/tickets.json").read()
		tickets = json.loads(json_data)
		embed = discord.Embed(title="Ticket Info", description="Information about the ticket nr. {}".format(ticket), color=0x00ff00)
		embed.add_field(name="Issuer Name", value=tickets[ticket]["ticket_data"][0][u"issuer_name"], inline=True)
		embed.add_field(name="Issuer ID", value=tickets[ticket]["ticket_data"][0][u"issuer_id"], inline=True)
		embed.add_field(name="Ticket ID", value=ticket, inline=True)
		embed.add_field(name="Ticket Message", value=tickets[ticket]["ticket_data"][0][u"ticket_message"], inline=True)
		await self.bot.say(embed=embed)

	@ticket.command(pass_context=True)
	@commands.has_role("Overseer")
	async def addtech(self, ctx):
		techie = ctx.message.mentions[0].id
		with open("data/techsupportstats.json", "r") as f:
			stats = json.load(f)
		if techie in stats:
			await self.bot.say("That Tech Support member is already in the statistics")
			return
		stats[techie] = 0
		with open("data/techsupportstats.json", "w") as f:
			json.dump(stats, f)
		await self.bot.say("You have succesfully added a new tech support member to the statistics.")

	@ticket.command(pass_context=True)
	@commands.has_role("Overseer")
	async def deltech(self, ctx):
		techie = ctx.message.mentions[0].id
		with open("data/techsupportstats.json", "r") as f:
			stats = json.load(f)
		if techie not in stats:
			await self.bot.say("That person is not in the statistics file.")
			return
		del stats[techie]
		with open("data/techsupportstats.json", "w") as f:
			json.dump(stats, f)
		await self.bot.say("You have succesfully removed a tech support member from the statistics file")


	

def setup(bot):
	bot.add_cog(ticketSystem(bot))
