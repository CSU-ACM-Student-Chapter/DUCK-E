# https://www.reddit.com/r/Discord_Bots/comments/wcqdfh/how_to_import_commands_from_a_cog_within_a_cog/
from discord.ext import commands

class Points(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Points(bot))