import discord
import requests
import nest_asyncio
import time
import os
import logging
import random

from discord.ext import commands
from blizzardapi import BlizzardApi
from datetime import datetime
from dataclasses import dataclass, field

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

nest_asyncio.apply()

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
discord_access_token = os.environ['DISCORD_ACCESS_TOKEN']

api_client = BlizzardApi(client_id, client_secret)

bot = commands.Bot(command_prefix="!", case_insensitive=True)

# Set side bar color in Discord embed
discord_embed_color_dict = {
    'Death Knight': 0xC41E3A,
    'Demon Hunter': 0xA330C9,
    'Druid': 0xFF7C0A,
    'Hunter': 0xAAD372,
    'Mage': 0x3FC7EB,
    'Monk': 0x00FF98,
    'Paladin': 0xF48CBA,
    'Priest': 0xFFFFFF,
    'Rogue': 0xFFF468,
    'Shaman': 0x0070DD,
    'Warlock': 0x8788EE,
    'Warrior': 0xC69B6D
}

footer = 'Might Infobot by Beylock-Arygos\nCommand executed at'


@bot.event
async def on_ready():
    print(f'Logged in: {bot.user}')  # show on console
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='Type !commands'))


@bot.command()
async def summary(ctx, arg):
    if ctx.author == bot.user:
        return
    try:
        print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
              f'{ctx.message.content} in the #{ctx.channel.name} channel')

        name_list = arg.split("-", 1)

        character_name = None
        server_slug = None
        if len(name_list) == 1:
            character_name = name_list[0].lower()
            server_slug = 'arygos'
        else:
            character_name = name_list[0].lower()
            server_slug = name_list[1].lower().replace("'", "").replace(" ", "")

        character_gear_object = api_client.wow.profile.get_character_profile_summary("us", "en_US", server_slug,
                                                                                     character_name)

        character_image_object = api_client.wow.profile.get_character_media_summary("us", "en_US", server_slug,
                                                                                    character_name)

        character_equipment_object = api_client.wow.profile.get_character_equipment_summary("us", "en_US", server_slug,
                                                                                            character_name)

        # Raider.io stats
        raider_io_api_url = (
            f'https://raider.io/api/v1/characters/profile?region=us&realm={server_slug}'
            f'&name={character_name}&fields=mythic_plus_scores_by_season%3Acurrent%2Craid_progression'
        )
        raider_io_object = requests.get(raider_io_api_url).json()

        @dataclass
        class Character:
            """Object for a player's character attributes"""
            name: str = character_gear_object['name']
            player_class: str = character_gear_object['character_class']['name']
            level: int = character_gear_object['level']
            race: str = character_gear_object['race']['name']
            spec: str = character_gear_object['active_spec']['name']
            guild: str = character_gear_object['guild']['name']
            faction: str = character_gear_object['faction']['name']
            realm: str = character_gear_object['realm']['name']
            ilvl_avg: int = character_gear_object['average_item_level']
            ilvl_equip: int = character_gear_object['equipped_item_level']
            cov_name: str = character_gear_object['covenant_progress']['chosen_covenant']['name']
            cov_renown: int = character_gear_object['covenant_progress']['renown_level']
            inset_image: str = character_image_object['assets'][1]['value']
            avatar_image: str = character_image_object['assets'][0]['value']
            full_image_bg: str = character_image_object['assets'][2]['value']
            full_image_no_bg: str = character_image_object['assets'][3]['value']
            class_color: str = hex(discord_embed_color_dict[character_gear_object['character_class']['name']])
            overall_io_rating: float = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['all']
            dps_io_rating: float = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['dps']
            healer_io_rating: float = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['healer']
            tank_io_rating: float = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['tank']
            nathria_raid_prog: str = raider_io_object['raid_progression']['castle-nathria']['summary']
            raider_io_url: str = f'https://raider.io/characters/us/{server_slug}/{character_name}'
            armory_url: str = f'https://worldofwarcraft.com/en-us/character/us/{server_slug}/{character_name}'
            warcraftlogs_url: str = f'https://www.warcraftlogs.com/character/us/{server_slug}/{character_name}'
            achievement_points: int = f'{character_gear_object["achievement_points"]:,}'
            last_login: str = datetime.fromtimestamp(
                (character_gear_object['last_login_timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

        character = Character()

        name_string = f"{character.name}, level {character.level} {character.race} {character.spec} {character.player_class}"

        guild_string = f"[{character.guild}](https://worldofwarcraft.com/en-us/guild/us/{server_slug}/{character.guild})" \
                       f"\n{character.faction} on {character.realm}"

        ilvl_string = f"Average ilvl: {character.ilvl_avg}\nEquipped ilvl: {character.ilvl_equip}"

        covenant_string = f"{character.cov_name}\nRenown {character.cov_renown}"

        enchant_string = ''
        for x in range(len(character_equipment_object['equipped_items'])):
            try:
                enchant_string += f"{character_equipment_object['equipped_items'][x]['enchantments'][0]['source_item']['name']}\n"
            except:
                pass

        legendary_string = None
        for x in range(len(character_equipment_object['equipped_items'])):
            if character_gear_object['level'] < 60:
                legendary_string = "No Legendary"
            elif character_equipment_object['equipped_items'][x]['quality']['name'] == "Legendary" and \
                    character_equipment_object['equipped_items'][x]['level']['value'] < 190:
                legendary_string = "No Legendary"
            elif character_equipment_object['equipped_items'][x]['quality']['name'] == "Legendary":
                legendary_string = (f"{character_equipment_object['equipped_items'][x]['name']}\n"
                                    f"{character_equipment_object['equipped_items'][x]['level']['display_string']}")

        raider_io_mplus_string = f'Overall rating: {character.overall_io_rating}\n' \
                                 f'DPS rating: {character.dps_io_rating}\n' \
                                 f'Healer rating: {character.healer_io_rating}\n' \
                                 f'Tank rating: {character.tank_io_rating}'

        raider_io_raid_string = f'Nathria: {character.nathria_raid_prog}'

        discord_embed_color = discord_embed_color_dict[character.player_class]

        # Create embed in Discord
        embed = discord.Embed(title=name_string, color=discord_embed_color)
        embed.set_author(name="Character Summary")
        embed.description = f'[Raider.io]({character.raider_io_url}) | [Armory]({character.armory_url})' \
                            f' | [Warcraft Logs]({character.warcraftlogs_url})'
        embed.add_field(name="Gear", value=ilvl_string, inline=True)
        embed.add_field(name="Guild", value=guild_string, inline=True)
        embed.add_field(name="Covenant", value=covenant_string, inline=True)
        embed.add_field(name='Raid Progression', value=raider_io_raid_string, inline=True)
        embed.add_field(name="Legendary", value=legendary_string, inline=True)
        embed.add_field(name="Raider.io Ratings\nCurrent Season", value=raider_io_mplus_string, inline=True)
        embed.add_field(name="Enchants", value=enchant_string, inline=True)
        embed.add_field(name="Achievement Points", value=character.achievement_points, inline=False)
        embed.add_field(name="Last login", value=character.last_login, inline=True)
        embed.add_field(name="Character images", value=f'[Avatar]({character.inset_image})\n'
                                                       f'[Headshot]({character.avatar_image})\n'
                                                       f'[Full body with background]({character.full_image_bg})\n'
                                                       f'[Full body no background]({character.full_image_no_bg})',
                        inline=False)
        embed.set_thumbnail(url=character.inset_image)
        embed.set_footer(text=f'{footer} {datetime.now()}')

        # Send embed, delete message
        await ctx.author.send(embed=embed)
        await ctx.message.delete()

    except KeyError:
        await ctx.author.send(
            f"Unable to find character {character.name}-{character.realm}. Check spelling "
            f"or wait til Blizzard sorts out their Armory problems")
        print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
              f'{ctx.message.content}. Error.')
        await ctx.message.delete()
    except IndexError:
        await ctx.author.send("Format error. Make sure it's in the form of Character-Server")
        print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
              f'{ctx.message.content}. Error.')
        await ctx.message.delete()


winner_dict = {}


@bot.command(pass_context=True)
async def win(ctx, *args):
    print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
          f'{ctx.message.content} in the #{ctx.channel.name} channel')
    if ctx.author == bot.user:
        return

    role = discord.utils.get(ctx.guild.roles, name="Officer")
    if role in ctx.author.roles:
        unpacked_list = [*args]
        unpacked_list_lower = []

        async for ctx.message in ctx.channel.history(limit=1):
            if ctx.message.author == bot.user:
                await ctx.message.delete()

        for string in unpacked_list:
            unpacked_list_lower.append(string.lower())

        for x in unpacked_list_lower:
            if x == "display":
                break
            if x == 'resetpvp':
                winner_dict.clear()
                break
            if x.startswith('-'):
                x = x.split('-')[1]
                winner_dict[x] -= 1
                if winner_dict[x] < 1:
                    winner_dict.pop(x, None)
            else:
                winner_dict[x] = winner_dict.get(x, 0) + 1

        scoreboard = ''
        if winner_dict:
            for name, score in sorted(winner_dict.items(), key=lambda item: item[1], reverse=True):
                scoreboard += f'{name.title()}: {score}\n'
        else:
            scoreboard = 'No winners yet'

        embed = discord.Embed(title=f'Might 2021 Battleground Contest', description='*March 23 through March 30*\n'
                                                                                    'First Place:\t125,000 :coin:\n'
                                                                                    'Second Place:\t90,000 :coin:\n'
                                                                                    'Third Place:\t35,000 :coin:',
                              color=0x14D804)
        embed.add_field(name='Current Scores:', value=scoreboard)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/'
                                'mightcoloredfinishedsmall.png')
        embed.set_image(url='https://i.imgur.com/ZnIwBzf.png')
        embed.set_footer(text=f'{footer} {datetime.now()}')
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.channel.send("You're not an officer! Quit trying to cheat")


