"""
数据模型定义
"""

from dataclasses import dataclass
from typing import List, Optional


# ==================== IndexService API 数据类 ====================

@dataclass
class CompatibleLens:
    """兼容镜片数据类"""
    tintBase: str
    brandName: str
    productId: str
    salePrice: float
    ignoreIncludedTints: bool
    isStandardDelivery: bool
    displayName: str
    cssValue: str
    groupBy: str
    classification: str
    isRushDelivery: bool
    lensIndex: float
    isPriority: bool
    recommendedIndex: float
    tintClassification: str
    price: float
    isRecommended: bool
    skuDisplayName: str
    sku: str
    inlineStyle: str


@dataclass
class CompatibleLensesResponse:
    """兼容镜片响应数据类"""
    compatibleLenses: List[CompatibleLens]


def create_compatible_lenses_response_from_dict(data: dict) -> CompatibleLensesResponse:
    """从字典创建CompatibleLensesResponse实例"""
    lenses = [CompatibleLens(**lens) for lens in data.get('compatibleLenses', [])]
    return CompatibleLensesResponse(compatibleLenses=lenses)


# ==================== TintService API 数据类 ====================

@dataclass
class TintItem:
    """Tint项目数据类 - 合并了CompatibleTint和TintItem"""
    # 基础字段
    tintBase: str
    displayName: str
    cssValue: str
    classification: str
    subType: str
    sku: str
    price: float
    productId: str
    isStandardDelivery: bool
    isRushDelivery: bool
    
    # 可选字段 - 来自CompatibleTint
    salePrice: Optional[float] = None
    inlineStyle: Optional[str] = None
    
    # 可选字段 - 来自TintItem
    additionalChargeInfo: Optional[dict] = None
    isSelect: Optional[bool] = None
    lensSku: Optional[str] = None


@dataclass
class CompatibleTintsResponse:
    """兼容Tint响应数据类"""
    compatibleTints: List[TintItem]
    additionalChargeInfo: dict


def create_compatible_tints_response_from_dict(data: dict) -> CompatibleTintsResponse:
    """从字典创建CompatibleTintsResponse实例"""
    tints = [TintItem(**tint) for tint in data.get('compatibleTints', [])]
    return CompatibleTintsResponse(
        compatibleTints=tints,
        additionalChargeInfo=data.get('additionalChargeInfo', {})
    )


# ==================== CoatingService API 数据类 ====================

@dataclass
class CoatingItem:
    """涂层项目数据类"""
    imageName: str
    productId: str
    salePrice: float
    isStandardDelivery: bool
    displayName: str
    isRushDelivery: bool
    coatingResistantType: str
    coatingTileDescription: str
    price: float
    isRecommended: bool
    coatingDescription: str
    sku: str


@dataclass
class CoatingType:
    """涂层类型数据类"""
    type: str
    items: List[CoatingItem]


@dataclass
class CompatibleCoatingsResponse:
    """兼容涂层响应数据类"""
    compatibleCoatings: List[CoatingType]


def create_coating_response_from_dict(data: dict) -> CompatibleCoatingsResponse:
    """从字典创建CompatibleCoatingsResponse实例"""
    processed_coatings = []
    for coating_dict in data.get('compatibleCoatings', []):
        items = [CoatingItem(**item) for item in coating_dict.get('items', [])]
        coating_type = CoatingType(type=coating_dict['type'], items=items)
        processed_coatings.append(coating_type)
    
    return CompatibleCoatingsResponse(compatibleCoatings=processed_coatings)


# ==================== 整合数据类 ====================

@dataclass
class CostInfo:
    """价格信息数据类"""
    price: float
    region: str


@dataclass
class CompressedLensIndex:
    """压缩后的镜片索引数据类"""
    cost: List[CostInfo]
    lensIndex: float
    sku: str


# ==================== Tint Configuration 数据类 ====================

