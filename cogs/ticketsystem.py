import discord
from discord.ext import commands
import json
import os
import random

class ticketSystem:
	def __init__(self, bot):
		self.bot = bot


	#TODO: add cooldown

	@commands.group(pass_context=True)
	async def ticket(self, ctx):
		if ctx.invoked_subcommand is None:
			await self.bot.send_cmd_help(ctx)


	@ticket.command(pass_context=True)
	async def send(self, ctx):

		issuer = ctx.message.author
		ticketmessage = ctx.message.content[13:]

		if ticketmessage == "":
			await self.bot.send_message(ctx.message.channel, "Please submit a message")
			return

		with open("data/tickets.json", "r") as f: 
			tickets = json.load(f)

		with open("data/claimedticketids.json", "r") as f:
			ticketids = json.load(f)

		if "amount_of_open_tickets" not in tickets:
			tickets["amount_of_open_tickets"] = 0

		ticketNumber = tickets["amount_of_open_tickets"] + 1
		tickets["amount_of_open_tickets"] = ticketNumber

		while discord.utils.get(issuer.server.channels, name="ticket-nr-{}".format(ticketNumber)) in issuer.server.channels:
			ticketNumber = ticketNumber + 1

		ticketids[ticketNumber] = "not_claimed"

		tickets[ticketNumber] = {"ticket_data": []}
		tickets[ticketNumber]["ticket_data"].append({"issuer_id": issuer.id, "issuer_name": issuer.name, "ticket_message": ticketmessage, "claimed": None})

		with open("data/tickets.json", "w") as f:
			json.dump(tickets, f)

		with open("data/claimedticketids.json", "w") as f:
			json.dump(ticketids, f)

		await self.bot.create_role(issuer.server, name="Ticket Nr. {}".format(ticketNumber))
		role = discord.utils.get(issuer.server.roles, name="Ticket Nr. {}".format(ticketNumber))
		while role == None:
			await self.bot.create_role(issuer.server, name="Ticket Nr. {}".format(ticketNumber))
			role = discord.utils.get(issuer.server.roles, name="Ticket Nr. {}".format(ticketNumber))
		await self.bot.add_roles(issuer, role)

		ticket_perms = discord.PermissionOverwrite(read_messages=True)
		everyone_perms = discord.PermissionOverwrite(read_messages=False)


		everyone = discord.ChannelPermissions(target=issuer.server.default_role, overwrite=everyone_perms)
		ticket = discord.ChannelPermissions(target=role, overwrite=ticket_perms)
		await self.bot.create_channel(issuer.server, "Ticket Nr. {}".format(ticketNumber), everyone, ticket)

		await self.bot.say("Thank you for submitting your ticket! It's ID is: {}".format(ticketNumber))

		embed = discord.Embed(name="Ticket nr. {}".format(ticketNumber), description="Ticket nr. {}".format(ticketNumber), color=0xff0000)
		embed.add_field(name="Ticket ID: ", value=ticketNumber, inline=True)
		embed.add_field(name="Issuer Name: ", value=issuer.name, inline=True)
		embed.add_field(name="Issuer ID: ", value=issuer.id, inline=True)
		embed.add_field(name="Ticket Message: ", value=ticketmessage, inline=True)
		channel = discord.utils.get(ctx.message.server.channels, name="tickets")

		await self.bot.send_message(channel, embed=embed)

	@ticket.command(pass_context=True)
	@commands.has_role("Tech Support")
	async def claim(self, ctx):

		claimer = ctx.message.author
		ticket = ctx.message.content[14:]

		if ticket == "":
			await self.bot.say("Please input a ticket id")
			return

		with open("data/claimedticketids.json", "r") as f:
			ticketids = json.load(f)

		if ticket not in ticketids:
			await self.bot.say("No ticket with that ID was found")
			return

		if ticketids[ticket] != "not_claimed":
			await self.bot.say("This ticket is already claimed.")
			return

		ticketids[ticket] = claimer.id

		with open("data/claimedticketids.json", "w") as f:
			json.dump(ticketids, f)

		role = discord.utils.get(claimer.server.roles, name="Ticket Nr. {}".format(ticket))
		await self.bot.add_roles(claimer, role)

		channel = discord.utils.get(ctx.message.server.channels, name="tickets")
		await self.bot.send_message(channel, claimer.name + " has claimed the ticket nr. " + ticket)



	@ticket.command(pass_context=True)
	@commands.has_role("Tech Support")
	async def close(self, ctx):

		closer = ctx.message.author
		ticket = ctx.message.content[14:]

		if ticket == "":
			await self.bot.say("Please input a ticket id")
			return

		with open("data/tickets.json", "r") as f:
			tickets = json.load(f)

		with open("data/claimedticketids.json") as f:
			ticketids = json.load(f)

		if ticket not in ticketids:
			await self.bot.say("No ticket with that ID was found")
			return

		if ticketids[ticket] == "not_claimed":
			await self.bot.say("This ticket hasn't been claimed yet.")
			return

		del tickets[ticket]

		ticketNumber = tickets["amount_of_open_tickets"] - 1
		tickets["amount_of_open_tickets"] = ticketNumber

		with open("data/tickets.json", "w") as f:
			json.dump(tickets, f)

		with open("data/claimedticketids.json", "w") as f:
			json.dump(ticketids, f)

		role = discord.utils.get(closer.server.roles, name="Ticket Nr. {}".format(ticket))
		await self.bot.delete_role(closer.server, role)

		channel = discord.utils.get(ctx.message.server.channels, name="tickets")
		await self.bot.send_message(channel, closer.name + " has closed the ticket nr. " + ticket)

		await self.bot.say("You have succesfully closed the ticket nr. " + ticket)

	@ticket.command(pass_context=True)
	@commands.has_role("Tech Support Lead")
	async def approve(self, ctx):
		#this is a way to prevent ticket farming, all tickets will have to be approved by the TSL before they get added to the statistics.

		ticket = ctx.message.content[16:]

		if ticket == "":
			await self.bot.say("Please input a ticket id")
			return

		with open("data/techsupportstats.json", "r") as f:
			techstats = json.load(f)
		with open("data/claimedticketids.json", "r") as f:
			tickets = json.load(f)

		claimedtech = tickets[ticket]

		if claimedtech == "not_claimed":
			await self.bot.say("This ticket has not been claimed yet.")
			return

		techstats[claimedtech] = techstats[claimedtech] + 1

		del tickets[ticket]
		channel = discord.utils.get(ctx.message.server.channels, name="ticket-nr-{}".format(ticket))
		await self.bot.delete_channel(channel)
		await self.bot.send_message(ctx.message.author, "You have approved the ticket. The tech support member will have this ticket added to his/her statistics")

		with open("data/techsupportstats.json", "w") as f:
			json.dump(techstats, f)
		with open("data/claimedticketids.json", "w") as f:
			json.dump(tickets, f)		

	@ticket.command(pass_context=True)
	async def deny(self,ctx):
		ticket = ctx.message.content[13:]
		if ticket == "":
			await self.bot.say("Please supply a ticket id")
			return
		await self.bot.send_message(ctx.message.author, "You have denied the ticket. The tech support member will not have this ticket added to his/her statistics.")
		channel = discord.utils.get(ctx.message.server.channels, name="ticket-nr-{}".format(ticket))
		await self.bot.delete_channel(channel)

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
	@commands.has_role("Tech Support Lead")
	async def AddTechSupport(self, ctx):
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
	@commands.has_role("Tech Support Lead")
	async def RemoveTechSupport(self, ctx):
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
