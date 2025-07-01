"""
LC API 数据模型定义
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