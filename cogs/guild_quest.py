import os
import sys

import discord
import yaml
from discord.ext import commands
from discord.utils import get

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
            embed1.add_field(name="Guild Quest: May 25, 2021",
                             value=f"{guild_member_role.mention} -- Find these three images and post your own for a raffle ticket!\n"
                                   "We're continuing the trend of Vanilla dungeons. You'll find this one in Desolace, "
                                   "in Kalimdor.\n\nPS -- Hope your vault isn't crap.")
            embed2 = discord.Embed(
                description="First Picture",
                color=config["success"]
            )
            embed2.set_image(url="https://i.imgur.com/q61uGE6.jpeg")
            embed3 = discord.Embed(
                description="Second Picture",
                color=config["success"]
            )
            embed3.set_image(url="https://i.imgur.com/XRljH2x.jpg")
            embed4 = discord.Embed(
                description="Third Picture",
                color=config["success"]
            )
            embed4.set_image(url="https://i.imgur.com/A4ggbfW.jpg")
            await context.send(embed=embed1)
            await context.send(embed=embed2)
            await context.send(embed=embed3)
            await context.send(embed=embed4)


def setup(bot):
    bot.add_cog(GuildQuest(bot))
