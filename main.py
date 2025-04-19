import discord
from discord.ext import commands
import os
import traceback

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot has logged in as {bot.user}')

# Command to set an absence
@bot.command()
async def absence(ctx, time: str, *, reason: str):
    # Check if the user has the right permissions (using specific role IDs)
    allowed_roles = [1333821999155380345, 1347052625736110231, 1333821257619079168, 1341709228624318474]

    if not any(role.id in allowed_roles for role in ctx.author.roles):
        await ctx.send("You do not have permission to use this command.")
        return

    # Send the absence message
    channel = bot.get_channel(1361195118731722841)
    await channel.send(f"{ctx.author.name} is **absent** for {reason}, they will come back in {time}.")

    # Store the absence in a dictionary (or database if needed)
    bot.absences[ctx.author.id] = {'time': time, 'reason': reason}

    await ctx.send(f"Your absence has been set to {time} with reason: {reason}.")

# Command to show absences
@bot.command()
async def check_absences(ctx):
    if ctx.author.id not in bot.absences:
        await ctx.send(f"{ctx.author.name}, you are not marked as absent.")
    else:
        absence_info = bot.absences[ctx.author.id]
        await ctx.send(f"{ctx.author.name}, you are absent for {absence_info['reason']} and will return in {absence_info['time']}.")

# Initialize the dictionary to store absences
bot.absences = {}

# Event when a user is mentioned
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check mentions
    if message.mentions:
        for user in message.mentions:
            if user.id in bot.absences:
                absence_info = bot.absences[user.id]
                await message.channel.send(f"{user.name} is **absent** for {absence_info['reason']}, they will come back in {absence_info['time']}.")
    
    # Remove absence if user sends a message
    if message.author.id in bot.absences:
        bot.absences.pop(message.author.id)
        await message.channel.send(f"Welcome back {message.author.name}! I've removed your **absence**.")

    await bot.process_commands(message)

# Global error handler
@bot.event
async def on_error(event, *args, **kwargs):
    error = traceback.format_exc()
    print(f"Error in event {event}: {error}")

# Run the bot
try:
    bot.run(os.getenv("DISCORD_TOKEN"))
except Exception as e:
    print(f"An error occurred while running the bot: {str(e)}")
