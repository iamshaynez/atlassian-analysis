import pandas as pd
from datetime import datetime

def analyze_clients_revenue(df):
    # 拷贝 df
    df_copy = df.copy()

    # 转换 saleDate 和 maintenanceEndDate 为 datetime
    df_copy['saleDate'] = pd.to_datetime(df_copy['saleDate'])
    df_copy['maintenanceEndDate'] = pd.to_datetime(df_copy['maintenanceEndDate'])

    # 添加一个新的列 'annualPrice'，根据 billingPeriod 转换为年收入
    df_copy['annualPrice'] = df_copy.apply(
        lambda row: row['purchasePrice'] * 12 if row['billingPeriod'] == 'Monthly' else row['purchasePrice'], axis=1)

    # 获取每个客户的最后一次购买记录
    last_purchase = df_copy.sort_values('saleDate').groupby('company').tail(1)

    # 标记客户是否流失
    def check_if_lost(row):
        if row['billingPeriod'] == 'Annual':
            return (datetime.now() - row['saleDate']).days > 367
        else:
            return (datetime.now() - row['saleDate']).days > 32

    last_purchase['lostCustomer'] = last_purchase.apply(check_if_lost, axis=1)

    # 选择需要的列
    result = last_purchase[['company', 'annualPrice', 'billingPeriod', 'saleDate', 'lostCustomer']]
    result = result.sort_values(by='annualPrice', ascending=False)

    return result


def analyze_sales_by_month(df):    # 拷贝 df 为 df_copy
    df_copy = df.copy()
    
    # 确保 saleDate 是 datetime 类型
    df_copy['saleDate'] = pd.to_datetime(df_copy['saleDate'])
    
    # 提取年月并添加为新列
    df_copy['year_month'] = df_copy['saleDate'].dt.strftime('%Y-%m')
    
    # 按年-月和地区统计销售总额
    sales_summary = df_copy.pivot_table(
        index='year_month',
        columns='region',
        values='purchasePrice',
        aggfunc='sum',
        fill_value=0
    )
    
    # 添加总计列
    sales_summary['total'] = sales_summary.sum(axis=1)
    
    # 转换 year_month 为 datetime 以便排序
    sales_summary.index = pd.to_datetime(sales_summary.index, format='%Y-%m')
    
    # 按 year_month 从近到远排序
    sales_summary = sales_summary.sort_index(ascending=False)
    
    # 重置索引并将 year_month 转回字符串格式
    sales_summary = sales_summary.reset_index()
    sales_summary['year_month'] = sales_summary['year_month'].dt.strftime('%Y-%m')
    
    return sales_summary

def analyze_sales_by_tier(df):
    # 拷贝数据集    # 拷贝数据集
    df_copy = df.copy()

    # 添加 year_month 列
    df_copy['saleDate'] = pd.to_datetime(df_copy['saleDate'])
    df_copy['year_month'] = df_copy['saleDate'].dt.to_period('M')
    
    # 按月统计销售总额并按照客户 tier 细分
    summary = df_copy.pivot_table(
        index='year_month',
        columns='tier',
        values='purchasePrice',
        aggfunc='sum',
        fill_value=0
    ).reset_index()

    # 计算每月的总销售额
    summary['total'] = summary.loc[:, summary.columns != 'year_month'].sum(axis=1)
    
    # 按照 year_month 从近到远排序
    summary = summary.sort_values(by='year_month', ascending=False)
    
    return summary

def analyze_sales_by_channel(df):
    df_copy = df.copy()

    # 添加 year_month 列
    df_copy['saleDate'] = pd.to_datetime(df_copy['saleDate'])
    df_copy['year_month'] = df_copy['saleDate'].dt.to_period('M')

    # 按月统计直接销售金额和代理商销售金额
    direct_sales = df_copy[df_copy['partnerName'].isna()]
    reseller_sales = df_copy[~df_copy['partnerName'].isna()]

    direct_sales_monthly = direct_sales.groupby('year_month')['purchasePrice'].sum().reset_index()
    direct_sales_monthly.rename(columns={'purchasePrice': 'direct_sales'}, inplace=True)

    reseller_sales_monthly = reseller_sales.groupby('year_month')['purchasePrice'].sum().reset_index()
    reseller_sales_monthly.rename(columns={'purchasePrice': 'reseller_sales'}, inplace=True)

    # 合并直接销售和代理商销售数据
    monthly_sales = pd.merge(direct_sales_monthly, reseller_sales_monthly, on='year_month', how='outer').fillna(0)
    monthly_sales['total'] = monthly_sales['direct_sales'] + monthly_sales['reseller_sales']

    # 按照 year_month 从近到远排序
    monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
    monthly_sales = monthly_sales.sort_values(by='year_month', ascending=False).reset_index(drop=True)

    return monthly_sales

def analyze_sales_by_reseller(df):
    # 复制 DataFrame，确保不修改原始数据
    df_copy = df.copy()

    # 过滤出包含代理商销售的记录
    reseller_sales = df_copy[df_copy['partnerName'].notna()]

    # 按代理商分组，计算销售总额、销售笔数和平均每笔金额
    reseller_summary = reseller_sales.groupby('partnerName').agg(
        total_sales=('purchasePrice', 'sum'),
        sales_count=('purchasePrice', 'count'),
        average_per_sale=('purchasePrice', 'mean')
    ).reset_index()

    return reseller_summary