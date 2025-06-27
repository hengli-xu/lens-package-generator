import requests
import json
from http.cookies import SimpleCookie
import yaml

from lenspackage.LensPackageConstant import getDefaultRx, csv_lens_type_map, decideRegion
from settings import env_key, yaml_cfg


class IndexService:
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

    def getCompatibleLenses(self, productId, frameSku, csvPackage):
        url = f"https://{self.atg_host}/api/v1/zenni-prescription-rules/compatibleLenses"

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
            "fulfillmentCenter": "",
            "usage": {
                "type": f"{lensType.type}",
                "subType": f"{lensType.sub_type}"
            },
            "productType": "configurable_prescription_frame"
        }

        response = self.session.post(url, headers=self.headers, json=data)

        if response.status_code == 200:
            print("Compatible lenses retrieved successfully: url ", response.text)
            return response.json()
        else:
            print(f"Failed to retrieve compatible lenses, status code: {response.status_code}")
            return None 

    def checkIndexCompatibility(self, csvPackage, compatible_lenses_response):
        """
        检查csvPackage.index与compatible_lenses的匹配，并压缩数据
        """
        if not compatible_lenses_response:
            return []
            
        compatible_lenses = compatible_lenses_response.get('compatibleLenses', [])
        csv_indexes = csvPackage.index  # 这是字符串列表，如 ["1.50", "1.61", "1.67"]
        
        # 将csv_indexes转换为浮点数列表
        csv_index_float = []
        for index_str in csv_indexes:
            try:
                csv_index_float.append(float(index_str))
            except ValueError:
                print(f"Warning: Invalid index value '{index_str}' in csvPackage.index")
                continue
        
        # 过滤匹配的镜片
        matched_lenses = []
        for lens in compatible_lenses:
            lens_index = lens.get('lensIndex')
            if lens_index in csv_index_float:
                matched_lenses.append(lens)
        
        # 压缩数据格式
        compressed_indexes = []
        for lens in matched_lenses:
            compressed_index = {
                "cost": [
                    {
                        "price": lens.get('price', 0),
                        "region": f"{decideRegion()}"  # 可以根据需要调整
                    }
                ],
                "lensIndex": lens.get('lensIndex'),
                "sku": lens.get('sku', '')
            }
            compressed_indexes.append(compressed_index)
        
        return compressed_indexes 