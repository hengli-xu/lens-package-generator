from lenspackage.LensPackageConstant import US_REGION
from lenspackage.datamodels.data_models import CompatibleTintsType, TintItem, CompatibleTintsConfigurationResponse

lc_tints_config = {
    "tints": [
        {
            "name": "Classic",
            "type": "Solid",
            "label": "Classic Tints",
            "order": 1
        },
        {
            "name": "Gradient",
            "type": "Gradient",
            "label": "Gradient Tints",
            "order": 2
        },
        {
            "name": "Fashion",
            "type": "Solid",
            "label": "Fashion Tints",
            "order": 3
        },
        {
            "name": "ClassicMirror",
            "type": "Solid",
            "label": "Classic Mirror Tints",
            "order": 4
        },
        {
            "name": "GradientMirror",
            "type": "Gradient",
            "label": "Gradient Mirror Tints",
            "order": 5
        },
        {
            "name": "Migraine",
            "type": "Migraine",
            "label": "FL-41 Lens Tints",
            "order": 6
        },
        {
            "name": "BlokzGaming",
            "type": "",
            "label": "Blokz Plus Tints",
            "order": 7
        }
    ]
}


def create_compatible_tints_configuration_response_from_dict(data: dict):
    """从字典创建CompatibleTintsConfigurationResponse实例"""
    from lenspackage.datamodels.data_models import TintTypeItem, CompatibleTintsConfigurationResponse
    
    tints = [TintTypeItem(**tint) for tint in data.get('tints', [])]
    # 按照order字段排序
    tints.sort(key=lambda x: x.order)
    return CompatibleTintsConfigurationResponse(tints=tints)


def create_compatible_tints_configuration_response_from_lc_config():
    """从lc_tints_config创建CompatibleTintsConfigurationResponse实例"""
    return create_compatible_tints_configuration_response_from_dict(lc_tints_config)


def group_tints_by_classification(unique_tints, lc_tints_config):
    """
    将unique_tints按照classification与lc_tints_config中的name进行分类聚合
    
    Args:
        unique_tints: TintItem列表
        lc_tints_config: lc_tints_config配置
        
    Returns:
        CompatibleTintsDto: 分类聚合后的数据
    """
    from lenspackage.datamodels.data_models import CompatibleTintsType
    
    # 创建分类映射
    type_groups = {}
    
    # 初始化所有配置的类型
    for i, config_item in enumerate(lc_tints_config.tints):
        type_groups[config_item.name] = CompatibleTintsType(
            label=config_item.label,
            price=0.0,  # 初始价格为0
            index=i,
            isOpen=True,
            isItemSelect=False
        )
    
    # 将tint项目分类
    for tint_item in unique_tints:
        if tint_item.classification in type_groups:
            type_group = type_groups[tint_item.classification]
            type_group.compatibleTintItemDtoList.append(tint_item)
            # 更新价格（取最高价格）
            if tint_item.price > type_group.price:
                type_group.price = tint_item.price
    
    # 过滤掉没有tint项目的类型，并按order排序
    filtered_type_list = []
    for config_item in lc_tints_config.tints:
        if config_item.name in type_groups and len(type_groups[config_item.name].compatibleTintItemDtoList) > 0:
            filtered_type_list.append(type_groups[config_item.name])

    return filtered_type_list


def validateTintConsistency(lens_tints_map):
    """
    校验lens_tints_map中不同key对应的List[TintItem]是否满足一致性条件
    
    Args:
        lens_tints_map: 包含每个lensIndex对应tint列表的字典
        
    Returns:
        bool: 校验是否通过
    """
    if not lens_tints_map:
        print("    ⚠ No lens tints map to validate")
        return True
    
    if len(lens_tints_map) == 1:
        print("    ✓ Tint validation SKIPPED: Only one lensIndex, no consistency check needed")
        return True
    
    # 获取第一个key作为参考
    first_key = list(lens_tints_map.keys())[0]
    first_tints = lens_tints_map[first_key]
    
    print(f"    Using lensIndex {first_key} as reference with {len(first_tints)} tints")
    
    # 条件1: 检查所有List[TintItem]的数量是否相同
    all_same_count = True
    for lens_index, tints in lens_tints_map.items():
        if len(tints) != len(first_tints):
            all_same_count = False
            print(f"    ✗ Tint count mismatch: {lens_index} has {len(tints)} tints, {first_key} has {len(first_tints)} tints")
            break
    
    if not all_same_count:
        print("    ✗ Tint validation FAILED: Different tint counts across lensIndexes")
        return False
    
    print(f"    ✓ Tint count validation PASSED: All lensIndexes have {len(first_tints)} tints")
    
    # 条件2: 检查tint一致性
    validation_passed = True
    
    for i, reference_tint in enumerate(first_tints):
        print(f"    Checking tint {i+1}: {reference_tint.tintBase} (sku: {reference_tint.sku or 'empty'})")
        
        # 检查其他所有lensIndex中是否存在匹配的tint
        for lens_index, tints in lens_tints_map.items():
            if lens_index == first_key:
                continue
            
            found_match = False
            
            if reference_tint.sku:  # sku不为空，按sku匹配
                for tint in tints:
                    if tint.sku == reference_tint.sku:
                        found_match = True
                        print(f"      ✓ Found matching SKU in {lens_index}: {tint.sku}")
                        break
            else:  # sku为空，按tintBase匹配
                for tint in tints:
                    if tint.tintBase == reference_tint.tintBase:
                        found_match = True
                        print(f"      ✓ Found matching tintBase in {lens_index}: {tint.tintBase}")
                        break
            
            if not found_match:
                validation_passed = False
                if reference_tint.sku:
                    print(f"      ✗ No matching SKU '{reference_tint.sku}' found in {lens_index}")
                else:
                    print(f"      ✗ No matching tintBase '{reference_tint.tintBase}' found in {lens_index}")
    
    if validation_passed:
        print("    ✓ Tint consistency validation PASSED: All tints are consistent across lensIndexes")
    else:
        print("    ✗ Tint consistency validation FAILED: Inconsistent tints found across lensIndexes")
    
    return validation_passed


