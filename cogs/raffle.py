import os
import sys
import discord
import yaml
import gspread
import random
import asyncio

from discord.ext import commands
from discord.ext.commands import Bot

gc = gspread.service_account()

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

bot = Bot(command_prefix=config["bot_prefix"], case_insensitive=True)


class Raffle(commands.Cog, name="raffle"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="startraffle")
    async def startraffle(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="WoW Expansion Reveal Raffle",
            color=config["success"]
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcoloredfinishedsmall.png"
        )
        embed.add_field(
            name="What Is It?",
            value=(
                f"Specimen wanted to share his excitement for the new expansion with the Might family. To that end, "
                f"he's giving away a Digital Collector's Edition of the new expansion when it releases!"
                )
        )
        embed.add_field(
            name="How to Enter",
            value=(
                f"This raffle is open to Might guild members (and Jason. Just join the guild, man). Click on the green "
                f"check mark under this message and you'll be entered to win!"
                )
        )
        embed.add_field(
            name="Timeframe",
            value=(
                f"The raffle will start taking applicants right now! The raffle will end when raid ends on Friday, April"
                f" 22nd. Get your entry in now by clicking the check!"
                )
        )
        msg = await ctx.channel.send(embed=embed)
        await msg.add_reaction("✅")
        await asyncio.sleep(5)

        cache_msg = discord.utils.get(msg.messages, id=msg.id)
        for reactor in cache_msg.reactions:
            reactors = await msg.get_reaction_users(reactor)

            # from here you can do whatever you need with the member objects
            for member in reactors:
                await ctx.channel.send(member.name)

    @commands.command(name="selectwinner")
    async def selectwinner(self, ctx):
        """
        Picks a winner for the Might raffle
            usage: !selectwinner
        """
        if ctx.message.author.display_name == "Specimen" or "Beylock":
            sheet = gc.open("raffle").get_worksheet(0)
            raffle_winner = random.choice(sheet.col_values(1))

            embed = discord.Embed(
                title="Digital Collector's Edition Raffle",
                color=config["success"]
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcoloredfinishedsmall.png"
            )
            embed.add_field(
                name="And the winner is...",
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


def setup(bot):
    bot.add_cog(Raffle(bot))
