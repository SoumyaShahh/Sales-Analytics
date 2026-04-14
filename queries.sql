-- ============================================================
-- Store Sales Performance Analysis — SQL Queries
-- San Martin Stores | Author: Soumya Shah
-- ============================================================


-- ============================================================
-- 1. OVERALL KPIs
-- ============================================================
SELECT
    COUNT(*)                                AS total_orders,
    ROUND(SUM(Sales), 2)                   AS total_revenue,
    ROUND(SUM(Profit), 2)                  AS total_profit,
    ROUND(SUM(Cost), 2)                    AS total_cost,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS profit_margin_pct,
    ROUND(AVG(Sales), 2)                   AS avg_order_value,
    ROUND(AVG(DATEDIFF(Shipping_Date, Order_Date)), 1) AS avg_shipping_days
FROM sales;


-- ============================================================
-- 2. REVENUE & PROFIT BY REGION
-- ============================================================
SELECT
    l.Region,
    COUNT(*)                                    AS total_orders,
    ROUND(SUM(s.Sales), 0)                      AS revenue,
    ROUND(SUM(s.Profit), 0)                     AS profit,
    ROUND(SUM(s.Profit) / SUM(s.Sales) * 100, 1) AS margin_pct,
    ROUND(SUM(s.Sales) / SUM(SUM(s.Sales)) OVER () * 100, 1) AS revenue_share_pct
FROM sales s
JOIN locations l ON s.Region_Key = l.Region_Key
GROUP BY l.Region
ORDER BY revenue DESC;


-- ============================================================
-- 3. SALES AGENT PERFORMANCE RANKING
-- ============================================================
SELECT
    a.Sales_Agent_Name,
    COUNT(*)                                        AS total_orders,
    ROUND(SUM(s.Sales), 0)                          AS revenue,
    ROUND(SUM(s.Profit), 0)                         AS profit,
    ROUND(SUM(s.Profit) / SUM(s.Sales) * 100, 1)   AS margin_pct,
    ROUND(SUM(s.Sales) / SUM(SUM(s.Sales)) OVER () * 100, 1) AS revenue_share_pct,
    RANK() OVER (ORDER BY SUM(s.Sales) DESC)        AS revenue_rank
FROM sales s
JOIN sales_agents a ON s.Sales_Agent_Key = a.Sales_Agent_Key
GROUP BY a.Sales_Agent_Name
ORDER BY revenue DESC;


-- ============================================================
-- 4. PRODUCT CATEGORY PERFORMANCE
-- ============================================================
SELECT
    p.Products_Category,
    COUNT(*)                                        AS total_orders,
    ROUND(SUM(s.Sales), 0)                          AS revenue,
    ROUND(SUM(s.Profit), 0)                         AS profit,
    ROUND(SUM(s.Profit) / SUM(s.Sales) * 100, 1)   AS margin_pct,
    ROUND(AVG(s.Sales), 2)                          AS avg_order_value,
    RANK() OVER (ORDER BY SUM(s.Profit) DESC)       AS profit_rank
FROM sales s
JOIN products p ON s.Product_Key = p.Product_Key
GROUP BY p.Products_Category
ORDER BY revenue DESC;


-- ============================================================
-- 5. YEARLY REVENUE TREND WITH YoY GROWTH
-- ============================================================
WITH yearly_sales AS (
    SELECT
        YEAR(Order_Date)            AS year,
        ROUND(SUM(Sales), 0)        AS revenue,
        ROUND(SUM(Profit), 0)       AS profit,
        COUNT(*)                    AS orders,
        ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS margin_pct
    FROM sales
    GROUP BY YEAR(Order_Date)
)
SELECT
    year,
    revenue,
    profit,
    orders,
    margin_pct,
    LAG(revenue) OVER (ORDER BY year)  AS prev_year_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year))
        / LAG(revenue) OVER (ORDER BY year) * 100, 1
    )                                  AS yoy_growth_pct
FROM yearly_sales
ORDER BY year;


-- ============================================================
-- 6. MONTHLY REVENUE TREND
-- ============================================================
SELECT
    YEAR(Order_Date)    AS year,
    MONTH(Order_Date)   AS month,
    MONTHNAME(Order_Date) AS month_name,
    ROUND(SUM(Sales), 0)  AS revenue,
    ROUND(SUM(Profit), 0) AS profit,
    COUNT(*)              AS orders
FROM sales
GROUP BY YEAR(Order_Date), MONTH(Order_Date), MONTHNAME(Order_Date)
ORDER BY year, month;