@bot.command(pass_context=True)
async def ironman(ctx):
    print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
          f'{ctx.message.content} in the #{ctx.channel.name} channel')

    if ctx.author == bot.user:
        return

    guild_roster = api_client.wow.profile.get_guild_roster("us", "en_US", "arygos", "might")

    rank_dict = {"GM": 0, "Officer": 1, "Officer Alt": 2, "Raider": 3, "Ready to Raid": 4, "Main": 5, "Alt": 6,
                 "Leveling": 7, "Ironman": 8, "New Invite": 9}

    roster_list = [guild_roster["members"][y]["character"]["name"] for y in range(len(guild_roster["members"])) if
                   guild_roster["members"][y]["rank"] == rank_dict["Ironman"]]

    server_list = ['arygos', 'llane']
    ironman_list = []
    ironman_scoreboard = ''

    for server in server_list:
        for name in roster_list:
            try:
                character = api_client.wow.profile.get_character_profile_summary("us", "en_US", server.lower(),
                                                                                 name.lower())
                ironman_list.append((f"{character['name']}: {character['race']['name']} "
                                     f"{character['active_spec']['name']} {character['character_class']['name']}, "
                                     f"Level {character['level']}"))
            except KeyError:
                pass

    for item in ironman_list:
        ironman_scoreboard += f'{item}\n'

    embed = discord.Embed(title=f'Might 2021 Ironman Contest')
    embed.add_field(name='Current Participants:', value=ironman_scoreboard)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcolored'
                            'finishedsmall.png')
    embed.set_footer(text=f'{footer} {datetime.now()}')
    await ctx.channel.send(embed=embed)
    await ctx.message.delete()


