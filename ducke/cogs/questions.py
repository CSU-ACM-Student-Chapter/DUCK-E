'''
TODO:
- Implement a way to stop the question flash events gracefully.
- Turn handler methods to discord tasks.
- Add error handling for invalid subjects.
- Disable commands where permissions are insufficient.
- Add points system for correct answers.
'''

from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded, Message, Thread, ChannelType 
import asyncio
import logging
import datetime
from typing import List
from ..models.question import Question
from ..constants import constants

_log = logging.getLogger(__name__)

class Questions(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    subject_options: app_commands.choices = [
        app_commands.Choice(name="General", value="General"),
        app_commands.Choice(name="Data Structures", value=constants.RESOURCES_QUESTIONS_DATA_STRUCTURES_FILE),
        app_commands.Choice(name="Networking", value=constants.RESOURCES_QUESTIONS_NETWORKING_BASICS_FILE),
        app_commands.Choice(name="AZ 900", value=constants.RESOURCES_QUESTIONS_AZ_900_FILE)
    ]
    
    timer_options: app_commands.choices = [
        app_commands.Choice(name="1 Minute", value=10),
        app_commands.Choice(name="5 Minutes", value=60 * 5),
        app_commands.Choice(name="10 Minutes", value=60 * 10),
        app_commands.Choice(name="30 Minutes", value=60 * 30),
        app_commands.Choice(name="1 Hour", value=60 * 60),
        app_commands.Choice(name="3 Hours", value=60 *60 * 3),
        app_commands.Choice(name="6 Hours", value=60 * 60 * 6),
        app_commands.Choice(name="1 Day", value=60 * 60 * 24)
    ]

    flash_timer_options: app_commands.choices = [
        app_commands.Choice(name="1 Minute", value=10),
        app_commands.Choice(name="3 Minutes", value=60 * 3),    
        app_commands.Choice(name="5 Minutes", value=60 * 5),
        app_commands.Choice(name="10 Minutes", value=60 * 10)
    ]

    frequency_options: app_commands.choices = [
        app_commands.Choice(name="Every 1 Hour", value=60 * 60),
        app_commands.Choice(name="Every 3 Hours", value=60 * 60 * 3),
        app_commands.Choice(name="Every 6 Hours", value=60 * 60 * 6),
        app_commands.Choice(name="Every 12 Hours", value=60 * 60 * 12),
        app_commands.Choice(name="Every 1 Day", value=60 * 60 * 24),
        app_commands.Choice(name="Every 2 Days", value=60 * 60 * 24 * 2),
        app_commands.Choice(name="Every 3 Days", value=60 * 60 * 24 * 3),
    ]

    quiz_length_options: app_commands.choices = [
        app_commands.Choice(name="3 Questions", value=3),
        app_commands.Choice(name="5 Questions", value=5),
        app_commands.Choice(name="10 Questions", value=10),
    ]

    @app_commands.command(name="question", description="Pulls a random question from the chosen topic and posts it.")
    @app_commands.describe(subject="Select a topic", seconds_to_answer="Time allowed to answer (minutes)")
    @app_commands.choices(subject=subject_options, seconds_to_answer=timer_options)
    @app_commands.rename(seconds_to_answer="minutes_to_answer")
    async def question(
        self,
        interaction: Interaction,
        subject: str,
        seconds_to_answer: int
    ) -> None:
        
        try:

            await interaction.response.send_message(f"✅ Question processing.", ephemeral=True) 
            channel = self.bot.get_channel(interaction.channel_id)
            await self.question_handler(channel, subject, seconds_to_answer)
        
        except:
            _log.exception(f"[ERROR in /question]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the question.")
            except InteractionResponded:
                pass

    @app_commands.command(name="question-flash-events", description="Sends questions at random. React FAST for Pts multiplier bonus!")
    @app_commands.describe(subject="Select a topic", question_frequency="How often to post question to channel", seconds_to_answer="Time allowed to answer")
    @app_commands.choices(subject=subject_options, question_frequency=frequency_options, seconds_to_answer=timer_options)
    @app_commands.rename(seconds_to_answer="minutes_to_answer")
    async def question_flash_events(    
        self,
        interaction: Interaction,
        subject: str,
        seconds_to_answer: int,
        question_frequency: int
    ) -> None:
        
        try:
            await interaction.response.send_message("✅ Question flash event started! A mod or admin must execute /end-task command to quit", ephemeral=True)
            channel = self.bot.get_channel(interaction.channel_id)
            await self.question_flash_events_handler(channel, subject, seconds_to_answer, question_frequency)
        
        except:
            _log.exception(f"[ERROR in /question-flash-events]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the question.")
            except InteractionResponded:
                pass

    @app_commands.command(name="quiz", description="Pulls several random questions from the chosen topic and posts it.")
    @app_commands.describe(subject="Select a topic", seconds_to_answer="Time allowed to answer")
    @app_commands.choices(subject=subject_options, seconds_to_answer=flash_timer_options, quiz_length=quiz_length_options)
    @app_commands.rename(seconds_to_answer="minutes_to_answer")
    async def quiz(
        self,
        interaction: Interaction, 
        subject: app_commands.Choice[str],
        seconds_to_answer: app_commands.Choice[int],
        quiz_length: app_commands.Choice[int]
    ) -> None:
        
        try:
            await interaction.response.send_message(f"✅ Quiz processing.", ephemeral=True) 
            channel = self.bot.get_channel(interaction.channel_id)

            if isinstance(interaction.channel, Thread):
                thread: Thread = channel
                await channel.send(f"### Quiz Started by {interaction.user.mention}!")
            else:

                thread_name = f"Quiz-{subject.name}-{datetime.date.today()}"

                thread_exists = False
                for t in channel.threads:
                    if t.name == thread_name:
                        thread_exists = True
                        thread: Thread = t

                if not thread_exists:
                    thread: Thread = await channel.create_thread(name=thread_name, type=ChannelType.public_thread)
                
                await channel.send(f"**Quiz started by {interaction.user.mention}! Quiz has been created in {thread.name}.**")

            await thread.send(f"## Quiz\n**Questions:** {quiz_length.value}\n**Subject:** {subject.name}\n**Time to answer:** {seconds_to_answer.name}\n**Quiz Start Time:** {datetime.datetime.now().strftime("%H:%M %b-%d")}\n**Quiz End Time:** {(datetime.datetime.now() + datetime.timedelta(seconds=seconds_to_answer.value)).strftime("%H:%M %b-%d")}")  
            await self.quiz_handler(thread, subject.value, seconds_to_answer.value, quiz_length.value)

        except:
            _log.exception(f"[ERROR in /quiz]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the quiz.")
            except InteractionResponded:
                pass
        

    async def question_flash_events_handler(
        self,
        channel: Message.channel,
        subject: str,
        seconds_to_answer: int,
        question_frequency: int
    ) -> None:
        
        await self.question_handler(channel, subject, seconds_to_answer)
        await asyncio.sleep(question_frequency)
        await self.question_flash_events_handler(channel, subject, seconds_to_answer, question_frequency)
        
    async def question_handler(
            self,
            channel: Message.channel,
            subject: str,
            seconds_to_answer: int
    ) -> None:

        question: Question = Question(subject, self.bot)

        message: Message = await channel.send(question.formatted_question)
        await question.attach_emojis(message)
        
        await asyncio.sleep(seconds_to_answer)
        message: Message = await message.channel.fetch_message(message.id)
        
        await question.generate_question_response(message)
    
    async def quiz_handler(
            self,
            thread: Thread,
            subject: str,
            seconds_to_answer: int,
            quiz_length: int
    ) -> None:
        
        questions: List[Question] = [Question(subject, self.bot) for _ in range(quiz_length)]
        
        messages: List[Message] = []
        for question in questions:
            message = await thread.send(question.formatted_question)
            messages.append(message)
            await asyncio.sleep(0.5)

        for message, question in zip(messages, questions):
            await question.attach_emojis(message)
            
        await asyncio.sleep(seconds_to_answer)

        for message, question in zip(messages, questions):
            message = await message.channel.fetch_message(message.id)
            await question.generate_question_response(message)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Questions(bot))