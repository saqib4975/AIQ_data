SELECT
    customer_id,
    name,
    username,
    email,
    city,
    SUM(quantity * price) AS total_sales_amount
FROM
    public.user_sales_data usd 
GROUP BY
    customer_id,
    name,
    username,
    email,
    city;

------  Determine the average order quantity per product.---  
  SELECT
    product_id,
    AVG(quantity) AS average_order_quantity
FROM
    public.user_sales_data 
GROUP BY
    product_id;
   
  -------top-selling products
   
   SELECT
    product_id,
    SUM(quantity) AS total_quantity_sold
FROM
    public.user_sales_data
GROUP BY
    product_id
ORDER BY
    total_quantity_sold DESC
LIMIT 5;
------------total_quantity_purchased
SELECT
    customer_id,
    SUM(quantity) AS total_quantity_purchased
FROM
    public.user_sales_data
GROUP BY
    customer_id
ORDER BY
    total_quantity_purchased DESC
LIMIT 5;
-----------------------------monthly_sales
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    SUM(quantity * price) AS monthly_sales
FROM
    public.user_sales_data
GROUP BY
    TO_CHAR(order_date, 'YYYY-MM')
ORDER BY
    TO_CHAR(order_date, 'YYYY-MM');

   ----quarterly_sales 
SELECT
    TO_CHAR(order_date, 'YYYY-Q') AS quarter,
    SUM(quantity * price) AS quarterly_sales
FROM
    public.user_sales_data
GROUP BY
    TO_CHAR(order_date, 'YYYY-Q')
ORDER BY
    TO_CHAR(order_date, 'YYYY-Q');

    ------------
 
===============Aggretive summary 
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_sales,
    AVG(price) AS average_price
FROM
    public.user_sales_data
GROUP BY
    TO_CHAR(order_date, 'YYYY-MM')
ORDER BY
    TO_CHAR(order_date, 'YYYY-MM');


