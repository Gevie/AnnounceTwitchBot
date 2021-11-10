"""The test for the twitch api file in the twitch announce bot module"""
import datetime
import unittest
from unittest.mock import patch
from twitch_api import TwitchHandler, TwitchHandlerInterface, TwitchStream


class TestTwitchStream(unittest.TestCase):
    """Test the twitch stream model concretion"""

    def test_instance(self):
        """
        Test the twitch stream instance and its properties

        Returns:
            None
        """

        # Give
        started_at = datetime.datetime.now()
        stream = TwitchStream(
            user_name='Test_Stream',
            game_name='Test Game',
            title='This is a test stream',
            viewer_count=15,
            started_at=started_at,
            thumbnail='imagepath',
        )

        # Then
        self.assertEqual(stream.user_name, 'Test_Stream')
        self.assertEqual(stream.game_name, 'Test Game')
        self.assertEqual(stream.title, 'This is a test stream')
        self.assertEqual(stream.viewer_count, 15)
        self.assertEqual(stream.started_at, started_at)
        self.assertEqual(stream.thumbnail, 'imagepath')


class TestTwitchHandler(unittest.TestCase):
    """Test the twitch handler concretion"""

    def test_instance(self):
        """
        Test the twitch handler instance and its properties

        Returns:
            None
        """

        with patch('twitch.TwitchHelix', autospec=True) as mock_twitch_client:
            # Give
            twitch_client = mock_twitch_client.return_value
            twitch_client.get_oauth.return_value = True

            # When
            twitch_handler = TwitchHandler()

            # Then
            self.assertTrue(isinstance(twitch_handler, TwitchHandlerInterface))
            self.assertTrue(twitch_handler.client.get_oauth())

    def test_get_streams(self):
        """
        Test the twitch handler get streams method

        Returns:
            None
        """

        with patch('twitch.TwitchHelix', autospec=True) as mock_twitch_client:
            # Give
            twitch_client = mock_twitch_client.return_value
            twitch_client.get_oauth.return_value = True
            started_at = datetime.datetime.now()

            class ResponseObject:
                """A mock object for the response of get_streams"""

            response_object = ResponseObject()
            response_object.user_name = 'Test_Stream'
            response_object.game_name = 'Test Game'
            response_object.title = 'This is a test stream'
            response_object.viewer_count = 15
            response_object.started_at = started_at
            response_object.thumbnail_url = 'imagepath'
            twitch_client.get_streams.return_value = [response_object]

            twitch_handler = TwitchHandler()

            class Streamer:
                """A mock streamer object"""

            streamer = Streamer()
            streamer.username = 'Test Streamer'

            # When
            stream = twitch_handler.get_streams([streamer])

            # Then
            self.assertTrue(isinstance(stream, dict))
