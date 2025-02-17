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
async def question(inter: discord.Interaction, subject: str, minutes_to_answer: int):
    await inter.response.defer()
    question, answer, choices = get_question()
    answer_emojis = ['🇦', '🇧', '🇨', '🇩']
    
    question = f"**{question}**\n**A:** {choices[0]}\n\
        **B:** {choices[1]}\n\
        **C:** {choices[2]}\n\
        **D:** {choices[3]}\n"
    
    msg = await inter.followup.send(question) 
    for emoji in answer_emojis:
        await msg.add_reaction(emoji)
    
    await asyncio.sleep(minutes_to_answer*8)  
    msg = await msg.channel.fetch_message(msg.id)
    
    await check_answers(msg, answer_emojis[answer])
    await msg.channel.send(f"**Answer:** {choices[answer]}")

@bot.tree.command(name="quiz", description="Will grab 10 random questions to give a quiz on")
async def quiz(inter: discord.Interaction, subject: str, minutes_to_answer: int):
    pass

@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("{}{}{}".format((message.upper() + " "), message + " ", message.lower() + " "))

@bot.tree.command(name="ping", description="Bots Latency")
async def ping(inter: discord.Interaction) -> None:
    '''Get the bots latency'''
    await inter.response.send_message(f"Pong! ({round(bot.latency * 1000)}ms)")

'''
OTHER FUNCTIONS
'''

# Gets random question & answer from subjects respective csv file
def get_question():
    df = pd.read_csv('Questions/algorithms.csv')
    questions = len(df)-1
    questions = random.randint(0, questions)
    question = str(df.iat[questions, 0])
    a = str(df.iat[questions,1])
    b = str(df.iat[questions,2])
    c = str(df.iat[questions,3])
    d = str(df.iat[questions,4])
    choices = [a, b, c, d]
    answer = match_letter_to_number(str(df.iat[questions,5]))
    return question, answer, choices

async def check_answers(message: object, answer_emoji: object):
    '''
    Need to break up the two functions below
    await check_duplicates()
    await verify_answers()
    '''
    # Check duplicates, will get called out if spamming all reacts
    
    # Grab list of the users for all question reactions
    users_list = []
    for reaction in message.reactions:
        async for user in reaction.users():
            if user != bot.user:
                users_list.append(user.name)

    # Check for duplicates in users list
    user_set = set()
    cheating_users = ""
    print(users_list)
    for user in users_list:
        print(user_set)
        if user in user_set:
            cheating_users += f'{user}, '
            print(user)
        else:
            user_set.add(user)

    cheating_users = cheating_users[:-2]
    print(user_set)
    print(cheating_users)
        
            
    # Check correct users
    for reaction in message.reactions:
        if (reaction.emoji == answer_emoji):
            correct_users = ""
            async for user in reaction.users():
                if user != bot.user:
                    correct_users += f'{user.name}, '
            correct_users = correct_users[:-2]
                
    await message.channel.send(f"Congratulation to {correct_users} for getting the question right!\n \
                               The correct answer was {answer_emoji}")
    
    if(len(cheating_users)>0):
        await message.channel.send(f"Multiple answers were given by {cheating_users}. Minus 10 points!")
              

def match_letter_to_number(answer: str)-> int:
    if str(answer).strip().upper() == "A":
        return 0
    elif str(answer).strip().upper() == "B":
        return 1
    elif str(answer).strip().upper() == "C":
        return 2
    elif str(answer).strip().upper() == "D":
        return 3
    else:
        return -1

'''
STEP 0: RUNNING BOT
'''
bot.run(os.getenv('DISCORD_TOKEN'))