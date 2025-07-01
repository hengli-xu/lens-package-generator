from dataclasses import dataclass
from pickletools import uint4
from typing import List

import requests
import json
from http.cookies import SimpleCookie
import yaml

from lenspackage.LensPackageConstant import getDefaultRx, csv_lens_type_map, decideRegion
from settings import env_key, yaml_cfg
from lenspackage.lcapi.data_models import (
    CompatibleLensesResponse, 
    create_compatible_lenses_response_from_dict, 
    group_lenses_by_index, 
    filter_lenses_by_index,
    create_compressed_lens_indexes,
    CompressedLensIndex
)

class IndexService:
    def __init__(self, session=None, token_value=None):
        self.session = session or requests.Session()
        self.token_value = token_value
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

        # 只有当progressiveUsage不为None时才添加画
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
            print("Compatible lenses retrieved successfully: url ", url)
            response_data = response.json()
            # 转换为data class
            return create_compatible_lenses_response_from_dict(response_data)
        else:
            print(f"Failed to retrieve compatible lenses, status code: {response.status_code}")
            return None

    def checkIndexCompatibility(self, csvPackage, compatible_lenses_response):
        """
        检查csvPackage.index与compatible_lenses的匹配，并压缩数据
        """
        if not compatible_lenses_response:
            return [], []

        # 现在compatible_lenses_response是CompatibleLensesResponse对象
        compatible_lenses = compatible_lenses_response.compatibleLenses
        csv_indexes = csvPackage.index  # 这是字符串列表，如 ["1.50", "1.61", "1.67"]

        # 将csv_indexes转换为浮点数列表
        csv_index_float = []
        for index_str in csv_indexes:
            try:
                csv_index_float.append(float(index_str))
            except ValueError:
                print(f"Warning: Invalid index value '{index_str}' in csvPackage.index")
                continue

        # 使用工具函数过滤匹配的镜片
        matched_lenses = filter_lenses_by_index(compatible_lenses, csv_index_float)

        # 使用data class创建压缩数据格式
        compressed_indexes = create_compressed_lens_indexes(matched_lenses, decideRegion())

        return matched_lenses, compressed_indexes

    def groupIndexesByLensIndex(self, indexes):
        """
        按lensIndex对indexes进行分组
        """
        groups = {}
        for index in indexes:
            lens_index = index.lensIndex
            if lens_index not in groups:
                groups[lens_index] = []
            groups[lens_index].append(index)
        return groups

    def getAllTintsForGroup(self, productId, frameSku, csvPackage, index_items):
        """
        获取该组所有可用的tint
        """
        from lenspackage.lcapi.TintService import TintService
        
        tint_service = TintService(session=self.session, token_value=self.token_value)
        all_tints = []

        # 获取每个indexSku的tint结果
        for index_item in index_items:
            index_sku = index_item.sku
            tint_result = tint_service.getCompatibleTints(productId, frameSku, csvPackage, index_sku)
            if tint_result:
                tints = tint_result.get('compatibleTints', [])
                all_tints.extend(tints)

        # 去重，保留唯一的tint
        unique_tints = []
        seen_skus = set()
        for tint in all_tints:
            tint_sku = tint.get('sku')
            if tint_sku and tint_sku not in seen_skus:
                unique_tints.append(tint)
                seen_skus.add(tint_sku)

        # 如果没有tint，也要添加一个None表示无tint的情况
        if not unique_tints:
            unique_tints.append(None)

        return unique_tints
