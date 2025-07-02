import requests

from lenspackage.LensPackageConstant import getDefaultRx, csv_lens_type_map, decideRegion
from settings import env_key, yaml_cfg
from lenspackage.lcapi.data_models import TintItem, CompatibleTintsResponse


class TintService:
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

    def getCompatibleTints(self, productId, frameSku, csvPackage, indexSku):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleTints"

        prescription_data = getDefaultRx()
        prescription_data["type"] = f"{csvPackage.rxType.prescription_type}"

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
            print("Compatible tints retrieved successfully")
            response_data = response.json()
            # 转换为data class
            return self.create_compatible_tints_response_from_dict(response_data)
        else:
            print(f"Failed to retrieve compatible tints, status code: {response.status_code}")
            return None

    def create_compatible_tints_response_from_dict(self, data: dict) -> CompatibleTintsResponse:
        """从字典创建CompatibleTintsResponse实例"""
        tints = [TintItem(**tint) for tint in data.get('compatibleTints', [])]
        return CompatibleTintsResponse(
            compatibleTints=tints,
            additionalChargeInfo=data.get('additionalChargeInfo', {})
        )