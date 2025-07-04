import requests
import json
from http.cookies import SimpleCookie
import yaml

from lenspackage.LensPackageConstant import US_REGION
from settings import env_key, yaml_cfg


class FusionAuthService:

    def __init__(self, region=None):
        self.region = region or US_REGION  # Default to US_REGION if no region provided
        config = yaml_cfg[self.region][env_key]
        self.host = config['host']
        self.application_id = config['application_id']
        self.api_key = config['api_key']
        self.auth_code = config['auth_code']
        self.atg_host = config['atg_host']
        self.session = requests.Session()
        self.cookies = SimpleCookie()


    def login(self, login_id, password, ip_address, no_jwt=False):
        url = f"{self.host}/api/login"
        payload = json.dumps({
            "loginId": login_id,
            "password": password,
            "applicationId": self.application_id,
            "noJWT": no_jwt,
            "ipAddress": ip_address
        })
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
        }

        response = self.session.post(url, headers=headers, data=payload)

        # Validate status code
        if response.status_code not in [200, 202]:
            raise Exception(f"Expected status code 200 or 202, but received {response.status_code}")

        # Parse response JSON
        response_data = json.loads(response.text)
        print("Login successful. Cookies set by the server:", self.session.cookies.get_dict())

        # Extract ak_bmsc cookie from the session
        ak_bmsc_value = self.session.cookies.get("ak_bmsc")
        if not ak_bmsc_value:
            raise Exception("ak_bmsc cookie not found in the response.")

        print(f"ak_bmsc cookie retrieved: {ak_bmsc_value}")

        # Extract token and refresh token from the response
        token_value = response_data.get("token")
        refresh_token_value = response_data.get("refreshToken")

        # Set additional cookies for the next request
        self.add_cookie_to_session({"key": "aWRfdG9rZW4.", "value": token_value, "path": "/"}, domain=self.atg_host)
        self.add_cookie_to_session({"key": "ak_bmsc", "value": ak_bmsc_value, "path": "/"}, domain=self.atg_host)
        self.add_cookie_to_session({"key": "cmVmcmVzaF90b2tlbg...", "value": "", "path": "/"}, domain=self.atg_host)
        self.add_cookie_to_session({"key": "auth", "value": self.auth_code, "path": "/"}, domain=self.atg_host)


        print(f"Token: {token_value}, Refresh Token: {refresh_token_value}")

        return token_value  # Return the token_value directly instead of adding it to the session

    # def get_current_user(self, token_value):
        # url = f"https://{self.atg_host}/api/v1/currentUser"
        # headers = {
        #     'Authorization': f"Bearer {token_value}",  # Use the token directly in the headers
        #     'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
        #     'Host': "qaca.zenniaws.com"  # Add any custom header here
        # }

        # response = self.session.get(url, headers=headers)

        # if response.status_code == 200:
        #     print("User data retrieved successfully:", response.text)
        # else:
        #     print(f"Failed to retrieve user data, status code: {response.status_code}")

    def add_cookie_to_session(self, cookie, domain):
        """Add a cookie to the session for a specific domain."""
        self.session.cookies.set(cookie["key"], cookie["value"], domain=domain, path=cookie["path"])
        print(f"Cookie '{cookie['key']}' added to session for domain: {domain}.")

