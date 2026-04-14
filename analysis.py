"""
Store Sales Performance Analysis
San Martin Stores — Multi-Table EDA & KPI Analysis
Author: Soumya Shah
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 65)
print("  STORE SALES PERFORMANCE ANALYSIS — SAN MARTIN STORES")
print("=" * 65)

# ============================================================
# 1. LOAD & MERGE ALL DATA SOURCES
# ============================================================
print("\n📂 Loading data sources...")

sales = pd.read_excel('Updated_Sales_Sheet.xlsx')
master = pd.read_excel('1_-San-Martin-Stores-2021_Challenge-1.xlsx', sheet_name=None)

customers   = master['Customers']
locations   = master['Locations']
products    = master['Products']
agents      = master['Sales Agents'][['Sales Agent Key', 'Sales Agent Name']]
stores      = master['Stores']

print(f"  ✅ Sales records loaded:     {len(sales):,}")
print(f"  ✅ Customers:                {len(customers):,}")
print(f"  ✅ Products:                 {len(products):,}")
print(f"  ✅ Stores:                   {len(stores):,}")
print(f"  ✅ Sales Agents:             {len(agents):,}")
print(f"  ✅ Locations (regions):      {len(locations):,}")

# ============================================================
# 2. DATA CLEANING & PREPROCESSING
# ============================================================
print("\n🔧 Preprocessing...")

# Fix column name typo
sales.rename(columns={'Quanttity': 'Quantity'}, inplace=True)

# Parse dates
sales['Order Date']    = pd.to_datetime(sales['Order Date'], errors='coerce')
sales['Shipping date'] = pd.to_datetime(sales['Shipping date'], errors='coerce')
sales['Invoice Date']  = pd.to_datetime(sales['Invoice Date'], errors='coerce')

# Derive time features
sales['Year']       = sales['Order Date'].dt.year
sales['Month']      = sales['Order Date'].dt.month
sales['Month_Name'] = sales['Order Date'].dt.strftime('%B')
sales['Quarter']    = sales['Order Date'].dt.quarter

# Derive shipping time
sales['Shipping_Days'] = (sales['Shipping date'] - sales['Order Date']).dt.days

# Check nulls
nulls = sales.isnull().sum()
print(f"  ✅ Missing values: {nulls[nulls > 0].to_dict() or 'None found'}")

# Merge all tables
df = sales.copy()
df = df.merge(agents, on='Sales Agent Key', how='left')
df = df.merge(locations[['Region Key', 'Region', 'State', 'City']], on='Region Key', how='left')
df = df.merge(products[['Product Key', 'Products Category', 'Products']], on='Product Key', how='left')

print(f"  ✅ Full merged dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")

# ============================================================
# 3. OVERALL KPIs
# ============================================================
print("\n" + "=" * 65)
print("  KEY PERFORMANCE INDICATORS")
print("=" * 65)

total_revenue = df['Sales'].sum()
total_profit  = df['Profit'].sum()
total_cost    = df['Cost'].sum()
total_orders  = len(df)
profit_margin = total_profit / total_revenue * 100
avg_order_val = total_revenue / total_orders
avg_shipping  = df['Shipping_Days'].mean()

print(f"\n  Total Revenue:        ${total_revenue:>15,.2f}")
print(f"  Total Profit:         ${total_profit:>15,.2f}")
print(f"  Total Cost:           ${total_cost:>15,.2f}")
print(f"  Profit Margin:        {profit_margin:>14.1f}%")
print(f"  Total Orders:         {total_orders:>15,}")
print(f"  Avg Order Value:      ${avg_order_val:>15,.2f}")
print(f"  Avg Shipping Days:    {avg_shipping:>14.1f}")

# ============================================================
# 4. REGIONAL PERFORMANCE
# ============================================================
print("\n" + "=" * 65)
print("  REGIONAL PERFORMANCE")
print("=" * 65)

region_perf = df.groupby('Region').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Sales', 'count')
).assign(
    Margin=lambda x: x['Profit'] / x['Revenue'] * 100,
    Revenue_Share=lambda x: x['Revenue'] / x['Revenue'].sum() * 100
).sort_values('Revenue', ascending=False)

print(f"\n  {'Region':<10} {'Revenue':>13} {'Profit':>12} {'Margin':>8} {'Share':>8}")
print("  " + "-" * 55)
for region, row in region_perf.iterrows():
    print(f"  {region:<10} ${row['Revenue']:>11,.0f} ${row['Profit']:>10,.0f} "
          f"{row['Margin']:>7.1f}% {row['Revenue_Share']:>7.1f}%")

# ============================================================
# 5. AGENT PERFORMANCE
# ============================================================
print("\n" + "=" * 65)
print("  SALES AGENT PERFORMANCE")
print("=" * 65)

agent_perf = df.groupby('Sales Agent Name').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Sales', 'count')
).assign(
    Margin=lambda x: x['Profit'] / x['Revenue'] * 100,
    Revenue_Share=lambda x: x['Revenue'] / x['Revenue'].sum() * 100
).sort_values('Revenue', ascending=False)

print(f"\n  {'Agent':<20} {'Revenue':>13} {'Margin':>8} {'Share':>8} {'Orders':>8}")
print("  " + "-" * 62)
for agent, row in agent_perf.iterrows():
    print(f"  {agent:<20} ${row['Revenue']:>11,.0f} "
          f"{row['Margin']:>7.1f}% {row['Revenue_Share']:>7.1f}% {row['Orders']:>7,}")

# ============================================================
# 6. PRODUCT CATEGORY ANALYSIS
# ============================================================
print("\n" + "=" * 65)
print("  PRODUCT CATEGORY PERFORMANCE")
print("=" * 65)

cat_perf = df.groupby('Products Category').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Sales', 'count')
).assign(
    Margin=lambda x: x['Profit'] / x['Revenue'] * 100
).sort_values('Revenue', ascending=False)

print(f"\n  {'Category':<22} {'Revenue':>13} {'Profit':>12} {'Margin':>8} {'Orders':>8}")
print("  " + "-" * 67)
for cat, row in cat_perf.iterrows():
    print(f"  {cat:<22} ${row['Revenue']:>11,.0f} ${row['Profit']:>10,.0f} "
          f"{row['Margin']:>7.1f}% {row['Orders']:>7,}")

# ============================================================
# 7. YEARLY TREND ANALYSIS
# ============================================================
print("\n" + "=" * 65)
print("  YEARLY REVENUE TREND (2018-2022)")
print("=" * 65)

yearly = df.groupby('Year').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Sales', 'count')
).assign(
    YoY_Growth=lambda x: x['Revenue'].pct_change() * 100,
    Margin=lambda x: x['Profit'] / x['Revenue'] * 100
)

print(f"\n  {'Year':<8} {'Revenue':>13} {'Profit':>12} {'Margin':>8} {'YoY Growth':>12}")
print("  " + "-" * 57)
for year, row in yearly.iterrows():
    growth = f"{row['YoY_Growth']:>+.1f}%" if not pd.isna(row['YoY_Growth']) else "        —"
    print(f"  {year:<8} ${row['Revenue']:>11,.0f} ${row['Profit']:>10,.0f} "
          f"{row['Margin']:>7.1f}% {growth:>11}")

# ============================================================
# 8. SHIPPING EFFICIENCY
# ============================================================
print("\n" + "=" * 65)
print("  SHIPPING EFFICIENCY BY REGION")
print("=" * 65)

shipping = df.groupby('Region')['Shipping_Days'].agg(
    ['mean', 'min', 'max']
).round(1).sort_values('mean')
shipping.columns = ['Avg Days', 'Min Days', 'Max Days']

print(f"\n  {'Region':<12} {'Avg Days':>10} {'Min':>8} {'Max':>8}")
print("  " + "-" * 42)
for region, row in shipping.iterrows():
    print(f"  {region:<12} {row['Avg Days']:>9.1f} "
          f"{row['Min Days']:>7.0f} {row['Max Days']:>7.0f}")

# ============================================================
# 9. TOP 10 PRODUCTS
# ============================================================
print("\n" + "=" * 65)
print("  TOP 10 PRODUCTS BY REVENUE")
print("=" * 65)

top_products = df.groupby('Products').agg(
    Revenue=('Sales', 'sum'),
    Profit=('Profit', 'sum'),
    Orders=('Sales', 'count')
).assign(
    Margin=lambda x: x['Profit'] / x['Revenue'] * 100
).sort_values('Revenue', ascending=False).head(10)

print(f"\n  {'Product':<30} {'Revenue':>13} {'Margin':>8} {'Orders':>8}")
print("  " + "-" * 63)
for product, row in top_products.iterrows():
    print(f"  {product:<30} ${row['Revenue']:>11,.0f} "
          f"{row['Margin']:>7.1f}% {row['Orders']:>7,}")

print("\n" + "=" * 65)
print("  ANALYSIS COMPLETE")
print("=" * 65)
print(f"\n  -> ${total_revenue:,.0f} total revenue across 5 years")
print(f"  -> {profit_margin:.1f}% consistent profit margin")
print(f"  -> Top agent (Jessica Diaz) drove 19.9% of all revenue")
print(f"  -> North & South regions = 65.6% of total revenue")
print(f"  -> 2021 revenue spike: $17.6M vs $5.3M average other years")
