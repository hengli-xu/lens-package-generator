"""
示例：如何使用IndexService API返回值的data class
"""

from lenspackage.lcapi.data_models import (
    CompatibleLens, 
    CompatibleLensesResponse, 
    create_compatible_lenses_response_from_dict,
    group_lenses_by_index,
    filter_lenses_by_index,
    get_recommended_lenses,
    get_lens_by_sku
)


def example_usage():
    """示例用法"""
    
    # 模拟API返回的JSON数据
    sample_api_response = {
        "compatibleLenses": [
            {
                "tintBase": "Gray",
                "brandName": "",
                "productId": "prodLensEyeQPlus",
                "salePrice": 0,
                "ignoreIncludedTints": False,
                "isStandardDelivery": True,
                "displayName": "1.50 EyeQLenz with Zenni ID Guard Digital Free Form Progressive",
                "cssValue": "eyeqpluswithzenniidguard-sunglass-solid-gray",
                "groupBy": "1.5_EyeQPlusWithZenniIdGuard",
                "classification": "premium",
                "isRushDelivery": False,
                "lensIndex": 1.5,
                "isPriority": False,
                "recommendedIndex": 1.5,
                "tintClassification": "Classic",
                "price": 109.95,
                "isRecommended": True,
                "skuDisplayName": "1.50 EyeQLenz with Zenni ID Guard Digital Free Form Progressive - Gray",
                "sku": "61199",
                "inlineStyle": " background: #726D6Eff;"
            },
            {
                "tintBase": "Brown",
                "brandName": "",
                "productId": "prodLensEyeQPlus",
                "salePrice": 0,
                "ignoreIncludedTints": False,
                "isStandardDelivery": True,
                "displayName": "1.50 EyeQLenz with Zenni ID Guard Digital Free Form Progressive",
                "cssValue": "eyeqpluswithzenniidguard-sunglass-solid-brown",
                "groupBy": "1.5_EyeQPlusWithZenniIdGuard",
                "classification": "premium",
                "isRushDelivery": False,
                "lensIndex": 1.5,
                "isPriority": False,
                "recommendedIndex": 0,
                "tintClassification": "Classic",
                "price": 109.95,
                "isRecommended": False,
                "skuDisplayName": "1.50 EyeQLenz with Zenni ID Guard Digital Free Form Progressive - Brown",
                "sku": "61198",
                "inlineStyle": "background: #805A50ff;"
            },
            {
                "tintBase": "Gray",
                "brandName": "",
                "productId": "prodLensEyeQPlus",
                "salePrice": 0,
                "ignoreIncludedTints": False,
                "isStandardDelivery": True,
                "displayName": "1.61 MR8Plus Hi-Index Impact-Resistant EyeQLenz with Zenni ID Guard Digital Free Form Progressive",
                "cssValue": "eyeqpluswithzenniidguard-sunglass-solid-gray",
                "groupBy": "1.61_EyeQPlusWithZenniIdGuard",
                "classification": "premium",
                "isRushDelivery": False,
                "lensIndex": 1.61,
                "isPriority": False,
                "recommendedIndex": 0,
                "tintClassification": "Classic",
                "price": 151.95,
                "isRecommended": False,
                "skuDisplayName": "1.61 MR8Plus Hi-Index Impact-Resistant EyeQLenz with Zenni ID Guard - Gray",
                "sku": "65199",
                "inlineStyle": " background: #726D6Eff;"
            }
        ]
    }
    
    # 1. 将JSON数据转换为data class
    print("=== 1. 转换JSON数据为data class ===")
    response = create_compatible_lenses_response_from_dict(sample_api_response)
    print(f"转换成功，共有 {len(response.compatibleLenses)} 个镜片")
    
    # 2. 按lensIndex分组
    print("\n=== 2. 按lensIndex分组 ===")
    index_groups = group_lenses_by_index(response.compatibleLenses)
    for index, lenses in index_groups.items():
        print(f"Index {index}: {len(lenses)} 个镜片")
        for lens in lenses:
            print(f"  - {lens.displayName} (SKU: {lens.sku}, Price: ${lens.price})")
    
    # 3. 获取唯一的tintBase
    print("\n=== 3. 获取唯一的tintBase ===")
    unique_tints = list(set(lens.tintBase for lens in response.compatibleLenses))
    print(f"可用的tintBase: {unique_tints}")
    
    # 4. 过滤特定index的镜片
    print("\n=== 4. 过滤特定index的镜片 ===")
    target_indexes = [1.5, 1.61]
    filtered_lenses = filter_lenses_by_index(response.compatibleLenses, target_indexes)
    print(f"Index {target_indexes} 的镜片数量: {len(filtered_lenses)}")
    
    # 5. 获取推荐的镜片
    print("\n=== 5. 获取推荐的镜片 ===")
    recommended = get_recommended_lenses(response.compatibleLenses)
    print(f"推荐的镜片数量: {len(recommended)}")
    for lens in recommended:
        print(f"  - {lens.displayName} (SKU: {lens.sku})")
    
    # 6. 按价格范围过滤
    print("\n=== 6. 按价格范围过滤 ===")
    affordable_lenses = [lens for lens in response.compatibleLenses if 0 <= lens.price <= 120]
    print(f"价格在 $0-$120 的镜片数量: {len(affordable_lenses)}")
    
    # 7. 根据SKU查找镜片
    print("\n=== 7. 根据SKU查找镜片 ===")
    target_sku = "61199"
    found_lens = get_lens_by_sku(response.compatibleLenses, target_sku)
    if found_lens:
        print(f"找到SKU {target_sku}: {found_lens.displayName}")
    else:
        print(f"未找到SKU {target_sku}")
    
    # 8. 按分类过滤
    print("\n=== 8. 按分类过滤 ===")
    premium_lenses = [lens for lens in response.compatibleLenses if lens.classification == "premium"]
    print(f"Premium分类的镜片数量: {len(premium_lenses)}")
    
    # 9. 直接访问data class属性
    print("\n=== 9. 直接访问data class属性 ===")
    first_lens = response.compatibleLenses[0]
    print(f"第一个镜片信息:")
    print(f"  - 名称: {first_lens.displayName}")
    print(f"  - SKU: {first_lens.sku}")
    print(f"  - 价格: ${first_lens.price}")
    print(f"  - Index: {first_lens.lensIndex}")
    print(f"  - Tint: {first_lens.tintBase}")
    print(f"  - 是否推荐: {first_lens.isRecommended}")
    print(f"  - 分类: {first_lens.classification}")


