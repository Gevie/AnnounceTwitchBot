from abc import ABC, abstractmethod
from dotenv import load_dotenv
import io
import json
import os

load_dotenv()


class NotFoundException(Exception):
    """Raised when something could not be found"""
    pass


class DatasourceHandlerInterface(ABC):
    @abstractmethod
    def add_role_to_streamer(self, user_id: int, role_id: int, name: str) -> None:
        pass

    @abstractmethod
    def add_streamer(self, user_id: int, username: str) -> None:
        pass

    @abstractmethod
    def delete_role_from_streamer(self, user_id: int, role_id: int) -> None:
        pass

    @abstractmethod
    def delete_streamer(self, user_id: int) -> None:
        pass

    @abstractmethod
    def exists(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def find(self, user_id: int) -> list:
        pass

    @abstractmethod
    def role_exists(self, roles: list, role_id: int) -> bool:
        pass


class JsonHandler(DatasourceHandlerInterface):
    """
    A class used to handle our whitelist json datasource

    We can add and remove streamers from the whitelist
    We can also add and remove roles assigned to a streamer in the whitelist
    """

    def __init__(self):
        """
        Initialize the class
        """
        self.__datasource = os.getenv('STREAMER_DATASOURCE')
        self.__template = os.getenv('TEMPLATE')
        self.__template_streamer = os.getenv('TEMPLATE_STREAMER')
        self.__template_role = os.getenv('TEMPLATE_ROLE')

    def __create(self) -> bool:
        """
        Attempts to create the file for the datasource

        Returns:
            bool: If the file was able to be created or not

        Raises:
            RuntimeError: If the file already exists when attempting to create it
        """

        if self.__exists():
            raise RuntimeError('Cannot create datasource as it already exists')

        with open(self.__template) as template:
            template_json = template.read()

        with io.open(self.__datasource, 'w') as db_file:
            db_file.write(template_json)

        return self.__exists()

    def __exists(self) -> bool:
        """
        Checks if the datasource file exists or not

        Returns:
            bool: If the datasource file exists or not
        """

        return os.path.isfile(self.__datasource) and os.access(self.__datasource, os.R_OK)

    def __load_contents(self) -> dict:
        """
        Loads the contents of the json datasource

        Returns:
            dict: The json contents as a dictionary

        Raises:
            RuntimeError: If we could not create the datasource if it did not exist already
        """

        if not self.__exists():
            datasource = self.__create()
            if not datasource:
                raise RuntimeError('Unable to load or create the datasource template')

        with open(self.__datasource) as datasource:
            return json.load(datasource)

    def __save_file(self, contents: dict) -> None:
        """
        Saves the contents passed to the datasource file

        This method will overwrite the entire file and not append.

        Args:
            contents (dict): The new file contents
        """

        datasource_file = open(self.__datasource, "w")
        json.dump(contents, datasource_file, ensure_ascii=False, indent='\t', separators=(',', ': '))
        datasource_file.close()

    def add_role_to_streamer(self, user_id: int, role_id: int, name: str) -> None:
        """
        Adds a new role to a streamer

        Args:
            user_id (int): The user id of the streamer
            role_id (int): The id of the role
            name (str): The name of the role

        Returns:
            bool: True if successful

        Raises:
            ValueError: If the streamer already has the role which we are trying to add
        """
        streamer = self.find(user_id)
        if self.role_exists(streamer['roles'], role_id):
            raise ValueError('Cannot add role id {} to user {} as it already exists'.format(role_id, user_id))

        with open(self.__template_role) as role_template:
            role = json.load(role_template)

        role['role_id'] = role_id;
        role['name'] = name;
        streamer['roles'].append(role);

        contents = self.__load_contents()
        streamer_index = self.get_streamer_index(user_id)
        contents['Streamers'][streamer_index] = streamer
        self.__save_file(contents)

    def add_streamer(self, user_id: int, username: str) -> None:
        """
        Adds a new streamer to the datasource

        Args:
            user_id (int): The user id of the streamer
            username (str): The username of the streamer

        Returns:
            bool: True if successful

        Raises:
            ValueError: If the streamer with user id already exists in datasource
        """
        if self.exists(user_id):
            raise ValueError('Cannot add user "{}" as they already exist'.format(user_id))

        contents = self.__load_contents()
        with open(self.__template_streamer) as streamer_template:
            streamer = json.load(streamer_template)

        streamer['user_id'] = user_id
        streamer['username'] = username
        contents['Streamers'].append(streamer)
        self.__save_file(contents)

    def delete_role_from_streamer(self, user_id: int, role_id: int) -> None:
        """
        Deletes a role from a user / streamer

        Args:
            user_id (int): The user id
            role_id (int): The role id

        Returns:
            None

        Raises:
            NotFoundException: If the role does not exist on the user
        """
        streamer = self.find(user_id)
        if not (self.role_exists(streamer['roles'], role_id)):
            raise NotFoundException('Cannot remove role {} from user {} as it does not exist'.format(role_id, user_id))

        role_index = self.get_role_index(streamer['roles'], role_id)
        streamer['roles'].pop(role_index)

        contents = self.__load_contents()
        streamer_index = self.get_streamer_index(user_id)
        contents['Streamers'][streamer_index] = streamer

        self.__save_file(contents)

    def delete_streamer(self, user_id: int) -> None:
        """
        Deletes a streamer from the whitelist datasource

        Args:
            user_id (int): The user id

        Returns:
            None

        Raises:
            NotFoundException: If the user cannot be found
        """
        if not (self.exists(user_id)):
            raise NotFoundException('Cannot find user with id {} for deletion'.format(user_id))

        contents = self.__load_contents()
        streamer_index = self.get_streamer_index(user_id)
        contents['Streamers'].pop(streamer_index)
        self.__save_file(contents)

    def exists(self, user_id: int) -> bool:
        """
        Check if the users exists by user id

        Args:
            user_id (int): The user id

        Returns:
            bool: True if found else false
        """
        contents = self.__load_contents()
        for streamer in contents['Streamers']:
            if streamer['user_id'] == user_id:
                return True

        return False

    def find(self, user_id: int) -> list:
        """
        Find the streamer by user id

        Args:
            user_id (int): The user id

        Returns:
            list: The streamer details with associated role

        Raises:
            NotFoundException: If the streamer requested could not be found
        """
        contents = self.__load_contents()
        for streamer in contents['Streamers']:
            if streamer['user_id'] == user_id:
                return streamer

        raise NotFoundException("Could not find streamer with user id '{}'".format(user_id))

    def get_role_index(self, roles: list, role_id: int) -> int:
        """
        Find the index key of the passed role_id from roles list

        Args:
            roles (list): The list of roles to check
            role_id (int): The role id

        Returns:
            int: The index of the role

        Raises:
            NotFoundException: If the role could not be found
        """

        for index, role in enumerate(roles):
            if role['role_id'] == role_id:
                return index

        raise NotFoundException('Could not find role "{}" to be able to get index'.format(role_id))

    def get_streamer_index(self, user_id: int) -> int:
        """
        Find the index key of the passed streamer

        Args:
            user_id (int): The user id

        Returns:
            int: The index of the streamer

        Raises:
            NotFoundException: If the streamer could not be found
        """
        contents = self.__load_contents()
        for index, streamer in enumerate(contents['Streamers']):
            if streamer['user_id'] == user_id:
                return index

        raise NotFoundException('Could not find user "{}" to be able to get index'.format(user_id))

    def role_exists(self, roles: list, role_id: int) -> bool:
        """
        Check if the role exists by role id

        Args:
            roles (list): The list of current roles
            role_id (int): The role id

        Returns:
            bool: True if found else false
        """
        for role in roles:
            if role['role_id'] == role_id:
                return True

        return False


# Grab our datasource
json_datasource = JsonHandler()

###
# Add the streamers
###
try:
    json_datasource.add_streamer(1, 'Gevie')
except ValueError:
    print('Gevie already exists in the whitelist')

try:
    json_datasource.add_streamer(2, 'Kimiko')
except ValueError:
    print('Kimiko already exists in the whitelist')

try:
    json_datasource.add_streamer(3, 'Doggey')
except ValueError:
    print('Doggey already exists in the whitelist')

###
# Add Roles to Gevie
###
try:
    json_datasource.add_role_to_streamer(1, 1, 'Dead by Daylight')
except ValueError:
    print('Gevie already has role Dead by Daylight')

try:
    json_datasource.add_role_to_streamer(1, 2, 'Tabletop Simulator')
except ValueError:
    print('Gevie already has role Tabletop Simulator')

try:
    json_datasource.add_role_to_streamer(1, 3, 'Stardew Valley')
except ValueError:
    print('Gevie already has role Stardew Valley')

###
# Add Roles to Kimiko
###
try:
    json_datasource.add_role_to_streamer(2, 3, 'Stardew Valley')
except ValueError:
    print('Kimiko already has role Stardew Valley')

###
# Add Roles to Doggey
###
try:
    json_datasource.add_role_to_streamer(3, 1, 'Dead by Daylight')
except ValueError:
    print('Doggey already has role Dead by Daylight')

try:
    json_datasource.add_role_to_streamer(3, 2, 'Tabletop Simulator')
except ValueError:
    print('Doggey already has role Tabletop Simulator')


##
# Delete Roles from Gevie
##
json_datasource.delete_role_from_streamer(1, 3)
json_datasource.delete_role_from_streamer(1, 1)

##
# Delete Doggey
##
json_datasource.delete_streamer(3)