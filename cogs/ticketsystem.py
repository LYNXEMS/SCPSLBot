import discord
from discord.ext import commands
import json
import os
import random

class ticketSystem:
	def __init__(self, bot):
		self.bot = bot



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

		while ticketNumber in tickets:
			ticketNumber + 1

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

		ticketids[ticket] = claimer.name

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
		del ticketids[ticket]

		ticketNumber = tickets["amount_of_open_tickets"] - 1
		tickets["amount_of_open_tickets"] = ticketNumber

		with open("data/tickets.json", "w") as f:
			json.dump(tickets, f)

		with open("data/claimedticketids.json", "w") as f:
			json.dump(ticketids, f)

		role = discord.utils.get(closer.server, name="Ticket Nr. " + str(ticket))
		await self.bot.delete_role(closer.server, role)

		channel = discord.utils.get(ctx.message.server.channels, name="tickets")
		await self.bot.send_message(channel, closer.name + " has closed the ticket nr. " + ticket)

		await self.bot.say("You have succesfully closed the ticket nr. " + ticket)


def setup(bot):
	bot.add_cog(ticketSystem(bot))
