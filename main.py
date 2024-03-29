"""
File modified under Apache License 2.0
https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/master/bot.py
"""

import discord
import nest_asyncio
import asyncio
import os
import platform
import yaml
import sys
import random

from discord.ext import commands
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

bot = Bot(command_prefix=config["bot_prefix"], case_insensitive=True)

bot.remove_command("help")

flex_list = ['https://cdn.discordapp.com/attachments/710566582845177888/940689395206484008/IMG_1965.jpg',
             'https://cdn.discordapp.com/attachments/710566582845177888/940696039952883772/20220208_134926.jpg',
             'https://cdn.discordapp.com/attachments/710566582845177888/946068676279414794/14AD1CE3-B03E-4AC1-AA28-983CF289D354.jpg']

command_dict = {
        'cool cool cool': 'https://tenor.com/view/andy-samberg-brooklyn99-jake-peralta-cool-gif-12063970',
        'listen here you little shit': 'https://i.pinimg.com/originals/ef/a6/48/efa648c67f3cb05287ded99612af130f.png',
        'suck it': 'https://imgur.com/Fy6RhWI'
    }

pfp_path = "beymax.jpg"
fp = open(pfp_path, 'rb')
pfp = fp.read()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Type !help for commands"))
    await bot.user.edit(avatar=pfp)
    print("\n-------------------")
    print(f'Logged in: {bot.user}')  # show on console
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------\n")
    #affirmation.start()


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


@bot.command(name="reload")
async def reload(ctx):
    """
    Reload extensions so I don't have to reboot the bot when I make changes
    """
    if ctx.message.author.id in config["owners"]:
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    bot.reload_extension(f"cogs.{extension}")
                    print(f"Reloaded extension '{extension}'")
                    embed = discord.Embed (
                        title="Functions have been reloaded"
                    )
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    print(f"Failed to reload extension {extension}\n{exception}")
                    embed = discord.Embed(
                        title="Functions have failed to be reloaded"
                    )
    else:
        embed = discord.Embed(
            title="Error!",
            description="You don't have the permission to use this command.",
            color=config["error"]
        )
    await ctx.channel.send(embed=embed)


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
    if "flex" in ctx.content.lower():
        await ctx.channel.send(random.choice(flex_list))

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


# @tasks.loop(hours=24)
# async def affirmation():
#     url = 'https://www.affirmations.dev'
#
#     request = requests.get(url)
#     affirmation_object = json.loads(request.text)
#
#     # Create embed in Discord
#     embed = discord.Embed(title="Daily Affirmation", color=config["success"])
#     embed.set_thumbnail(url='https://www.pitara.com/media/lotus-flower_hu4aeaffed200a0cfd996c55c6e5156325_90396_600x0_resize_q60_box.jpg')
#     embed.add_field(name='Affirmation', value=affirmation_object['affirmation'])
#
#     # Declare #might-health as destination channel
#     await bot.get_channel(710566582845177888).send(embed=embed)


@bot.command(name='broncena', help='Make Kat hate you forever')
async def join(ctx):
    if ctx.message.author.id in config["owners"]:
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = "broncena-intro.ogg"
                voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=filename))
        except:
            pass
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await ctx.message.delete()
            await asyncio.sleep(13)
            await voice_client.disconnect()
        else:
            pass


@bot.command(name='emotionaldamage', help='EMOTIONAL DAMAGE')
async def join(ctx):
    if ctx.message.author.id in config["owners"]:
        if not ctx.message.author.voice:
            await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = "emotional_damage.mp3"
                voice_channel.play(discord.FFmpegPCMAudio(executable="/usr/bin/ffmpeg", source=filename))
        except:
            pass
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await ctx.message.delete()
            await asyncio.sleep(4)
            await voice_client.disconnect()
        else:
            pass


@bot.command(name='stop', help='Stops the BRON')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# Run the bot with the token
bot.run(config["discord_token"])
