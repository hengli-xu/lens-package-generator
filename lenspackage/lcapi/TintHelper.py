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
