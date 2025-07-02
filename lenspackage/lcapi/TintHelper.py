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
    from lenspackage.lcapi.data_models import TintTypeItem, CompatibleTintsConfigurationResponse
    
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
    from lenspackage.lcapi.data_models import CompatibleTintsType, CompatibleTintsDto
    
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
    
    return CompatibleTintsDto(
        typeList=filtered_type_list,
        additionalChargeInfo={},
        indexTintsRequest=False
    )


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
