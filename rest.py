import json
import os
from abc import ABC, abstractmethod
from urllib.parse import urlencode

from Tools.scripts.make_ctype import method
from dotenv import load_dotenv
from main import __version__
from platform import platform, python_version
import requests
from requests import Response

load_dotenv()


class ResponseInterface(ABC):
    """
    The response interface
    """

    @abstractmethod
    def __init__(self, response) -> None:
        """
        Initialize the class

        Args:
            response: The response
        """

    @abstractmethod
    def body(self) -> json:
        """
        Gets the request body

        Returns:
            json: The response body
        """

    @abstractmethod
    def error(self) -> dict:
        """
        Get any errors attached to the request

        Returns:
            dict: The errors as a dictionary
        """

    @abstractmethod
    def is_successful(self) -> bool:
        """
        Determines if the response was successful or not

        Returns:
            bool: True if successful, else false
        """


class RestResponse(ResponseInterface):
    def __init__(self, response) -> None:
        pass


class RequestInterface(ABC):
    """
    The request interface
    """

    @abstractmethod
    def __init__(self, endpoint: str, method: str, data: dict) -> None:
        """
        Initialize the class

        Args:
            endpoint (str): The endpoint to call
            method (str): The rest method to use
            data (dict): The data to add
        """

    @abstractmethod
    def set_headers(self, headers: dict) -> None:
        """
        Set the headers for the request

        Args:
            headers (dict): The headers to set

        Returns:
            None
        """


class Request(RequestInterface):
    """
    The request
    """

    __allowedMethods = [
        'get',
        'post',
        'put',
        'patch',
        'delete'
    ]

    def __init__(self, endpoint: str, method: str, headers: dict = None, data: dict = None) -> None:
        """
        Initialize the class

        Args:
            endpoint (str): The endpoint to request
            method (str): The request method to use (Default is None)
            data (dict): The request data to send (Default is None)
        """

        self.__headers = None
        if method not in self.__allowedMethods:
            raise ValueError(f'The method {method} is not in the allowed list of methods')

        self.__set_headers(headers)
        self.__endpoint = endpoint
        self.__method = method
        self.__data = data
        self.__set_url()

    def __set_headers(self, headers: dict) -> None:
        """
        Set the appropriate headers for the request

        Args:
            headers (dict): A dictionary of possible header keys

        Returns:
            None
        """
        if 'token' in headers:
            self.__headers['Authorization:'] = f"Bearer: {headers['token']}"

        if 'id' in headers:
            self.__headers['Client-Id'] = headers['id']

        self.__headers['User-Agent'] = f"PythonClient/{__version__} {platform(True)}; Python {python_version()}"

    def __set_url(self) -> None:
        """
        Sets the url for the request

        Returns:
            None
        """

        url = os.getenv('TWITCH_API_URL')
        data = urlencode(self.__data)if self.__data is not None else None

        self.__url = f"{url}/{self.__endpoint}?{data}"

    def submit(self):
        """
        Submit the request

        Returns:
            ResponseInterface: The request response
        """

        if self.__method == 'get':
            return RestResponse(requests.get(self.__url, headers=self.__headers))


class RestClientInterface(ABC):
    """
    The rest client interface
    """

    @abstractmethod
    def __init__(self):
        """
        Initialize the Rest client
        """

    @abstractmethod
    def __call(self, request: RequestInterface) -> ResponseInterface:
        """
        Create a request and call the service

        Args:
            request (RequestInterface): The request

        Returns:
            ResponseInterface: The response
        """

    @abstractmethod
    def get(self, endpoint: str) -> ResponseInterface:
        """
        Issue a GET request and receive the response

        Args:
            endpoint (str): The endpoint to hit

        Returns:
            ResponseInterface: The response
        """

    @abstractmethod
    def post(self, endpoint: str, data: dict) -> ResponseInterface:
        """
        Issue a POST request and receive the response

        Args:
            endpoint (str): The endpoint to hit
            data (dict): The data to send

        Returns:
            ResponseInterface: The response
        """

    @abstractmethod
    def put(self, endpoint: str, data: dict) -> ResponseInterface:
        """
        Issue a PUT request and receive the response

        Args:
            endpoint (str): The endpoint to hit
            data (dict): The data to send

        Returns:
            ResponseInterface: The response
        """

    @abstractmethod
    def patch(self, endpoint: str, data: dict) -> ResponseInterface:
        """
        Issue a PATCH request and receive the response

        Args:
            endpoint (str): The endpoint to hit
            data (dict): The data to send

        Returns:
            ResponseInterface: The response
        """

    @abstractmethod
    def delete(self, endpoint: str, data: dict) -> ResponseInterface:
        """
        Issue a DELETE request and receive the response

        Args:
            endpoint (str): The endpoint to hit
            data (dict): The data to send

        Returns:
            ResponseInterface: The response
        """
