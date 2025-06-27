# id,
# packageTitle,
# packageDescription,
# packageshortdesc,
# backgroundUrl,
# LensType(e.g. BlokzGeneralUse:Blokz),
# index(e.g. 1.5/1.51/1.61),
# Tint(e.g. Gray/light Green),
# Coating(e.g. oil-res coating),
# platform
from lenspackage.lens_package_simple import gen_rx_type


class CsvPackage:
    def __init__(self, id, packageTitle, packageDescription, packageshortdesc, backgroundUrl, LensType, index, Tint,
                 Coating, platform):
        self.id = id
        self.packageTitle = packageTitle
        self.packageDescription = packageDescription
        self.packageshortdesc = packageshortdesc
        self.backgroundUrl = backgroundUrl
        self.LensType = LensType
        self.index = index
        self.tint = Tint,
        self.coating = Coating,
        self.platform = platform
        self.rxType = gen_rx_type(platform, LensType)


class CsvProductPackageList:
    def __init__(self, productId, packageList):
        self.productId = productId
        self.packageList = packageList
