import pandas as pd
from transactions.sales import analyze_sales_by_reseller
from transactions.sales import analyze_clients_revenue
from transactions.sales import analyze_sales_by_month
from transactions.sales import analyze_sales_by_tier
from transactions.sales import analyze_sales_by_channel
from transactions.clients import analyze_clients_by_region

# 读取 transactions.csv 文件，保存成 pandas DataFrame
df = pd.read_csv('transactions.csv')

# 将所有处理方法添加到一个列表中
process_methods = [
    ('Sales by Month', analyze_sales_by_month),
    ('Sales by Tier', analyze_sales_by_tier),
    ('Sales by Channel', analyze_sales_by_channel),
    ('Sales by Reseller', analyze_sales_by_reseller),
    ('Clients by Revenue and Lost', analyze_clients_revenue),
    ('Clients by Region', analyze_clients_by_region)
    # 在这里可以添加更多的处理方法
]

# 获取所有唯一的 addonKey
addon_keys = df['addonKey'].unique()

# 按 addonKey 分组并分别处理
for addon_key in addon_keys:
    df_subset = df[df['addonKey'] == addon_key]
    
    # 用于存储所有处理结果的字典
    results = {}

    # 循环调用每个处理方法，并将结果存储在字典中
    for method_name, method in process_methods:
        df_result = method(df_subset)
        results[method_name] = df_result

    # 将所有处理结果输出到一个 Excel 文件，每个结果作为一个 sheet
    output_file = f'transactions_report_{addon_key}.xlsx'
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for sheet_name, result_df in results.items():
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print(f"Processing for addonKey {addon_key} done. Results saved to {output_file}")

print("All processing done for all addonKeys.")