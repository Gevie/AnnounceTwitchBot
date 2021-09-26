from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
from streamer import StreamerInterface, StreamerMapper
import os
import twitch

from whitelist import JsonDatasourceHandler

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

    def get_streams(self, streamers: list) -> list:
        """
        Gets a list of streams based on streamers passed

        Args:
            streamers (list): The streamers to check for

        Returns:
            list: A list of TwitchStreamInterfaces
        """

        users = list(map(lambda streamer: streamer.username, streamers))
        response = self.client.get_streams(user_logins=users)

        streams = []
        for stream in response:
            streams.append(TwitchStream(
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
                thumbnail=stream.thumbnail,
                is_mature=stream.is_mature
            ))

        return streams


streamerMapper = StreamerMapper(JsonDatasourceHandler())
streamers = streamerMapper.map()

twitch_handler = TwitchHandler()
streams = twitch_handler.get_streams(streamers)

print(streams)
