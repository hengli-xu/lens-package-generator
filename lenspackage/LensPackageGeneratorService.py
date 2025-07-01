from lenspackage.CsvPackage import CsvProductPackageList, CsvPackage
from lenspackage.lcapi.IndexService import IndexService
from lenspackage.lcapi.LensTypeService import LensTypeService
from lenspackage.lcapi.PdpService import PdpService
from lenspackage.lcapi.RxTypeService import RxTypeService

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
        compatible_lenses, indexes = self.checkIndexWithAtg(csvPackage, frameSku, productId)

        # 4. 按lensIndex分组处理tint
        self.processTintsByLensIndex(productId, frameSku, csvPackage, compatible_lenses)

        print(f"<------ lens package: productId {productId} frameSku {frameSku} packageId : {csvPackage.id} end")

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

    def processTintsByLensIndex(self, productId, frameSku, csvPackage, compatible_lenses):
        """
        按lensIndex分组处理tint
        """
        from lenspackage.lcapi.TintService import TintService
        from lenspackage.lcapi.data_models import TintItem
        
        # 按lensIndex分组
        index_service = IndexService(session=self.session, token_value=self.tokenValue)
        index_groups = index_service.groupIndexesByLensIndex(compatible_lenses)
        
        tint_service = TintService(session=self.session, token_value=self.tokenValue)
        
        for lens_index, lens_items in index_groups.items():
            print(f"------> Processing tints for lensIndex: {lens_index}")
            
            # 收集该lensIndex的所有tints
            all_tints = []
            
            for lens_item in lens_items:
                # 如果tintClassification不为空，直接生成tint对象
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
                    all_tints.append(tint_item)
                    print(f"  Generated tint for SKU {lens_item.sku}: {tint_item.tintBase} ({tint_item.classification})")
                else:
                    # 如果tintClassification为空，调用TintService
                    tint_result = tint_service.getCompatibleTints(productId, frameSku, csvPackage, lens_item.sku)
                    if tint_result:
                        # 将API返回的tints添加到列表中
                        api_tints = tint_result.compatibleTints
                        all_tints.extend(api_tints)
                        print(f"  Called TintService for SKU {lens_item.sku}, got {len(api_tints)} tints")
                    else:
                        print(f"  No tint result for SKU {lens_item.sku}")
            
            # 去重，保留唯一的tint（基于sku）
            unique_tints = []
            seen_skus = set()
            for tint in all_tints:
                if tint.sku and tint.sku not in seen_skus:
                    unique_tints.append(tint)
                    seen_skus.add(tint.sku)
                elif not tint.sku:  # 对于没有sku的tint（如手动创建的），基于tintBase去重
                    if tint.tintBase not in seen_skus:
                        unique_tints.append(tint)
                        seen_skus.add(tint.tintBase)
            
            print(f"  Total unique tints for lensIndex {lens_index}: {len(unique_tints)}")
            # TODO：每组内去[1.5/1.61/1.67]去校验每个tint的baseTint是一样的是一样的

    def generateJsonFile(self):
        print("read csv file start ------>")
        csvProductIdPackages: list[CsvProductPackageList] = []  # 明确列表将存储 CsvProductPackageList 对象
        parseCsvAndGenProductPackagesList(self, csvProductIdPackages)

        result_map: dict[str, CsvPackage] = {}
        parseCsvAndGenPackageDetails(self, result_map)

        print("parse csv file end")

        for productPackage in csvProductIdPackages:
            pdp_service = PdpService(session=self.session, token_value=self.tokenValue)
            product_skus =pdp_service.getPdp(productPackage.productId)
            # 目前只使用一个sku进行查询，后续需要考虑是否需要遍历每个sku，理论上一个productId下面的每个sku只是颜色不同，走lc流程的所有数据都是一样的
            picked_sku = product_skus[0]
            for packageId in productPackage.packageList:
                self.checkAtgData(productId=productPackage.productId,frameSku = picked_sku, csvPackage = result_map[packageId])
