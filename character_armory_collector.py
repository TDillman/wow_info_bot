import os
import json

from alive_progress import alive_bar
from blizzardapi import BlizzardApi

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

api_client = BlizzardApi(client_id, client_secret)

server_slug = 'arygos'
guild_name = 'might'

guild_roster = api_client.wow.profile.get_guild_roster("us", "en_US", server_slug, guild_name)

char_list = [guild_roster['members'][x]['character']['name'] for x in
             range(len(guild_roster['members'])) if guild_roster['members'][x]['character']['level'] == 60]

char_list.sort()

with alive_bar(len(char_list)) as bar:
    for character_name in char_list:
        try:
            character_gear_object = json.dumps(api_client.wow.profile.get_character_profile_summary("us", "en_US", server_slug,
                                                                                                    character_name.lower()))
            with open(f"/home/ubuntu/might_bot/gear/{character_name}.json", "w") as gear_file:
                gear_file.write(character_gear_object)
        except:
            os.remove(f"/home/ubuntu/might_bot/gear/{character_name}.json")

        try:
            character_image_object = json.dumps(api_client.wow.profile.get_character_media_summary("us", "en_US", server_slug,
                                                                                                   character_name.lower()))
            with open(f"/home/ubuntu/might_bot/media/{character_name}.json", "w") as media_file:
                media_file.write(character_image_object)
        except:
            os.remove(f"/home/ubuntu/might_bot/media/{character_name}.json")

        try:
            character_equipment_object = json.dumps(api_client.wow.profile.get_character_equipment_summary("us", "en_US", server_slug,
                                                                                                           character_name.lower()))
            with open(f"/home/ubuntu/might_bot/equipment/{character_name}.json", "w") as equipment_file:
                equipment_file.write(character_equipment_object)
        except:
            os.remove(f"/home/ubuntu/might_bot/equipment/{character_name}.json")

        try:
            character_achievement_object = json.dumps(api_client.wow.profile.get_character_achievements_summary("us", "en_US", server_slug,
                                                                                                                character_name.lower()))
            with open(f"/home/ubuntu/might_bot/achievement/{character_name}.json", "w") as achievement_file:
                achievement_file.write(character_achievement_object)
        except:
            os.remove(f"/home/ubuntu/might_bot/achievement/{character_name}.json")

        bar()
