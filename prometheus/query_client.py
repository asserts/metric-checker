import json
import requests
from requests.exceptions import RequestException, HTTPError
from base64 import b64encode


class QueryClient:
    """QueryClient for making http requests"""

    def __init__(self, host, username, password):
        """
        Args:
            host (str): The host to make queries against

        Attrs:
            host (str): The host to make queries against
            headers (dict): http headers
        """

        self.host = host
        self.username = username
        self.password = password
        self.headers = {}

    def set_header(self, key, val):
        """Set an http header for this QueryClient

        Args:
            key (str): header key
            val (str): header val
        """

        self.headers[key] = val

    def handle_request(self, endpoint, request_type, data=None):
        """Handle http requests for the QueryClient

        Args:
            endpoint (str): the endpoint to make the request against
            request_type (str): the request type (valid types = ['GET', 'POST'])
            data (dict): the data to POST (default=None)

        Returns:
            dict: the json response
        """

        json_response = {}

        url = self.host + endpoint
        try:
            print(f'Performing method={request_type} for client={self.__class__.__name__} at url={url}')

            if self.username is not None and self.password is not None:
                self.set_header('Authorization', "Basic {}".format(
                    b64encode(bytes(f"{self.username}:{self.password}", "utf-8")).decode("ascii")))

            if request_type == 'GET':
                self.set_header('Content-Type', 'application/json')
                r = requests.get(url, headers=self.headers)
            elif request_type == 'POST':
                self.set_header('Content-Type', 'application/json')
                r = requests.post(url, headers=self.headers, data=data)
        except RequestException as e:
            raise(e)
        except HTTPError as e:
            raise(e)

        if r.status_code == 200:
            json_response = json.loads(r.text)
        else:
            msg = f'{request_type} request to url={url} received status_code={r.status_code}.\n{r.text}'
            print(msg)
            json_response = None

        return json_response
