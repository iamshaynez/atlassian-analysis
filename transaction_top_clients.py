import pandas as pd

# 读取 CSV 文件到 DataFrame，并将 saleDate 解析为日期时间类型
df = pd.read_csv('transactions.csv', parse_dates=['saleDate'])

# 定义一个函数来计算年收入
def calculate_annual_revenue(row):
    if row['billingPeriod'] == 'monthly':
        return row['purchasePrice'] * 12
    return row['purchasePrice']

# 添加一个新列 'annualRevenue'，用于存储年收入
df['annualRevenue'] = df.apply(calculate_annual_revenue, axis=1)

# 按公司和最后一次购买日期分组，获取每个公司的最新交易记录
latest_transactions = df.loc[df.groupby('company')['saleDate'].idxmax()]

# 按年收入降序排序
sorted_df = latest_transactions.sort_values(by='annualRevenue', ascending=False)

# 选择所需的列，并重命名以便更好理解
final_df = sorted_df[['company', 'annualRevenue', 'billingPeriod', 'saleDate']].rename(columns={
    'annualRevenue': 'CurrentAnnualPrice',
    'billingPeriod': 'SubscriptionType',
    'saleDate': 'LastPurchaseDate'
})

# 输出结果
print(final_df)

# 保存结果到 CSV 文件
final_df.to_csv('sorted_customers_by_revenue.csv', index=False)