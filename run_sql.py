
import sqlite3
import pandas as pd

# Read the sales dataset
data = pd.read_csv("retail_sales.csv")

# Create a database and add the data
conn = sqlite3.connect("retail_sales.db")
data.to_sql("retail_sales", conn, if_exists="replace", index=False)

# Ask SQL to calculate sales by product
query = """
SELECT product,
       SUM(units_sold) AS total_units,
       SUM(units_sold * unit_price_inr) AS total_revenue,
       SUM(units_sold * (unit_price_inr - unit_cost_inr)) AS total_profit
FROM retail_sales
GROUP BY product
ORDER BY total_revenue DESC;
"""

result = pd.read_sql_query(query, conn)
print(result.to_string(index=False))

conn.close()
