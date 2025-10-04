from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded

class Staff(commands.Cog):

    def __init__(self, bot):
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
    async def announcement(self, interaction: Interaction, month: app_commands.Choice[int], day: int, hour: app_commands.Choice[int], message: str) -> None:
        """
        Returns:
            None (Command)
        Parameters:
            interaction (Interaction):      The interaction that triggered the command
            month app_commands.Choice[int]: Month selected to send the message
            day (int):                      Day of the month between 1-31
            hour app_commands.Choice[int]:  Hour selected between 0-23
            message (str):                  The message to announce at a later date

        Functionality:
            (To be implemented) Announces the message at the specified date and time within the current year. 
        """
        try:
            await interaction.response.send_message("ACM is currently working on this command. Please be patient.")
        except Exception as e:
            print(f"[ERROR in /announcement] {e}")
            try:
                await interaction.followup.send("❌ Something went wrong while making the announcement.")
            except InteractionResponded:
                pass
    
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Staff(bot))