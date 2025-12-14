from discord import Intents
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging

_log = logging.getLogger(__name__)

load_dotenv('.env')                                         # Load environment variables from .env (e.g., DISCORD_TOKEN='token here')

intents = Intents.default()                                 # Set up default bot intents (permissions)
intents.message_content = True                              # Enable intent to read message content (needed for commands)

bot = commands.Bot(command_prefix='/', intents=intents)     # Create bot object with slash command prefix and default intents

async def setup_hook() -> None:
    try:
        for file in os.listdir("ducke/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                await bot.load_extension(f"ducke.cogs.{file[:-3]}")

        await bot.tree.sync()
        _log.info(f"Commands synced")
    except:
        _log.exception("setup_hook() failed")

bot.setup_hook = setup_hook
bot.run(os.getenv('DISCORD_TOKEN'), root_logger=True)