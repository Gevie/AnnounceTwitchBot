import os
import discord
from dotenv import load_dotenv
from streamer import StreamerMapper

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


# announce = AnnounceClient()
# announce.run(TOKEN)

streamerMapper = StreamerMapper()
streamers = streamerMapper.map()

# Loop through all streamers and their roles and print for debug
for idx, streamer in enumerate(streamers):
    print("\n----- Streamer {} -----".format(idx))
    print("Username: ", streamer.get_username())
    for role in streamer.get_roles():
        print("Role ID:", role.get_id())
        print("Role Name:", role.get_name())
