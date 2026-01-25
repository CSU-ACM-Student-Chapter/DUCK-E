import random
import pandas as pd
import os
import re
from discord import Message,Thread, TextChannel, File
from discord.ext import commands
from ..constants import constants
import ducke.cogs.points as points_cog

class Question:
    
    def __init__(self, subject: str, bot: commands.Bot):
        self.subject = subject
        self.bot = bot
        
        df = pd.read_csv(subject)
        
        self.question_number = random.randint(0, len(df)-1)
        self.question = str(df.iat[self.question_number, 0])

        a = str(df.iat[self.question_number,1])
        b = str(df.iat[self.question_number,2])
        c = str(df.iat[self.question_number,3])
        d = str(df.iat[self.question_number,4])
        
        self.answer = self._match_letter_to_number(str(df.iat[self.question_number,5]))
        self.explanation = str(df.iat[self.question_number,6])
        picture = str(df.iat[self.question_number,7])
        self.picture = picture if (not pd.isna(df.iloc[self.question_number, 7]) and picture.strip() != "") else None

        self.answer_list = [a, b, c, d]
        self.answer_emojis = ['🇦', '🇧', '🇨', '🇩']

    # Attach a list of emojis to a discord message
    async def attach_emojis(self, message: Message) -> None:
        for emoji in self.answer_emojis:
            await message.add_reaction(emoji)

    async def generate_question_response_with_points(self, message: Message, points: int, is_flash_event: bool) -> None:
        cheaters = await self._duplicate_reacts(message)
        winners = await self._correct_reacts(message, cheaters)

        cheaters_message, winners_message = await self._build_question_response(cheaters, winners)

        if is_flash_event and cheaters_message is None and winners_message is None:
            await message.delete()
            return
        
        await message.reply(f"**Q{self.question_number} Answer:** {self.answer_emojis[self.answer]} {self.answer_list[self.answer]}")
        
        if winners:
            for winner in winners:
                points_cog.add_points(winner.id, points)
        
        await message.channel.send(winners_message)
        
        if cheaters:
            for cheater in cheaters:
                points_cog.remove_points(cheater.id, points)
            await message.channel.send(cheaters_message)

    async def submit_question(self, channel: TextChannel|Thread, flash_event: bool) -> Message:
        formatted_question = ""
        
        if flash_event:
            with open(constants.RESOURCES_RESPONSES_FLASH_QUESTION_ANNOUNCEMENTS, "r", encoding='utf-8') as file:
                lines = file.readlines()

            formatted_question += f"{random.choice(lines).strip()} - I will self-destruct if 0 correct answers!\n\n"
        
        formatted_question += f"**Q{self.question_number} {self.question}**\n\
            **A:** {self.answer_list[0]}\n\
            **B:** {self.answer_list[1]}\n\
            **C:** {self.answer_list[2]}\n\
            **D:** {self.answer_list[3]}\n"
        
        if self.picture and self.picture.strip() != "":
            question_message = await channel.send(formatted_question, file=File(os.path.join(constants.RESOURCES_QUESTIONS_PYTHON_IMAGES_FOLDER, self.picture)))
        else:
            question_message = await channel.send(formatted_question)

        return question_message
            
    # Find any users that gave more two reactions           
    async def _duplicate_reacts(self, message: Message) -> list:
        users_list = []
        duplicates = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.bot:
                    continue
                users_list.append(user)
                if users_list.count(user) > 1:
                    duplicates.add(user)
                
        return list(duplicates)

    # Find users that gave a matching reaction and do not appear in the list of cheaters
    async def _correct_reacts(self, message: Message, cheaters: set) -> list:
        correct_users = set()
        for reaction in message.reactions:
            if (reaction.emoji == self.answer_emojis[self.answer]):
                async for user in reaction.users():
                    if user != self.bot.user and user not in cheaters:                    
                        correct_users.add(user)
        
        return list(correct_users)
    
    async def _build_question_response(self, cheaters: list, winners: list) -> str:
        cheaters_message = ""
        winners_message = ""

        if not cheaters and not winners:
            return None, None
        
        if cheaters:
            cheating_users = ""
            for cheater in cheaters:
                cheating_users += f"{cheater}"
                cheating_users += ", " if len(cheaters) > 2 and cheater != cheaters[:-1] else " "
                cheating_users += "& " if len(cheaters) > 1 and cheater == cheaters[:-2] else ""
            
            with open(constants.RESOURCES_RESPONSES_QUESTION_CHEATER, "r", encoding='utf-8') as file:
                lines = file.readlines()

            cheaters_message = re.sub(r'@CHEATERS', cheating_users, random.choice(lines).strip())

        if winners:
            winning_users = ""
            for winner in winners:
                winning_users += f"{winner}"
                winning_users += ", " if len(winners) > 2 and winner != winners[:-1] else " "
                winning_users += "& " if len(winners) > 1 and winner == winners[:-2] else ""
        
            with open(constants.RESOURCES_RESPONSES_QUESTION_CORRECT, "r", encoding='utf-8') as file:
                lines = file.readlines()

            winners_message = re.sub(r'@WINNERS', winning_users, random.choice(lines).strip())
        else:
            with open(constants.RESOURCES_RESPONSES_QUESTION_INCORRECT, "r", encoding='utf-8') as file:
                lines = file.readlines()

            winners_message = random.choice(lines).strip()

        return cheaters_message, winners_message
    
    # Match 0,1,2,3 to A,B,C,D respectively
    def _match_letter_to_number(self, answer_letter: str) -> int:
        if str(answer_letter).strip().upper() == "A":
            return 0
        elif str(answer_letter).strip().upper() == "B":
            return 1
        elif str(answer_letter).strip().upper() == "C":
            return 2
        elif str(answer_letter).strip().upper() == "D":
            return 3
        else:
            return -1