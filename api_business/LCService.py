import requests
import json
from http.cookies import SimpleCookie
import yaml
from settings import env_key, yaml_cfg

class LCService:
    def __init__(self, session=None, token_value=None):
        self.session = session or requests.Session()
        config = yaml_cfg["CA"][env_key]
        self.atg_host = config['atg_host']

        self.headers = {
            'Authorization': f"Bearer {token_value}",  # Use the token directly in the headers
            'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
            'Host': self.atg_host  # Add any custom header here
        }

    def addToCart(self):
        url = f"https://{self.atg_host}/api/v1/cart/commerceItems/orderGlasses"
        print("Request URL:", url)

        data = {
            "rushDelivery": False,
            "quantity": 1,
            "selectedFrameAndLens": {
                "lenskuId": "1519",
                "mainFrameProductId": "78024",
                "frameSkuId": "7802429",
                "coatingId": "ctsku100002_free"
            },
            "prescription": {
                "pdSingle": 40,
                "prismEnabled": False,
                "singlePd": True,
                "prescriptionSavedName": "40",
                "prescriptionSavedYear": "2025",
                "birthYear": "2000",
                "odCyl": 0,
                "prescriptionType": "SingleVision",
                "prescriptionRenewMonths": "183",
                "pdLeft": 0,
                "odSph": -7.75,
                "osCyl": 0,
                "prescriptionSavedMonth": "4",
                "prescriptionIsToBeSaved": True,
                "pdRight": 0,
                "odAxis": 0,
                "osAxis": 0,
                "prescriptionSavedDay": "23",
                "osSph": -7.75,
                "prescriptionIsRenew": True
            }
        }

        print("Request URL:", url)
        # print("Request Data:", data)

        response = self.session.post(url, headers=self.headers, json=data)

        print("Response Status Code:", response.status_code)
        # print("Response Body:", response.text)

        if response.status_code == 200:
            print("Item added to cart successfully:", response.json())
        else:
            print(f"Failed to add item to cart, status code: {response.status_code}")

    def getCompatibleTints(self):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleTints"
        print("Request URL:", url)

        data = {
            "prescription": {
                "pdDualLeft": 0,
                "os": {
                    "sph": 0,
                    "cyl": 0,
                    "prismValueHorizontal": 0,
                    "prismValueVertical": 0,
                    "axis": 0
                },
                "birthYear": 0,
                "pdSingle": 0,
                "prismEnabled": False,
                "type": "NonPrescription",
                "nvAdd": 0,
                "pdDualRight": 0,
                "od": {
                    "prismValueVertical": 0,
                    "sph": 0,
                    "axis": 0,
                    "cyl": 0,
                    "prismValueHorizontal": 0
                }
            },
            "fulfillmentCenter": "",
            "frameSku": "7802429",
            "lensSku": "2417",
            "usage": {
                "type": "Blokz",
                "subType": "BlokzTinted"
            }
        }

        response = self.session.post(url, headers=self.headers, json=data)

        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            print("Compatible tints retrieved successfully:", response.json())
            return response.json()
        else:
            print(f"Failed to retrieve compatible tints, status code: {response.status_code}")
            return None

    def getCompatibleLensTypes(self):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleLensTypes"
        print("Request URL:", url)

        data = {
            "frameSku": "7802429",
            "fulfillmentCenter": ""
        }

        response = self.session.post(url, headers=self.headers, json=data)

        print("Request URL:", url)
        print("Request Data:", data)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            print("Compatible lens types retrieved successfully:", response.json())
            return response.json()
        else:
            print(f"Failed to retrieve compatible lens types, status code: {response.status_code}")
            return None

    def getUsageTypes(self):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/usageTypes"

        data = {
            "prescription": {
                "prismEnabled": False,
                "pdSingle": 0,
                "pdDualRight": 0,
                "birthYear": 0,
                "type": "NonPrescription",
                "nvAdd": 0,
                "pdDualLeft": 0,
                "os": {
                    "sph": 0,
                    "axis": 0,
                    "prismValueHorizontal": 0,
                    "prismValueVertical": 0,
                    "cyl": 0
                },
                "od": {
                    "prismValueHorizontal": 0,
                    "cyl": 0,
                    "prismValueVertical": 0,
                    "sph": 0,
                    "axis": 0
                }
            },
            "frameSku": "7802429",
            "fulfillmentCenter": ""
        }

        response = self.session.post(url, headers=self.headers, json=data)

        print("Request URL:", url)
        print("Request Data:", data)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            print("Usage types retrieved successfully:", response.json())
            return response.json()
        else:
            print(f"Failed to retrieve usage types, status code: {response.status_code}")
            return None

    def getCompatibleLenses(self):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleLenses"

        data = {
            "fulfillmentCenter": "",
            "prescription": {
                "nvAdd": 0,
                "od": {
                    "cyl": 0,
                    "prismValueHorizontal": 0,
                    "axis": 0,
                    "sph": 0,
                    "prismValueVertical": 0
                },
                "birthYear": 0,
                "type": "NonPrescription",
                "pdDualRight": 0,
                "pdDualLeft": 0,
                "os": {
                    "axis": 0,
                    "prismValueHorizontal": 0,
                    "cyl": 0,
                    "prismValueVertical": 0,
                    "sph": 0
                },
                "prismEnabled": False,
                "pdSingle": 0
            },
            "frameSku": "7802429",
            "usage": {
                "subType": "BlokzTinted",
                "type": "Blokz"
            }
        }

        response = self.session.post(url, headers=self.headers, json=data)

        print("Request URL:", url)
        print("Request Data:", data)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)

        if response.status_code == 200:
            print("Compatible lenses retrieved successfully:", response.json())
            return response.json()
        else:
            print(f"Failed to retrieve compatible lenses, status code: {response.status_code}")
            return None

    def getCompatibleCoatings(self):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleCoatings"

        data = {
            "prescription": {
                "birthYear": 0,
                "pdSingle": 0,
                "pdDualRight": 0,
                "od": {
                    "sph": 0,
                    "prismValueHorizontal": 0,
                    "cyl": 0,
                    "axis": 0,
                    "prismValueVertical": 0
                },
                "pdDualLeft": 0,
                "os": {
                    "prismValueHorizontal": 0,
                    "cyl": 0,
                    "sph": 0,
                    "prismValueVertical": 0,
                    "axis": 0
                },
                "prismEnabled": False,
                "type": "NonPrescription",
                "nvAdd": 0
            },
            "usage": {
                "type": "Blokz",
                "subType": "BlokzTinted"
            },
            "tintSku": "tsku2000035",
            "frameSku": "7802429",
            "fulfillmentCenter": "",
            "lensSku": "2417"
        }

        response = self.session.post(url, headers=self.headers, json=data)

        print("Request URL:", url)
        print("Request Data:", data)
        print("Response Status Code:", response.status_code)
        print("Response Body:", response.text)


