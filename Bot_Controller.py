import discord
import os
import Website_Filter
from dotenv import load_dotenv

# This example requires the 'message_content' intent.
load_dotenv('.env')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
WF = Website_Filter
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    #should be master event for all msgs
    if message.author == client.user:
        return

    #TODO: test bot response, current
    if message.content:
        isSafe = WF.Website_Filter.has_SafeMsgLinks('Accepted_Links.txt',message.content)
        if(not isSafe):
            # TODO: delete msg content if
            await  client.delete_message(message)
            # TODO: Change Bot response
            await message.channel.send('Hello!')

client.run(os.getenv('DISCORD_TOKEN'))