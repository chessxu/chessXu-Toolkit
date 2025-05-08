import pandas as pd
from collections import Counter
import argparse


def analyze_column_distribution(csv_file, column_name):
    """
    统计CSV文件中指定列的数据值分布情况

    参数:
        csv_file (str): CSV文件路径
        column_name (str): 要分析的列名

    返回:
        dict: 包含值分布统计结果的字典
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_file)

        # 检查列是否存在
        if column_name not in df.columns:
            available_columns = ", ".join(df.columns)
            raise ValueError(f"列 '{column_name}' 不存在。可用列有: {available_columns}")

        # 获取指定列的数据
        column_data = df[column_name]

        # 统计值分布
        value_counts = Counter(column_data)

        # 计算百分比
        total = len(column_data)
        distribution = {
            'total_count': total,
            'unique_values': len(value_counts),
            'value_counts': value_counts,
            'percentage': {k: (v / total) * 100 for k, v in value_counts.items()}
        }

        return distribution

    except Exception as e:
        print(f"发生错误: {e}")
        return None


def print_distribution_report(distribution):
    """打印分布统计报告"""
    if not distribution:
        return

    print("\n=== 数据分布统计报告 ===")
    print(f"总数据量: {distribution['total_count']}")
    print(f"唯一值数量: {distribution['unique_values']}")

    print("\n值计数:")
    for value, count in distribution['value_counts'].most_common():
        print(f"  {value}: {count}次 ({distribution['percentage'][value]:.2f}%)")


# 示例用法
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-csv_path', help="the path of corresponding csv")
    parser.add_argument("-target_column", help="target column name")
    args = parser.parse_args()

    # 分析数据分布
    distribution = analyze_column_distribution(args.csv_path, args.target_column)

    # 打印报告
    if distribution:
        print_distribution_report(distribution)
    else:
        print("未能生成分布报告。")