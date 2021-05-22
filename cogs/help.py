import os
import sys
import datetime
import discord
import yaml

from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)


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
        embed.set_image(url='https://www.filmandtvnow.com/wp-content/uploads/2014/12/Baymax.jpg')
        embed.add_field(name="Response Time",
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


def setup(bot):
    bot.add_cog(Help(bot))
