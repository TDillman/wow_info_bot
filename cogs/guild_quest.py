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
            embed1.add_field(
                name="Guild Quest: June 22nd, 2021",
                value=f"{guild_member_role.mention} -- Guild Quest Tuesday! Technically this quest isn't today. It's "
                      f"next Sunday, the 27th. This week's guild quest is the Running of the Trolls!"
            )
            embed2 = discord.Embed(
                description="Running of the Trolls",
                color=config["success"]
            )
            embed2.add_field(
                name="What It Is",
                value="A bunch of folks create Troll characters on Feathermoon-US and run from the starting zone "
                      "all the way up to Silvermoon City. The event is to raise awareness for [The Trevor Project](https://give.thetrevorproject.org/TrollRun2021), "
                      "which is a foundation aimed at ending LGBTQ youth suicide.")
            embed2.set_image(url="https://i.redd.it/0owzblq9vb571.jpg")
            embed3 = discord.Embed(
                description="When and Where",
                color=config["success"]
            )
            embed3.add_field(
                name="Feathermoon-US on Sunday, June 27th\n6pm Pacific Time/9pm Eastern Time",
                value="Whoever would like to join, come hang out and run with us. I'll be creating a character there "
                      "and logging in around 5:30PM Pacific Time just to get ready and hang out for a bit, then participating "
                      "in the run when it's time. Everyone who joins us for the run gets a raffle ticket!\n\nAlso I'll "
                      "donate $5 to the Trevor Project for every member of Might who runs with us."
            )
            await context.send(embed=embed1)
            await context.send(embed=embed2)
            await context.send(embed=embed3)
            await context.message.delete()


def setup(bot):
    bot.add_cog(GuildQuest(bot))
