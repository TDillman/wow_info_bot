import sys
import yaml
import discord

from youtube_easy_api.easy_wrapper import *
from discord.ext import commands

if not os.path.isfile("config.yaml"):
    sys.exit("'config.yaml' not found! Please add it and try again.")
else:
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

youtube_wrapper = YoutubeEasyWrapper()
youtube_wrapper.initialize(api_key=config["youtube_api_key"])


class Jams(commands.Cog, name="jams"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="jams")
    async def jams(self, ctx, *, args):
        """
        Links a YouTube video with the requested search result
            Usage: !jams Gaslight Anthem
        """
        try:
            results = youtube_wrapper.search_videos(search_keyword=args, order='relevance')
        except HttpError:
            await ctx.channel.send("We're over our YouTube API quota. Whoops. It'll reset over night. Sorry.")
        video_string = ''.replace('&#39;', '\'')
        if len(results) == 0:
            await ctx.channel.send(f"No results for {args}")
        else:
            youtube_video_url = f"https://www.youtube.com/watch?v={results[0]['video_id']}"
            await ctx.channel.send(youtube_video_url)
            embed = discord.Embed(
                title=f"Not what you're looking for?",
                color=config["success"]
            )
            if len(results) < 5:
                for video in results[1:len(results)]:
                    video_string += f"[{video['title']}](https://www.youtube.com/watch?v={video['video_id']})\n"
            if len(results) >= 5:
                for video in results[1:6]:
                    video_string += f"[{video['title']}](https://www.youtube.com/watch?v={video['video_id']})\n"
        embed.add_field(
            name=f"More relevant videos for {args}:",
            value=video_string
        )
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Jams(bot))
