"""The twitch api file for the announce twitch bot module"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from itertools import islice
import os
from dotenv import load_dotenv
import twitch

load_dotenv()


@dataclass
class TwitchStream:
    """
    The twitch stream implementation
    """
    user_name: str
    game_name: str
    title: str
    viewer_count: int
    started_at: datetime
    thumbnail: str


class TwitchHandlerInterface(ABC):
    """
    The Twitch handler interface
    """

    @abstractmethod
    def get_streams(self, streamers: list) -> dict:
        """
        Gets a list of streams based on streamers passed

        Args:
            streamers (list): The streamers to check for

        Returns:
            list: A list of TwitchStreamInterfaces
        """


class TwitchHandler(TwitchHandlerInterface):
    """
    The Twitch handler
    """

    def __init__(self):
        """
        Initialize the class, set up twitch oauth client
        """
        client_id = os.getenv('TWITCH_APP_ID')
        client_secret = os.getenv('TWITCH_APP_SECRET')

        self.client = twitch.TwitchHelix(
            client_id=client_id,
            client_secret=client_secret,
            scopes=[twitch.constants.OAUTH_SCOPE_ANALYTICS_READ_EXTENSIONS]
        )

        self.client.get_oauth()

    def get_streams(self, streamers: list) -> dict:
        """
        Gets a list of streams based on streamers passed

        Args:
            streamers (list): The streamers to check for

        Returns:
            list: A list of TwitchStreamInterfaces
        """

        users = list(map(lambda streamer: streamer.username, streamers))
        response = self.client.get_streams(user_logins=users)

        print("Checking Streams...")

        streams = {}
        for stream in islice(response, 1, len(users)):
            streams[stream.user_login] = TwitchStream(
                user_name=stream.user_name,
                game_name=stream.game_name,
                title=stream.title,
                viewer_count=stream.viewer_count,
                started_at=stream.started_at,
                thumbnail=stream.thumbnail_url
            )

        return streams
