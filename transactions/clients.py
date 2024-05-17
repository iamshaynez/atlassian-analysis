import pandas as pd

def analyze_clients_by_region(df):
    # 拷贝 df 为 df_copy
    df_copy = df.copy()

    # 将 saleDate 转换为 datetime 类型
    df_copy['saleDate'] = pd.to_datetime(df_copy['saleDate'])

    # 按照 company 去重，只保留每个公司最早的记录
    df_copy = df_copy.sort_values('saleDate').drop_duplicates(subset='company', keep='first')

    # 提取 year_month 列
    df_copy['year_month'] = df_copy['saleDate'].dt.to_period('M')

    # 按照 year_month 和 region 分组统计客户总数
    grouped = df_copy.groupby(['year_month', 'region']).size().unstack(fill_value=0)

    # 计算截止每个月的累计总数
    cumulative = grouped.cumsum()

    # 计算 total 列
    cumulative['total'] = cumulative.sum(axis=1)

    # 按照 year_month 从近到远排序
    cumulative = cumulative.sort_index(ascending=False)

    return cumulative.reset_index()

# 示例用法
if __name__ == "__main__":
    # 读取 CSV 文件
    file_path = 'transactions.csv'
    df = pd.read_csv(file_path)

    # 分析数据
    result_df = analyze_clients_by_region(df)

    # 输出结果
    print(result_df)