@bot.command(pass_context=True)
async def token(ctx):
    print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
          f'{ctx.message.content} in the #{ctx.channel.name} channel')

    if ctx.author == bot.user:
        return

    token_object = api_client.wow.game_data.get_token_index("us", "en_US")

    embed = discord.Embed(title='WoW Token')
    embed.add_field(name='Current Price', value=f'{token_object["price"]/10000:,.0f} gold')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcolored'
                            'finishedsmall.png')
    embed.set_footer(text=f'{footer} {datetime.now()}')
    await ctx.channel.send(embed=embed)

    time.sleep(.25)
    await ctx.message.delete()


@bot.command(pass_context=True)
async def status(ctx):
    print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
          f'{ctx.message.content} in the #{ctx.channel.name} channel')

    if ctx.author == bot.user:
        return

    server_object = api_client.wow.game_data.get_connected_realm("us", "en_US", 99)

    @dataclass
    class Server:
        """Object to store data about Arygos for status updates"""
        status: str = server_object['status']['name']
        population: str = server_object['population']['name']
        has_queue: bool = server_object['has_queue']
        region: str = server_object['realms'][0]['region']['name']
        country: str = server_object['realms'][0]['category']
        timezone: str = server_object['realms'][0]['timezone']
        connections: list = field(default_factory=lambda: [server_object['realms'][x]['name'] for x in
                                                           range(len(server_object['realms']))])
        name: str = 'Arygos'

    server = Server()

    if server.status == "Up":
        status_color = 0x00ff00  # Green for up
    else:
        status_color = 0xff0000  # Red for down

    server_string = ', '.join(str(name) for name in server.connections)

    embed = discord.Embed(title='Arygos', color=status_color)
    embed.add_field(name='Current Status', value=f'Server is currently {server.status}', inline=True)
    if server.population == 'Offline':
        embed.add_field(name='Current Population', value=f'This server is currently {server.population}')
    else:
        embed.add_field(name='Current Population', value=f'This is a {server.population} pop server', inline=True)
    embed.add_field(name='Connected Realms', value=server_string, inline=False)
    if server.has_queue:
        embed.add_field(name='Queue Active', value='Server has a login queue')
    embed.add_field(name="Timezone", value=server.timezone, inline=True)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcolored'
                            'finishedsmall.png')
    embed.set_footer(text=f'{footer} {datetime.now()}')
    await ctx.channel.send(embed=embed)

    time.sleep(.25)
    await ctx.message.delete()