@dataclass
class TintTypeItem:
    """Tint类型项目数据类 - 对应Kotlin的TintTypeItem"""
    name: str
    type: str
    label: str
    order: float


@dataclass
class CompatibleTintsConfigurationResponse:
    """兼容Tint配置响应数据类 - 对应Kotlin的CompatibleTintsConfigurationResponse"""
    tints: List[TintTypeItem]


def create_compatible_tints_configuration_response_from_dict(data: dict) -> CompatibleTintsConfigurationResponse:
    """从字典创建CompatibleTintsConfigurationResponse实例"""
    tints = [TintTypeItem(**tint) for tint in data.get('tints', [])]
    # 按照order字段排序
    tints.sort(key=lambda x: x.order)
    return CompatibleTintsConfigurationResponse(tints=tints)


def create_compatible_tints_configuration_response_from_lc_config() -> CompatibleTintsConfigurationResponse:
    """从lc_tints_config创建CompatibleTintsConfigurationResponse实例"""
    from lenspackage.lcapi.tints_config import lc_tints_config
    return create_compatible_tints_configuration_response_from_dict(lc_tints_config)


# ==================== 工具函数 ====================

def group_lenses_by_index(lenses: List[CompatibleLens]) -> dict:
    """按lensIndex对镜片进行分组"""
    groups = {}
    for lens in lenses:
        lens_index = lens.lensIndex
        if lens_index not in groups:
            groups[lens_index] = []
        groups[lens_index].append(lens)
    return groups


def filter_lenses_by_index(lenses: List[CompatibleLens], target_indexes: List[float]) -> List[CompatibleLens]:
    """根据目标index列表过滤镜片"""
    return [lens for lens in lenses if lens.lensIndex in target_indexes]


def get_recommended_lenses(lenses: List[CompatibleLens]) -> List[CompatibleLens]:
    """获取推荐的镜片"""
    return [lens for lens in lenses if lens.isRecommended]


def get_lens_by_sku(lenses: List[CompatibleLens], sku: str) -> Optional[CompatibleLens]:
    """根据SKU获取镜片"""
    for lens in lenses:
        if lens.sku == sku:
            return lens
    return None


def create_compressed_lens_indexes(lenses: List[CompatibleLens], region: str) -> List[CompressedLensIndex]:
    """将镜片列表转换为压缩格式"""
    compressed_indexes = []
    for lens in lenses:
        cost_info = CostInfo(price=lens.price, region=region)
        compressed_index = CompressedLensIndex(
            cost=[cost_info],
            lensIndex=lens.lensIndex,
            sku=lens.sku
        )
        compressed_indexes.append(compressed_index)
    return compressed_indexes


# ==================== Compatible Tints DTO 数据类 ====================

@dataclass
class CompatibleTintsType:
    """兼容Tint类型数据类 - 对应Kotlin的CompatibleTintsType"""
    label: str
    price: float
    compatibleTintItemDtoList: Optional[List[TintItem]] = None
    index: int = 0
    isOpen: bool = True
    isItemSelect: bool = False
    selectedTintBall: Optional[TintItem] = None
    
    def __post_init__(self):
        if self.compatibleTintItemDtoList is None:
            self.compatibleTintItemDtoList = []


@dataclass
class CompatibleTintsDto:
    """兼容Tint DTO数据类 - 对应Kotlin的CompatibleTintsDto"""
    typeList: List[CompatibleTintsType]
    additionalChargeInfo: Optional[dict] = None
    indexTintsRequest: bool = False


def group_tints_by_classification(unique_tints: List[TintItem], lc_tints_config: CompatibleTintsConfigurationResponse) -> CompatibleTintsDto:
    """
    将unique_tints按照classification与lc_tints_config中的name进行分类聚合
    
    Args:
        unique_tints: TintItem列表
        lc_tints_config: lc_tints_config配置
        
    Returns:
        CompatibleTintsDto: 分类聚合后的数据
    """
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