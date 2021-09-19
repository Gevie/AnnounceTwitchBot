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
        """Adds a role to a streamer in the whitelist"""

    @abstractmethod
    def add_streamer(self, user_id: int, username: str) -> None:
        """Add a streamer to the whitelist"""

    @abstractmethod
    def delete_role_from_streamer(self, user_id: int, role_id: int) -> None:
        """Delete a role from a streamer in the whitelist"""

    @abstractmethod
    def delete_streamer(self, user_id: int) -> None:
        """Delete a streamer from the whitelist"""

    @abstractmethod
    def exists(self, user_id: int) -> bool:
        """Check if a streamer exists in whitelist by user id"""

    @abstractmethod
    def find(self, user_id: int) -> dict:
        """Find a streamer in te whitelist via user id"""

    @abstractmethod
    def get_contents(self) -> dict:
        """Get the contents of the datasource"""

    @abstractmethod
    def role_exists(self, roles: dict, role_id: int) -> bool:
        """Check if a role exists against a streamer by id and role list"""


class JsonDatasourceHandler(DatasourceHandlerInterface):
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
            raise RuntimeError('Cannot create json datasource as it already exists')

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

        role['role_id'] = role_id
        role['name'] = name
        streamer['roles'].append(role)

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

    def find(self, user_id: int) -> dict:
        """
        Find the streamer by user id

        Args:
            user_id (int): The user id

        Returns:
            dict: The streamer details with associated role

        Raises:
            NotFoundException: If the streamer requested could not be found
        """

        contents = self.__load_contents()
        for streamer in contents['Streamers']:
            if streamer['user_id'] == user_id:
                return streamer

        raise NotFoundException("Could not find streamer with user id '{}'".format(user_id))

    def get_role_index(self, roles: dict, role_id: int) -> int:
        """
        Find the index key of the passed role_id from roles dict

        Args:
            roles (dict): The dict of roles to check
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

    def get_contents(self) -> dict:
        """
        Get the contents of the datasource

        Returns:
            dict: The contents
        """

        return self.__load_contents()

    def role_exists(self, roles: dict, role_id: int) -> bool:
        """
        Check if the role exists by role id

        Args:
            roles (dict): The dict of current roles
            role_id (int): The role id

        Returns:
            bool: True if found else false
        """

        for role in roles:
            if role['role_id'] == role_id:
                return True

        return False
