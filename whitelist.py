import re
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import json
import io
import os

load_dotenv()


class NotFoundException(Exception):
    """Raised when something could not be found"""
    pass


class DatasourceHandlerInterface(ABC):
    @abstractmethod
    def add_streamer(self, user_id: int, username: str):
        pass

    @abstractmethod
    def add_role_to_streamer(self, streamer, role_id: int, name: str):
        pass


class JsonHandler(DatasourceHandlerInterface):
    """
    A class used to handle our whitelist json datasource
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

        print(contents)

        datasource_file = open(self.__datasource, "w")
        json.dump(contents, datasource_file, ensure_ascii=False, sort_keys=True, indent='\t', separators=(',', ': '))
        datasource_file.close()

    def add_streamer(self, user_id: int, username: str) -> bool:
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
        print(contents)

        with open(self.__template_streamer) as streamer_template:
            streamer = json.load(streamer_template)

        streamer['user_id'] = user_id
        streamer['username'] = username
        contents['Streamers'].append(streamer)
        self.__save_file(contents)

        return True

    def add_role_to_streamer(self, streamer, role_id: int, name: str) -> bool:
        pass

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
            if streamer['user_id'] == str(user_id):
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
            if streamer['user_id'] == str(user_id):
                return streamer

        raise NotFoundException("Could not find streamer with user id '{}'".format(user_id))


json_datasource = JsonHandler()
json_datasource.add_streamer(12345, 'Gevie')
