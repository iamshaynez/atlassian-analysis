import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('transactions.csv')

# 过滤出代理商的记录，排除直接购买的情况
reseller_df = df.dropna(subset=['partnerName'])

# 统计每个代理商的总计销售金额，笔数，笔均销售金额
reseller_stats = reseller_df.groupby('partnerName').agg(
    total_sales_amount=('purchasePrice', 'sum'),
    total_sales_count=('purchasePrice', 'count'),
    average_sales_amount=('purchasePrice', 'mean')
).reset_index()

# 获取代理商的联系方式
reseller_contact_info = reseller_df[['partnerName', 'partnerContactEmail', 'partnerContactName']].drop_duplicates()

# 合并统计信息和联系方式
reseller_info = pd.merge(reseller_stats, reseller_contact_info, on='partnerName')

# 输出结果
print(reseller_info)

# 保存结果到新的 CSV 文件
reseller_info.to_csv('reseller_sales_summary.csv', index=False)