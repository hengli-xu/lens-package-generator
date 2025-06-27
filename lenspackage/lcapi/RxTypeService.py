import requests
import json
from http.cookies import SimpleCookie
import yaml

from lenspackage.LensPackageConstant import decideRegion
from settings import env_key, yaml_cfg


class RxTypeService:
    def __init__(self, session=None, token_value=None):
        self.session = session or requests.Session()
        config = yaml_cfg[decideRegion()][env_key]
        self.atg_host = config['atg_host']

        self.headers = {
            'Authorization': f"Bearer {token_value}",
            'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
            'Host': self.atg_host,
            'Content-Type': 'application/json'
        }

    def getCompatibleLensTypes(self, productId, frameSku, csvPackage):
        # 虽然是RxType的校验，但是调用接口的名字是compatibleLensTypes
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleLensTypes"

        print(url)
        print(self.session)

        data = {
            "frameSku": f"{frameSku}",
            "fulfillmentCenter": ""
        }

        response = self.session.post(url, headers=self.headers, json= data)

        if response.status_code == 200:
            print("Compatible lens types retrieved successfully:")
            return response.json()
        else:
            print(f"Failed to retrieve compatible lens types, status code: {response.status_code}")
            return None


    def checkRxTypeCompatibility(self, csvPackage, compatible_lens_types_response):
        """
        检查csvPackage的RxType是否与compatible_lens_types匹配
        """
        compatible_lens_types = compatible_lens_types_response.get('compatibleLensTypes', [])
        print(f"rxType check compatible_lens_types: {compatible_lens_types}")

        for item in compatible_lens_types:
            item_type = item.get('type')
            prescription_types = item.get('prescriptionTypes')
            
            # 当item的type是prescription时，检查RxType是否在prescriptionTypes中
            if item_type == 'prescription' and prescription_types:
                if csvPackage.rxType.prescription_type in prescription_types:
                    return True
            
            # 检查RxType是否直接匹配item的type
            elif csvPackage.rxType.prescription_type == item_type:
                return True
        
        return False