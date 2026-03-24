import pandas as pd 
import sqlite3

df = pd.read_csv(r'C:\Users\HP\Desktop\superstore_data\train.csv')

#connect database
conn = sqlite3.connect("superstore.db")

#store data in table 


print("Total Rows and Columns:", df.shape)
print("\nColumn Names:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print(df.info())

df.to_sql('orders', conn, if_exists= 'replace', index = False)
print("Data loaded into database")
print("Total records in database:")
results = pd.read_sql("select count(*) as total_records from orders", conn)
print(results)

# qyery 1 : which region makes most money
print("\n query 1 : sales by region")
query1 = """
    SELECT Region,
           ROUND(SUM(Sales), 2) as Total_Sales,
           ROUND(AVG(Sales), 2) as Avg_Order_Value,
           COUNT(Region) as Total_Orders
    FROM orders
    GROUP BY Region
    ORDER BY Total_Sales DESC
"""
result1 = pd.read_sql(query1,conn)
print(result1)

print(df.columns.tolist())

# Fix column datatype
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

# Reload into SQLite with fixed datatypes
df.to_sql('orders', conn, if_exists='replace', index=False)
print("Data reloaded with fixed datatypes")

#query 2 : profit by category
print("\n query2:profit by category")
query2 = """
    SELECT Category,
           ROUND(SUM(Sales), 2) as Total_Sales,
           ROUND(AVG(Sales), 2) as Avg_Sales,
           COUNT(Category) as Total_Orders
    FROM orders
    GROUP BY Category
    ORDER BY Total_Sales DESC

"""
result2 = pd.read_sql(query2,conn)
print(result2)

# query3 monthly sales trend
print("\n Query3: monthly sales trend")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Month']= df['Order Date'].dt.month
df['Year']=df['Order Date'].dt.year
df.to_sql('orders', conn, if_exists='replace',index=False)

query3 = """
  select Year,
  Month,
  Round(sum(Sales),2)as Monthly_Sales,
  count("Order ID") as Total_Oders
from orders
group by Year, Month
order by Year,Month
"""
result3 = pd.read_sql(query3,conn)
print(result3)

#query4 : top 10 customers by sale
print("\n query4:top 10 customers by sale")
query4 = """select "Customer Name",
                "Customer ID",
                Segment,
                Round(sum("Sales"),2) as Total_Sales,
                count("Order ID") as Total_Orders
            from orders
            group by "Customer ID"
            order by Total_Sales DESC
            limit 10
        """
result4 = pd.read_sql(query4,conn)

print(result4)

#query5
print("\nquery5 : top and bottom sub category")
query5 = """
      select "Sub-Category",
      round(sum("Sales"),2) as Total_Sales,
      round(avg("Sales"),2) as Avg_Sales,
      Count("Order ID") as Total_Orders
     from orders
     group by "Sub-Category"
     order by Total_Sales desc
     """
result5 = pd.read_sql(query5, conn)
print(result5)
