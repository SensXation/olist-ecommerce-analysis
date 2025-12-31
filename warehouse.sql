-- 1. Drop the table if it already exists (so we can re-run this script safely)
DROP TABLE IF EXISTS analytics_orders;

-- 2. Create the Master Table using a Complex Join
CREATE TABLE analytics_orders AS
SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_timestamp,
    
    -- Customer Info (Joined from customers table)
    c.customer_city,
    c.customer_state,
    
    -- Payment Info (Joined from payments table)
    -- Note: We use aggregation here because one order can have multiple payments
    -- (e.g. part credit card, part voucher). We want the TOTAL amount per order.
    SUM(p.payment_value) as total_order_value,
    STRING_AGG(DISTINCT p.payment_type, ', ') as payment_types
    
FROM orders o

-- Join Customers to get location
LEFT JOIN customers c 
    ON o.customer_id = c.customer_id

-- Join Payments to get money info
LEFT JOIN order_payments p
    ON o.order_id = p.order_id

WHERE 
    o.order_status = 'delivered' -- We only care about completed orders

GROUP BY 
    o.order_id, 
    o.customer_id, 
    o.order_status, 
    o.order_purchase_timestamp, 
    c.customer_city, 
    c.customer_state;

-- 3. Verify it worked by selecting the first 5 rows
SELECT * FROM analytics_orders LIMIT 5;