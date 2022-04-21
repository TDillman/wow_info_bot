import os
import sys
import yaml
import aiohttp
import random

from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

peaceout_list = ["https://tenor.com/view/drive-by-50cent-smile-see-ya-swag-gif-5548830",
                 "https://giphy.com/gifs/S7jKEqmTbee7S",
                 "https://tenor.com/view/50cent-bert-gif-3799566",
                 "https://cdn.discordapp.com/attachments/710566582845177888/952209615402201148/peaceout.gif"
                 ]


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
        Dem abs
        """
        await ctx.send("https://tenor.com/view/arrested-development-claw-hand-juice-box-laughing-evil-laugh-gif-5335530")

    @commands.command(name="whatever")
    async def whatever(self, ctx):
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
        Is that a headless person?
        """
        await ctx.send("https://media.discordapp.net/attachments/676183284123828236/899091363046522910/unknown.png")

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

    @commands.command(name="hakkd")
    async def hakkd(self, ctx):
        """
        Not a "burnin' down the house" joke?
        """
        await ctx.send("https://tenor.com/view/mad-monster-dont-let-it-happen-again-gif-14024298")

    @commands.command(name="wtf")
    async def wtf(self, ctx):
        """
        Best WTF gif there is
        """
        await ctx.send("https://giphy.com/gifs/what-the-fuck-wtf-ukGm72ZLZvYfS")

    @commands.command(name="rain")
    async def rain(self, ctx):
        """
        He said it himself
        """
        await ctx.send("https://cdn.discordapp.com/attachments/676183384061378571/856642945481310228/unknown.png")

    @commands.command(name="imout")
    async def imout(self, ctx):
        """
        That flip though
        """
        await ctx.send("https://media.discordapp.net/attachments/676183306924064768/866005404839837706/sylvanas.gif")

    @commands.command(name="daddychill", aliases=["whatthehell"])
    async def daddychill(self, ctx):
        """
        Daddy, chill!
        """
        await ctx.send("https://tenor.com/view/what-the-hell-is-even-gif-20535402")

    @commands.command(name="guacdrop", aliases=["droptheguac"])
    async def guacdrop(self, ctx):
        """
        Daddy, chill!
        """
        await ctx.send("https://media.discordapp.net/attachments/917450971569877044/917465265036488704/20211105_213516.jpg")

    @commands.command(name="rightright", aliases=["ohright", "rightrightright"])
    async def rightright(self, ctx):
        """
        Right right right right right right...
        """
        await ctx.send("https://tenor.com/view/seinfeld-jerry-seinfeld-oh-right-agree-gif-4436696")

    @commands.command(name="shit")
    async def shit(self, ctx):
        """
        Get your shit together
        """
        await ctx.send("https://giphy.com/gifs/get-well-then-woTdBa435yy6A")

    @commands.command(name="hydrate")
    async def hydrate(self, ctx):
        """
        DRINK
        """
        await ctx.send("https://tenor.com/view/water-smile-drink-water-gif-13518129")

    @commands.command(name="spoon", aliases=["party"])
    async def spoon(self, ctx):
        """
        A little party never killed nobody...except Belushi.
        """
        await ctx.send("https://media.discordapp.net/attachments/503025662546935809/747820543918735370/A_little_party_never_killed_no_body_gif.gif")

    @commands.command(name="imdumb")
    async def imdumb(self, ctx):
        """
        Dumbest boy in school
        """
        await ctx.send("https://tenor.com/view/winston-schmidt-max-greenfield-new-girl-gif-15041554")

    @commands.command(name="aster", aliases=["asterend"])
    async def aster(self, ctx):
        """
        Cheeeeese!
        """
        await ctx.send("https://cdn.discordapp.com/attachments/938971434246631435/940347663533084732/Chaotic_Aster.png")

    @commands.command(name="cat")
    async def cat(self, ctx):
        """
        It's a cat
        """
        async with aiohttp.ClientSession() as session:
            async with session.get('http://aws.random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    await ctx.send(js['file'])
    @commands.command(name="peaceout")
    async def peaceout(self, ctx):
        """
        Peace out
        """
        await ctx.send(random.choice(peaceout_list))


def setup(bot):
    bot.add_cog(User(bot))
