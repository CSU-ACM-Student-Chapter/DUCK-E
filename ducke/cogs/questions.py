from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded, Message, Thread, ChannelType
import asyncio
import logging
import datetime
import random
from typing import List, TypedDict
from ..models.question import Question
from ..constants import constants

_log = logging.getLogger(__name__)

cursor = constants.MYSQL_CONNECTION.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS flash_events (channel_id BIGINT PRIMARY KEY, subject TEXT, seconds_to_answer INT, points INT)''')

class Questions(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.flash_events: FlashEventTypedDict = {}

    SUBJECT_OPTIONS: app_commands.choices = [
        #app_commands.Choice(name="General", value="General"), #TODO: Add General CSV for main channel
        app_commands.Choice(name="Data Structures", value=constants.RESOURCES_QUESTIONS_DATA_STRUCTURES_FILE),
        app_commands.Choice(name="Networking", value=constants.RESOURCES_QUESTIONS_NETWORKING_BASICS_FILE),
        app_commands.Choice(name="AZ 900", value=constants.RESOURCES_QUESTIONS_AZ_900_FILE)
    ]
    
    TIMER_OPTIONS: app_commands.choices = [
        app_commands.Choice(name="1 Minute", value=constants.MINUTE_IN_SECONDS),
        app_commands.Choice(name="5 Minutes", value=constants.MINUTE_IN_SECONDS * 5),
        app_commands.Choice(name="10 Minutes", value=constants.MINUTE_IN_SECONDS * 10),
        app_commands.Choice(name="30 Minutes", value=constants.MINUTE_IN_SECONDS * 30),
        app_commands.Choice(name="1 Hour", value=constants.HOUR_IN_SECONDS),
        app_commands.Choice(name="3 Hours", value=constants.HOUR_IN_SECONDS * 3),
        app_commands.Choice(name="6 Hours", value=constants.HOUR_IN_SECONDS * 6),
        app_commands.Choice(name="1 Day", value=constants.DAY_IN_SECONDS)
    ]

    FLASH_TIMER_OPTIONS: app_commands.choices = [
        app_commands.Choice(name="1 Minute", value=constants.MINUTE_IN_SECONDS),
        app_commands.Choice(name="3 Minutes", value=constants.MINUTE_IN_SECONDS * 3),    
        app_commands.Choice(name="5 Minutes", value=constants.MINUTE_IN_SECONDS * 5),
        app_commands.Choice(name="10 Minutes", value=constants.MINUTE_IN_SECONDS * 10),
    ]

    QUIZ_LENGTH_OPTIONS: app_commands.choices = [
        app_commands.Choice(name="3 Questions", value=3),
        app_commands.Choice(name="5 Questions", value=5),
        app_commands.Choice(name="10 Questions", value=10),
    ]

    @app_commands.command(name="flash-events-start", description="Sends questions at random. React FAST for Pts multiplier bonus!")
    @app_commands.choices(subject=SUBJECT_OPTIONS, seconds_to_answer=FLASH_TIMER_OPTIONS)
    @app_commands.describe(subject="Select a topic", seconds_to_answer="Time allowed to answer")
    @app_commands.rename(seconds_to_answer="minutes_to_answer")
    async def flash_events_start(
        self,
        interaction: Interaction,
        subject: str,
        seconds_to_answer: int
    ) -> None:
        
        try:
            if(not interaction.channel.permissions_for(interaction.guild.me).send_messages or
               not interaction.channel.permissions_for(interaction.guild.me).add_reactions):
                await interaction.response.send_message("❌ I don't have permissions to complete this command in this channel. Please grant access in the Discord Developer Portal.", ephemeral=True)
                return
            
            await interaction.response.send_message("ℹ️ Question flash is starting. An admin must execute /flash-events-stop command to quit", ephemeral=True)
            channel = self.bot.get_channel(interaction.channel_id)
            await self.start_flash_event(channel, subject, seconds_to_answer, constants.POINTS_FOR_CORRECT_FLASH_QUESTION_ANSWER)
        
        except:
            _log.exception(f"[ERROR in /flash-events-start]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the question.")
            except InteractionResponded:
                pass
    
    @app_commands.command(name="flash-events-stop", description="Stops an ongoing question flash event in the channel.")
    async def flash_events_stop(
        self,
        interaction: Interaction
    ) -> None:
        
        try:
            if(not interaction.channel.permissions_for(interaction.guild.me).send_messages):
                await interaction.response.send_message("❌ I don't have permissions to complete this command in this channel. Please grant access in the Discord Developer Portal.", ephemeral=True)
                return
            
            if(not interaction.user.guild_permissions.administrator):
                await interaction.response.send_message("❌ You do not have permission to stop this flash event.", ephemeral=True)
                return
            
            await interaction.response.send_message("ℹ️ Question flash event is being removed.", ephemeral=True)
            channel = self.bot.get_channel(interaction.channel_id)
            await self.stop_flash_event(channel)
        
        except:
            _log.exception(f"[ERROR in /flash-events-stop]")
            try:
                await interaction.followup.send("❌ Something went wrong while stopping the question flash event.")
            except InteractionResponded:
                pass
    
    @app_commands.command(name="question", description="Pulls a random question from the chosen topic and posts it.")
    @app_commands.choices(subject=SUBJECT_OPTIONS, seconds_to_answer=TIMER_OPTIONS)
    @app_commands.describe(subject="Select a topic", seconds_to_answer="Time allowed to answer")
    @app_commands.rename(seconds_to_answer="time_to_answer")
    async def question(
        self,
        interaction: Interaction,
        subject: str,
        seconds_to_answer: int
    ) -> None:
        
        try:

            if(not interaction.channel.permissions_for(interaction.guild.me).send_messages or
               not interaction.channel.permissions_for(interaction.guild.me).add_reactions):
                await interaction.response.send_message("❌ I don't have permissions to complete this command in this channel.", ephemeral=True)
                return
            
            await interaction.response.send_message(f"✅ Question processing.", ephemeral=True) 
            channel = self.bot.get_channel(interaction.channel_id)
            await self.question_handler(channel, subject, seconds_to_answer, constants.POINTS_FOR_CORRECT_QUESTION_ANSWER)
        
        except:
            _log.exception(f"[ERROR in /question]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the question.")
            except InteractionResponded:
                pass

    @app_commands.command(name="quiz", description="Pulls several random questions from the chosen topic and posts it.")
    @app_commands.choices(subject=SUBJECT_OPTIONS, seconds_to_answer=TIMER_OPTIONS, quiz_length=QUIZ_LENGTH_OPTIONS)
    @app_commands.describe(subject="Select a topic", seconds_to_answer="Time allowed to answer")
    @app_commands.rename(seconds_to_answer="time_to_answer")
    async def quiz(
        self,
        interaction: Interaction, 
        subject: app_commands.Choice[str],
        seconds_to_answer: app_commands.Choice[int],
        quiz_length: app_commands.Choice[int]
    ) -> None:
        
        try:
            if(not interaction.channel.permissions_for(interaction.guild.me).send_messages or
               not interaction.channel.permissions_for(interaction.guild.me).add_reactions or
               not interaction.channel.permissions_for(interaction.guild.me).create_public_threads):
                await interaction.response.send_message("❌ I don't have permissions to complete this command in this channel.", ephemeral=True)
                return
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
            await self.quiz_handler(thread, subject.value, seconds_to_answer.value, quiz_length.value, constants.POINTS_FOR_CORRECT_QUIZ_ANSWER)

        except:
            _log.exception(f"[ERROR in /quiz]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the quiz.")
            except InteractionResponded:
                pass

    async def question_handler(
            self,
            channel: Message.channel,
            subject: str,
            seconds_to_answer: int,
            points: int
    ) -> None:

        question: Question = Question(subject, self.bot)

        message: Message = await channel.send(question.formatted_question)
        await question.attach_emojis(message)
        
        await asyncio.sleep(seconds_to_answer)
        message: Message = await message.channel.fetch_message(message.id)
        
        await question.generate_question_response_with_points(message, points)
    
    async def quiz_handler(
            self,
            thread: Thread,
            subject: str,
            seconds_to_answer: int,
            quiz_length: int,
            points_per_question: int
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
            await question.generate_question_response_with_points(message, points_per_question)

    async def start_flash_event(
        self,
        channel: Message.channel,
        subject: str,
        seconds_to_answer: int,
        points: int
    ) -> None:
        
        cursor.execute("SELECT channel_id FROM flash_events WHERE channel_id = %s", (channel.id,))
        result = cursor.fetchone()
        if result:
            await channel.send("❌ A flash event is already registered for this channel.")
            return
        
        cursor.execute("INSERT INTO flash_events (channel_id, subject, seconds_to_answer, points) VALUES (%s, %s, %s, %s)", 
                       (channel.id, subject, seconds_to_answer, points))
        constants.MYSQL_CONNECTION.commit()
        
        flash_event = FlashEvent(
            channel=channel,
            subject=subject,
            seconds_to_answer=seconds_to_answer,
            points=points,
            cog=self
        )
        self.flash_events[channel.id] = flash_event
        await flash_event.start()

    async def stop_flash_event(self, channel: Message.channel) -> None:
        
        cursor.execute("SELECT channel_id FROM flash_events WHERE channel_id = %s", (channel.id,))
        result = cursor.fetchone()
        if not result:
            await channel.send("❌ No flash event is registered for this channel.")
            return
        
        cursor.execute("DELETE FROM flash_events WHERE channel_id = %s", (channel.id,))
        constants.MYSQL_CONNECTION.commit()

        flash_event: FlashEvent = self.flash_events[channel.id]
        await flash_event.stop()
        self.flash_events.pop(channel.id)
        await channel.send("✅ Flash event has been stopped.", ephemeral=True)

    async def restart_flash_events_on_ready(self) -> None:
        cursor.execute("SELECT channel_id, subject, seconds_to_answer, points FROM flash_events")
        results = cursor.fetchall()
        for channel_id, subject, seconds_to_answer, points in results:
            channel = self.bot.get_channel(channel_id)
            if channel:
                flash_event = FlashEvent(
                    channel=channel,
                    subject=subject,
                    seconds_to_answer=seconds_to_answer,
                    points=points,
                    cog=self
                )
                self.flash_events[channel.id] = flash_event
                await flash_event.restart()
                _log.info(f"Restarted flash event in Channel: {channel.name} ID: {channel_id}")

async def setup(bot: commands.Bot) -> None:  
    await bot.add_cog(Questions(bot))

class FlashEvent:

    def __init__(
        self, 
        channel: Message.channel,
        subject: str,
        seconds_to_answer: int,
        points: int,
        cog: Questions
    ):
        self.channel = channel
        self.subject = subject
        self.seconds_to_answer = seconds_to_answer
        self.points = points
        self.cog = cog
        self.task = None

    async def start(self) -> None:
        self.task = asyncio.create_task(self.run())
    
    async def stop(self) -> None:
        if self.task:
            self.task.cancel()

    async def restart(self) -> None:
        await self.stop()
        await self.start()

    async def run(self) -> None:
        
        while True:
            flash_event_period = constants.DAY_IN_SECONDS
            pre_question_delay = random.randint(0, flash_event_period - self.seconds_to_answer)
            post_question_delay = flash_event_period - self.seconds_to_answer - pre_question_delay
            
            await asyncio.sleep(pre_question_delay)
            await self.cog.question_handler(self.channel, self.subject, self.seconds_to_answer, self.points)
            await asyncio.sleep(post_question_delay)

class FlashEventTypedDict(TypedDict):
    channel_id: int
    flash_event: FlashEvent