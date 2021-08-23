from abc import ABC, abstractmethod
from dataclasses import dataclass
from dotenv import load_dotenv
import json
import os

load_dotenv()


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

    def is_match(self, username) -> bool:
        """
        Checks if the passed username matches the streamer

        Args:
            username (str): The username to check against

        Returns:
            bool: True if match, else false
        """

        return self.username == username


class RoleMapper(MapperInterface):
    """
    Maps a list of roles into role objects
    """

    def map(self, datasource: list) -> list:
        """
        Map the roles from datasource to a list of objects

        Args:
            datasource (list): The roles from datasource

        Returns:
            list: The list of role objects
        """

        roles = []
        for role in datasource:
            roles.append(Role(int(role['role_id']), role['name']))

        return roles


class StreamerMapper(MapperInterface):
    """
    Maps streamers from the datasource into objects
    """

    def map(self) -> list:
        """
        Map streamers from the datasource into objects

        Returns:
            list: A list of streamer objects
        """

        STREAMER_DATASOURCE = os.getenv('STREAMER_DATASOURCE')

        streamers = []
        with open(STREAMER_DATASOURCE) as streamers_file:
            data = json.load(streamers_file)

            for streamer in data['Streamers']:
                role_mapper = RoleMapper()
                roles = role_mapper.map(streamer['roles'])

                streamers.append(Streamer(int(streamer['user_id']), streamer['username'], roles))

        return streamers
