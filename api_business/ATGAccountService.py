import requests
import json
from http.cookies import SimpleCookie
import yaml
from settings import env_key, yaml_cfg

class ATGAccountService:
    def __init__(self, session=None, token_value=None):
        self.session = session or requests.Session()
        config = yaml_cfg["CA"][env_key]
        self.atg_host = config['atg_host']

        self.headers = {
            'Authorization': f"Bearer {token_value}",  # Use the token directly in the headers
            'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
            'Host': self.atg_host  # Add any custom header here
        }

    def get_current_user(self):
        url = f"https://{self.atg_host}/api/v1/currentUser"

        print(url)
        print(self.session)

        response = self.session.get(url, headers=self.headers)
    
        print(response)

        if response.status_code == 200:
            print("User data retrieved successfully:", response.text)
        else:
            print(f"Failed to retrieve user data, status code: {response.status_code}")