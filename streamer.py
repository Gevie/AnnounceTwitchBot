from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from twitch_api import TwitchStreamInterface, TwitchHandlerInterface
from whitelist import DatasourceHandlerInterface


class StreamerInterface(ABC):
    """
    The streamer interface
    """

    @abstractmethod
    def is_match(self, username: str) -> bool:
        """
        Checks if the username matches the streamer

        Args:
            username (str): The username to check against

        Returns
            bool: True if matched else false
        """


class MapperInterface(ABC):
    """
    The mapper interface
    """

    @abstractmethod
    def map(self) -> list:
        """
        Map the data from external source to objects

        Returns:
            list: The list of mapped objects
        """


@dataclass
class Role:
    """
    Holds an instance of a role
    """
    id: int
    name: str


@dataclass
class Streamer(StreamerInterface):
    """
    Holds an instance of a streamer
    """
    id: int
    username: str
    roles: list
    twitch_stream: Optional[TwitchStreamInterface] = None

    def is_match(self, username) -> bool:
        """
        Checks if the passed username matches the streamer

        Args:
            username (str): The username to check against

        Returns:
            bool: True if match, else false
        """

        return self.username == username


@dataclass
class RoleMapper(MapperInterface):
    """
    Maps a list of roles into role objects
    """
    datasource: list

    def map(self) -> list:
        """
        Map the roles from datasource to a list of objects

        Returns:
            list: The list of role objects
        """

        roles = []
        for role in self.datasource:
            roles.append(Role(int(role['role_id']), role['name']))

        return roles


@dataclass
class StreamerMapper(MapperInterface):
    """
    Maps streamers from the datasource into objects
    """
    datasource_handler: DatasourceHandlerInterface
    twitch_handler: TwitchHandlerInterface

    def map(self) -> list:
        """
        Map streamers from the datasource into objects

        Returns:
            list: A list of streamer objects
        """

        data = self.datasource_handler.get_contents()

        streamers = []
        for index, streamer in enumerate(data['Streamers']):
            twitch_stream = self.twitch_handler.get_stream(streamer['username'])

            roles = RoleMapper(streamer['roles']).map()
            streamers.append(Streamer(int(streamer['user_id']), streamer['username'], roles, twitch_stream))

        return streamers