def advanced_usage_example():
    """高级用法示例"""
    print("\n" + "="*50)
    print("高级用法示例")
    print("="*50)
    
    # 模拟更复杂的数据处理场景
    sample_data = {
        "compatibleLenses": [
            {
                "tintBase": "Gray",
                "brandName": "",
                "productId": "prodLensEyeQPlus",
                "salePrice": 0,
                "ignoreIncludedTints": False,
                "isStandardDelivery": True,
                "displayName": "1.50 EyeQLenz with Zenni ID Guard Digital Free Form Progressive",
                "cssValue": "eyeqpluswithzenniidguard-sunglass-solid-gray",
                "groupBy": "1.5_EyeQPlusWithZenniIdGuard",
                "classification": "premium",
                "isRushDelivery": False,
                "lensIndex": 1.5,
                "isPriority": False,
                "recommendedIndex": 1.5,
                "tintClassification": "Classic",
                "price": 109.95,
                "isRecommended": True,
                "skuDisplayName": "1.50 EyeQLenz with Zenni ID Guard Digital Free Form Progressive - Gray",
                "sku": "61199",
                "inlineStyle": " background: #726D6Eff;"
            }
        ]
    }
    
    response = create_compatible_lenses_response_from_dict(sample_data)
    
    # 复杂查询：找到价格最低的推荐镜片
    recommended_lenses = get_recommended_lenses(response.compatibleLenses)
    if recommended_lenses:
        cheapest_recommended = min(recommended_lenses, key=lambda x: x.price)
        print(f"最便宜的推荐镜片: {cheapest_recommended.displayName} (${cheapest_recommended.price})")
    
    # 按多个条件过滤
    def filter_by_multiple_criteria(lenses, min_price=0, max_price=float('inf'), 
                                  target_indexes=None, is_recommended=None):
        """多条件过滤"""
        filtered = lenses
        
        # 价格过滤
        filtered = get_lenses_by_price_range(filtered, min_price, max_price)
        
        # Index过滤
        if target_indexes:
            filtered = filter_lenses_by_index(filtered, target_indexes)
        
        # 推荐状态过滤
        if is_recommended is not None:
            filtered = [lens for lens in filtered if lens.isRecommended == is_recommended]
        
        return filtered
    
    # 使用多条件过滤
    custom_filtered = filter_by_multiple_criteria(
        response.compatibleLenses,
        min_price=100,
        max_price=200,
        target_indexes=[1.5, 1.61],
        is_recommended=True
    )
    
    print(f"多条件过滤结果: {len(custom_filtered)} 个镜片")


if __name__ == "__main__":
    example_usage()
    advanced_usage_example() 