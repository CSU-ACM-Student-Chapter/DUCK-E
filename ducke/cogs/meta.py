from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded
import logging

_log = logging.getLogger(__name__)

class Meta(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Get the bots Latency")
    async def ping(self, interaction: Interaction) -> None:
        try:
            await interaction.response.send_message(f"Pong! ({round(self.bot.latency * 1000)}ms)")
        except:
            _log.exception(f"[ERROR in /ping]")
            try:
                await interaction.followup.send("❌ Something went wrong while pinging the bot client.")
            except InteractionResponded:
                pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meta(bot))