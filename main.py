import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import logging

_log = logging.getLogger(__name__)

load_dotenv('.env')                                         # Load environment variables from .env (e.g., DISCORD_TOKEN='token here')

intents = discord.Intents.default()                         # Set up default bot intents (permissions)
intents.message_content = True                              # Enable intent to read message content (needed for commands)

bot = commands.Bot(command_prefix='/', intents=intents)     # Create bot object with slash command prefix and default intents

@bot.event
async def on_ready() -> None:
    try:
        await setup_hook(bot)
        _log.info(f'We have logged in as {bot.user}')
        await bot.tree.sync()
        _log.info(f"Commands synced")
    except Exception as e:
        _log.exception("on_ready() failed")

async def setup_hook(bot: commands.Bot) -> None:
        for file in os.listdir("ducke/cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                await bot.load_extension(f"ducke.cogs.{file[:-3]}")

bot.run(os.getenv('DISCORD_TOKEN'), root_logger=True)