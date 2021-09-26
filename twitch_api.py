from dotenv import load_dotenv
import os
import twitch

load_dotenv()

client_id = os.getenv('TWITCH_APP_ID')
client_secret = os.getenv('TWITCH_APP_SECRET')

user_logins = [
    'theg3vie',
    'epic_sabo',
    'zedgehog',
    'xxbasicelementxx'
]

client = twitch.TwitchHelix(
    client_id=client_id,
    client_secret=client_secret,
    scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS]
)

token = client.get_oauth()
streams = client.get_streams(user_logins=user_logins)

print(streams)
