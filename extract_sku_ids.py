import json
from typing import List, Dict, Any

def extract_sku_ids_from_response(response_data: Dict[str, Any]) -> List[str]:
    """
    从API响应中快速提取所有SKU的id
    
    Args:
        response_data: API响应的JSON数据
        
    Returns:
        List[str]: 包含所有SKU id的列表
    """
    # 方法1: 使用列表推导式（推荐）
    sku_ids = [item['id'] for item in response_data.get('items', [])]
    return sku_ids

def extract_sku_ids_with_validation(response_data: Dict[str, Any]) -> List[str]:
    """
    从API响应中提取SKU的id，包含验证
    
    Args:
        response_data: API响应的JSON数据
        
    Returns:
        List[str]: 包含所有SKU id的列表
    """
    sku_ids = []
    items = response_data.get('items', [])
    
    for item in items:
        if isinstance(item, dict) and 'id' in item:
            sku_ids.append(item['id'])
    
    return sku_ids

def extract_sku_info(response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    提取SKU的更多信息，包括id、displayName、color等
    
    Args:
        response_data: API响应的JSON数据
        
    Returns:
        List[Dict]: 包含SKU信息的列表
    """
    sku_info = []
    items = response_data.get('items', [])
    
    for item in items:
        if isinstance(item, dict):
            info = {
                'id': item.get('id'),
                'displayName': item.get('displayName'),
                'color': item.get('color', {}).get('cleanName'),
                'stockQuantity': item.get('stockQuantity'),
                'status': item.get('status')
            }
            sku_info.append(info)
    
    return sku_info

# 示例使用
if __name__ == "__main__":
    # 你的API响应数据（这里只展示部分数据作为示例）
    sample_response = {
        "hasMore": "false",
        "links": [...],
        "items": [
            {
                "id": "2018918",
                "displayName": "2018918 Rectangle Glasses",
                "color": {"cleanName": "Red", "code": "Red", "description": "Red"},
                "stockQuantity": 6334,
                "status": "enabled"
            },
            {
                "id": "2018921", 
                "displayName": "2018921 Rectangle Glasses",
                "color": {"cleanName": "Black", "code": "Black", "description": "Black"},
                "stockQuantity": 36637,
                "status": "enabled"
            }
        ]
    }
    
    # 方法1: 只提取id
    print("=== 只提取SKU ID ===")
    sku_ids = extract_sku_ids_from_response(sample_response)
    print(f"SKU IDs: {sku_ids}")
    print(f"总共 {len(sku_ids)} 个SKU")
    
    # 方法2: 提取更多信息
    print("\n=== 提取SKU详细信息 ===")
    sku_info = extract_sku_info(sample_response)
    for info in sku_info:
        print(f"ID: {info['id']}, 名称: {info['displayName']}, 颜色: {info['color']}, 库存: {info['stockQuantity']}")
    
    # 方法3: 如果你有完整的API响应，可以这样使用
    print("\n=== 实际使用示例 ===")
    # 假设你的API响应存储在变量 api_response 中
    # sku_ids = extract_sku_ids_from_response(api_response)
    # print(f"提取到的SKU IDs: {sku_ids}") 