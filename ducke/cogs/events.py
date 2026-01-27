from .questions import Questions
from discord import Message
from discord.ext import commands, tasks
import logging, datetime
from .points import add_points
from ..constants import constants

_log = logging.getLogger(__name__)

cursor = constants.get_cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS daily_messages (
        user_id BIGINT PRIMARY KEY,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
)
constants.MYSQL_CONNECTION.commit()

class Events(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            questions_cog: Questions = self.bot.get_cog('Questions')
            await questions_cog.restart_flash_events_on_ready()
            _log.info(f'Login as {self.bot.user} successful')
        except:
            _log.exception("on_ready() failed")

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        try: 
            if message.author == self.bot.user:
                return
        
            self._daily_message_handler(message)
        except:
            _log.exception(f"on_message() failed for Message: {message.content} ID: {message.id}")
            
    def _daily_message_handler(self, message: Message) -> None:
        cursor = constants.get_cursor()

        cursor.execute(
            "SELECT 1 FROM daily_messages WHERE user_id = %s",
            (message.author.id,)
        )
        first_message_today: bool = cursor.fetchone() is None


        cursor.execute(
            """
            INSERT INTO daily_messages (user_id, message, timestamp)
            VALUES (%s, %s, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE
            message = VALUES(message), timestamp = CURRENT_TIMESTAMP
            """,
            (message.author.id, message.content)
        )
        constants.MYSQL_CONNECTION.commit() 
        if first_message_today:
            add_points(message.author.id, constants.POINTS_FOR_FIRST_DAILY_MESSAGE)
        else:
            add_points(message.author.id, constants.POINTS_FOR_MESSAGE)

        cursor.close()
    
    @tasks.loop(time=datetime.time.min)
    async def _empty_daily_message(self) -> None:
        cursor = constants.get_cursor()
        cursor.execute("DELETE FROM daily_messages WHERE DATE(timestamp) < CURDATE()")
        constants.MYSQL_CONNECTION.commit()
        cursor.close()
        _log.info("Emptied daily_messages table.")
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
