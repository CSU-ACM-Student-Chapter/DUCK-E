from discord.ext import commands, tasks
import datetime
from discord import app_commands, Interaction, InteractionResponded
from ..models.joke import Joke
from ..constants import constants
import logging

_log = logging.getLogger(__name__)

cursor = constants.MYSQL_CONNECTION.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS jokes (server_guid BIGINT PRIMARY KEY, jokes INT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

class Fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    '''
    @app_commands.command(name="code-hangman", description="Get the bots Latency")
    async def code_hangman(self, interaction: Interaction, phrase: str) -> None:
        try:
            await interaction.response.send_message(f"{interaction.user.mention} started a game of Code Hangman. Guess correctly to win points!")
        except:
            _log.exception(f"[ERROR in /ping]")
            try:
                await interaction.followup.send("❌ Something went wrong while setting up the game.")
            except InteractionResponded:
                pass
    '''

    @app_commands.command(name="tell-a-joke", description="Lighten the mood with a joke")
    async def tell_joke(self, interaction: Interaction) -> None:
        try:
            if self._has_reached_daily_joke_limit(interaction.guild.id):
                await interaction.response.send_message("❌ The daily joke limit for the day has been reached. Try again tomorrow 00:00 GMT!", ephemeral=True)
                return
            
            await interaction.response.send_message("Joke processing...", ephemeral=True)

            joke = Joke(self.bot)
        
            await joke.announce_joke(interaction.channel, interaction.user)
            await joke.tell_joke(interaction.channel)

            self._increase_daily_joke_count(interaction.guild.id)
        except:
            _log.exception(f"[ERROR in /tell-a-joke]")
            try:
                await interaction.followup.send("❌ Something went wrong while trying to tell a joke.")
            except InteractionResponded:
                pass

    @tasks.loop(time=datetime.time.min)
    async def _reset_daily_joke_limit(self) -> None:
        cursor.execute("DELETE FROM jokes WHERE DATE(timestamp) < CURDATE()")
        constants.MYSQL_CONNECTION.commit()
        _log.info("Emptied jokes table.")

    def _has_reached_daily_joke_limit(self, server_guid: int) -> bool:
        cursor.execute(
            """
            SELECT jokes FROM jokes
            WHERE server_guid = %s AND DATE(timestamp) = CURDATE()
            """,
            (server_guid,)
        )
        result = cursor.fetchone()
        if result is not None and result[0] >= 3:
            return True
        return False
    
    def _increase_daily_joke_count(self, server_guid: int) -> None:
        cursor.execute(
            """
            INSERT INTO jokes (server_guid, jokes, timestamp)
            VALUES (%s, 1, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE
            jokes = jokes + 1, timestamp = CURRENT_TIMESTAMP
            """,
            (server_guid,)
        )

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))