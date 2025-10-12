from discord.ext import commands
from discord import app_commands, Interaction, InteractionResponded, Message
import asyncio
import logging
from ..models.question import Question
from ..constants import constants

_log = logging.getLogger(__name__)

class Questions(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    response = {
        "winning_message": "",
        "cheating_message": ""
    }

    @app_commands.command(
        name="question", 
        description="Pulls a random question from the chosen topic and posts it."
    )
    @app_commands.describe(
        subject="Select a topic", 
        minutes_to_answer="Time allowed to answer (minutes)"
    )
    @app_commands.choices(
        subject=[
            app_commands.Choice(name="General", value="General"),
            app_commands.Choice(name="Data Structures", value=constants.RESOURCES_QUESTIONS_DATA_STRUCTURES_FILE),
            app_commands.Choice(name="Networking", value=constants.RESOURCES_QUESTIONS_NETWORKING_BASICS_FILE),
            app_commands.Choice(name="AZ 900", value=constants.RESOURCES_QUESTIONS_AZ_900_FILE)
        ],
        minutes_to_answer=[
            app_commands.Choice(name="1 Minute", value=1),
            app_commands.Choice(name="5 Minutes", value=5),
            app_commands.Choice(name="10 Minutes", value=10),
            app_commands.Choice(name="30 Minutes", value=30),
            app_commands.Choice(name="1 Hour", value=60),
            app_commands.Choice(name="3 Hours", value=60 * 3),
            app_commands.Choice(name="6 Hours", value=60 * 6),
            app_commands.Choice(name="1 Day", value=60 * 24)
        ]
    )
    async def question(
        self,
        interaction: Interaction,
        subject: str,
        minutes_to_answer: int
    ):
        await interaction.response.defer()
        try:
            question = Question(subject, self.bot)
            
            message: Message = await interaction.followup.send(question.formatted_question)
            await question.attach_emojis(message)
            
            await asyncio.sleep(minutes_to_answer*8)
            message = await message.channel.fetch_message(message.id)
            
            await question.generate_question_response(message)
        
        except:
            _log.exception(f"[ERROR in /question]")
            try:
                await interaction.followup.send("❌ Something went wrong while processing the question.")
            except InteractionResponded:
                pass

    @app_commands.describe(subject="Select a topic", minutes_to_answer="Time allowed to answer")
    @app_commands.choices(subject=[
            app_commands.Choice(name="General", value="General"),
            app_commands.Choice(name="Data Structures", value=constants.RESOURCES_QUESTIONS_DATA_STRUCTURES_FILE),
            app_commands.Choice(name="Networking", value=constants.RESOURCES_QUESTIONS_NETWORKING_BASICS_FILE),
            app_commands.Choice(name="AZ 900", value=constants.RESOURCES_QUESTIONS_AZ_900_FILE)
        ],
        minutes_to_answer=[
            app_commands.Choice(name="1 Minute", value=1),
            app_commands.Choice(name="5 Minutes", value=5),
            app_commands.Choice(name="10 Minutes", value=10),
            app_commands.Choice(name="30 Minutes", value=30),
            app_commands.Choice(name="1 Hour", value=60),
            app_commands.Choice(name="3 Hours", value=60 * 3),
            app_commands.Choice(name="6 Hours", value=60 * 6),
            app_commands.Choice(name="1 Day", value=60 * 24)
        ]
    )
    async def quiz(
        self,
        interaction: Interaction, 
        subject: str,
        minutes_to_answer: int
        ) -> None:
        
        pass
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Questions(bot))