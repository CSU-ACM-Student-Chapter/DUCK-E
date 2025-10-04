from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded, Message
import asyncio
import os
import glob
import random
import pandas as pd

class Questions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="question", description="Give a random question")
    @app_commands.describe(subject="Select a topic", minutes_to_answer="Time allowed to answer")
    @app_commands.choices(subject=[
        app_commands.Choice(name="General", value="General"),
        app_commands.Choice(name="Data Structures", value="data structure basics"),
        app_commands.Choice(name="Networking", value="networking basics"),
        app_commands.Choice(name="AZ 900", value="az 900"),
    ])
    async def question(self, interaction: Interaction, subject: app_commands.Choice[str], minutes_to_answer: int):
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
            if not self.valid_subject(subject):
                await interaction.followup.send(f"Invalid subject. {self.available_subjects()}") 
            
            formatted_question, question, answer, answer_list, answer_emojis = self.get_question(subject)
            
            message = await interaction.followup.send(formatted_question) 
            await self.attach_emojis(answer_emojis, message)
            
            await asyncio.sleep(minutes_to_answer*8)  
            message = await message.channel.fetch_message(message.id)
            
            await self.check_answers(message, answer_emojis[answer])
            await message.channel.send(f"**Answer:** {answer_emojis[answer]} {answer_list[answer]}")
        except Exception as e:
            print(f"[ERROR in /question] {e}")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the question.")
            except InteractionResponded:
                pass

    @app_commands.command(name="quiz", description="Grab 10 random questions to give a quiz on")
    async def quiz(interaction: Interaction, subject: str, minutes_to_answer: int) -> None:
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

    # Get random question & answer from the subjects respective csv file
    def get_question(self, subject: str) -> None:
        df = pd.read_csv(f'cogs/resources/questions/{subject}.csv')
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
        answer = self.match_letter_to_number(str(df.iat[question_row,5]))
        return formatted_question, question, answer, answer_list, answer_emojis

    # TODO: Add function to check 
    # Check if provided string is an available subject to pull questions from
    def valid_subject(self, subject: str) -> bool:
        #self.available_subjects()
        return True

    def available_subjects(self) -> list:
        full_path = os.path.join(os.getcwd(), 'cogs/resources/questions')
        csv_files = glob.glob(os.path.join(full_path, "*.csv"))
        return csv_files

    # Attach a list of emojis to a discord message
    async def attach_emojis(self, emojis: list, message: Message) -> None:
        for emoji in emojis:
            await message.add_reaction(emoji)

    # Get the winners and cheaters of a question and send a message to the server
    async def check_answers(self, message: Message, answer_emoji: str) -> None:
        cheaters = await self.duplicate_reacts(message)
        winners = await self.correct_reacts(message, answer_emoji, cheaters)

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
    async def duplicate_reacts(self, message: object) -> list:
        users_list = []
        duplicates = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                if user != self.bot.user:
                    users_list.append(user)
                    if users_list.count(user) > 1:
                        duplicates.add(user)
                
        return list(duplicates)

    # Find users that gave a matching reaction and do not appear in the list of cheaters
    async def correct_reacts(self, message: object, answer_emoji: object, cheaters: set) -> list:
        correct_users = set()
        for reaction in message.reactions:
            if (reaction.emoji == answer_emoji):
                async for user in reaction.users():
                    if user != self.bot.user and user not in cheaters:                    
                        correct_users.add(user)
        
        return list(correct_users)

    # Match 0,1,2,3 to A,B,C,D respectively
    def match_letter_to_number(self, answer: str)-> int:
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
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Questions(bot))