from streamer import RoleMapper, Streamer, StreamerMapper
import unittest


class TestStreamer(unittest.TestCase):
    def test_is_match(self):
        # Give
        streamer = Streamer(1, 'Test Streamer', [])

        # When
        successfulMatch = streamer.is_match('Test Streamer')
        failedMatch = streamer.is_match('Failed Streamer')

        # Then
        self.assertTrue(successfulMatch)
        self.assertFalse(failedMatch)


class TestStreamerMapper(unittest.TestCase):
    def test_map(self):
        # Give
        streamer_mapper = StreamerMapper()

        # TODO: Learn how to mock so I can test this


class TestRoleMapper(unittest.TestCase):
    def test_map(self):
        # Give
        role_mapper = RoleMapper()

        # TODO: Learn how to mock so I can test this


if __name__ == '__main__':
    unittest.main()