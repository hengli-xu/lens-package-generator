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


 