from discord.ext import commands
import logging

_log = logging.getLogger(__name__)

class Events(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            _log.info(f'We have logged in as {self.bot.user}')
        except:
            _log.exception("on_ready() failed")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
