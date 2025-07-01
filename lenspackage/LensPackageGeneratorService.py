import requests
from requests import session
from dataclasses import dataclass
from typing import List

from lenspackage.CsvPackage import CsvProductPackageList, CsvPackage
from lenspackage.lcapi.CoatingService import CoatingService
from lenspackage.lcapi.IndexService import IndexService
from lenspackage.lcapi.LensTypeService import LensTypeService
from lenspackage.lcapi.PdpService import PdpService
from lenspackage.lcapi.RxTypeService import RxTypeService
from lenspackage.LensPackageConstant import csv_lens_type_map

from lenspackage.parsecsv.CsvParser import parseCsvAndGenProductPackagesList, parseCsvAndGenPackageDetails
from settings import env_key, yaml_cfg

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
