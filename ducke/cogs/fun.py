from discord.ext import commands
import logging

_log = logging.getLogger(__name__)

class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))