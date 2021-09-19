from streamer import Role, RoleMapper, MapperInterface, Streamer, StreamerInterface, StreamerMapper
from unittest.mock import Mock
from whitelist import DatasourceHandlerInterface
import unittest


class TestRole(unittest.TestCase):
    """Test the role model concretion"""

    def test_instance(self):
        """
        Test the role instance and its properties

        Returns:
            None
        """

        # Give
        role = Role(1, 'Test')

        # Then
        self.assertTrue(isinstance(role, Role))
        self.assertEqual(role.id, 1)
        self.assertEqual(role.name, 'Test')


class TestStreamer(unittest.TestCase):
    """Test the streamer model concretion"""

    def test_instance(self):
        """
        Test the streamer instance and its properties

        Returns:
            None
        """

        # Give
        streamer = Streamer(1, 'Test', [
            Role(1, 'Test')
        ])

        # Then
        self.assertTrue(isinstance(streamer, Streamer))
        self.assertEqual(streamer.id, 1)
        self.assertEqual(streamer.username, 'Test')

        self.assertTrue(isinstance(streamer.roles, list))

        self.assertTrue(isinstance(streamer.roles[0], Role))
        self.assertEqual(streamer.roles[0].id, 1)
        self.assertEqual(streamer.roles[0].name, 'Test')

    def test_is_match(self):
        """
        Test the streamer is_match method

        Returns:
            None
        """

        # Give
        streamer = Streamer(1, 'Test Streamer', [])

        # When
        successful_match = streamer.is_match('Test Streamer')
        failed_match = streamer.is_match('Failed Streamer')

        # Then
        self.assertTrue(successful_match)
        self.assertFalse(failed_match)


class TestStreamerMapper(unittest.TestCase):
    """Test the streamer mapper concretion"""

    def test_instance(self):
        """
        Test the streamer mapper instance and its properties

        Returns:
            None
        """

        # Give
        datasource_handler = Mock(spec=DatasourceHandlerInterface)
        streamer_mapper = StreamerMapper(datasource_handler)

        # Then
        self.assertTrue(streamer_mapper, MapperInterface)
        self.assertTrue(isinstance(streamer_mapper.datasource_handler, DatasourceHandlerInterface))

    def test_map(self):
        """
        Test the streamer mapper map method

        Returns:
            None
        """

        # Give
        datasource = Mock(spec=DatasourceHandlerInterface)
        datasource.get_contents.return_value = {
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

        streamer_mapper = StreamerMapper(datasource)

        # When
        mapped_streamers = streamer_mapper.map()

        # Then
        self.assertTrue(isinstance(mapped_streamers[0], StreamerInterface))
        self.assertEqual(mapped_streamers[0].id, 1)
        self.assertEqual(mapped_streamers[0].username, 'HelloWorld')

        self.assertTrue(isinstance(mapped_streamers[0].roles, list))

        self.assertTrue(isinstance(mapped_streamers[0].roles[0], Role))
        self.assertEqual(mapped_streamers[0].roles[0].id, 1)
        self.assertEqual(mapped_streamers[0].roles[0].name, 'UnitTest')

        self.assertTrue(isinstance(mapped_streamers[0].roles[1], Role))
        self.assertEqual(mapped_streamers[0].roles[1].id, 2)
        self.assertEqual(mapped_streamers[0].roles[1].name, 'MockObject')


class TestRoleMapper(unittest.TestCase):
    """ Test the role mapper concretion"""

    def test_instance(self):
        """
        Test the role mapper concretion and its properties

        Returns:
            None
        """

        # Give
        role_mapper = RoleMapper([])

        # Then
        self.assertTrue(role_mapper, MapperInterface)
        self.assertTrue(isinstance(role_mapper.datasource, list))

    def test_map(self):
        """
        Test the role mapper map method

        Returns:
            None
        """

        # Give
        roles = [
            {
                "role_id": 1,
                "name": "UnitTest"
            },
            {
                "role_id": 2,
                "name": "MockObject"
            }
        ]

        role_mapper = RoleMapper(roles)

        # When
        mapped_roles = role_mapper.map()

        # Then
        self.assertTrue(isinstance(mapped_roles, list))

        self.assertTrue(isinstance(mapped_roles[0], Role))
        self.assertEqual(mapped_roles[0].id, 1)
        self.assertEqual(mapped_roles[0].name, 'UnitTest')

        self.assertTrue(isinstance(mapped_roles[1], Role))
        self.assertEqual(mapped_roles[1].id, 2)
        self.assertEqual(mapped_roles[1].name, 'MockObject')


if __name__ == '__main__':
    unittest.main()
