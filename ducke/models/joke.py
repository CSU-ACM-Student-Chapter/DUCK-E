from discord.ext import commands
from discord import TextChannel, Thread, File, User, Member
from ..constants import constants
import random
import asyncio
import os
import pandas as pd

class Joke:
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        df = pd.read_csv(constants.RESOURCES_RESPONSES_JOKES)
        
        self.joke_number = random.randint(0, len(df)-1)

        self.joke = str(df.iat[self.joke_number, 0])

        punchline = str(df.iat[self.joke_number, 1])
        self.punchline = punchline\
        if (not pd.isna(df.iat[self.joke_number, 1]) and punchline.strip() != "") else None
        
        attachment = str(df.iat[self.joke_number, 2])
        self.attachment = os.path.join(constants.RESOURCES_JOKE_ATTACHMENTS_FOLDER, attachment)\
        if (not pd.isna(df.iat[self.joke_number, 2]) and attachment.strip() != "") else None

    async def announce_joke(self, channel: TextChannel|Thread, user: User|Member) -> None:
        announcement_phrases = []
        with open(constants.RESOURCES_RESPONSE_JOKE_ANNOUNCEMENTS, 'r', encoding='utf-8') as f:
            announcement_phrases = f.readlines()
        
        announcement_phrase = random.choice(announcement_phrases).strip().replace("@USER", user.mention)
        
        await channel.send(content=announcement_phrase)
    
    async def tell_joke(self, channel: TextChannel|Thread) -> None:
        if self.punchline is not None:
            if self.attachment is not None:
                await channel.send(self.joke)
                await asyncio.sleep(3)
                await channel.send(content=self.punchline, file=File(self.attachment))
            else:
                await channel.send(self.joke)
                await asyncio.sleep(3)
                await channel.send(self.punchline)

        else:
            if self.attachment is not None:
                await channel.send(content=self.joke, file=File(self.attachment))
            else:
                await channel.send(self.joke)