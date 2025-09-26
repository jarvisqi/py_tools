import pandas as pd
import glob
import chardet
import polars as pl
import os


settle_path = "/Documents/XX_资金结算_01_20241231.xlsx"


# 先检测文件编码
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result["encoding"]


def company_codes():
    file_path = "/Users/jarvis/Documents/XXX_银行账户_01_20241231(0714).xlsx"
    pd_data = pd.read_excel(file_path, engine="openpyxl")

    columns_to_duplicate = pd_data[["开户单位编码", "开户单位名称"]]
    deduplicated_df = columns_to_duplicate.drop_duplicates()
    deduplicated_df.to_excel("company_codes.xlsx", index=False)


def simple_merge_csv(input_folder, output_file):
    csv_files = glob.glob(f"{input_folder}/*.csv")
    df_list = [pd.read_csv(f, encoding="utf-8") for f in csv_files]
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"合并了 {len(csv_files)} 个文件，总行数: {len(merged_df)}")


# 合并多个CSV文件
def merge_csv_flexible(input_folder, output_file):
    csv_files = glob.glob(f"{input_folder}/*.csv")

    df_list = []
    for file in csv_files:
        try:
            # 方法1: 使用 error_bad_lines=False 跳过有问题的行
            # df = pd.read_csv(file, encoding="utf-8", on_bad_lines="skip")

            encoding = detect_encoding(file)
            print(f"检测到的编码: {encoding}")

            # 方法2: 或者使用 engine='python' 和更宽松的解析
            df = pd.read_csv(
                file, encoding="utf-8", engine="python", on_bad_lines="skip"
            )

            df_list.append(df)
            print(f"成功读取: {file}")

        except Exception as e:
            print(f"读取 {file} 时出错: {e}")
            # 尝试使用不同的分隔符或处理方式
            try:
                df = pd.read_csv(
                    file,
                    encoding="utf-8",
                    sep=None,
                    engine="python",
                    on_bad_lines="skip",
                )
                df_list.append(df)
                print(f"使用备用方法成功读取: {file}")
            except:
                print(f"无法读取文件: {file}")

    if df_list:
        merged_df = pd.concat(df_list, ignore_index=True)
        merged_df.to_csv(output_file, index=False, encoding="utf-8")
        print(f"合并完成！总行数: {len(merged_df)}")
    else:
        print("没有成功读取任何文件")


def merge_excel():
    # 步骤1: 读取Excel文件中的A1和A2两个Sheet
    dfa1 = pd.read_excel(settle_path, sheet_name="A1")
    dfa2 = pd.read_excel(settle_path, sheet_name="12月")

    # 步骤2: 创建映射字典
    c2_to_c1_map = pd.Series(
        dfa1["开户单位编码"].values, index=dfa1["开户单位名称"]
    ).to_dict()

    # 步骤3: 使用映射更新A2中的'D1'列
    dfa2["本方单位编码"] = dfa2["本方单位名称"].map(c2_to_c1_map)

    # 步骤4: 将更新后的A2表格保存为CSV文件
    csv_file = "XXX_资金结算_17_20241231.csv"
    dfa2.to_csv(csv_file, index=False)

    print("finished")


def process_with_polars(input_file, output_file):
    """使用Polars处理大CSV文件"""

    # 读取文件（Polars对大数据更高效）
    df = pl.read_csv(
        input_file,
        infer_schema_length=0,  # 重要：不推断数据类型
        try_parse_dates=False,  # 不尝试解析日期
    )

    print(f"数据形状: {df.shape}")
    print(f"内存使用: {df.estimated_size() / 1024 / 1024:.2f} MB")

    # 先处理原始格式
    df = df.with_columns(
        pl.col("交易时间")
        # 处理 2024/8/59:13 格式
        .str.replace(r"^(\d{4})/(\d{1,2})/(\d{1})(\d{1,2}:\d{2})$", r"$1-$2-$3 $4")
        .str.replace(r"^(\d{4})/(\d{1,2})/(\d{2})(\d{1,2}:\d{2})$", r"$1-$2-$3 $4")
        .str.replace("/", "-")
    )

    # 再修复已经部分转换的格式
    df = df.with_columns(
        pl.col("交易时间").str.replace(
            r"^(\d{4})-(\d{1,2})-(\d{2})\s+(\d{1,2}:\d{2})$", r"$1-$2-$3 $4"
        )
    )

    # 保存结果
    df.write_csv(output_file)
    return df


def batch_excel_to_csv(input_folder, output_folder=None):
    """
    批量转换Excel文件为CSV

    Args:
        input_folder: 输入文件夹路径
        output_folder: 输出文件夹路径（可选）
    """
    if output_folder is None:
        output_folder = input_folder

    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历目录中的所有文件
    for file in os.listdir(input_folder):
        if file.endswith((".xls", ".xlsx")):
            try:
                # 读取第一个工作表
                df = pd.read_excel(os.path.join(input_folder, file))

                # 生成输出文件名
                csv_name = os.path.splitext(file)[0] + ".csv"
                output_path = os.path.join(output_folder, csv_name)

                # 保存为CSV
                df.to_csv(output_path, index=False, encoding="utf-8-sig")
                print(f"✓ 已转换: {file} -> {csv_name}")

            except Exception as e:
                print(f"✗ 转换失败 {file}: {e}")


def simple_convert_to_utf8(folder_path, create_backup=True):
    """
    简单直接的UTF-8转换方案
    """
    # 常见的中文编码
    encodings_to_try = ["utf-8", "gbk", "gb2312", "latin1", "iso-8859-1"]

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".csv"):
            file_path = os.path.join(folder_path, filename)

            # 创建备份
            if create_backup:
                backup_path = os.path.join(folder_path, f"backup_{filename}")
                import shutil

                shutil.copy2(file_path, backup_path)
                print(f"创建备份: {backup_path}")

            # 尝试不同编码读取
            df = None
            used_encoding = None

            for encoding in encodings_to_try:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    used_encoding = encoding
                    print(f"成功读取 {filename} 使用编码: {encoding}")
                    break
                except (UnicodeDecodeError, pd.errors.EmptyDataError) as e:
                    continue

            if df is not None:
                # 保存为UTF-8 with BOM（更好的中文兼容性）
                df.to_csv(file_path, index=False, encoding="utf-8-sig")
                print(f"✓ 已转换: {filename} (原编码: {used_encoding} -> UTF-8)")
            else:
                print(f"✗ 无法读取: {filename}")


if __name__ == "__main__":
    # main()/Users/jarvis

    merge_csv_flexible(
        "/Volumes/NO NAME/完整数据2/AA",
        "/Volumes/NO NAME/完整数据2/CC/XXX_资金结算_03_20241231.csv",
    )

    # # 设置你的目录路径
    # excel_dir = "/Volumes/NO NAME/完整数据2/"  # 修改为你的Excel文件目录
    # csv_dir = "/Volumes/NO NAME/完整数据2/AA"  # 修改为你想保存CSV的目录

    # batch_excel_to_csv(excel_dir, csv_dir)

    # process_with_polars(
    #     "/Users/Downloads/XXX_资金结算_02_20241231.csv",
    #     "/Users/Downloads/XXX_资金结算_02_20241231_01.csv",
    # )

    # # 使用
    # simple_convert_to_utf8("/Volumes/NO NAME/完整数据2/BB")
