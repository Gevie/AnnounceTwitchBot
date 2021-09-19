import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!", description='A bot for announcing twitch streamers')
bot.load_extension('commands')


@bot.event
async def on_ready():
    """
    Runs on bot on ready event

    Returns:
        None
    """

    game = discord.Game("Gevie is currently working on me.")
    await bot.change_presence(status=discord.Status.idle, activity=game)


load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)