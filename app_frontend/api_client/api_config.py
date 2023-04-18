from django.conf import settings
import requests, json, socket

class ApiConfig:
    def __init__(self):
        self.api_base_url = settings.API_BASE_URL
        self.api_version = settings.API_VERSION
        self.api_token = settings.API_TOKEN
        self.ip_address = socket.gethostbyname(socket.gethostname())

    def get_api_base_url(self):
        return self.api_base_url

    def get_jwt_token(self, username, password):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'username': username, 'password': password})
        jwt_url = f"{self.api_base_url}/{self.api_version}/{self.api_token}/"
        response = requests.post(jwt_url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()['access']
        return None

    @staticmethod
    def get_authenticated_data(url, token):
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except ValueError:
                return None
        return None
