import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix="!", description='A bot for announcing twitch streams')
bot.load_extension('commands')

load_dotenv()


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    game = discord.Game("Gevie is coding me")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print(f'Successfully logged in and booted...!')


bot.run(os.getenv('DISCORD_TOKEN'), bot=True, reconnect=True)
