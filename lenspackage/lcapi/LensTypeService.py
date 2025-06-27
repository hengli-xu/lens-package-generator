import requests
import json
from http.cookies import SimpleCookie
import yaml

from lenspackage.LensPackageConstant import getDefaultRx
from settings import env_key, yaml_cfg


class LensTypeService:
    def __init__(self, session=None, token_value=None):
        self.session = session or requests.Session()
        config = yaml_cfg["CA"][env_key]
        self.atg_host = config['atg_host']

        self.headers = {
            'Authorization': f"Bearer {token_value}",
            'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
            'Host': self.atg_host,
            'Content-Type': 'application/json'
        }

    def getUsageTypes(self, productId, frameSku, csvPackage):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/usageTypes"

        print(url)
        print(self.session)

        prescription_data = getDefaultRx()
        prescription_data["type"] = f"{csvPackage.rxType.prescription_type}"

        # 只有当progressiveUsage不为None时才添加
        if csvPackage.rxType.progressive_usage:
            prescription_data["progressiveUsage"] = f"{csvPackage.rxType.progressive_usage}"

        data = {
            "productId": f"{productId}",
            "frameSku": f"{frameSku}",
            "prescription": prescription_data,
            "fulfillmentCenter": "",
            "productType": "configurable_prescription_frame"
        }
        response = self.session.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Usage types retrieved successfully: url ", url)
            return response.json()
        else:
            print(f"Failed to retrieve usage types, status code: {response.status_code}")
            return None
