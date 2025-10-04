from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))