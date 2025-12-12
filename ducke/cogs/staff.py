from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded
import logging

_log = logging.getLogger(__name__)

class Staff(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="announcements", description="Schedule an announcement for the server.")
    @app_commands.describe(
        month="Select a month",
        day="Select a day (1-31)",
        hour="Select an hour (24H format 0-23)",
        message="Announcement message"
    )
    @app_commands.choices(month=[
            app_commands.Choice(name="January", value=1),
            app_commands.Choice(name="February", value=2),
            app_commands.Choice(name="March", value=3),
            app_commands.Choice(name="April", value=4),
            app_commands.Choice(name="May", value=5),
            app_commands.Choice(name="June", value=6),
            app_commands.Choice(name="July", value=7),
            app_commands.Choice(name="August", value=8),
            app_commands.Choice(name="September", value=9),
            app_commands.Choice(name="October", value=10),
            app_commands.Choice(name="November", value=11),
            app_commands.Choice(name="December", value=12)
        ],
        hour=[
            app_commands.Choice(name=f"{i:02d}:00", value=i) for i in range(0, 24)
        ]
    )
    async def announcement(self, interaction: Interaction, month: int, day: int, hour: int, message: str) -> None:
        try:
            await interaction.response.send_message("ACM is currently working on this command. Please be patient.")
        except:
            _log.exception(f"[ERROR in /announcement]")
            try:
                await interaction.followup.send("❌ Something went wrong while making the announcement.")
            except InteractionResponded:
                pass
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Staff(bot))