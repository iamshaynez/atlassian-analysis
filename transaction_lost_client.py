import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('transactions.csv')

# 将 saleDate 和 maintenanceEndDate 转换为日期格式
df['saleDate'] = pd.to_datetime(df['saleDate'])
df['maintenanceEndDate'] = pd.to_datetime(df['maintenanceEndDate'])

# 找出最后一次购买的记录
last_purchases = df.sort_values(by='saleDate').groupby('company').last().reset_index()

# 当前日期
current_date = pd.to_datetime('today')

# 找出不再续费的客户（maintenanceEndDate 早于当前日期）
former_customers = last_purchases[last_purchases['maintenanceEndDate'] < current_date]

# 选择需要的列
result = former_customers[['company', 'saleDate', 'tier', 'purchasePrice', 'maintenanceEndDate']]

print(result)

# 将结果保存到 CSV 文件
result.to_csv('former_customers.csv', index=False)