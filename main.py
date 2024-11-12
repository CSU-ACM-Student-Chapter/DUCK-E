'''
TODO: Clean
'''
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import datetime, asyncio

'''
STEP 1: SETTING UP ENVIRONMENT AND OBJECTS NEEDED FOR BOT
'''
load_dotenv('.env')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
tree = bot.tree

'''
STEP 2: PRINTING AN ON READY MESSAGE TO THE TERMINAL
'''
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)
'''
STEP 3: ASYNCRONOUS OBSERVER FOR MESSAGES ON THE SERVER
'''

'''
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')
'''

@bot.tree.command(name="question", description="Gives a random question. Not yet least but one day!")
async def schedule_daily_message(inter: discord.Interaction):
    now = datetime.datetime.now()
    #then = now+datetime.timedelta(minute)
    then = now.replace(hour=20, minute=41)
    print(then)
    print(now)
    wait_time = (then-now).total_seconds()
    print(wait_time)
    await asyncio.sleep(wait_time)
    await inter.response.send_message("Question Testing")

'''
Commands
'''
@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("{}{}{}".format((message.upper() + " "), message + " ", message.lower() + " "))

@bot.tree.command(name="ping", description="Bots Latency")
async def ping(inter: discord.Interaction) -> None:
    '''Get the bots latency'''
    await inter.response.send_message(f"Pong! ({round(bot.latency * 1000)}ms)")
    '''
    try:
        await inter.response.send_message(f"Trying to send a second message...")
    except discord.InteractionResponded:
        await inter.followup.send(f"Responding again failed, as expected.")
    '''     

'''
STEP 0: RUNNING BOT
'''  
bot.run(os.getenv('DISCORD_TOKEN'))