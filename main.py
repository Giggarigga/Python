import discord
from discord.ext import commands
from discord import app_commands
import os
import traceback

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

# Slash command: /absence time: <string> reason: <string>
@tree.command(name="absence", description="Set your absence with a reason and time.")
@app_commands.describe(time="How long you'll be absent (e.g. 2d 5h)", reason="Why you're absent")
async def absence(interaction: discord.Interaction, time: str, reason: str):
    try:
        await interaction.response.send_message(
            f"{interaction.user.mention} is now marked **absent** for `{reason}`. They’ll return in `{time}`.",
            ephemeral=True
        )
    except Exception as e:
        print("Error in /absence command:")
        traceback.print_exc()
        await interaction.response.send_message("Something went wrong. Please try again later.", ephemeral=True)

# Global error handler (catch startup or runtime issues)
try:
    bot.run(os.getenv("DISCORD_TOKEN"))
except Exception as e:
    print("Error while running the bot:")
    traceback.print_exc()
