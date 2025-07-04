import requests
import json
from http.cookies import SimpleCookie
import yaml
from typing import Dict, Any, List

from lenspackage.LensPackageConstant import US_REGION
from settings import env_key, yaml_cfg


class PdpService:
    def __init__(self, session=None, token_value=None, region=None):
        self.session = session or requests.Session()
        self.region = region or US_REGION  # Default to US_REGION if no region provided
        config = yaml_cfg[self.region][env_key]
        self.atg_host = config['atg_host']

        self.headers = {
            'Authorization': f"Bearer {token_value}",  # Use the token directly in the headers
            'User-Agent': 'ZenniAppIos/6.1.4 Mozilla/5.0 (iPhone; CPU iPhone OS 18.3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/605.1.15 ZenniAppIos',
            'Host': self.atg_host  # Add any custom header here
        }

    def extract_sku_ids_from_response(self, response_data: Dict[str, Any]) -> List[str]:
        """
        从API响应中提取SKU ID列表
        
        Args:
            response_data: API响应的JSON数据
            
        Returns:
            List[str]: SKU ID列表
        """
        sku_ids = [item['id'] for item in response_data.get('items', [])]
        print(f"sku_ids: {sku_ids}")  # 修复字符串格式化
        return sku_ids

    def getPdp(self, productId):
        url = f"https://{self.atg_host}/api/v1/skus?parentItemId={productId}&parentPropertyName=childSKUs&parentItemType=product"

        print(url)
        print(self.session)

        response = self.session.get(url, headers=self.headers)

        if response.status_code == 200:
            print(f"User data retrieved successfully: url = {url}")

            # 解析JSON响应
            try:
                response_data = response.json()
                # 正确调用方法，传递解析后的JSON数据
                sku_ids = self.extract_sku_ids_from_response(response_data)
                print(f"提取到的SKU IDs: {sku_ids}")
                return sku_ids
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}")
                return []
        else:
            print(f"Failed to retrieve user data, status code: {response.status_code}")
            return []
