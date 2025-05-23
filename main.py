import os
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

absence_data = {}

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        print(f'Logged in as {bot.user}')
    except Exception as e:
        print(f"Error in on_ready event: {e}")

@bot.tree.command(name="setabsence", description="Mark a user as absent.")
@app_commands.describe(user="Who is absent?", reason="Why are they absent?")
async def setabsence(interaction: discord.Interaction, user: discord.Member, reason: str):
    try:
        absence_data[user.id] = {
            "reason": reason
        }

        embed = discord.Embed(
            title="Staff Absence",
            color=discord.Color.red()
        )
        embed.add_field(name="• Staff Member:", value=user.mention, inline=False)
        embed.add_field(name="• Reason:", value=reason, inline=False)
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in setabsence command: {e}")
        await interaction.response.send_message("An error occurred while setting the absence. Please try again later.")

@bot.event
async def on_message(message):
    try:
        if message.author.bot:
            return

        # Check if any absent user is pinged
        for user_id, data in absence_data.items():
            if f"<@{user_id}>" in message.content or f"<@!{user_id}>" in message.content:
                user = await bot.fetch_user(user_id)
                await message.channel.send(
                    f"{user.mention} is **absent** for **{data['reason']}**, they will come back when available."
                )
                break

        # Auto-remove absence if the absent user sends a message
        if message.author.id in absence_data:
            del absence_data[message.author.id]
            msg = await message.channel.send(
                f"Welcome back {message.author.mention}! I’ve removed your **absence**."
            )
            await msg.delete(delay=15)

        await bot.process_commands(message)
    except Exception as e:
        print(f"Error in on_message event: {e}")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"An error occurred in event {event}: {args} {kwargs}")

# Ensure bot token is available
try:
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise ValueError("No token found in environment variables.")
    bot.run(token)
except Exception as e:
    print(f"Error running bot: {e}")
