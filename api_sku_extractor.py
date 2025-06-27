import requests
import json
from typing import List, Dict, Any, Optional

class SKUExtractor:
    """SKU数据提取器"""
    
    def __init__(self, base_url: str = "http://sitca.zenniaws.com:80"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_skus_by_product(self, product_id: str, limit: int = 30) -> Optional[Dict[str, Any]]:
        """
        获取指定产品的SKU列表
        
        Args:
            product_id: 产品ID
            limit: 每页数量限制
            
        Returns:
            API响应数据或None
        """
        url = f"{self.base_url}/api/v1/skus"
        params = {
            'parentItemId': product_id,
            'parentPropertyName': 'childSKUs',
            'parentItemType': 'product',
            'limit': limit
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API请求失败: {e}")
            return None
    
    def extract_sku_ids(self, response_data: Dict[str, Any]) -> List[str]:
        """
        快速提取SKU ID列表
        
        Args:
            response_data: API响应数据
            
        Returns:
            SKU ID列表
        """
        return [item['id'] for item in response_data.get('items', [])]
    
    def extract_sku_details(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        提取SKU详细信息
        
        Args:
            response_data: API响应数据
            
        Returns:
            SKU详细信息列表
        """
        sku_details = []
        items = response_data.get('items', [])
        
        for item in items:
            detail = {
                'id': item.get('id'),
                'displayName': item.get('displayName'),
                'color': item.get('color', {}).get('cleanName'),
                'stockQuantity': item.get('stockQuantity'),
                'status': item.get('status'),
                'price': item.get('rushSku', {}).get('listPrice'),
                'imageUrl': item.get('imageUrl'),
                'seoName': item.get('seoName')
            }
            sku_details.append(detail)
        
        return sku_details
    
    def get_all_sku_ids(self, product_id: str) -> List[str]:
        """
        获取产品的所有SKU ID（处理分页）
        
        Args:
            product_id: 产品ID
            
        Returns:
            所有SKU ID列表
        """
        all_sku_ids = []
        offset = 0
        limit = 30
        
        while True:
            response = self.get_skus_by_product(product_id, limit)
            if not response:
                break
            
            sku_ids = self.extract_sku_ids(response)
            all_sku_ids.extend(sku_ids)
            
            # 检查是否还有更多数据
            has_more = response.get('hasMore', 'false').lower() == 'true'
            if not has_more:
                break
            
            offset += limit
        
        return all_sku_ids

# 使用示例
def main():
    # 创建提取器实例
    extractor = SKUExtractor()
    
    # 示例产品ID（从你的数据中看到的）
    product_id = "20189"
    
    print(f"正在获取产品 {product_id} 的SKU信息...")
    
    # 方法1: 获取单页SKU ID
    response = extractor.get_skus_by_product(product_id)
    if response:
        sku_ids = extractor.extract_sku_ids(response)
        print(f"提取到的SKU IDs: {sku_ids}")
        print(f"总共 {len(sku_ids)} 个SKU")
        
        # 方法2: 获取详细信息
        sku_details = extractor.extract_sku_details(response)
        print("\n=== SKU详细信息 ===")
        for detail in sku_details:
            print(f"ID: {detail['id']}")
            print(f"  名称: {detail['displayName']}")
            print(f"  颜色: {detail['color']}")
            print(f"  库存: {detail['stockQuantity']}")
            print(f"  价格: ${detail['price']}")
            print(f"  状态: {detail['status']}")
            print()
    
    # 方法3: 如果你有完整的API响应数据，可以直接使用
    print("=== 直接处理API响应数据 ===")
    
    # 你的完整API响应数据
    api_response = {
        "hasMore": "false",
        "links": [...],
        "items": [
            {
                "id": "2018918",
                "displayName": "2018918 Rectangle Glasses",
                "color": {"cleanName": "Red", "code": "Red", "description": "Red"},
                "stockQuantity": 6334,
                "status": "enabled",
                "rushSku": {"listPrice": 19.0, "salePrice": 0.0},
                "imageUrl": "https://sit-static.zenniaws.com/production/products/general/20/18/2018918-eyeglasses-front-view.jpg?output-quality=90&resize=800px:*"
            },
            {
                "id": "2018921",
                "displayName": "2018921 Rectangle Glasses", 
                "color": {"cleanName": "Black", "code": "Black", "description": "Black"},
                "stockQuantity": 36637,
                "status": "enabled",
                "rushSku": {"listPrice": 19.0, "salePrice": 0.0},
                "imageUrl": "https://sit-static.zenniaws.com/production/products/general/20/18/2018921-eyeglasses-front-view.jpg?output-quality=90&resize=800px:*"
            }
        ]
    }
    
    # 快速提取ID
    ids = extractor.extract_sku_ids(api_response)
    print(f"从完整响应中提取的SKU IDs: {ids}")

if __name__ == "__main__":
    main() 