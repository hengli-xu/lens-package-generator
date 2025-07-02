from typing import List

from lenspackage.CsvPackage import CsvProductPackageList, CsvPackage
from lenspackage.LensPackageConstant import csv_lens_type_map
from lenspackage.datamodels.package_data_models import ProductPackage
from lenspackage.lcapi.IndexService import IndexService
from lenspackage.lcapi.LensTypeService import LensTypeService
from lenspackage.lcapi.PdpService import PdpService
from lenspackage.lcapi.RxTypeService import RxTypeService
from lenspackage.lcapi.TintHelper import create_compatible_tints_configuration_response_from_lc_config, \
    group_tints_by_classification, validateTintConsistency, populateLensPackageIndexTintList
from lenspackage.lcapi.CoatingHelper import validateCoatingSkus
from lenspackage.datamodels.data_models import CoatingItem

from lenspackage.parsecsv.CsvParser import parseCsvAndGenProductPackagesList, parseCsvAndGenPackageDetails


class LensPackageGeneratorService:
    package_detail_csv_file = "./csv/PackagesDetail.csv"
    product_packages_csv_file = "./csv/Product-Packages.csv"

    def __init__(self, session=None, token_value=None):
        self.session = session
        self.tokenValue = token_value

    # 核心方法，检查atg数据是否符合要求
    def checkAtgData(self, productId, frameSku, csvPackage):
        print(f"------> lens package: productId {productId} frameSku {frameSku} packageId : {csvPackage.id} start")

        # 1. 获取RxType(e.g. Single Vision)的详情
        self.checkRxTypeWithAtg(csvPackage, frameSku, productId)
        # 2. 获取lensType的详情
        lens_type_service = LensTypeService(session=self.session, token_value=self.tokenValue)
        compatible_lens_types = lens_type_service.getUsageTypes(productId, frameSku, csvPackage)
        # 3. 获取index的详情
        # indexes是用作lens package需要的字段
        # compatible_lenses是从atg取得的所有index的详细信息
        atg_compatible_lenses, indexes = self.checkIndexWithAtg(csvPackage, frameSku, productId)

        # 4. 按lensIndex分组处理tint
        lens_package = self.processTintsAndCoatingByLensIndex(productId, frameSku, csvPackage, atg_compatible_lenses,indexes)

        print(f"<------ lens package: productId {productId} frameSku {frameSku} packageId : {csvPackage.id} end")
        
        return lens_package

    def checkRxTypeWithAtg(self, csvPackage, frameSku, productId):
        rx_type_service = RxTypeService(session=self.session, token_value=self.tokenValue)
        compatible_lens_types = rx_type_service.getCompatibleLensTypes(productId, frameSku, csvPackage)
        passCheck = rx_type_service.checkRxTypeCompatibility(csvPackage, compatible_lens_types)
        if passCheck:
            print(f"------> RxType check : productId {productId} frameSku {frameSku} packageId : {csvPackage.id} pass")
        else:
            print(f"------> RxType check : productId {productId} frameSku {frameSku} packageId : {csvPackage.id} fail")

    def checkIndexWithAtg(self, csvPackage, frameSku, productId):
        index_service = IndexService(session=self.session, token_value=self.tokenValue)
        compatible_lenses_response = index_service.getCompatibleLenses(productId, frameSku, csvPackage)
        compatible_lenses, compressed_indexes = index_service.checkIndexCompatibility(csvPackage, compatible_lenses_response)
        
        if compressed_indexes:
            print(f"------> Index check : productId {productId} frameSku {frameSku} packageId : {csvPackage.id} pass compatible_lenses size {len(compatible_lenses)} compressed_indexes size {len(compressed_indexes)}")
        else:
            print(f"------> Index check : productId {productId} frameSku {frameSku} packageId : {csvPackage.id} fail")
        
        return compatible_lenses, compressed_indexes

    def processTintsAndCoatingByLensIndex(self, productId, frameSku, csvPackage, atg_compatible_lenses, packageIndexes):
        """
        按lensIndex分组处理tint
        """
        from lenspackage.lcapi.TintService import TintService
        from lenspackage.datamodels.data_models import TintItem
        
        # 按lensIndex分组
        index_service = IndexService(session=self.session, token_value=self.tokenValue)
        index_groups = index_service.groupIndexesByLensIndex(atg_compatible_lenses)
        
        tint_service = TintService(session=self.session, token_value=self.tokenValue)
        # 比如1.5对应的所有tint，1.61对应的所有tint的map
        lens_tints_map: dict[str, List[TintItem]] = {}
        # 比如1.5对应的所有coating，1.61对应的所有coating的map
        lens_coating_map: dict[str, CoatingItem] = {}
        for lens_index, lens_items in index_groups.items():
            print(f"------> Processing tints for lensIndex: {lens_index}")

            lens_tints = []
            for lens_item in lens_items:
                if lens_item.tintClassification:
                    tint_item = TintItem(
                        tintBase=lens_item.tintBase,
                        displayName=lens_item.displayName,
                        cssValue=lens_item.cssValue,
                        classification=lens_item.tintClassification,
                        subType="Solid",  # solid是固定值
                        sku="",
                        price=0,  # 价格为0，因为这不是真正的tint
                        productId="",
                        isStandardDelivery=lens_item.isStandardDelivery,
                        isRushDelivery=lens_item.isRushDelivery,
                        # 可选字段
                        additionalChargeInfo={},
                        isSelect=False,
                        lensSku=lens_item.sku
                    )
                    lens_tints.append(tint_item)
                    print(
                        f"  Generated tint for SKU {lens_item.sku}: {tint_item.tintBase} ({tint_item.classification}) lens_tints size :{len(lens_tints)}")
                # 不管tintClassification是否为空，都要调用TintService
                tint_result = tint_service.getCompatibleTints(productId, frameSku, csvPackage, lens_item.sku)
                if tint_result:
                    # 将API返回的tints添加到列表中
                    api_tints = tint_result.compatibleTints
                    lens_tints.extend(api_tints)
                    print(f"  Called TintService for SKU {lens_item.sku}, got {len(api_tints)} tints")
                else:
                    print(f"  No tint result for SKU {lens_item.sku}")

            lc_tints_config = create_compatible_tints_configuration_response_from_lc_config()
            result = group_tints_by_classification(lens_tints, lc_tints_config)

            print(f"  group_tints_by_classification typeList size:  {len(result)}")
            lens_tints_map[lens_index] = lens_tints
            # 对每个lens_item调用CoatingService并校验coating
            from lenspackage.lcapi.CoatingService import CoatingService
            coating_service = CoatingService(session=self.session, token_value=self.tokenValue)

            # 存储每个lens_item的最高价格coating
            max_price_coatings = {}

            for lens_item in lens_items:
                coating_result = coating_service.getCompatibleCoatings(productId, frameSku, csvPackage, lens_item.sku)
                if coating_result:
                    print(f"    Got coatings for lensSku {lens_item.sku} coating size: {len(coating_result.compatibleCoatings)}")

                    # 找出价格最高的coatingItem
                    max_price_coating = None
                    max_price = -1

                    for coating_type in coating_result.compatibleCoatings:
                        for coating_item in coating_type.items:
                            if coating_item.price > max_price:
                                max_price = coating_item.price
                                max_price_coating = coating_item

                    if max_price_coating:
                        max_price_coatings[lens_item.sku] = max_price_coating
                        print(f"      Max price coating for {lens_item.sku}: {max_price_coating.sku} (${max_price_coating.price})")
                else:
                    print(f"    No coatings for lensSku {lens_item.sku}")

            # 选择最高价格的coating作为该lensIndex的代表coating
            if max_price_coatings:
                # 从所有最高价格coating中选择一个作为代表
                representative_coating = list(max_price_coatings.values())[0]
                lens_coating_map[lens_index] = representative_coating
                print(f"    Selected representative coating for lensIndex {lens_index}: {representative_coating.sku}")
            else:
                print(f"    No coating selected for lensIndex {lens_index}")

        # 在所有lensIndex处理完毕后，校验lens_coating_map中每个CoatingItem的sku是否都相同
        print(f"\n------> Validating coating SKUs across all lensIndexes")
        validateCoatingSkus(lens_coating_map)

        print(f"遍历完成，lens_coating_map size = {len(lens_tints_map)} lens_tints_map size = {len(lens_tints_map)}")

        # 在所有lensIndex处理完毕后，校验lens_tints_map
        print(f"\n------> Validating tint consistency across all lensIndexes")
        validateTintConsistency(lens_tints_map)

        # 校验完成后，为TintItem填充lensPackageIndexTintList字段
        print(f"\n------> Populating lensPackageIndexTintList for TintItems")
        processed_first_tints = populateLensPackageIndexTintList(lens_tints_map)
        print(f"\n------> Populating lensPackageIndexTintList for TintItems end")
        
        # 使用处理后的数据，原始lens_tints_map保持不变
        lens_package_tints = group_tints_by_classification(processed_first_tints, lc_tints_config)
        print(f"Original lens_tints_map size: {len(lens_tints_map)}")

        # 组装LensPackage数据
        lens_package = self.assembleLensPackage(csvPackage, lens_coating_map, lens_package_tints, packageIndexes)
        print(f"Assembled LensPackage: {lens_package.id} - {lens_package.title}")
        
        return lens_package

    def assembleLensPackage(self, csvPackage, lens_coating_map, lens_package_tints, package_indexes):
        """
        组装LensPackage数据
        
        Args:
            csvPackage: CsvPackage对象，包含基础信息
            lens_coating_map: 镜片涂层映射
            lens_package_tints: 处理后的tint数据
            index_groups: 按lensIndex分组的镜片数据
            
        Returns:
            LensPackage: 组装好的镜片包数据
        """
        from lenspackage.datamodels.package_data_models import (
            LensPackage, CoatingType, Index, LensType,
            RxType, CompatibleTintsType, TintItem, CostType
        )
        from lenspackage.LensPackageConstant import decideRegion
        
        # 1. 从CsvPackage获取基础信息
        # 解析LensType (e.g. "BlokzGeneralUse:Blokz")
        lens_type = LensType(
            displayName=f"{csv_lens_type_map[csvPackage.LensType].type} {csv_lens_type_map[csvPackage.LensType].sub_type}",
            subType=csv_lens_type_map[csvPackage.LensType].sub_type,
            type=csv_lens_type_map[csvPackage.LensType].type
        )

        # 3. 构建coatingType
        representative_coating = None
        if lens_coating_map:
            representative_coating = list(lens_coating_map.values())[0]
        
        coating_type = CoatingType(
            cost=[CostType(region=decideRegion(), price=representative_coating.price)] if representative_coating else [],
            displayName=representative_coating.coatingResistantType if representative_coating else "",
            sku=representative_coating.sku if representative_coating else ""
        )

        # 6. 构建RxType
        rx_type = RxType(
            prescriptionType=csvPackage.rxType.prescription_type,
            progressiveUsage=csvPackage.rxType.progressive_usage or None
        )
        
        # 7. 组装LensPackage
        lens_package = LensPackage(
            backgroundUrl=csvPackage.backgroundUrl,
            coatingType=coating_type,
            description=csvPackage.packageDescription,
            id=csvPackage.id,
            indexes=package_indexes,
            lensType=lens_type,
            rxType=rx_type,
            shortDescription=csvPackage.packageshortdesc,
            tintType=lens_package_tints,
            title=csvPackage.packageTitle,
            platform=csvPackage.platform
        )
        
        return lens_package

    def assembleProductPackage(self, product_id, lens_packages):
        """
        组装ProductPackage数据
        
        Args:
            product_id: 产品ID
            lens_packages: LensPackage列表
            
        Returns:
            ProductPackage: 组装好的产品包数据
        """
        from lenspackage.datamodels.package_data_models import ProductPackage
        
        product_package = ProductPackage(
            lensPackages=lens_packages,
            objectID=product_id,
            productId=product_id
        )
        
        return product_package

    def saveProductPackagesToFile(self, product_packages: List[ProductPackage]):
        """
        将ProductPackage列表保存到本地JSON文件
        
        Args:
            product_packages: ProductPackage列表
        """
        import json
        import os
        from datetime import datetime
        
        # 创建输出目录
        output_dir = "./output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成文件名（包含时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"product_packages_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        # 将ProductPackage对象转换为字典
        def dataclass_to_dict(obj):
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    if isinstance(value, list):
                        result[key] = [dataclass_to_dict(item) for item in value]
                    elif hasattr(value, '__dict__'):
                        result[key] = dataclass_to_dict(value)
                    else:
                        result[key] = value
                return result
            return obj
        
        # 转换数据
        data_to_save = [dataclass_to_dict(package) for package in product_packages]
        
        # 写入文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            print(f"ProductPackages saved to: {filepath}")
        except Exception as e:
            print(f"Error saving ProductPackages to file: {e}")

    def generateJsonFile(self) -> List[ProductPackage]:
        print("read csv file start ------>")
        csvProductIdPackages: list[CsvProductPackageList] = []  # 明确列表将存储 CsvProductPackageList 对象
        parseCsvAndGenProductPackagesList(self, csvProductIdPackages)

        result_map: dict[str, CsvPackage] = {}
        parseCsvAndGenPackageDetails(self, result_map)

        print("parse csv file end")

        # 收集所有ProductPackage
        all_product_packages = []
        
        for productPackage in csvProductIdPackages:
            pdp_service = PdpService(session=self.session, token_value=self.tokenValue)
            product_skus =pdp_service.getPdp(productPackage.productId)
            # 目前只使用一个sku进行查询，后续需要考虑是否需要遍历每个sku，理论上一个productId下面的每个sku只是颜色不同，走lc流程的所有数据都是一样的
            picked_sku = product_skus[0]
            
            # 收集该productId下的所有lens packages
            lens_packages = []
            for packageId in productPackage.packageList:
                lens_package = self.checkAtgData(productId=productPackage.productId, frameSku=picked_sku, csvPackage=result_map[packageId])
                if lens_package:
                    lens_packages.append(lens_package)
            
            # 组装ProductPackage
            if lens_packages:
                product_package = self.assembleProductPackage(productPackage.productId, lens_packages)
                all_product_packages.append(product_package)
                print(f"Assembled ProductPackage: {product_package.productId} with {len(product_package.lensPackages)} lens packages")
                # 这里可以进一步处理product_package，比如保存到文件或返回
            print(f"generate lens package for more productId {productPackage.productId} end")
        
        print("generate lens package end")
        print(f"Total ProductPackages generated: {len(all_product_packages)}")
        
        # 将ProductPackage列表写入本地文件
        self.saveProductPackagesToFile(all_product_packages)
        
        return all_product_packages