#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速SKU ID提取器
用于从API响应中快速提取SKU的id列表
"""

import json
from typing import List, Dict, Any

def quick_extract_sku_ids(response_data: Dict[str, Any]) -> List[str]:
    """
    快速提取SKU ID列表 - 一行代码解决
    
    Args:
        response_data: API响应的JSON数据
        
    Returns:
        List[str]: SKU ID列表
    """
    return [item['id'] for item in response_data.get('items', [])]

def quick_extract_sku_ids_safe(response_data: Dict[str, Any]) -> List[str]:
    """
    安全提取SKU ID列表（包含错误处理）
    
    Args:
        response_data: API响应的JSON数据
        
    Returns:
        List[str]: SKU ID列表
    """
    try:
        return [item['id'] for item in response_data.get('items', []) if 'id' in item]
    except (KeyError, TypeError, AttributeError):
        return []

# 示例：你的API响应数据
sample_response = {
    "hasMore": "false",
    "links": [
        {"method": "GET", "rel": "last", "href": "http://sitca.zenniaws.com:80/api/v1/skus?parentItemId=20189&parentPropertyName=childSKUs&parentItemType=product&offset=0&limit=6"},
        {"method": "GET", "rel": "self", "href": "http://sitca.zenniaws.com:80/api/v1/skus?parentItemId=20189&parentPropertyName=childSKUs&parentItemType=product"},
        {"method": "GET", "rel": "canonical", "href": "http://sitca.zenniaws.com:80/api/v1/skus"},
        {"method": "GET", "rel": "first", "href": "http://sitca.zenniaws.com:80/api/v1/skus?parentItemId=20189&parentPropertyName=childSKUs&parentItemType=product&offset=0&limit=30"}
    ],
    "items": [
        {"id": "2018918", "displayName": "2018918 Rectangle Glasses", "color": {"cleanName": "Red"}},
        {"id": "2018921", "displayName": "2018921 Rectangle Glasses", "color": {"cleanName": "Black"}},
        {"id": "2018916", "displayName": "2018916 Rectangle Glasses", "color": {"cleanName": "Blue"}},
        {"id": "2018915", "displayName": "2018915 Rectangle Glasses", "color": {"cleanName": "Brown"}},
        {"id": "2018923", "displayName": "2018923 Rectangle Glasses", "color": {"cleanName": "Clear"}},
        {"id": "2018924", "displayName": "2018924 Rectangle Glasses", "color": {"cleanName": "Green"}}
    ]
}

if __name__ == "__main__":
    print("=== 快速SKU ID提取示例 ===")
    
    # 方法1: 最简单的提取方式
    sku_ids = quick_extract_sku_ids(sample_response)
    print(f"提取到的SKU IDs: {sku_ids}")
    print(f"总共 {len(sku_ids)} 个SKU")
    
    # 方法2: 如果你有字符串形式的JSON数据
    print("\n=== 处理字符串JSON数据 ===")
    json_string = json.dumps(sample_response)
    parsed_data = json.loads(json_string)
    ids_from_string = quick_extract_sku_ids(parsed_data)
    print(f"从字符串解析的SKU IDs: {ids_from_string}")
    
    # 方法3: 实际使用示例
    print("\n=== 实际使用示例 ===")
    print("在你的代码中，可以这样使用：")
    print("""
# 假设你的API响应存储在变量 api_response 中
sku_ids = quick_extract_sku_ids(api_response)
print(f"SKU IDs: {sku_ids}")

# 或者如果你有JSON字符串
import json
response_data = json.loads(json_string)
sku_ids = quick_extract_sku_ids(response_data)
print(f"SKU IDs: {sku_ids}")
    """)
    
    # 方法4: 一行代码版本
    print("\n=== 一行代码版本 ===")
    print("最简洁的提取方式：")
    print("sku_ids = [item['id'] for item in response_data.get('items', [])]")
    
    # 演示
    one_line_result = [item['id'] for item in sample_response.get('items', [])]
    print(f"一行代码提取结果: {one_line_result}") 