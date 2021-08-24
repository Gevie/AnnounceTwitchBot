import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

__version_info__ = ('0', '3', '0')
__version__ = '.'.join(__version_info__)

bot = commands.Bot(command_prefix="!", description='A bot for announcing twitch streamerss')
bot.load_extension('commands')


@bot.event
async def on_ready():
    """
    Runs on bot on ready event

    Returns:
        None
    """

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    game = discord.Game("Gevie is coding me")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print(f'Successfully logged in and booted...!')


load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)