@bot.command()
async def talk(ctx, *, arg):
    await ctx.message.delete()
    await ctx.channel.send(arg)


@bot.command()
async def sim(ctx):
    pass


@bot.command()
async def raidbots(ctx):
    pass


@bot.command()
async def commands(ctx):
    if ctx.author == bot.user:
        return

    print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
          f'{ctx.message.content} in the #{ctx.channel.name} channel')


    await ctx.author.send(
        "Chat commands: \n\n!summary Character-Server\n!status\n!token\n!custom\n"
        "This bot is configured to have Arygos as the default server, so if your character is on Arygos, you don't need"
        " to specify the realm"
    )

    time.sleep(.25)
    await ctx.message.delete()


@bot.command()
async def custom(ctx):
    if ctx.author == bot.user:
        return

    print(f'{datetime.now()}: {ctx.message.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
          f'{ctx.message.content} in the #{ctx.channel.name} channel')

    await ctx.author.send(
        'Custom commands: \n\n!scrumpy\n!golfclap\n!spooky\n!whatever\n!cool\n!myst\n!beylock\n!flex\n!happybirthday'
        '\n!magic\n!lynkz\n!calendar\n!candercane\n!pirate\n!thisisfine\n!wat\n!justice\n!thisisfine\n!pirate\n!suckit'
    )

    time.sleep(.25)
    await ctx.message.delete()


