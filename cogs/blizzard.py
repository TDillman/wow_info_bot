import os
import sys
import yaml
import json
import requests
import discord
import time

from discord.ext import commands
from blizzardapi import BlizzardApi
from dataclasses import dataclass, field
from datetime import datetime

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

api_client = BlizzardApi(config["blizzard_client_id"], config["blizzard_secret_id"])

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


class Blizzard(commands.Cog, name="blizzard"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="summary")
    async def summary(self, ctx, arg):
        """
        Gives a character summary for officers to quicky determine if a character is raid-ready.
            Usage: !summary Character-Server
            If the character is on Arygos, just do !summary Character
        """
        begin_time = datetime.now()
        try:
            name_list = arg.split("-", 1)

            character_name = None
            server_slug = None
            if len(name_list) == 1:
                character_name = name_list[0].lower()
                server_slug = 'arygos'
            else:
                character_name = name_list[0].lower()
                server_slug = name_list[1].lower().replace("'", "").replace(" ", "")

            try:
                with open(f'/home/ubuntu/might_bot/gear/{character_name.capitalize()}.json', 'r') as gear_file:
                    character_gear_object = json.loads(gear_file.read())
                    print(f'\tGear: Grabbing from file: /home/ubuntu/might_bot/gear/{character_name.capitalize()}.json')
                    character_name_object = character_gear_object['name']
                    character_player_class_object = character_gear_object['character_class']['name']
                    character_level_object = character_gear_object['level']
                    character_race_object = character_gear_object['race']['name']
                    character_spec_object = character_gear_object['active_spec']['name']
                    character_faction_object = character_gear_object['faction']['name']
                    character_realm_object = character_gear_object['realm']['name']
                    character_ilvl_avg_object = character_gear_object['average_item_level']
                    character_ilvl_equip_object = character_gear_object['equipped_item_level']
                    character_class_color_object = hex(
                        discord_embed_color_dict[character_gear_object['character_class']['name']])
                    character_ach_points_object = f'{character_gear_object["achievement_points"]:,}'
                    character_last_login_object = datetime.fromtimestamp(
                        (character_gear_object['last_login_timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            except:
                try:
                    character_gear_object = api_client.wow.profile.get_character_profile_summary("us", "en_US",
                                                                                                 server_slug,
                                                                                                 character_name)
                    print('\tGear: Pulling from Armory')
                    character_name_object = character_gear_object['name']
                    character_player_class_object = character_gear_object['character_class']['name']
                    character_level_object = character_gear_object['level']
                    character_race_object = character_gear_object['race']['name']
                    character_spec_object = character_gear_object['active_spec']['name']
                    character_faction_object = character_gear_object['faction']['name']
                    character_realm_object = character_gear_object['realm']['name']
                    character_ilvl_avg_object = character_gear_object['average_item_level']
                    character_ilvl_equip_object = character_gear_object['equipped_item_level']
                    character_class_color_object = hex(
                        discord_embed_color_dict[character_gear_object['character_class']['name']])
                    character_ach_points_object = f'{character_gear_object["achievement_points"]:,}'
                    character_last_login_object = datetime.fromtimestamp(
                        (character_gear_object['last_login_timestamp']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    print('\t\tCharacter not found')
                    character_name_object = character_name.capitalize()
                    character_player_class_object = 'Character not found'
                    character_level_object = 0
                    character_race_object = 'Character not found'
                    character_spec_object = 'Character not found'
                    character_faction_object = 'Character not found'
                    character_realm_object = server_slug.capitalize()
                    character_ilvl_avg_object = 0
                    character_ilvl_equip_object = 0
                    character_class_color_object = 0
                    character_ach_points_object = 0
                    character_last_login_object = 'Character not found'

            try:
                with open(f'/home/ubuntu/might_bot/media/{character_name.capitalize()}.json', 'r') as media_file:
                    character_image_object = json.loads(media_file.read())
                    print(
                        f'\tImage: Grabbing from file: /home/ubuntu/might_bot/media/{character_name.capitalize()}.json')
                    character_image_object_inset = character_image_object['assets'][1]['value']
                    character_image_object_avatar = character_image_object['assets'][0]['value']
                    character_image_object_full_bg = character_image_object['assets'][2]['value']
                    character_image_object_full_no_bg = character_image_object['assets'][3]['value']
            except:
                try:
                    character_image_object = api_client.wow.profile.get_character_media_summary("us", "en_US",
                                                                                                server_slug,
                                                                                                character_name)
                    print('\tImage: Pulling from Armory')
                    character_image_object_inset = character_image_object['assets'][1]['value']
                    character_image_object_avatar = character_image_object['assets'][0]['value']
                    character_image_object_full_bg = character_image_object['assets'][2]['value']
                    character_image_object_full_no_bg = character_image_object['assets'][3]['value']
                except:
                    print('\t\tCharacter not found')
                    character_image_object_inset = 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'
                    character_image_object_avatar = 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'
                    character_image_object_full_bg = 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'
                    character_image_object_full_no_bg = 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'

            try:
                with open(f'/home/ubuntu/might_bot/equipment/{character_name.capitalize()}.json',
                          'r') as equipment_file:
                    character_equipment_object = json.loads(equipment_file.read())
                    print(
                        f'\tEquipment: Grabbing from file: /home/ubuntu/might_bot/equipment/{character_name.capitalize()}.json')
            except:
                try:
                    character_equipment_object = api_client.wow.profile.get_character_equipment_summary("us", "en_US",
                                                                                                        server_slug,
                                                                                                        character_name)
                    print('\tEquipment: Pulling from Armory')
                except:
                    print('\t\tCharacter not found')

            # Raider.io stats
            raider_io_api_url = (
                f'https://raider.io/api/v1/characters/profile?region=us&realm={server_slug}'
                f'&name={character_name}&fields=mythic_plus_scores_by_season%3Acurrent%2Craid_progression'
            )
            raider_io_object_raw = requests.get(raider_io_api_url)

            if raider_io_object_raw.ok:
                raider_io_object = raider_io_object_raw.json()
                raider_io_overall = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['all']
                raider_io_dps = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['dps']
                raider_io_heal = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['healer']
                raider_io_tank = raider_io_object['mythic_plus_scores_by_season'][0]['scores']['tank']
                raider_io_nathria = raider_io_object['raid_progression']['castle-nathria']['summary']
                raider_io_sanky_d = raider_io_object['raid_progression']['sanctum-of-domination']['summary']
                raider_io_sofo = raider_io_object['raid_progression']['sepulcher-of-the-first-ones']['summary']
            else:
                raider_io_overall = "Unavailable"
                raider_io_dps = "Unavailable"
                raider_io_heal = "Unavailable"
                raider_io_tank = "Unavailable"
                raider_io_nathria = "Unavailable"
                raider_io_sanky_d = "Unavailable"
                raider_io_sofo = "Unavailable"

            try:
                covenant_name = character_gear_object['covenant_progress']['chosen_covenant']['name']
                covenant_renown = character_gear_object['covenant_progress']['renown_level']
            except:
                covenant_name = "None selected"
                covenant_renown = 0

            try:
                char_guild = character_gear_object['guild']['name']
            except:
                char_guild = "None"

            @dataclass
            class Character:
                """Object for a player's character attributes"""
                name: str = character_name_object
                player_class: str = character_player_class_object
                level: int = character_level_object
                race: str = character_race_object
                spec: str = character_spec_object
                guild: str = char_guild
                faction: str = character_faction_object
                realm: str = character_realm_object
                ilvl_avg: int = character_ilvl_avg_object
                ilvl_equip: int = character_ilvl_equip_object
                cov_name: str = covenant_name
                cov_renown: int = covenant_renown
                inset_image: str = character_image_object_inset
                avatar_image: str = character_image_object_avatar
                full_image_bg: str = character_image_object_full_bg
                full_image_no_bg: str = character_image_object_full_no_bg
                class_color: str = character_class_color_object
                overall_io_rating: float = raider_io_overall
                dps_io_rating: float = raider_io_dps
                healer_io_rating: float = raider_io_heal
                tank_io_rating: float = raider_io_tank
                nathria_raid_prog: str = raider_io_nathria
                sanky_d_raid_prog: str = raider_io_sanky_d
                sofo_raid_prog: str = raider_io_sofo
                raider_io_url: str = f'https://raider.io/characters/us/{server_slug}/{character_name}'
                armory_url: str = f'https://worldofwarcraft.com/en-us/character/us/{server_slug}/{character_name}'
                warcraftlogs_url: str = f'https://www.warcraftlogs.com/character/us/{server_slug}/{character_name}'
                achievement_points: int = character_ach_points_object
                last_login: str = character_last_login_object

            character = Character()

            name_string = f"{character.name}, level {character.level} {character.race} {character.spec} {character.player_class}"

            guild_string = f"[{character.guild}](https://worldofwarcraft.com/en-us/guild/us/{server_slug}/{character.guild.replace(' ','-')})" \
                           f"\n{character.faction} on {character.realm}"

            ilvl_string = f"Average ilvl: {character.ilvl_avg}\nEquipped ilvl: {character.ilvl_equip}"

            covenant_string = f"{character.cov_name}\nRenown {character.cov_renown}"

            enchant_string = ''
            for x in range(len(character_equipment_object['equipped_items'])):
                try:
                    enchant_string += f"{character_equipment_object['equipped_items'][x]['enchantments'][0]['source_item']['name']}\n"
                except:
                    pass

            if not enchant_string:
                enchant_string = "No enchantments detected"

            legendary_string =""
            for x in range(len(character_equipment_object['equipped_items'])):
                if character_gear_object['level'] < 60:
                    legendary_string = "Character under level 60"
                elif character_equipment_object['equipped_items'][x]['quality']['name'] == "Legendary" and \
                        character_equipment_object['equipped_items'][x]['level']['value'] < 190:
                    legendary_string = "No Legendary"
                elif character_equipment_object['equipped_items'][x]['quality']['name'] == "Legendary":
                    legendary_string += (f"{character_equipment_object['equipped_items'][x]['name']}\n"
                                         f"{character_equipment_object['equipped_items'][x]['level']['display_string']}\n")

            raider_io_mplus_string = f'Overall rating: {character.overall_io_rating}\n' \
                                     f'DPS rating: {character.dps_io_rating}\n' \
                                     f'Healer rating: {character.healer_io_rating}\n' \
                                     f'Tank rating: {character.tank_io_rating}'

            raider_io_raid_string = f'Nathria: {character.nathria_raid_prog}\n' \
                                    f'Sanctum: {character.sanky_d_raid_prog}\n' \
                                    f'Sepulcher: {character.sofo_raid_prog}'

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
            embed.set_footer(text=f'Executed in {datetime.now() - begin_time}')
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

    @commands.command(pass_context=True, name="token")
    async def token(self, ctx):
        """
        Returns an embed with the current WoW token price in gold
        """
        token_object = api_client.wow.game_data.get_token_index("us", "en_US")

        embed = discord.Embed(title='WoW Token')
        embed.add_field(name='Current Price', value=f'{token_object["price"] / 10000:,.0f} gold')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcolored'
                'finishedsmall.png')
        await ctx.channel.send(embed=embed)

        time.sleep(.25)
        await ctx.message.delete()

    @commands.command(pass_context=True, name="status", aliases=["serverstatus", "arygos"])
    async def status(self, ctx):
        """
        Returns an embed with the current status (up/down) of Arygos
        """
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
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/676183284123828236/679823287521771602/mightcolored'
                'finishedsmall.png')
        await ctx.channel.send(embed=embed)

        time.sleep(.25)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Blizzard(bot))
