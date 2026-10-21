
-- 1. Create a table for retail sales
CREATE TABLE retail_sales (
    sale_date DATE,
    region VARCHAR(20),
    category VARCHAR(30),
    product VARCHAR(50),
    units_sold INT,
    unit_price DECIMAL(10,2),
    unit_cost DECIMAL(10,2)
);

-- 2. Calculate revenue and profit by product
SELECT
    product,
    SUM(units_sold) AS total_units,
    SUM(units_sold * unit_price) AS total_revenue,
    SUM(units_sold * (unit_price - unit_cost)) AS total_profit
FROM retail_sales
GROUP BY product
ORDER BY total_revenue DESC;

-- 3. Compare revenue by region
SELECT
    region,
    SUM(units_sold * unit_price) AS revenue
FROM retail_sales
GROUP BY region
ORDER BY revenue DESC;

-- 4. Compare category performance
SELECT
    category,
    SUM(units_sold) AS units_sold,
    SUM(units_sold * unit_price) AS revenue
FROM retail_sales
GROUP BY category
ORDER BY revenue DESC;

-- 5. Monthly revenue trend (SQLite)
SELECT
    strftime('%Y-%m', sale_date) AS month,
    SUM(units_sold * unit_price) AS monthly_revenue
FROM retail_sales
GROUP BY month
ORDER BY month;
