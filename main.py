'''
Grabbing Questions
TODO: Get questions from any website into its own CSV file for a given topic. 
TODO: Add conditional in question for channel, if already open question, cancel and send a 'cancellation' statement
"There is already an open question in this channel./n{Question}" 
TODO: Allow users to select their subject, this subject will then decide which table to obtain question from.
    Subjects: All, Tech-Trivia, Algorithms, Networking, CyberSecurity, AI & Machine Learning

TODO: Look into putting functionality to grab a random question into a different file

Checking Questions
TODO: Add functionality to grab answers from user. If a conditional is already in place to only allow 1 question per channel. 
        Then this should only need to check the channel to obtain the current question.
'''
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import datetime, time, asyncio
import pandas as pd
import random

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
STEP 3: ASYNCRONOUS OBSERVER FOR COMMANDS ON THE SERVER
'''

@bot.tree.command(name="question", description="Gives a random question. Not yet atleast but one day!")
async def question(inter: discord.Interaction, reoccuring: bool, subject: str):
    await inter.response.send_message(get_question())

@bot.tree.command(name="answer", description="Takes in an answer and notifies if the answer is correct or not")
async def question(inter: discord.Interaction):
    await inter.response.send_message("")

@bot.tree.command(name="announcement", description="Announces information to the club")
async def schedule_message(inter: discord.Interaction, mention: int):
    now = datetime.datetime.now()
    #then = now+datetime.timedelta(minute)
    then = now.replace(hour=20, minute=41)
    print(then)
    print(now)
    wait_time = (then-now).total_seconds()
    print(wait_time)
    await asyncio.sleep(wait_time)
    await inter.response.send_message("Question Testing")

@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("{}{}{}".format((message.upper() + " "), message + " ", message.lower() + " "))

@bot.tree.command(name="ping", description="Bots Latency")
async def ping(inter: discord.Interaction) -> None:
    '''Get the bots latency'''
    await inter.response.send_message(f"Pong! ({round(bot.latency * 1000)}ms)")

def get_question() -> str:
    df = pd.read_csv('Questions/algorithms.csv')
    questions = len(df)-1
    
    question = str(df.iat[questions, 0])
    return question

'''
STEP 0: RUNNING BOT
'''
bot.run(os.getenv('DISCORD_TOKEN'))