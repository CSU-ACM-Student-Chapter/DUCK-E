import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# This example requires the 'message_content' intent.
load_dotenv('.env')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!'):
        await hello(message)

    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')

@bot.command
async def hello(message):
    await message.channel.send(f"Hello {message.author.id}")
    
client.run(os.getenv('DISCORD_TOKEN'))