def populateLensPackageIndexTintList(lens_tints_map, region=US_REGION):
    """
    为lens_tints_map中第一个基准的TintItem填充lensPackageIndexTintList字段
    
    Args:
        lens_tints_map: 包含每个lensIndex对应tint列表的字典
        region: 区域参数，默认为US_REGION
        
    Returns:
        list: 包含填充了lensPackageIndexTintList的第一个基准TintItem列表
    """
    from lenspackage.datamodels.data_models import IndexSkuTintSku, CostType, TintItem

    if not lens_tints_map or len(lens_tints_map) <= 1:
        print("    ⚠ No need to populate lensPackageIndexTintList: lens_tints_map size <= 1")
        return list(lens_tints_map.values())[0] if lens_tints_map else []
    
    # 获取第一个key作为基准
    first_key = list(lens_tints_map.keys())[0]
    first_tints = lens_tints_map[first_key]
    
    # 创建第一个基准tint列表的深拷贝，避免修改原始数据
    processed_first_tints = []
    for tint in first_tints:
        # 创建TintItem的深拷贝
        new_tint = TintItem(
            tintBase=tint.tintBase,
            displayName=tint.displayName,
            cssValue=tint.cssValue,
            classification=tint.classification,
            subType=tint.subType,
            sku=tint.sku,
            price=tint.price,
            productId=tint.productId,
            isStandardDelivery=tint.isStandardDelivery,
            isRushDelivery=tint.isRushDelivery,
            salePrice=tint.salePrice,
            inlineStyle=tint.inlineStyle,
            additionalChargeInfo=tint.additionalChargeInfo,
            isSelect=tint.isSelect,
            lensSku=tint.lensSku,
            lensPackageIndexTintList=[]  # 初始化为空列表
        )
        processed_first_tints.append(new_tint)
    
    print(f"    Populating lensPackageIndexTintList using {first_key} as reference")
    
    # 遍历基准tint列表中的每个TintItem
    for i, reference_tint in enumerate(processed_first_tints):
        print(f"    Processing tint {i+1}: {reference_tint.tintBase} (sku: {reference_tint.sku or 'empty'})")
        
        if reference_tint.sku:  # sku不为空，直接填充当前tint的信息
            # 创建CostType
            cost_type = CostType(
                region=region,  # 使用传入的区域参数
                price=reference_tint.price
            )
            
            # 创建IndexSkuTintSku
            index_sku_tint_sku = IndexSkuTintSku(
                indexSku=reference_tint.lensSku,
                tintSku=reference_tint.sku,
                price=[cost_type]
            )
            
            reference_tint.lensPackageIndexTintList.append(index_sku_tint_sku)
            print(f"      ✓ Added direct tint info: indexSku={reference_tint.lensSku}, tintSku={reference_tint.sku}")
            
        else:  # sku为空，需要在所有lensIndex中查找相同tintBase的tint
            for lens_index, tints in lens_tints_map.items():
                # 在当前lensIndex的tint列表中查找相同tintBase的tint
                for tint in tints:
                    if tint.tintBase == reference_tint.tintBase:
                        # 创建CostType
                        cost_type = CostType(
                            region=region,  # 使用传入的区域参数
                            price=tint.price
                        )
                        
                        # 创建IndexSkuTintSku
                        index_sku_tint_sku = IndexSkuTintSku(
                            indexSku=tint.lensSku,
                            tintSku=tint.sku,
                            price=[cost_type]
                        )
                        
                        reference_tint.lensPackageIndexTintList.append(index_sku_tint_sku)
                        print(f"      ✓ Added matching tintBase info from {lens_index}: indexSku={tint.lensSku}, tintSku={tint.sku}")
                        break  # 找到匹配项后跳出内层循环
        
        print(f"      Total items in lensPackageIndexTintList: {len(reference_tint.lensPackageIndexTintList)}")
    
    print("    ✓ Finished populating lensPackageIndexTintList for all reference tints")
    return processed_first_tints
