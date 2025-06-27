import csv
import pandas as pd

from lenspackage.CsvPackage import CsvPackage, CsvProductPackageList


def parseCsvAndGenPackageDetails(self, result_map):
    try:
        # 2. 使用 pandas 读取 CSV 文件
        df = pd.read_csv(self.package_detail_csv_file, skipinitialspace=True, dtype={'id': str})
        print("Original DataFrame (before cleaning):")
        print(df)
        print("-" * 30)
        # 3. 数据清洗和转换
        # 重命名列名，使其与类属性名匹配
        df.rename(columns={
            'LensType(e.g. BlokzGeneralUse:Blokz)': 'LensType',
            'index(e.g. 1.5/1.51/1.61)': 'index',
            'Tint(e.g. Gray/light Green)': 'Tint',
            'Coating(e.g. oil-res coating)': 'Coating'
        }, inplace=True)

        # 处理 'index' 列：去除空白和换行符，分割并转换为字符串列表
        def parse_index_list_str(index_str):  # 函数名也相应修改，表示返回字符串列表
            if pd.isna(index_str):
                return []
            # 移除所有空白字符（包括换行符、空格），然后按逗号分割
            clean_str = str(index_str).replace('\n', '').replace(' ', '')
            if not clean_str:  # 如果清理后是空字符串，返回空列表
                return []
            # 仅仅分割，不再转换为浮点数，但保留strip()以防空格
            return [s.strip() for s in clean_str.split(',') if s.strip()]  # 确保s不是空字符串

        df['index'] = df['index'].apply(parse_index_list_str)  # 调用新的解析函数
        # 处理 'Tint', 'Coating', 'backgroundUrl', 'platform' 列中的 NaN 值，将其转换为 None
        for col in ['backgroundUrl', 'Tint', 'Coating', 'platform']:
            df[col] = df[col].astype(str).replace({'nan': None, '': None})
        print("\nDataFrame after cleaning and parsing:")
        print(df)
        print("-" * 30)
        # 4. 遍历 DataFrame 的每一行，创建 CsvPackage 实例并添加到字典
        for _, row in df.iterrows():
            current_id = row['id']
            obj = CsvPackage(
                id=current_id,
                packageTitle=row['packageTitle'],
                packageDescription=row['packageDescription'],
                packageshortdesc=row['packageshortdesc'],
                backgroundUrl=row['backgroundUrl'],
                LensType=row['LensType'],
                index=row['index'],  # 此时已经是字符串列表
                Tint=row['Tint'],
                Coating=row['Coating'],
                platform=row['platform']
            )
            result_map[current_id] = obj
        print("\nResulting map (key: id, value: CsvPackage object):")
        for key, value in result_map.items():
            print(f"Key: '{key}', Value: {value}")
    except FileNotFoundError:
        print(f"Error: The file '{self.package_detail_csv_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()


def parseCsvAndGenProductPackagesList(self, result_objects):
    try:
        # 2. 使用 pandas 读取 CSV 文件
        df = pd.read_csv(self.product_packages_csv_file, dtype={'productId': str})  # 确保 productId 被读取为字符串
        print("Original DataFrame:")
        print(df)
        print("-" * 30)

        # 3. 解析 'packages' 列的字符串到字符串列表
        def parse_packages_to_list(packages_str):
            if pd.isna(packages_str):
                return []
            # 使用 strip() 移除可能的空白字符，转换为字符串列表
            return [s.strip() for s in str(packages_str).split(',')]

        # 对 DataFrame 的 'packages' 列应用解析函数
        df['packages'] = df['packages'].apply(parse_packages_to_list)
        print("\nDataFrame after parsing 'packages' column:")
        print(df)
        print("-" * 30)
        # 4. 遍历 DataFrame 的每一行，创建 CsvProductPackageList 实例
        for index, row in df.iterrows():
            # 注意：productId 默认可能被 pandas 推断为 int，
            # 如果你希望它始终是字符串，可以在 read_csv 时使用 dtype={'productId': str}
            # 或者在这里显式转换为字符串：str(row['productId'])
            product_id = str(row['productId'])
            package_list = row['packages']  # 此时已经是字符串列表了
            obj = CsvProductPackageList(productId=product_id, packageList=package_list)
            result_objects.append(obj)
    except FileNotFoundError:
        print(f"Error: The file '{self.product_packages_csv_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")