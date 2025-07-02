"""
Package数据模型定义
"""

from dataclasses import dataclass
from typing import List, Optional

# 从data_models.py导入基础数据类
from lenspackage.datamodels.data_models import CostType, IndexSkuTintSku


@dataclass
class CoatingType:
    """涂层类型数据类"""
    cost: List[CostType]
    displayName: str
    sku: str


@dataclass
class Index:
    """镜片索引数据类"""
    cost: List[CostType]
    lensIndex: float
    sku: str


@dataclass
class LensType:
    """镜片类型数据类"""
    displayName: str
    subType: str
    type: str


@dataclass
class RxType:
    """处方类型数据类"""
    prescriptionType: str
    progressiveUsage: Optional[str] = None


@dataclass
class TintItem:
    """Tint项目数据类"""
    additionalChargeInfo: dict
    classification: str
    cssValue: str
    displayName: str
    isRushDelivery: bool
    isSelect: bool
    isStandardDelivery: bool
    lensPackageIndexTintList: List[IndexSkuTintSku]
    lensSku: str
    price: float
    productId: str
    sku: str
    subType: str
    tintBase: str


@dataclass
class CompatibleTintsType:
    """Tint类型数据类"""
    compatibleTintItemDtoList: List[TintItem]
    index: int
    isItemSelect: bool
    isOpen: bool
    label: str
    price: float


@dataclass
class LensPackage:
    """镜片包数据类"""
    backgroundUrl: str
    coatingType: CoatingType
    description: str
    id: str
    indexes: List[Index]
    lensType: LensType
    rxType: RxType
    shortDescription: str
    tintType: List[CompatibleTintsType]
    title: str
    platform: Optional[str] = None


@dataclass
class ProductPackage:
    """产品包数据类"""
    lensPackages: List[LensPackage]
    objectID: str
    productId: str 