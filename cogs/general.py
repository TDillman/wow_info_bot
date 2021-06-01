import os
import sys
import aiohttp
import json
import discord
import yaml
import random

from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", aliases=["echo"])
    async def say(self, ctx, *, args):
        """
        The bot will say anything you want. Only officers can use this one.
        """
        await ctx.message.delete()
        if ctx.message.author.id in config["owners"]:
            await ctx.channel.send(args)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )
            await ctx.author.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if context.message.author.id in config["owners"]:
            embed = discord.Embed(
                description=args,
                color=config["success"]
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=config["error"]
            )
            await context.send(embed=embed)

    @commands.command(name="poll")
    async def poll(self, ctx, *args):
        """
        Create a poll where members can vote.
            Usage: !poll Is Santa real?
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=config["success"]
        )
        embed.set_footer(
            text=f"Poll created by: {ctx.message.author} • React to vote!"
        )
        embed_message = await ctx.channel.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="bitcoin")
    async def bitcoin(self, ctx):
        """
        Get the current price of bitcoin.
        """
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=config["success"]
            )
            await ctx.channel.send(embed=embed)

    @commands.command(name="roll")
    async def roll(self, ctx, arg):
        """
        Rolls a random number between 1 and the user's selection
            usage: !roll 50
            will roll a number between 1 and 50
        """
        roll = random.randint(1, int(arg))
        embed = discord.Embed(
            description=f"{ctx.message.author.display_name} rolled a **{roll}** (1 through {arg})."
        )
        if roll == 1:
            victory_string = f"{ctx.message.author.display_name} loses!"
            embed.add_field(
                name="Defeat!",
                value=victory_string
            )

        await ctx.message.delete()
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
