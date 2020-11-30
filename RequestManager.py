import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


class RequestManager():

    def __init__(self, headers):

        self.session = Session()
        self.session.headers.update(headers)        

    def send_request(self, parameters, url=None):
        try:
            self.response = self.session.get(url, params=parameters)
            self.status_code = self.response.status_code
            data = json.loads(self.response.text)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
