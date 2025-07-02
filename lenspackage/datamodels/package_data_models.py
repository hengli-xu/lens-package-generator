"""
Package数据模型定义
"""

from dataclasses import dataclass
from typing import List, Optional

# 从data_models.py导入重复的数据类
from lenspackage.datamodels.data_models import CostType


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
class LensPackage:
    """镜片包数据类"""
    backgroundUrl: str
    coatingType: CoatingType
    description: str
    id: str
    indexes: List[Index]
    lensType: LensType
    minPackageCost: List[CostType]
    rxType: RxType
    shortDescription: str
    tintType: List[TintType]
    title: str
    platform: Optional[str] = None


@dataclass
class ProductPackage:
    """产品包数据类"""
    lensPackages: List[LensPackage]
    objectID: str
    productId: str 