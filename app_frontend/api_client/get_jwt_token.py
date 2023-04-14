import requests
import json

def get_jwt_token(username, password, url):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': username, 'password': password})
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json()['access']
    return None


def get_authenticated_data(url, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            return data[0] if data else None
        except ValueError:
            return None
    return None