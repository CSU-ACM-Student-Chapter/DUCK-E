from discord.ext import commands, tasks
from discord import app_commands, Interaction, InteractionResponded, Member
import logging, sqlite3
from ..constants import constants

_log = logging.getLogger(__name__)
conn = sqlite3.connect(constants.POINTS_DB_PATH)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS points (user_id INTEGER PRIMARY KEY, points INTEGER DEFAULT 0)''')
conn.commit()

class Points(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="my-points", description="Check your points.")
    async def points(self, interaction: Interaction):
        try:
            points = get_or_initialize_user_points(interaction.user.id)
            await interaction.response.send_message(f"{interaction.user.mention}, you have {format_points(points)} points.", ephemeral=True)
        except Exception as e:
            _log.exception(f"[ERROR in /my-points]")
            try:
                await interaction.followup.send("❌ Something went wrong while fetching your points.", ephemeral=True)
            except InteractionResponded:
                pass

    @app_commands.command(name="leaderboard", description="Show the top 10 users.")
    async def leaderboard(self, interaction: Interaction):
        try: 
            cursor.execute("SELECT user_id, points FROM points ORDER BY points DESC LIMIT 10")
            leaderboard_data = cursor.fetchall()
            if leaderboard_data:
                leaderboard_message = "**Leaderboard:**\n"
                for idx, (user_id, points) in enumerate(leaderboard_data, start=1):
                    user = await self.bot.fetch_user(user_id)
                    leaderboard_message += f"{idx}. {user.name} - {format_points(points)} points\n"
                await interaction.response.send_message(leaderboard_message)
            else:
                await interaction.response.send_message("No points have been recorded yet.")
        except Exception as e:
            _log.exception(f"[ERROR in /leaderboard]")
            try:
                await interaction.followup.send("❌ Something went wrong while fetching the leaderboard.", ephemeral=True)
            except InteractionResponded:
                pass

    @app_commands.command(name="add-points", description="Add points to a user.")
    @app_commands.describe(member="The member to add points to", points="Number of points to add")
    async def addpoints(self, interaction: Interaction, member: Member, points: int):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
                return
            add_points(member.id, points)
            await interaction.response.send_message(f"{format_points(points)} points have been added to {member.mention}.")
        except Exception as e:
            _log.exception(f"[ERROR in /add-points]")
            try:
                await interaction.followup.send("❌ Something went wrong while adding points.", ephemeral=True)
            except InteractionResponded:
                pass

    @app_commands.command(name="remove-points", description="Remove points from a user.")
    @app_commands.describe(member="The member to remove points from", points="The number of points to remove")
    async def removepoints(self, interaction: Interaction, member: Member, points: int):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
                return
            remove_points(member.id, points)
            await interaction.response.send_message(f"{format_points(points)} points have been removed from {member.mention}.")
        except Exception as e:
            _log.exception(f"[ERROR in /remove-points]")
            try:
                await interaction.followup.send("❌ Something went wrong while removing points.", ephemeral=True)
            except InteractionResponded:
                pass

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Points(bot))

# Fetch or initialize points for a user
def get_or_initialize_user_points(user_id, formatted=False) -> int:
    cursor.execute("SELECT points FROM points WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute("INSERT INTO points (user_id, points) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        return 0

# Add points to a user
def add_points(user_id: int, points: int) -> None:
    current_points = get_or_initialize_user_points(user_id)
    cursor.execute("UPDATE points SET points = ? WHERE user_id = ?", (current_points + points, user_id))
    conn.commit()

# Remove points from a user
def remove_points(user_id: int, points: int) -> None:
    current_points = get_or_initialize_user_points(user_id)
    new_points = max(0, current_points - points)
    cursor.execute("UPDATE points SET points = ? WHERE user_id = ?", (new_points, user_id))
    conn.commit()

# Format points with commas
def format_points(points: int) -> str:
    return '{:,}'.format(points)