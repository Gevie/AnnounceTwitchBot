from abc import ABC, abstractmethod
from dotenv import load_dotenv
import json
import os

load_dotenv()


class RoleInterface(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class Role(RoleInterface):
    """
    Holds an instance of a role
    """

    def __init__(self, role_id: int, name: str):
        """
        Initialize the role

        Args:
            role_id (int): The id of the role
            name (str): The name of the role
        """

        self._id = role_id
        self._name = name

    def get_id(self) -> int:
        """
        Get the role id

        Returns:
            int: The role id
        """

        return self._id

    def get_name(self) -> str:
        """
        Get the role name

        Returns:
            str: The role name
        """

        return self._name


class StreamerInterface(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def get_roles(self) -> list:
        pass

    @abstractmethod
    def is_match(self, username) -> bool:
        pass


class Streamer(StreamerInterface):
    """
    Holds an instance of a streamer
    """

    def __init__(self, user_id: int, username: str, roles: list):
        """
        Initialize the streamer

        Args:
            user_id (int): The id of the user
            username (str): The twitch username of the user
            roles (list): A list of role objects
        """

        self._id = user_id
        self._username = username
        self._roles = roles

    def get_id(self) -> int:
        """
        Get the id of the streamer

        Returns:
            int: The streamer id
        """

        return self._id

    def get_username(self) -> str:
        """
        Get the twitch username of the streamer

        Returns:
            str: The streamer username
        """

        return self._username

    def get_roles(self) -> list:
        """
        Get the roles for the streamer

        Returns:
            list: A list of role objects
        """

        return self._roles

    def is_match(self, username) -> bool:
        """
        Checks if the passed username matches the streamer

        Args:
            username (str): The username to check against

        Returns:
            bool: True if match, else false
        """

        return self._username == username


class MapperInterface(ABC):
    @abstractmethod
    def map(self) -> list:
        pass


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
