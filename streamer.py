from abc import ABC, abstractmethod
from dotenv import load_dotenv
import json
import os

load_dotenv()
STREAMER_DATASOURCE = os.getenv('STREAMER_DATASOURCE')


class RoleInterface(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class Role(RoleInterface):
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name


class StreamerInterface(ABC):
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
    def __init__(self, username: str, roles: dict):
        self._username = username
        self._roles = roles

    def get_username(self) -> str:
        return self._username

    def get_roles(self) -> dict:
        return self._roles

    def is_match(self, username) -> bool:
        return self._username == username


class MapperInterface(ABC):
    @abstractmethod
    def map(self):
        pass


class RoleMapper(MapperInterface):
    def map(self, datasource: dict):
        roles = []
        for role in datasource:
            roles.append(Role(role['role_id'], role['name']))

        return roles


class StreamerMapper(MapperInterface):
    def map(self):
        streamers = []
        with open(STREAMER_DATASOURCE) as streamers_file:
            data = json.load(streamers_file)

            for streamer in data['Streamers']:
                role_mapper = RoleMapper()
                roles = role_mapper.map(streamer['roles'])

                streamers.append(Streamer(streamer['username'], roles))

        return streamers


streamerMapper = StreamerMapper()
streamers = streamerMapper.map()

# Loop through all streamers and their roles and print for debug
for idx, streamer in enumerate(streamers):
    print("\n----- Streamer {} -----".format(idx))
    print("Username: ", streamer.get_username())
    for role in streamer.get_roles():
        print("Role ID:", role.get_id())
        print("Role Name:", role.get_name())
