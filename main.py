import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

'''
STEP 1: SETTING UP ENVIRONMENT AND OBJECTS NEEDED FOR BOT
'''
load_dotenv('.env')                                         # Load environment variables from .env (e.g., DISCORD_TOKEN)

intents = discord.Intents.default()                         # Set up default bot intents (permissions)
intents.message_content = True                              # Enable intent to read message content (needed for commands)

bot = commands.Bot(command_prefix='/', intents=intents)     # Create bot object with slash command prefix

'''
STEP 2: SYNCING AND PRINTING AN ON READY MESSAGE TO THE TERMINAL
'''
@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')
    try:
        await setup_hook(bot)
    except Exception as e:
        print(e)

async def setup_hook(bot: commands.Bot):
        for file in os.listdir("./cogs"):
            if file.endswith(".py") and not file.startswith("_"):
                await bot.load_extension(f"cogs.{file[:-3]}")

'''
STEP 3: RUNNING BOT
'''
bot.run(os.getenv('DISCORD_TOKEN'))