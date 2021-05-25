import os
import sys
import yaml

from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


class User(commands.Cog, name="user"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scrumpy")
    async def scrumpy(self, ctx):
        """
        Scrumpy's opinion
        """
        await ctx.send("Thinks your bags are awful")

    @commands.command(name="calendar")
    async def calendar(self, ctx):
        """
        Remind Kat to update the in-game calendar
        """
        await ctx.send("<@267888830634262529> needs to update the calendar!")

    @commands.command(name="golfclap")
    async def golfclap(self, ctx):
        """
        Sends a golfclap
        """
        await ctx.send("https://tenor.com/view/charlie-sheen-emilio-estevez-golf-clap-men-at-work-gif-7577611")

    @commands.command(name="spooky")
    async def spooky(self, ctx):
        """
        bwAAAAAAAHHHP!
        """
        await ctx.send("https://img1.cgtrader.com/items/1911482/ca45cf3f32/air-horn-3d-model-max-obj-mtl-3ds-fbx-dxf.jpg")

    @commands.command(name="whatever")
    async def scrumpy(self, ctx):
        """
        That's just, like, your opinion man
        """
        await ctx.send("https://media.discordapp.net/attachments/765619338337058827/802299499908563024/whatever.gif")

    @commands.command(name="cool")
    async def cool(self, ctx):
        """
        Detective Jake Peralta
        """
        await ctx.send("https://tenor.com/view/andy-samberg-brooklyn99-jake-peralta-cool-gif-12063970")

    @commands.command(name="myst")
    async def myst(self, ctx):
        """
        The condescension is palpable.
        """
        await ctx.send("https://tenor.com/view/is-it-though-thor-smile-gif-13334930")

    @commands.command(name="beylock")
    async def beylock(self, ctx):
        """
        Loves Weird Al
        """
        await ctx.send("https://imgur.com/a/xux2u6p")

    @commands.command(name="happybirthday")
    async def happybirthay(self, ctx):
        """
        PARTY TIME
        """
        await ctx.send("https://giphy.com/gifs/i8htPQwChFOVcpnImq")

    @commands.command(name="magic")
    async def magic(self, ctx):
        """
        Magic. Simple.
        """
        await ctx.send("https://media.discordapp.net/attachments/676183284123828236/761438362720272394/Kat_Confetti.gif")

    @commands.command(name="lynkz")
    async def lynkz(self, ctx):
        """
        Just one man's opinion
        """
        await ctx.send("https://tenor.com/view/james-franco-fuck-that-dude-fuckoff-annoyed-annoying-gif-11146686")

    @commands.command(name="candercane")
    async def candercane(self, ctx):
        """
        My favorite gif on the planet. Use when you're angry.
        """
        await ctx.send("https://giphy.com/gifs/angry-mad-anger-l1J9u3TZfpmeDLkD6")

    @commands.command(name="wat")
    async def wat(self, ctx):
        """
        Kat doesn't know what that was.
        """
        await ctx.send("https://imgur.com/a/PnB5eFk")

    @commands.command(name="thisisfine")
    async def thisisfine(self, ctx):
        """
        Someone help Kat.
        """
        await ctx.send("https://imgur.com/a/uDAO5In")

    @commands.command(name="pirate")
    async def pirate(self, ctx):
        """
        Pirate shimmy. Self-explanatory.
        """
        await ctx.send("https://imgur.com/a/TDot4Ba")

    @commands.command(name="justice")
    async def justice(self, ctx):
        """
        An eye for an eye.
        """
        await ctx.send("https://gfycat.com/adorablespotlesshammerheadbird")

    @commands.command(name="suckit")
    async def suckit(self, ctx):
        """
        Dance, monkey
        """
        await ctx.send("https://imgur.com/Fy6RhWI")

    @commands.command(name="risn")
    async def risn(self, ctx):
        """
        Look man...
        """
        await ctx.send("https://www.circlek.com/themes/custom/circlek/images/logos/logo-full-color-rgb.jpg")


def setup(bot):
    bot.add_cog(User(bot))
