import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Connect to database
conn = sqlite3.connect('superstore.db')

# Set style for all charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ============================================
# CHART 1: Sales by Region
# ============================================
query1 = """
    SELECT Region,
           ROUND(SUM(Sales), 2) as Total_Sales
    FROM orders
    GROUP BY Region
    ORDER BY Total_Sales DESC
"""
region_data = pd.read_sql(query1, conn)

plt.figure()
colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
bars = plt.bar(region_data['Region'], 
               region_data['Total_Sales'], 
               color=colors)

# Add value labels on top of each bar
for bar, value in zip(bars, region_data['Total_Sales']):
    plt.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + 5000,
             f'${value:,.0f}', 
             ha='center', fontsize=11, fontweight='bold')

plt.title('Total Sales by Region', fontsize=16, fontweight='bold')
plt.xlabel('Region', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.tight_layout()
plt.savefig('chart1_region_sales.png', dpi=150)
plt.show()
print("Chart 1 saved!")

# ============================================
# CHART 2: Sales by Category
# ============================================
query2 = """
    SELECT Category,
           ROUND(SUM(Sales), 2) as Total_Sales
    FROM orders
    GROUP BY Category
    ORDER BY Total_Sales DESC
"""
category_data = pd.read_sql(query2, conn)

plt.figure()
colors2 = ['#9b59b6', '#1abc9c', '#e67e22']
bars2 = plt.bar(category_data['Category'],
                category_data['Total_Sales'],
                color=colors2)

for bar, value in zip(bars2, category_data['Total_Sales']):
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 5000,
             f'${value:,.0f}',
             ha='center', fontsize=11, fontweight='bold')

plt.title('Total Sales by Category', fontsize=16, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
plt.tight_layout()
plt.savefig('chart2_category_sales.png', dpi=150)
plt.show()
print("Chart 2 saved!")

# ============================================
# CHART 3: Monthly Sales Trend
# ============================================
# Recreate Month and Year columns
df = pd.read_sql("SELECT * FROM orders", conn)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')
df['Month'] = df['Order Date'].dt.month
df['Year'] = df['Order Date'].dt.year
df.to_sql('orders', conn, if_exists='replace', index=False)
print("Month and Year columns added")

query3 = """
    SELECT Year, Month,
           ROUND(SUM(Sales), 2) as Monthly_Sales
    FROM orders
    GROUP BY Year, Month
    ORDER BY Year, Month
"""
monthly_data = pd.read_sql(query3, conn)

# Create Year-Month label
monthly_data['Period'] = monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str).str.zfill(2)

plt.figure(figsize=(16, 6))
plt.plot(monthly_data['Period'], 
         monthly_data['Monthly_Sales'],
         color='#2980b9', linewidth=2.5,
         marker='o', markersize=4)

# Highlight November peaks
for _, row in monthly_data[monthly_data['Month'] == 11].iterrows():
    plt.annotate('Nov Peak', 
                xy=(row['Period'], row['Monthly_Sales']),
                xytext=(0, 15), textcoords='offset points',
                ha='center', fontsize=9,
                color='red', fontweight='bold')

plt.title('Monthly Sales Trend 2015-2018', fontsize=16, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Monthly Sales ($)', fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('chart3_monthly_trend.png', dpi=150)
plt.show()
print("Chart 3 saved!")


# ============================================
# CHART 4: Top 10 Customers
# ============================================
query4 = """
    SELECT "Customer Name",
           ROUND(SUM(Sales), 2) as Total_Sales
    FROM orders
    GROUP BY "Customer Name"
    ORDER BY Total_Sales DESC
    LIMIT 10
"""
top_customers = pd.read_sql(query4, conn)

plt.figure(figsize=(12, 6))
bars4 = plt.barh(top_customers['Customer Name'],
                 top_customers['Total_Sales'],
                 color='#2ecc71')

for bar, value in zip(bars4, top_customers['Total_Sales']):
    plt.text(bar.get_width() + 200,
             bar.get_y() + bar.get_height()/2,
             f'${value:,.0f}',
             va='center', fontsize=10, fontweight='bold')

plt.title('Top 10 Customers by Sales', fontsize=16, fontweight='bold')
plt.xlabel('Total Sales ($)', fontsize=12)
plt.ylabel('Customer Name', fontsize=12)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('chart4_top_customers.png', dpi=150)
plt.show()
print("Chart 4 saved!")