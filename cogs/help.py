import os
import sys
import datetime
import discord
import yaml
import time
import random

from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

shit_list = ['https://i.pinimg.com/originals/ef/a6/48/efa648c67f3cb05287ded99612af130f.png',
             'https://i.kym-cdn.com/entries/icons/original/000/017/372/ClmrSzk.jpg.png',
             'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAuOPyTLmaoq6hrHNNUnNzzk9_OeRtpLX80g&usqp=CAU',
             'https://i.kym-cdn.com/photos/images/facebook/000/917/464/752.jpg',
             'https://memegenerator.net/img/instances/40808454/listen-here-you-little-shit.jpg',
             'https://ih1.redbubble.net/image.1045539425.2307/poster,840x830,f8f8f8-pad,1000x1000,f8f8f8.jpg',
             'https://memegenerator.net/img/instances/71923924/listen-here-you-little-shit.jpg',
             'https://pics.ballmemes.com/listen-here-you-little-shit-8006247.png'
             ]

command_dict = {
        '!scrumpy': 'Thinks your bags are awful',
        '!calendar': '<@267888830634262529> needs to update the calendar!',
        '!golfclap': 'https://tenor.com/view/charlie-sheen-emilio-estevez-golf-clap-men-at-work-gif-7577611',
        '!spooky': 'https://img1.cgtrader.com/items/1911482/ca45cf3f32/air-horn-3d-model-max-obj-mtl-3ds-fbx-dxf.jpg',
        '!whatever': 'https://media.discordapp.net/attachments/765619338337058827/802299499908563024/whatever.gif',
        '!cool': 'https://tenor.com/view/andy-samberg-brooklyn99-jake-peralta-cool-gif-12063970',
        'cool cool cool': 'https://tenor.com/view/andy-samberg-brooklyn99-jake-peralta-cool-gif-12063970',
        '!myst': 'https://tenor.com/view/is-it-though-thor-smile-gif-13334930',
        '!beylock': 'https://imgur.com/a/xux2u6p',
        'flex': 'https://cdn.discordapp.com/attachments/676183284123828236/823278892676022353/image0.jpg',
        '!happybirthday': 'https://giphy.com/gifs/i8htPQwChFOVcpnImq',
        '!magic': 'https://media.discordapp.net/attachments/676183284123828236/761438362720272394/Kat_Confetti.gif',
        '!lynkz': 'https://tenor.com/view/james-franco-fuck-that-dude-fuckoff-annoyed-annoying-gif-11146686',
        'listen here you little shit': random.choice(shit_list),
        '!candercane': 'https://giphy.com/gifs/angry-mad-anger-l1J9u3TZfpmeDLkD6',
        '!wat': 'https://imgur.com/a/PnB5eFk',
        '!thisisfine': 'https://imgur.com/a/uDAO5In',
        '!pirate': 'https://imgur.com/a/TDot4Ba',
        '!justice': 'https://gfycat.com/adorablespotlesshammerheadbird',
        '!suckit': 'https://imgur.com/Fy6RhWI',
        'suck it': 'https://imgur.com/Fy6RhWI'
    }


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Pings the bot to make sure it's online and responding
        """
        begin_time = datetime.datetime.now()
        embed = discord.Embed(
            color=config["success"]
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.add_field(name="Respose Time",
                        value=f'Bot responded in {datetime.datetime.now() - begin_time}.')
        embed.set_footer(
            text=f"Pong request by {ctx.message.author}"
        )
        await ctx.send(embed=embed)

    @commands.command(name="help")
    async def help(self, context):
        """
        List all commands from every module the bot has loaded.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="List of available commands:", color=config["success"])
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            command_list = [command.name for command in commands]
            command_description = [command.help for command in commands]
            help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
            embed.add_field(name=i.capitalize(), value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)

    @commands.command(name="custom")
    async def custom(self, ctx):
        """
        Returns a list of the custom commands for Might (mostly memes, really)
        """
        custom_command_list = list(command_dict.keys())
        custom_command_list.sort()
        custom_command_string = "\n".join(custom_command_list)

        await ctx.author.send(custom_command_string)

        time.sleep(.25)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Help(bot))