-- ============================================================
-- 7. TOP 10 PRODUCTS BY REVENUE
-- ============================================================
SELECT
    p.Products                                      AS product_name,
    p.Products_Category                             AS category,
    COUNT(*)                                        AS orders,
    ROUND(SUM(s.Sales), 0)                          AS revenue,
    ROUND(SUM(s.Profit), 0)                         AS profit,
    ROUND(SUM(s.Profit) / SUM(s.Sales) * 100, 1)   AS margin_pct
FROM sales s
JOIN products p ON s.Product_Key = p.Product_Key
GROUP BY p.Products, p.Products_Category
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 8. HIGH VALUE CUSTOMERS (TOP 20 BY LIFETIME VALUE)
-- ============================================================
SELECT
    c.Customers                                     AS customer_name,
    COUNT(*)                                        AS total_orders,
    ROUND(SUM(s.Sales), 0)                          AS lifetime_value,
    ROUND(AVG(s.Sales), 0)                          AS avg_order_value,
    ROUND(SUM(s.Profit), 0)                         AS total_profit,
    RANK() OVER (ORDER BY SUM(s.Sales) DESC)        AS value_rank
FROM sales s
JOIN customers c ON s.Customer_Key = c.Customer_Key
GROUP BY c.Customers
ORDER BY lifetime_value DESC
LIMIT 20;


-- ============================================================
-- 9. SHIPPING EFFICIENCY ANALYSIS
-- ============================================================
SELECT
    l.Region,
    ROUND(AVG(DATEDIFF(s.Shipping_Date, s.Order_Date)), 1) AS avg_shipping_days,
    MIN(DATEDIFF(s.Shipping_Date, s.Order_Date))           AS min_shipping_days,
    MAX(DATEDIFF(s.Shipping_Date, s.Order_Date))           AS max_shipping_days,
    COUNT(*)                                               AS total_orders
FROM sales s
JOIN locations l ON s.Region_Key = l.Region_Key
WHERE s.Shipping_Date IS NOT NULL
GROUP BY l.Region
ORDER BY avg_shipping_days;


-- ============================================================
-- 10. AGENT PERFORMANCE BY REGION (Cross-analysis)
-- ============================================================
SELECT
    a.Sales_Agent_Name,
    l.Region,
    COUNT(*)                                        AS orders,
    ROUND(SUM(s.Sales), 0)                          AS revenue,
    ROUND(SUM(s.Profit) / SUM(s.Sales) * 100, 1)   AS margin_pct
FROM sales s
JOIN sales_agents a ON s.Sales_Agent_Key = a.Sales_Agent_Key
JOIN locations l ON s.Region_Key = l.Region_Key
GROUP BY a.Sales_Agent_Name, l.Region
ORDER BY a.Sales_Agent_Name, revenue DESC;


-- ============================================================
-- 11. QUARTERLY PERFORMANCE BREAKDOWN
-- ============================================================
SELECT
    YEAR(Order_Date)     AS year,
    QUARTER(Order_Date)  AS quarter,
    ROUND(SUM(Sales), 0) AS revenue,
    ROUND(SUM(Profit), 0) AS profit,
    COUNT(*)              AS orders,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 1) AS margin_pct
FROM sales
GROUP BY YEAR(Order_Date), QUARTER(Order_Date)
ORDER BY year, quarter;


-- ============================================================
-- 12. PROFIT MARGIN OUTLIERS — BELOW AVERAGE PERFORMING STORES
-- ============================================================
WITH store_perf AS (
    SELECT
        st.Store_Name,
        ROUND(SUM(s.Sales), 0)                          AS revenue,
        ROUND(SUM(s.Profit) / SUM(s.Sales) * 100, 1)   AS margin_pct,
        COUNT(*)                                         AS orders
    FROM sales s
    JOIN stores st ON s.Store_Key = st.Store_Key
    GROUP BY st.Store_Name
),
avg_margin AS (
    SELECT ROUND(AVG(margin_pct), 1) AS avg_margin FROM store_perf
)
SELECT
    sp.Store_Name,
    sp.revenue,
    sp.margin_pct,
    am.avg_margin,
    ROUND(sp.margin_pct - am.avg_margin, 1) AS margin_gap
FROM store_perf sp
CROSS JOIN avg_margin am
WHERE sp.margin_pct < am.avg_margin
ORDER BY margin_gap ASC
LIMIT 10;
