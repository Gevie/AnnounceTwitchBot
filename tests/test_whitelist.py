from unittest.mock import Mock, patch
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
        print(json_datasource_handler._JsonDatasourceHandler__datasource)


if __name__ == '__main__':
    unittest.main()