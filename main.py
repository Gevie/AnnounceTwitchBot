# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LISTENING_CHANNEL = os.getenv('DISCORD_LISTEN_CHANNEL')

class AnnounceClient(discord.Client):
    """
    A class used to announce

    ...

    Attributes
    ----------
    discord.Client : Client
        The discord client to interact with

    Methods
    -------
    on_ready(self)
        Executed when the client is ready
    """

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.channel.id == LISTENING_CHANNEL:
            await message.channel.send('Identified a message in #test-announce!')


client = AnnounceClient()
client.run(TOKEN)
