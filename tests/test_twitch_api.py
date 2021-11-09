import datetime
import unittest
from unittest.mock import patch
from twitch_api import TwitchHandler, TwitchHandlerInterface, TwitchStream, TwitchStreamInterface


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
            id=1,
            user_id=1,
            user_login='test_stream',
            user_name='Test_Stream',
            game_id=1,
            game_name='Test Game',
            live='Live',
            title='This is a test stream',
            viewer_count=15,
            started_at=started_at,
            language='English',
            thumbnail='imagepath',
            is_mature=False
        )

        # Then
        self.assertTrue(isinstance(stream, TwitchStreamInterface))
        self.assertEqual(stream.id, 1)
        self.assertEqual(stream.user_id, 1)
        self.assertEqual(stream.user_login, 'test_stream')
        self.assertEqual(stream.user_name, 'Test_Stream')
        self.assertEqual(stream.game_id, 1)
        self.assertEqual(stream.game_name, 'Test Game')
        self.assertEqual(stream.live, 'Live')
        self.assertEqual(stream.title, 'This is a test stream')
        self.assertEqual(stream.viewer_count, 15)
        self.assertEqual(stream.started_at, started_at)
        self.assertEqual(stream.language, 'English')
        self.assertEqual(stream.thumbnail, 'imagepath')
        self.assertFalse(stream.is_mature)

    def test_is_live(self):
        """
        Test the twitch stream is live method

        Returns:
            None
        """

        # Give
        started_at = datetime.datetime.now()
        live_stream = TwitchStream(
            id=1,
            user_id=1,
            user_login='test_stream',
            user_name='Test_Stream',
            game_id=1,
            game_name='Test Game',
            live='Live',
            title='This is a test stream',
            viewer_count=15,
            started_at=started_at,
            language='English',
            thumbnail='imagepath',
            is_mature=False
        )

        offline_stream = TwitchStream(
            id=1,
            user_id=1,
            user_login='test_stream',
            user_name='Test_Stream',
            game_id=1,
            game_name='Test Game',
            live='Offline',
            title='This is a test stream',
            viewer_count=15,
            started_at=started_at,
            language='English',
            thumbnail='imagepath',
            is_mature=False
        )

        # Then
        self.assertTrue(live_stream.is_live())
        self.assertFalse(offline_stream.is_live())


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

    def test_get_stream(self):
        """
        Test the twitch handler get stream method

        Returns:
            None
        """

        with patch('twitch.TwitchHelix', autospec=True) as mock_twitch_client:
            # Give
            twitch_client = mock_twitch_client.return_value
            twitch_client.get_oauth.return_value = True
            started_at = datetime.datetime.now()

            class ResponseObject(object):
                pass

            response_object = ResponseObject()
            response_object.id = 1,
            response_object.user_id = 1,
            response_object.user_login = 'test_stream',
            response_object.user_name = 'Test_Stream',
            response_object.game_id = 1,
            response_object.game_name = 'Test Game',
            response_object.type = 'Live',
            response_object.title = 'This is a test stream',
            response_object.viewer_count = 15,
            response_object.started_at = started_at,
            response_object.language = 'English',
            response_object.thumbnail_url = 'imagepath',
            response_object.is_mature = False
            twitch_client.get_streams.return_value = [response_object]

            twitch_handler = TwitchHandler()

            # When
            stream = twitch_handler.get_stream('test_stream')

            # Then
            self.assertTrue(isinstance(stream, TwitchStreamInterface))