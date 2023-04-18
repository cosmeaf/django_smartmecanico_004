import jwt
import requests
from jwt import decode
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import logging

logger = logging.getLogger(__name__)

class APIClient:

    def __init__(self, token=None):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def _send_request(self, method, url, *args, **kwargs):
        response = requests.request(method, url, headers=self.headers, *args, **kwargs)
        return response

    def post(self, url, *args, **kwargs):
        return self._send_request('POST', url, *args, **kwargs)

    def get(self, url, *args, **kwargs):
        return self._send_request('GET', url, *args, **kwargs)

    def validate_token(self, secret_key):
        try:
            payload = jwt.decode(self.token, secret_key, algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
