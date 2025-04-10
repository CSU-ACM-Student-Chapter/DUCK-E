'''
Grabbing Questions

TODO: Allow users to select their subject, this subject will then decide which table to obtain question from.
    Subjects: All, Tech-Trivia, Algorithms, Networking, CyberSecurity, AI & Machine Learning
TODO: Look into putting functionality to grab a random question into a different file

Checking Questions
TODO: Add functionality to grab answers from user. If a conditional is already in place to only allow 1 question per channel. 
        Then this should only need to check the channel to obtain the current question.
''' 

import discord
import os
import datetime, time
import glob
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import asyncio
import pandas as pd
import random

'''
Commands:
    announcement():     (Planned) Announces the message at the specified date and time.
    echo():             Echoes the user's message in uppercase, original, and lowercase formats.
    ping():             Responds with "Pong!" and the bot's current latency in milliseconds.
    question():         Posts a random multiple-choice question from a selected topic, allows reactions, and evaluates answers.
    quiz():             (Planned) Will provide 10 random questions from a selected topic as a quiz format.

Helper Functions: 
    attach_emojis(emojis: list, message: discord.Message) -> None:
        Attach a list of emojis to a discord message
    
    get_question():                            
        Fetches and formats a question and answer set from a topic CSV file.
    
    check_answers(message, answer_emoji):      
        Analyzes reactions to determine correct answers and cheaters.
    
    match_letter_to_number(answer: str) -> int: 
        Converts A/B/C/D to 0/1/2/3 for answer indexing.
'''

'''
STEP 1: SETTING UP ENVIRONMENT AND OBJECTS NEEDED FOR BOT
'''
load_dotenv('.env')                                         # Load environment variables from .env (e.g., DISCORD_TOKEN)

intents = discord.Intents.default()                         # Set up default bot intents (permissions)
intents.message_content = True                              # Enable intent to read message content (needed for commands)

bot = commands.Bot(command_prefix='/', intents=intents)     # Create bot object with slash command prefix
tree = bot.tree                                             # Reference the bot’s command tree for slash commands

'''
STEP 2: PRINTING AN ON READY MESSAGE TO THE TERMINAL
'''
@bot.event
async def on_ready() -> None:
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

'''
STEP 3: ASYNCRONOUS OBSERVER FOR COMMANDS ON THE SERVER
'''
@bot.tree.command(name="announcements", description="Schedule an announcement for the server.")
@app_commands.describe(
    month="Select a month",
    day="Select a day (1-31)",
    hour="Select an hour (24H format 0-23)",
    message="Announcement message",
)
@app_commands.choices(
    month=[
        app_commands.Choice(name="January", value="1"),
        app_commands.Choice(name="February", value="2"),
        app_commands.Choice(name="March", value="3"),
        app_commands.Choice(name="April", value="4"),
        app_commands.Choice(name="May", value="5"),
        app_commands.Choice(name="June", value="6"),
        app_commands.Choice(name="July", value="7"),
        app_commands.Choice(name="August", value="8"),
        app_commands.Choice(name="September", value="9"),
        app_commands.Choice(name="October", value="10"),
        app_commands.Choice(name="November", value="11"),
        app_commands.Choice(name="December", value="12"),
    ],
    hour=[
        app_commands.Choice(name=f"{i:02d}:00", value=i) for i in range(0, 24)
    ],
)
async def announcement(interaction: discord.Interaction, month: app_commands.Choice[int], day: int, hour: app_commands.Choice[int], message: str) -> None:
    """
    Returns:
        None (Command)

    Parameters:
        interaction (Interaction):      The interaction that triggered the command
        month app_commands.Choice[int]: Date and time to send the message
        day (int):                      Day of the month between 1-31
        hour app_commands.Choice[int]:    
        message (str):                  The message to announce at a later date

    Functionality:
        (To be implemented) Announces the message at the specified date and time. 
    """
    try:
        await interaction.response.send_message("ACM is currently working on this command. Please be patient.")
    except Exception as e:
        print(f"[ERROR in /announcement] {e}")
        try:
            await interaction.followup.send("❌ Something went wrong while making the announcement.")
        except discord.InteractionResponded:
            pass

@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str) -> None:
    """
    Returns:
        None (Command)

    Parameters:
        interaction (Interaction): The interaction that triggered the command
        message (str): The message to echo back

    Functionality:
        Echo the message in uppercase, normal case, and lowercase.
    """
    try:
        await interaction.response.send_message("{}{}{}".format((message.upper() + " "), message + " ", message.lower() + " "))
    except Exception as e:
        print(f"[ERROR in /echo] {e}")
        try:
            await interaction.followup.send("❌ Something went wrong while echoing.")
        except discord.InteractionResponded:
            pass

@bot.tree.command(name="ping", description="Get the bots Latency")
async def ping(interaction: discord.Interaction) -> None:
    """
    Returns: 
        None (Command)

    Parameters: 
        inter (Interaction):        An action that needs to be notified

    Functionality: 
        Get the latency of the bot.
    """
    try:
        await interaction.response.send_message(f"Pong! ({round(bot.latency * 1000)}ms)")
    except Exception as e:
        print(f"[ERROR in /ping] {e}")
        try:
            await interaction.followup.send("❌ Something went wrong while pinging the bot client.")
        except discord.InteractionResponded:
            pass

'''
Quiz and Question Commands 
+ Helper Functions
'''

