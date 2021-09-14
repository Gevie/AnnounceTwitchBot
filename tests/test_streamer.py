from streamer import RoleMapper, Streamer, StreamerMapper
from unittest import mock
import unittest


class TestStreamer(unittest.TestCase):
    def test_is_match(self):
        # Give
        streamer = Streamer(1, 'Test Streamer', [])

        # When
        successful_match = streamer.is_match('Test Streamer')
        failed_match = streamer.is_match('Failed Streamer')

        # Then
        self.assertTrue(successful_match)
        self.assertFalse(failed_match)


class TestStreamerMapper(unittest.TestCase):
    def test_map(self):
        # Give
        streamer_mapper = StreamerMapper()

        with patch('')

        # TODO: Learn how to mock so I can test this


class TestRoleMapper(unittest.TestCase):
    def test_map(self):
        # Give
        role_mapper = RoleMapper()

        # TODO: Learn how to mock so I can test this


if __name__ == '__main__':
    unittest.main()
