# Should be used for admin tasks and commands. Commands will require 
# admin role priviledges. And tasks will contain for example Web Site Filtering
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))