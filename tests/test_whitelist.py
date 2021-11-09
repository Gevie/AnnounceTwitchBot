"""The test for the whitelist file in the twitch announce bot module"""
from unittest.mock import Mock, patch, mock_open
import unittest
from whitelist import DatasourceHandlerInterface, NotFoundException, JsonDatasourceHandler


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
        Test the ability to add a role to a streamer with a successful response

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

        role_data = '{"role_id": "<role_id:placeholder>", "name": "<name:placeholder>"}'

        with patch("builtins.open", mock_open(read_data=role_data)):
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

    def test_add_role_to_streamer_failure(self):
        """
        Test the ability to add a role to a streamer with a failed response

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

        json_datasource_handler.find = Mock()
        json_datasource_handler.find.return_value = old_streamer

        json_datasource_handler.role_exists = Mock()
        json_datasource_handler.role_exists.return_value = True

        # When
        with self.assertRaises(ValueError):
            json_datasource_handler.add_role_to_streamer(1, 1, 'UnitTest')

    def test_delete_role_from_streamer_success(self):
        """
        Test the ability to delete a role from a streamer with a successful response

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
                },
                {
                    "role_id": 2,
                    "name": "MockObject"
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
                        }
                    ]
                }
            ]
        }

        json_datasource_handler.find = Mock()
        json_datasource_handler.find.return_value = old_streamer

        json_datasource_handler.role_exists = Mock()
        json_datasource_handler.role_exists.return_value = True

        json_datasource_handler.get_role_index = Mock()
        json_datasource_handler.get_role_index.return_value = 1

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = new_streamer

        json_datasource_handler.get_streamer_index = Mock()
        json_datasource_handler.get_streamer_index.return_value = 0

        json_datasource_handler._JsonDatasourceHandler__save_file = Mock()

        # When
        json_datasource_handler.delete_role_from_streamer(1, 2)

        # Then
        json_datasource_handler.find.assert_called_with(1)
        json_datasource_handler.role_exists.assert_called_with(old_streamer['roles'], 2)
        json_datasource_handler.get_role_index.assert_called_with(old_streamer['roles'], 2)
        json_datasource_handler.get_streamer_index.assert_called_with(1)
        json_datasource_handler._JsonDatasourceHandler__save_file.assert_called_with(new_streamer)

    def test_delete_role_from_streamer_failure(self):
        """
        Test the ability to delete a role from a streamer with a failed response

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

        json_datasource_handler.find = Mock()
        json_datasource_handler.find.return_value = old_streamer

        json_datasource_handler.role_exists = Mock()
        json_datasource_handler.role_exists.return_value = False

        # When
        with self.assertRaises(NotFoundException):
            json_datasource_handler.delete_role_from_streamer(1, 1)

    def test_delete_streamer_success(self):
        """
        Test the ability to delete a streamer with a successful response

        Returns:
            None
        """

        # Give
        old_streamer = {
            "Streamers": [
                {
                    "user_id": 1,
                    "username": "HelloWorld",
                    "roles": [
                        {
                            "role_id": 1,
                            "name": "UnitTest"
                        }
                    ]
                }
            ]
        }

        new_streamer = {
            "Streamers": []
        }

        json_datasource_handler = JsonDatasourceHandler()
        json_datasource_handler.exists = Mock()
        json_datasource_handler.exists.return_value = True

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = old_streamer

        json_datasource_handler.get_streamer_index = Mock()
        json_datasource_handler.get_streamer_index.return_value = 0

        json_datasource_handler._JsonDatasourceHandler__save_file = Mock()

        # When
        json_datasource_handler.delete_streamer(1)

        # Then
        json_datasource_handler._JsonDatasourceHandler__save_file.assert_called_with(new_streamer)

    def test_delete_streamer_failure(self):
        """
        Test the ability to delete a streamer with a failed response

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()
        json_datasource_handler.exists = Mock()
        json_datasource_handler.exists.return_value = False

        # When
        with self.assertRaises(NotFoundException):
            json_datasource_handler.delete_streamer(1)

    def test_exists(self):
        """
        Test the ability to check if a streamer exists

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        contents = {
            "Streamers": [
                {
                    "user_id": 1,
                    "username": "HelloWorld",
                    "roles": []
                }
            ]
        }

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = contents

        # When
        successful_response = json_datasource_handler.exists(1)
        failed_response = json_datasource_handler.exists(2)

        # Then
        self.assertTrue(successful_response)
        self.assertFalse(failed_response)

    def test_find(self):
        """
        Test the ability to find a streamer by user id successfully

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        contents = {
            "Streamers": [
                {
                    "user_id": 1,
                    "username": "HelloWorld",
                    "roles": []
                }
            ]
        }

        streamer = {
            "user_id": 1,
            "username": "HelloWorld",
            "roles": []
        }

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = contents

        # When
        success = json_datasource_handler.find(1)
        with self.assertRaises(NotFoundException):
            json_datasource_handler.find(2)

        # Then
        self.assertEqual(streamer, success)

    def get_role_index_success(self):
        """
        Test the ability to check if a role index exists

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        roles = [
            {
                "role_id": 1,
                "name": "UnitTest"
            }
        ]

        # When
        successful_response = json_datasource_handler.get_role_index(roles, 1)
        with self.assertRaises(NotFoundException):
            json_datasource_handler.get_role_index(roles, 2)

        # Then
        self.assertEqual(successful_response, 1)

    def get_streamer_index_success(self):
        """
        Test the ability to check if a streamer index exists

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        streamers = {
            "Streamers": [
                {
                    "user_id": 1,
                    "username": "HelloWorld",
                    "roles": []
                }
            ]
        }

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = streamers

        # When
        successful_response = json_datasource_handler.get_streamer_index(1)
        with self.assertRaises(NotFoundException):
            json_datasource_handler.get_role_index(2)

        # Then
        self.assertEqual(successful_response, 1)

    def test_get_contents(self):
        """
        Test the ability to load contents

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        contents = {
            "Streamers": [
                {
                    "user_id": 1,
                    "username": "HelloWorld",
                    "roles": []
                }
            ]
        }

        json_datasource_handler._JsonDatasourceHandler__load_contents = Mock()
        json_datasource_handler._JsonDatasourceHandler__load_contents.return_value = contents

        # When
        response = json_datasource_handler.get_contents()

        # Then
        self.assertEqual(response, contents)

    def role_exists(self):
        """
        Test the role exists method

        Returns:
            None
        """

        # Give
        json_datasource_handler = JsonDatasourceHandler()

        roles = roles = [
            {
                "role_id": 1,
                "name": "UnitTest"
            }
        ]

        # When
        successful_response = json_datasource_handler.role_exists(roles, 1)
        failed_response = json_datasource_handler.role_exists(roles, 2)

        # Then
        self.assertTrue(successful_response)
        self.assertFalse(failed_response)
