import os
import sys

import discord
import yaml
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class GuildQuest(commands.Cog, name="guildquest"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gquest")
    async def gquest(self, context):
        """
        Posts the weekly guild quest.
        """
        guild_member_role = discord.utils.get(context.guild.roles, name="Guild Member")

        if context.message.author.id in config["owners"]:
            embed1 = discord.Embed(
                description="Weekly Guild Quest!",
                color=config["success"]
            )
            embed1.add_field(name="Guild Quest: June 1st, 2021",
                             value=f"{guild_member_role.mention} -- Find these three images and post your own for a raffle ticket!\n"
                                   "We're continuing the trend of Vanilla dungeons. You'll find this one in Eastern Kingdoms."
                                   "It's the smallest dungeon I've ever seen in my life, and it's super easy to find")
            embed2 = discord.Embed(
                description="First Picture",
                color=config["success"]
            )
            embed2.set_image(url="https://i.imgur.com/enkzyHl.jpg")
            embed3 = discord.Embed(
                description="Second Picture",
                color=config["success"]
            )
            embed3.set_image(url="https://i.imgur.com/OK7ezEO.jpg")
            embed4 = discord.Embed(
                description="Third Picture",
                color=config["success"]
            )
            embed4.set_image(url="https://i.imgur.com/LSQoC14.jpg")
            await context.send(embed=embed1)
            await context.send(embed=embed2)
            await context.send(embed=embed3)
            await context.send(embed=embed4)


def setup(bot):
    bot.add_cog(GuildQuest(bot))
