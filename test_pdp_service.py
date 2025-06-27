#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试PdpService的SKU ID提取功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lenspackage.lcapi.PdpService import PdpService

def test_sku_extraction():
    """测试SKU ID提取功能"""
    
    # 创建PdpService实例（不传递token，仅用于测试）
    pdp_service = PdpService()
    
    # 模拟API响应数据
    mock_response_data = {
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
    
    print("=== 测试SKU ID提取功能 ===")
    
    # 测试extract_sku_ids_from_response方法
    try:
        sku_ids = pdp_service.extract_sku_ids_from_response(mock_response_data)
        print(f"✅ 测试成功！提取到的SKU IDs: {sku_ids}")
        print(f"✅ 总共提取到 {len(sku_ids)} 个SKU")
        
        # 验证提取的ID
        expected_ids = ["2018918", "2018921", "2018916", "2018915", "2018923", "2018924"]
        if sku_ids == expected_ids:
            print("✅ SKU ID提取结果正确！")
        else:
            print(f"❌ SKU ID提取结果不正确！期望: {expected_ids}, 实际: {sku_ids}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

def test_with_real_api_call():
    """测试真实的API调用（需要有效的token）"""
    print("\n=== 测试真实API调用 ===")
    print("注意：这个测试需要有效的token才能成功")
    
    # 这里你可以传入真实的token进行测试
    # token = "your_real_token_here"
    # pdp_service = PdpService(token_value=token)
    # result = pdp_service.getPdp("20189")
    
    print("跳过真实API调用测试（需要token）")

if __name__ == "__main__":
    test_sku_extraction()
    test_with_real_api_call() 