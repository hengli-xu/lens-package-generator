#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simplified Lens Package Constants
Closer to original Kotlin structure
"""

from dataclasses import dataclass
from typing import Optional

# ==================== Constants ====================

US_REGION = "US"
CA_REGION = "CA"

def decideRegion():
    return CA_REGION

# CSV lens type constants
CSV_LENS_TYPE_BLOKZ_PHOTOCHROMIC = "Blokz Photochromic"
CSV_LENS_TYPE_EYE_Q_LENZ_PLUS = "EyeQLenz+"
CSV_LENS_TYPE_PREMIUM_PROGRESSIVE_PLUS_BLOKZ = "Premium Progressive+Blokz"
CSV_LENS_TYPE_BLOKZ = "Blokz"
CSV_LENS_TYPE_PHOTOCHROMIC_TRANSITIONS_XTRACTIVE_NEW_GEN = "Photochromic (Transitions® XTRActive® New Gen)"
CSV_LENS_TYPE_POLARIZED_SUNGLASSES = "Polarized Sunglasses"
CSV_LENS_TYPE_PREMIUM_PROGRESSIVE_PLUS_PHOTOCHROMIC_POLARIZED = "Premium Progressive+Photochromic Polarized (Transitions® XTP)"
CSV_LENS_TYPE_IMPACT_RESISTANT_PHOTOCHROMIC_TRANSITIONS_GEN_S = "Impact-resistant Photochromic (Transitions® Gen S )"
CSV_LENS_TYPE_HIGH_POWER_BLOKZ = "High-power Blokz"
CSV_LENS_TYPE_153_BLOKZ = "1.53 blokz"
CSV_LENS_TYPE_TRANSITIONS_DRIVEWEAR = "Transitions Drivewear"
CSV_LENS_TYPE_GENERAL_USE_CLEAR_LENS = "General use clear lens"

RX_TYPE_SINGLE_VISION = "SingleVision"

# Platform constants
PLATFORM_IOS = "iOS"
PLATFORM_ANDROID = "Android"

# CSV index constants
CSV_PACKAGE_ID_INDEX = 0
CSV_PACKAGE_TITLE_INDEX = 1
CSV_PACKAGE_DESC_INDEX = 2
CSV_PACKAGE_SHORT_DESC_INDEX = 3
CSV_PACKAGE_BG_URL_INDEX = 4
CSV_PACKAGE_LENS_TYPE_INDEX = 5
CSV_PACKAGE_INDEX_INDEX = 6
CSV_PACKAGE_TINT_INDEX = 7
CSV_PACKAGE_COATING_INDEX = 8
CSV_PACKAGE_PLATFORM_INDEX = 9

CSV_PRODUCT_PACKAGE_PRODUCT_ID_INDEX = 0
CSV_PRODUCT_PACKAGE_PACKAGE_LIST_INDEX = 1

# ==================== Data Classes ====================

@dataclass
class LensType:
    """Lens type data class"""
    type: str
    sub_type: str

@dataclass
class RxType:
    """Rx type data class"""
    prescription_type: str
    progressive_usage: Optional[str] = None

# ==================== Lazy Objects (using functions) ====================


"""Lens type for Blokz"""
lens_type_blokz = LensType(
    type="Clear",
    sub_type="BlokzGeneralUse"
)
    
"""Lens type for polarized sunglasses"""
lens_type_polarized_sunglass = LensType(
        type="Sunglasses",
        sub_type="Polarized"
    )

"""Lens type for EyeQLenz+"""
lens_type_eye_q_lenz_plus = LensType(
        type="ZenniIdGuard",
        sub_type="EyeQPlusWithZenniIdGuard"
    )

csv_lens_type_map = {
        CSV_LENS_TYPE_BLOKZ_PHOTOCHROMIC: LensType(
            type="Blokz",
            sub_type="Photochromic"
        ),
        CSV_LENS_TYPE_EYE_Q_LENZ_PLUS: lens_type_eye_q_lenz_plus,
        CSV_LENS_TYPE_BLOKZ: lens_type_blokz,
        CSV_LENS_TYPE_PREMIUM_PROGRESSIVE_PLUS_BLOKZ: lens_type_blokz,
        CSV_LENS_TYPE_POLARIZED_SUNGLASSES: lens_type_polarized_sunglass
    }

rx_type_single_vision = RxType(
        prescription_type=RX_TYPE_SINGLE_VISION
    )

rx_type_progressive_premium = RxType(
        prescription_type="Progressive",
        progressive_usage="Premium"
    )

csv_rx_type_map = {
        CSV_LENS_TYPE_BLOKZ_PHOTOCHROMIC: rx_type_single_vision,
        CSV_LENS_TYPE_BLOKZ: rx_type_single_vision,
        CSV_LENS_TYPE_PREMIUM_PROGRESSIVE_PLUS_BLOKZ: rx_type_progressive_premium,
        f"{CSV_LENS_TYPE_EYE_Q_LENZ_PLUS}_{PLATFORM_ANDROID}": rx_type_progressive_premium,
        f"{CSV_LENS_TYPE_EYE_Q_LENZ_PLUS}_{PLATFORM_IOS}": rx_type_single_vision,
        CSV_LENS_TYPE_POLARIZED_SUNGLASSES: rx_type_single_vision
    }

# default rx
def getDefaultRx():
    return {
        "birthYear": 1993,
        "pdType": "Single",
        "pdSingle": 64.0,
        "od": {
            "axis": 0.0,
            "cyl": 0.0,
            "sph": -2.0
        },
        "os": {
            "axis": 0.0,
            "cyl": 0.0,
            "sph": -2.0
        },
        "prismEnabled": False
    }

# ==================== Main Function ====================

def gen_rx_type(platform: Optional[str], lens_type: str) -> Optional[RxType]:
    """
    Generate Rx type based on platform and lens type
    This is the Python equivalent of the Kotlin genRxType function

    Args:
        platform: Platform string (iOS/Android) or None
        lens_type: Lens type string

    Returns:
        RxType or None
    """
    if platform and platform.lower() == PLATFORM_IOS.lower():
        return csv_rx_type_map.get(f"{lens_type}_{PLATFORM_IOS}")

    if platform and platform.lower() == PLATFORM_ANDROID.lower():
        return csv_rx_type_map.get(f"{lens_type}_{PLATFORM_ANDROID}")

    return csv_rx_type_map.get(lens_type)
