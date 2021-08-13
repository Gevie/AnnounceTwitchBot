import re
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import json
import io
import os

load_dotenv()


class DatasourceHandlerInterface(ABC):
    @abstractmethod
    def add_streamer(self, user_id: int, username: str):
        pass

    @abstractmethod
    def add_role_to_streamer(self, streamer, role_id: int, name: str):
        pass


class JsonHandler(DatasourceHandlerInterface):
    def __init__(self):
        self.__datasource = os.getenv('STREAMER_DATASOURCE')
        self.__template = os.getenv('TEMPLATE')
        self.__template_streamer = os.getenv('TEMPLATE_STREAMER')
        self.__template_role = os.getenv('TEMPLATE_ROLE')

    def __create(self) -> bool:
        with open(self.__template) as template:
            template_json = template.read()

        with io.open(self.__datasource, 'w') as db_file:
            db_file.write(template_json)

        return self.__exists()

    def __exists(self) -> bool:
        return os.path.isfile(self.__datasource) and os.access(self.__datasource, os.R_OK)

    def __load(self) -> dict:
        if not self.__exists():
            create_template = self.__create()
            if not create_template:
                raise RuntimeError('Unable to load or create the datasource template')

        with open(self.__datasource) as datasource:
            return json.load(datasource)

    def add_streamer(self, user_id: int, username: str) -> bool:
        datasource = self.__load()

        with open(self.__template_streamer) as streamer_template:
            streamer = streamer_template.read()

        streamer = re.sub('<user_id:placeholder>', str(user_id), streamer)
        streamer = re.sub('<username:placeholder>', username, streamer)

        datasource['Streamers'].append(streamer)
        print(datasource)

        datasource_file = open(self.__datasource, "w")
        json.dump(datasource, datasource_file)
        datasource_file.close()

        pass

    def add_role_to_streamer(self, streamer, role_id: int, name: str) -> bool:
        pass


json_datasource = JsonHandler()
json_datasource.add_streamer(12345, 'Gevie')