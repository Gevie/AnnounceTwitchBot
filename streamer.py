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
    def __init__(self, role_id: int, name: str):
        self._id = role_id
        self._name = name

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name


class StreamerInterface(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def get_roles(self) -> dict:
        pass

    @abstractmethod
    def is_match(self, username) -> bool:
        pass


class Streamer(StreamerInterface):
    def __init__(self, user_id: int, username: str, roles: dict):
        self._id = user_id
        self._username = username
        self._roles = roles

    def get_id(self) -> int:
        return self._id

    def get_username(self) -> str:
        return self._username

    def get_roles(self) -> dict:
        return self._roles

    def is_match(self, username) -> bool:
        return self._username == username


class MapperInterface(ABC):
    @abstractmethod
    def map(self) -> list:
        pass


class RoleMapper(MapperInterface):
    def map(self, datasource: dict) -> list:
        roles = []
        for role in datasource:
            roles.append(Role(role['role_id'], role['name']))

        return roles


class StreamerMapper(MapperInterface):
    def map(self) -> list:
        STREAMER_DATASOURCE = os.getenv('STREAMER_DATASOURCE')

        streamers = []
        with open(STREAMER_DATASOURCE) as streamers_file:
            data = json.load(streamers_file)

            for streamer in data['Streamers']:
                role_mapper = RoleMapper()
                roles = role_mapper.map(streamer['roles'])

                streamers.append(Streamer(streamer['user_id'], streamer['username'], roles))

        return streamers