@bot.tree.command(name="question", description="Give a random question")
@app_commands.describe(subject="Select a topic", minutes_to_answer="Time allowed to answer")
@app_commands.choices(subject=[
    app_commands.Choice(name="General", value="General"),
    app_commands.Choice(name="Data Structures", value="data structure basics"),
    app_commands.Choice(name="Networking", value="networking basics"),
    app_commands.Choice(name="AZ 900", value="az 900"),
])
async def question(interaction: discord.Interaction, subject: app_commands.Choice[str], minutes_to_answer: int):
    """
    Returns:
        None (Command)

    Parameters:
        interaction (Interaction): The interaction that triggered the command
        subject (str): Subject/topic to pull questions from
        minutes_to_answer (int): How long users have to answer before results are shown

    Functionality:
        Pull a random question from the chosen topic and post it to the server.
        Attach reactions for answers. Wait, check, and report correct responses.
    """
    await interaction.response.defer()
    try:
        subject = subject.value.lower()
        if not valid_subject(subject):
            await interaction.followup.send(f"Invalid subject. {available_subjects()}") 
        
        formatted_question, question, answer, answer_list, answer_emojis = get_question(subject)
        
        message = await interaction.followup.send(formatted_question) 
        await attach_emojis(answer_emojis, message)
        
        await asyncio.sleep(minutes_to_answer*8)  
        message = await message.channel.fetch_message(message.id)
        
        await check_answers(message, answer_emojis[answer])
        await message.channel.send(f"**Answer:** {answer_emojis[answer]} {answer_list[answer]}")
    except Exception as e:
        print(f"[ERROR in /question] {e}")
        try:
            await interaction.followup.send("❌ Something went wrong while processing the question.")
        except discord.InteractionResponded:
            pass

@bot.tree.command(name="quiz", description="Grab 10 random questions to give a quiz on")
async def quiz(interaction: discord.Interaction, subject: str, minutes_to_answer: int) -> None:
    """
    Returns:
        None (Command)

    Parameters:
        interaction (Interaction): The interaction that triggered the command
        subject (str): The quiz topic to select questions from
        minutes_to_answer (int): Time users have to answer each question

    Functionality:
        (Not implemented yet) Will eventually pull 10 random questions and quiz users.
    """
    pass

'''
HELPER FUNCTIONS
'''

# Get random question & answer from the subjects respective csv file
def get_question(subject: str) -> None:
    df = pd.read_csv(f'Questions/{subject}.csv')
    question_row = random.randint(0, len(df)-1)
    question = str(df.iat[question_row, 0])
    a = str(df.iat[question_row,1])
    b = str(df.iat[question_row,2])
    c = str(df.iat[question_row,3])
    d = str(df.iat[question_row,4])
    answer_list = [a, b, c, d]
    answer_emojis = ['🇦', '🇧', '🇨', '🇩']
    
    formatted_question = f"**{question}**\n\
        **A:** {answer_list[0]}\n\
        **B:** {answer_list[1]}\n\
        **C:** {answer_list[2]}\n\
        **D:** {answer_list[3]}\n"
    answer = match_letter_to_number(str(df.iat[question_row,5]))
    return formatted_question, question, answer, answer_list, answer_emojis

# TODO: Add function to check 
# Check if provided string is an available subject to pull questions from
def valid_subject(subject: str) -> bool:
    available_subjects()
    return True

def available_subjects() -> list:
    full_path = os.path.join(os.getcwd(), 'Questions')
    csv_files = glob.glob(os.path.join(full_path, "*.csv"))
    return csv_files

# Attach a list of emojis to a discord message
async def attach_emojis(emojis: list, message: discord.Message) -> None:
    for emoji in emojis:
        await message.add_reaction(emoji)

# Get the winners and cheaters of a question and send a message to the server
async def check_answers(message: discord.Message, answer_emoji: str) -> None:
    cheaters = await duplicate_reacts(message)
    winners = await correct_reacts(message, answer_emoji, cheaters)

    if cheaters:
        cheating_users =""
        for cheater in cheaters:
            cheating_users += f"{cheater}"
            cheating_users += ", " if len(cheaters) > 2 and cheater != cheaters[:-1] else " "
            cheating_users += "& " if len(cheaters) > 1 and cheater == cheaters[:-2] else ""

        await message.channel.send(f"Multiple answers were given by {cheating_users}.🤥 Minus 10 points that don't exist yet!")
    
    if winners:
        winning_users = ""
        for winner in winners:
            winning_users += f"{winner}"
            winning_users += ", " if len(winners) > 2 and winner != winners[:-1] else " "
            winning_users += "& " if len(winners) > 1 and winner == winners[:-2] else ""
        
        await message.channel.send(f"Congratulation to {winning_users} for getting the question right!😁")
    else:
        await message.channel.send(f"No correct or valid answers 😢")

# Find any users that gave more two reactions           
async def duplicate_reacts(message: object) -> list:
    users_list = []
    duplicates = set()
    for reaction in message.reactions:
        async for user in reaction.users():
            if user != bot.user:
                users_list.append(user)
                if users_list.count(user) > 1:
                    duplicates.add(user)
            
    return list(duplicates)

# Find users that gave a matching reaction and do not appear in the list of cheaters
async def correct_reacts(message: object, answer_emoji: object, cheaters: set) -> list:
    correct_users = set()
    for reaction in message.reactions:
        if (reaction.emoji == answer_emoji):
            async for user in reaction.users():
                if user != bot.user and user not in cheaters:                    
                    correct_users.add(user)
    
    return list(correct_users)

# Match 0,1,2,3 to A,B,C,D respectively
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
Points Management Commands
+ Helper Functions
'''

async def points(users: list, action: app_commands.Choice[str], points: int) ->None:
    for user in users:
        pass
        

'''
STEP 0: RUNNING BOT
'''
bot.run(os.getenv('DISCORD_TOKEN'))