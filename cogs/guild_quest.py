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
                name="Guild Quest: June 8, 2021",
                value=f"{guild_member_role.mention} -- Alright night owls, this is a unique guild quest because it "
                      f"requires you to be in a certain place at a certain time in WoW. Hopefully you're not doing "
                      f"anything at midnight PST on Saturday night/Sunday morning."
            )
            embed2 = discord.Embed(
                description="Where to be",
                color=config["success"]
            )
            embed2.add_field(
                name="Location",
                value="Be at the Photonic Playground in Legion Dalaran at midnight PST Saturday night/Sunday morning "
                      "when the chest spawns. It's upstairs at 44.8 47.3")
            embed2.set_image(url="https://i.imgur.com/WMzWwuF.jpeg")
            embed3 = discord.Embed(
                description="What you're looking for",
                color=config["success"]
            )
            embed3.add_field(
                name="Find this chest",
                value="This chest will spawn on the floor at midnight PST. Loot it to get your new shoe shining kit!"
                      "Post an image of you looting the chest, using the toy, or the toy in your toybox for a raffle "
                      "ticket."
            )
            embed3.set_image(url="https://wow.zamimg.com/uploads/screenshots/normal/562799-sheddles-chest.jpg")
            await context.send(embed=embed1)
            await context.send(embed=embed2)
            await context.send(embed=embed3)
            await context.send("https://youtu.be/0j0owojgGOc?t=239")
            await context.message.delete()


def setup(bot):
    bot.add_cog(GuildQuest(bot))
