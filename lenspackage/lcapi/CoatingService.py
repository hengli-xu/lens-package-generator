import requests
import json
import yaml

from lenspackage.LensPackageConstant import getDefaultRx, csv_lens_type_map, decideRegion
from settings import env_key, yaml_cfg
from lenspackage.lcapi.data_models import CoatingItem, CoatingType, CompatibleCoatingsResponse


class CoatingService:
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

    def getCompatibleCoatings(self, productId, frameSku, csvPackage, indexSku):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleCoatings"

        print(url)
        print(self.session)

        prescription_data = getDefaultRx()
        prescription_data["type"] = f"{csvPackage.rxType.prescription_type}"

        # 只有当progressiveUsage不为None时才添加
        if csvPackage.rxType.progressive_usage:
            prescription_data["progressiveUsage"] = f"{csvPackage.rxType.progressive_usage}"

        lensType = csv_lens_type_map[csvPackage.LensType]

        data = {
            "productId": f"{productId}",
            "frameSku": f"{frameSku}",
            "prescription": prescription_data,
            "usage": {
                "type": f"{lensType.type}",
                "subType": f"{lensType.sub_type}"
            },
            "lensSku": f"{indexSku}",
            "fulfillmentCenter": "",
            "productType": "configurable_prescription_frame"
        }

        response = self.session.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Compatible coatings retrieved successfully: url ", url)
            response_data = response.json()
            # 转换为data class
            return self.create_coating_response_from_dict(response_data)
        else:
            print(f"Failed to retrieve compatible coatings, status code: {response.status_code}")
            return None

    def create_coating_response_from_dict(self, data: dict) -> CompatibleCoatingsResponse:
        """从字典创建CompatibleCoatingsResponse实例"""
        processed_coatings = []
        for coating_dict in data.get('compatibleCoatings', []):
            items = [CoatingItem(**item) for item in coating_dict.get('items', [])]
            coating_type = CoatingType(type=coating_dict['type'], items=items)
            processed_coatings.append(coating_type)
        
        return CompatibleCoatingsResponse(compatibleCoatings=processed_coatings)
