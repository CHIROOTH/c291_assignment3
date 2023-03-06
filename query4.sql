SELECT COUNT(DISTINCT Sellers.seller_postal_code)
FROM Orders
JOIN Customers ON Customers.customer_id = Orders.customer_id
JOIN Order_items ON Orders.order_id = Order_items.order_id
JOIN Sellers ON Order_items.seller_id = Sellers.seller_id
WHERE Customers.customer_id IN (
    SELECT Orders.customer_id 
    FROM (
        SELECT customer_id, COUNT(DISTINCT order_item_id) AS item_count
        FROM Orders 
        JOIN Order_items ON Orders.order_id = Order_items.order_id
        GROUP BY customer_id
        HAVING item_count > 1
    ) AS multi_item_customers
)
GROUP BY Orders.order_id;
