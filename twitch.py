from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


def is_live_stream(streamer_name, client_id):
    twitch_api_stream_url = "https://api.twitch.tv/kraken/streams/" \
                    + streamer_name + "?client_id=" + client_id

    streamer_html = requests.get(twitch_api_stream_url)
    streamer = json.loads(streamer_html.content)

    print(streamer)

    return streamer["stream"] is not None


isLive = is_live_stream('theg3vie', os.getenv('TWITCH_APP_ID'))
print(isLive)

