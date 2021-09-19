from unittest.mock import Mock
from whitelist import DatasourceHandlerInterface, NotFoundException, JsonDatasourceHandler
import unittest


class TestJsonDatasourceHandler(unittest.TestCase):
    """Test the json datasource handler concretion"""

    def test_instance(self):
        """
        Test the json datasource handler instance

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        # Then
        self.assertTrue(isinstance(json_datasource_handler, DatasourceHandlerInterface))

    def test_add_role_to_streamer_success(self):
        """
        Test the ability to add a role to a streamer with successful response

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        old_streamer = {
            "user_id": 1,
            "username": "HelloWorld",
            "roles": [
                {
                    "role_id": 1,
                    "name": "UnitTest"
                }
            ]
        }

        new_streamer = {
            "Streamers": [
                {
                    "user_id": 1,
                    "username": "HelloWorld",
                    "roles": [
                        {
                            "role_id": 1,
                            "name": "UnitTest"
                        },
                        {
                            "role_id": 2,
                            "name": "MockObject"
                        }
                    ]
                }
            ]
        }

        json_datasource_handler.find = Mock()
        json_datasource_handler.find.return_value = old_streamer

        json_datasource_handler.role_exists = Mock()
        json_datasource_handler.role_exists.return_value = False

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = new_streamer

        json_datasource_handler.get_streamer_index = Mock()
        json_datasource_handler.get_streamer_index.return_value = 0

        json_datasource_handler._JsonDatasourceHandler__save_file = Mock()

        # When
        json_datasource_handler.add_role_to_streamer(1, 2, 'MockObject')

        # Then
        json_datasource_handler.find.assert_called_with(1)
        json_datasource_handler.role_exists.assert_called_with(old_streamer['roles'], 2)
        json_datasource_handler.get_streamer_index.assert_called_with(1)
        json_datasource_handler._JsonDatasourceHandler__save_file.assert_called_with(new_streamer)
