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


# Build the streamer instances and the roles
streamers = []
with open(STREAMER_DATASOURCE) as streamers_file:
    data = json.load(streamers_file)

    for streamer in data['Streamers']:
        roles = []
        for role in streamer['roles']:
            roles.append(Role(role['role_id'], role['name']))

        streamers.append(Streamer(streamer['username'], roles))

# Loop through all streamers and their roles and print for debug
for idx, streamer in enumerate(streamers):
    print("\n----- Streamer {} -----".format(idx))
    print("Username: ", streamer.get_username())
    for role in streamer.get_roles():
        print("Role ID:", role.get_id())
        print("Role Name:", role.get_name())
