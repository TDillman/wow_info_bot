import os
import sys
import discord
import yaml
import random
import gspread

from discord.ext import commands
from datetime import datetime

gc = gspread.service_account()

month_dict = {
    "January": 0,
    "February": 1,
    "March": 2,
    "April": 3,
    "May": 4,
    "June": 5,
    "July": 6,
    "August": 7,
    "September": 8,
    "October": 9,
    "November": 10,
    "December": 11
}

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class Raffle(commands.Cog, name="raffle"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="selectwinner")
    async def selectwinner(self, ctx, arg):
        """
        Picks a winner for the monthly Might raffle
            usage: !selectwinner <Month>
            example: !selectwinner June
        """
        if ctx.message.author.id in config["raffle"]:
            sheet = gc.open("Might Raffle Tickets 2021").get_worksheet(month_dict[arg])
            raffle_winner = random.choice(sheet.col_values(1))

            embed = discord.Embed(
                title="Monthly Might Raffle",
                color=config["success"]
            )
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcoloredfinishedsmall.png")
            embed.add_field(name="And the winner is...",
                            value=f'\n**{raffle_winner}**'
                            )
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)

    @commands.command(name="addticket")
    async def addticket(self, ctx, *, args):
        """
        Award someone a ticket.
            Usage: !addticket "<User - Reason>"
            example: !addticket HealtoDeath - Raid Attendance
        """
        current_month = datetime.now().month - 1
        if ctx.message.author.id in config["owner"]:
            sheet = gc.open("Might Raffle Tickets 2021").get_worksheet(current_month)
            length_of_sheet = len(sheet.col_values(1))
            sheet.update(f'A{length_of_sheet + 1}', args)
            embed = discord.Embed(
                title=f"Raffle Ticket Awarded!",
                description=f"Reason: {args}",
                color=config["success"]
            )
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)

    @commands.command(name="showtickets")
    async def showtickets(self, ctx, arg):
        """
        Get the tickets awarded for the given month.
            Usage: !showtickets <Month>
            example: !showtickets May
        """
        sheet = gc.open("Might Raffle Tickets 2021").get_worksheet(month_dict[arg])
        ticket_string = ''
        ticket_list = sheet.col_values(1)
        for ticket in ticket_list:
            ticket_string += f'{ticket}\n'
        embed = discord.Embed(
            title=f"Raffle Tickets for {arg}!",
            description=f"{arg} 2021",
            color=config["success"]
        )
        embed.add_field(
            name="Current ticket:",
            value=ticket_string
        )
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Raffle(bot))