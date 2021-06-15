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
                name="Guild Quest: June 15th, 2021",
                value=f"{guild_member_role.mention} -- Guild Quest Tuesday! If you do things right, you'll get "
                      f"two toys from this one. But there's a catch: You have to be a Horde character to complete "
                      f"this particular quest. Our main quest is to find the [Zandalari Effigy Amulet]"
                      f"(https://ptr.wowhead.com/item=156649/zandalari-effigy-amulet)"
            )
            embed2 = discord.Embed(
                description="Location",
                color=config["success"]
            )
            embed2.add_field(
                name="Where to Start",
                value="Start in Dazar'Alor's Grand Bazaar, with Griftah (our BC Classic brethren may recognize him "
                      "from Shattrath City).\n\nhttps://i.imgur.com/pWQy8RT.jpg")
            embed2.set_image(url="https://wow.zamimg.com/uploads/screenshots/normal/742830-griftah.jpg")
            embed3 = discord.Embed(
                description="Map of Dazar'Alor",
                colour=config["success"]
            )
            embed3.set_image(url="https://i.imgur.com/pWQy8RT.jpg")
            embed4 = discord.Embed(
                description="Time to Trade",
                color=config["success"]
            )
            embed4.add_field(
                name="Steps:",
                value=f"1. Purchase a  Sack of 'Discarded' Hearthstones from Griftah (52.9, 89.9).\n"
                      f"2. Go to Rakle the Wretched (34.8, 11.5) and trade the  Sack of 'Discarded' Hearthstones for a  Much-Too-Hot Pepper.\n"
                      f"3. Go to Trader Haw'li (37.8, 14.7) and trade the  Much-Too-Hot Pepper for some  Golden Seeds. **This "
                      f"vendor also sells Haw'li's Hot & Spicy Chili, so you can pick that up here too**\n"
                      f"4. Go to Granda Watae (42.2, 35.7) and trade the  Golden Seeds for a  Centennial Blossom.\n"
                      f"5. Go to Trader Nog (57.2, 91.5) and trade the  Centennial Blossom for a  Preserved Night Elf Head.\n"
                      f"6. Go to 'Black Eye' Zenru (53.8, 86) and trade the  Preserved Night Elf Head for a  Counterfeit Rastakhan Mask.\n"
                      f"7. Finally, return to Griftah (52.9, 89.9) and trade the  Counterfeit Rastakhan Mask for the  Zandalari Effigy Amulet.\n"
            )
            await context.send(embed=embed1)
            await context.send(embed=embed2)
            await context.send(embed=embed3)
            await context.send(embed=embed4)
            await context.message.delete()


def setup(bot):
    bot.add_cog(GuildQuest(bot))
