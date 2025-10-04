from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded

class Meta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Get the bots Latency")
    async def ping(self, interaction: Interaction) -> None:
        """
        Returns: 
            None (Command)

        Parameters: 
            interaction (Interaction): An action that needs to be notified

        Functionality: 
            Get the latency of the bot.
        """
        try:
            await interaction.response.send_message(f"Pong! ({round(self.bot.latency * 1000)}ms)")
        except Exception as e:
            print(f"[ERROR in /ping] {e}")
            try:
                await interaction.followup.send("❌ Something went wrong while pinging the bot client.")
            except InteractionResponded:
                pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Meta(bot))

    
