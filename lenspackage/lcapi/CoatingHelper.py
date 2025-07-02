def validateCoatingSkus(lens_coating_map):
    """
    校验lens_coating_map中每个CoatingItem的sku是否都相同
    
    Args:
        lens_coating_map: 包含每个lensIndex对应coating的字典
        
    Returns:
        bool: 校验是否通过
    """
    if not lens_coating_map:
        print("    ⚠ No lens coating map to validate")
        return True
    
    # 收集所有coating的sku
    all_skus = []
    for lens_index, coating in lens_coating_map.items():
        if coating and hasattr(coating, 'sku'):
            all_skus.append((lens_index, coating.sku))
    
    if not all_skus:
        print("    ⚠ No coatings with SKU found in lens coating map")
        return True
    
    # 检查所有sku是否相同
    first_sku = all_skus[0][1]
    all_same_sku = all(sku == first_sku for _, sku in all_skus)
    
    if all_same_sku:
        print(f"    ✓ Coating SKU validation PASSED: All coatings have same SKU: {first_sku}")
        return True
    else:
        print(f"    ✗ Coating SKU validation FAILED: Different coating SKUs found:")
        for lens_index, sku in all_skus:
            print(f"      Lens {lens_index}: {sku}")
        return False 