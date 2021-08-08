import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
LISTENING_CHANNEL = os.getenv('DISCORD_LISTEN_CHANNEL')
BOT_ID = os.getenv('DISCORD_BOT_ID')


class AnnounceClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.channel.id != LISTENING_CHANNEL:
            pass

        # if message.author == BOT_ID
        #     pass

        await message.channel.send('Identified a message in #test-announce!')


announce = AnnounceClient()
announce.run(TOKEN)
