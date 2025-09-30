import shutil
import json
from decouple import config
import requests
import env

API_URL = env.api_url


def get_access_token(username, password):
    auth = {"username": username, "password": password}
    token_request = requests.post(f"{API_URL}/authenticate", json=auth, verify=False, timeout=10)
    return token_request.json()["access_token"]


class API:
    def __init__(self, username=config("API_USERNAME"), password=config("API_PASSWORD")):
        self.username = username
        self.password = password
        self.token = get_access_token(username, password)
        self.session = requests.Session()
        self.session.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "charset": "utf-8",
        }

    def user_setup(self):
        production_user = {
            "cookies": [],
            "origins": [
                {
                    "origin": f"http://{env.ip}",
                    "localStorage": [
                        {"name": "refreshToken0", "value": self.token},
                        {"name": "accessToken0", "value": self.token},
                        {"name": "username0", "value": self.username},
                    ],
                }
            ],
        }
        with open(f"{self.username}.json", "w") as f:
            json.dump(production_user, f)

    def endpoint_to_url(self, endpoint: str) -> str:
        """
        Helper function that converts an endpoint to a full API URL to be
        used in requests.
        Args:
            endpoint (str): API endpoint or URL
        Returns:
            str: The full API URL
        """
        if not endpoint.startswith("http"):
            # Corrects endpoint if necessary
            if not endpoint.startswith("/"):
                endpoint = f"/{endpoint}"
            # Adds root API URL to endpoint
            endpoint = API_URL + endpoint
        return endpoint

    def request(self, request_type: str, endpoint: str, data=None):
        """Make a request to the API
        Args:
            request_type (str): get, post, delete, put, update
            endpoint (str): Endpoint (/users, etc) or an URL (https://...)
            data (dict, optional): Data to be sent. Defaults to None
        Returns:
            tuple: 1st item is the JSON response, 2nd is the status code
        """
        # To avoid inconsistency, makes all str parameters lowercase
        request_type = request_type.lower()

        if request_type == "post":
            response = self.session.post(self.endpoint_to_url(endpoint), json=data)
        elif request_type == "put":
            response = self.session.put(self.endpoint_to_url(endpoint), json=data)
        elif request_type == "get":
            response = self.session.get(self.endpoint_to_url(endpoint), json=data)
        elif request_type == "delete":
            response = self.session.delete(self.endpoint_to_url(endpoint))
        else:
            raise ValueError("Unknown request type")

        return response.json(), response.status_code

    def post(self, endpoint: str, data: dict) -> tuple[dict, int]:
        """
        alias for request('post', ...)
        Returns:
            tuple: 1st item is the JSON response, 2nd is the status code
        """
        return self.request("post", endpoint, data)

    def put(self, endpoint: str, data: dict = None) -> tuple[dict, int]:
        """
        alias for request('post', ...)
        Returns:
            tuple: 1st item is the JSON response, 2nd is the status code
        """
        return self.request("put", endpoint, data)

    def get(self, endpoint: str, data: dict = None) -> tuple[dict, int]:
        """
        alias for request('get', ...)
        Returns:
            tuple: 1st item is the JSON response, 2nd is the status code
        """
        return self.request("get", endpoint, data)

    def delete(self, endpoint: str) -> tuple[dict, int]:
        """
        alias for request('delete', ...)
        Returns:
            tuple: 1st item is the JSON response, 2nd is the status code
        """
        return self.request("delete", endpoint)

    def download(self, endpoint: str, filename: str) -> int:
        """Downloads a file from an endpoint
        Args:
            endpoint (str): API endpoint or URL
            filename (str): Full path and filename to save the file
        Returns:
            int: Request status code
        """
        with requests.get(self.endpoint_to_url(endpoint), stream=True, timeout=100) as r:
            with open(filename, "wb") as f:
                shutil.copyfileobj(r.raw, f)
            return r.status_code