# There has to be a better way to do this
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    def print_to_console():
        print(f'{datetime.now()}: {ctx.guild.name} -- {ctx.author.display_name} ({ctx.author}) ran '
              f'"{ctx.content}" in the #{ctx.channel.name} channel')

    shit_list = ['https://i.pinimg.com/originals/ef/a6/48/efa648c67f3cb05287ded99612af130f.png',
                 'https://i.kym-cdn.com/entries/icons/original/000/017/372/ClmrSzk.jpg.png',
                 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTAuOPyTLmaoq6hrHNNUnNzzk9_OeRtpLX80g&usqp=CAU',
                 'https://i.kym-cdn.com/photos/images/facebook/000/917/464/752.jpg',
                 'https://memegenerator.net/img/instances/40808454/listen-here-you-little-shit.jpg',
                 'https://ih1.redbubble.net/image.1045539425.2307/poster,840x830,f8f8f8-pad,1000x1000,f8f8f8.jpg',
                 'https://memegenerator.net/img/instances/71923924/listen-here-you-little-shit.jpg',
                 'https://pics.ballmemes.com/listen-here-you-little-shit-8006247.png']

    if '!scrumpy' in ctx.content.lower():
        await ctx.channel.send('Thinks your bags are awful')
        print_to_console()
    if '!calendar' in ctx.content.lower():
        await ctx.channel.send('<@267888830634262529> needs to update the calendar!')
        print_to_console()
    if '!golfclap' in ctx.content.lower():
        await ctx.channel.send('https://tenor.com/view/charlie-sheen-emilio-estevez-golf-clap-men-at-work-gif-7577611')
        print_to_console()
    if '!spooky' in ctx.content.lower():
        await ctx.channel.send('https://img1.cgtrader.com/items/1911482/ca45cf3f32/'
                               'air-horn-3d-model-max-obj-mtl-3ds-fbx-dxf.jpg')
        print_to_console()
    if '!whatever' in ctx.content.lower():
        await ctx.channel.send('https://media.discordapp.net/attachments/765619338337058827/802299499908563024/'
                               'whatever.gif')
        print_to_console()
    if '!cool' in ctx.content.lower() or 'cool cool cool' in ctx.content.lower():
        await ctx.channel.send('https://tenor.com/view/andy-samberg-brooklyn99-jake-peralta-cool-gif-12063970')
        print_to_console()
    if '!myst' in ctx.content.lower():
        await ctx.channel.send('https://tenor.com/view/is-it-though-thor-smile-gif-13334930')
        print_to_console()
    if '!beylock' in ctx.content.lower():
        await ctx.channel.send('https://imgur.com/a/xux2u6p')
        print_to_console()
    if 'flex' in ctx.content.lower():
        await ctx.channel.send(
            'https://cdn.discordapp.com/attachments/676183284123828236/823278892676022353/image0.jpg')
        print_to_console()
    if '!happybirthday' in ctx.content.lower():
        await ctx.channel.send('https://giphy.com/gifs/i8htPQwChFOVcpnImq')
        print_to_console()
    if '!magic' in ctx.content.lower():
        await ctx.channel.send('https://media.discordapp.net/attachments/676183284123828236/761438362720272394/'
                               'Kat_Confetti.gif')
        print_to_console()
    if '!lynkz' in ctx.content.lower():
        await ctx.channel.send(
            'https://tenor.com/view/james-franco-fuck-that-dude-fuckoff-annoyed-annoying-gif-11146686')
        print_to_console()
    if 'listen here you little shit' in ctx.content.lower():
        await ctx.channel.send(random.choice(shit_list))
        print_to_console()
    if '!candercane' in ctx.content.lower():
        await ctx.channel.send('https://giphy.com/gifs/angry-mad-anger-l1J9u3TZfpmeDLkD6')
        print_to_console()
    if '!wat' in ctx.content.lower():
        await ctx.channel.send('https://imgur.com/a/PnB5eFk')
        print_to_console()
    if '!thisisfine' in ctx.content.lower() or 'this is fine' in ctx.content.lower():
        await ctx.channel.send('https://imgur.com/a/uDAO5In')
        print_to_console()
    if '!pirate' in ctx.content.lower():
        await ctx.channel.send('https://imgur.com/a/TDot4Ba')
        print_to_console()
    if '!justice' in ctx.content.lower():
        await ctx.channel.send('https://gfycat.com/adorablespotlesshammerheadbird')
        print_to_console()
    if '!suckit' in ctx.content.lower() or 'suck it' in ctx.content.lower():
        await ctx.channel.send('https://imgur.com/Fy6RhWI')
        print_to_console()

    # Without the following line, the bot gets stuck and won't process commands
    await bot.process_commands(ctx)

bot.run(discord_access_token)
