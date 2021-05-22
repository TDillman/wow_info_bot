import discord
import nest_asyncio
import os
import random
import platform
import yaml
import sys

from discord.ext import commands, tasks
from discord.ext.commands import Bot
from blizzardapi import BlizzardApi

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

nest_asyncio.apply()

client_id = config["blizzard_client_id"]
client_secret = config["blizzard_secret_id"]
discord_access_token = config["discord_token"]

api_client = BlizzardApi(client_id, client_secret)

bot = Bot(command_prefix=config["bot_prefix"])

bot.remove_command("help")

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
        'cool cool cool': 'https://tenor.com/view/andy-samberg-brooklyn99-jake-peralta-cool-gif-12063970',
        'flex': 'https://cdn.discordapp.com/attachments/676183284123828236/823278892676022353/image0.jpg',
        'listen here you little shit': random.choice(shit_list),
        'suck it': 'https://imgur.com/Fy6RhWI'
    }


@bot.event
async def on_ready():
    print("\n-------------------")
    print(f'Logged in: {bot.user}')  # show on console
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------\n\n")


# Setup the game status task of the bot
@tasks.loop(minutes=1.0)
async def status_task():
    statuses = ["with you!", "with dynamite!", f"{config['bot_prefix']}help", "with fire!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        return
    # Ignores if a command is being executed by a blacklisted user

    if message.author.id in config["blacklist"]:
        return
    await bot.process_commands(message)


# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    full_command_name = ctx.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


@bot.event
async def on_message(ctx):
    for key in command_dict:
        if key in ctx.content.lower():
            await ctx.channel.send(command_dict[key])

    # Without the following line, the bot gets stuck and won't process commands
    await bot.process_commands(ctx)


# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Error!",
            description="This command is on a %.2fs cool down" % error.retry_after,
            color=config["error"]
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=config["error"]
        )
        await context.send(embed=embed)
    raise error


# Run the bot with the token
bot.run(config["discord_token"])
