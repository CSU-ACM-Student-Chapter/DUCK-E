# Should be used for admin tasks and commands. Commands will require 
# admin role priviledges. And tasks will contain for example Web Site Filtering
from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded
import logging

_log = logging.getLogger(__name__)

class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="sync", description="Sync Commands")
    async def sync(self, interaction: Interaction) -> None:
        try:
            await self.bot.tree.sync()

        except:
            _log.exception(f"[ERROR in /sync]")
            try:
                await interaction.followup.send("❌ Something went wrong while trying to sync commands.", ephemeral=True)
            except InteractionResponded:
                pass  

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))