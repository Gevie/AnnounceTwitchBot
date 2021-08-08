import json


class Role:
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name


class Streamer:
    def __init__(self, username: str, roles: Role):
        self._username = username
        self._roles = roles

    def get_username(self):
        return self._username

    def get_roles(self):
        return self._roles

    def is_match(self, username):
        return self._username == username


# Build the streamer instances and the roles
streamers = []
with open('streamers.json') as streamers_file:
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