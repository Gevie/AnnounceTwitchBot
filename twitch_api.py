from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from itertools import islice
from typing import Optional

from dotenv import load_dotenv
import os
import twitch

load_dotenv()


class TwitchStreamInterface(ABC):
    """
    The twitch stream interface
    """

    @abstractmethod
    def is_live(self) -> bool:
        """
        Checks if the user passed is currently live

        Args
            username (str): The twitch username / user_login

        Returns
            bool: True if live, else false
        """


@dataclass
class TwitchStream(TwitchStreamInterface):
    """
    The twitch stream implementation
    """
    id: int
    user_id: int
    user_login: str
    user_name: str
    game_id: int
    game_name: str
    live: str
    title: str
    viewer_count: int
    started_at: datetime
    language: str
    thumbnail: str
    is_mature: bool

    def is_live(self):
        """
        Checks if the user passed is currently live

        Args
            username (str): The twitch username / user_login

        Returns
            bool: True if live, else false
        """
        return self.live == 'Live'


class TwitchHandlerInterface(ABC):
    """
    The Twitch handler interface
    """

    @abstractmethod
    def get_stream(self, username: str) -> Optional[TwitchStreamInterface]:
        """
        Grabs an individual stream object if passed streamer is live

        Args:
            username (str): The username to check

        Returns:
            TwitchStreamInterface: If the stream is live, else none
        """

    @abstractmethod
    def get_streams(self, streamers: list) -> list:
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

    def get_stream(self, username: str) -> Optional[TwitchStreamInterface]:
        """
        Grabs an individual stream object if passed streamer is live

        Args:
            username (str): The username to check

        Returns:
            TwitchStreamInterface: If the stream is live, else none
        """

        response = self.client.get_streams(user_logins=username)
        if not response:
            return None

        return TwitchStream(
            id=response[0].id,
            user_id=response[0].user_id,
            user_login=response[0].user_login,
            user_name=response[0].user_name,
            game_id=response[0].game_id,
            game_name=response[0].game_name,
            live=response[0].type,
            title=response[0].title,
            viewer_count=response[0].viewer_count,
            started_at=response[0].started_at,
            language=response[0].language,
            thumbnail=response[0].thumbnail_url,
            is_mature=response[0].is_mature
        )

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

        streams = {}
        for stream in islice(response, 1, len(users)):
            streams[stream.user_name] = TwitchStream(
                id=stream.id,
                user_id=stream.user_id,
                user_login=stream.user_login,
                user_name=stream.user_name,
                game_id=stream.game_id,
                game_name=stream.game_name,
                live=stream.type,
                title=stream.title,
                viewer_count=stream.viewer_count,
                started_at=stream.started_at,
                language=stream.language,
                thumbnail=stream.thumbnail_url,
                is_mature=stream.is_mature
            )

        return streams
