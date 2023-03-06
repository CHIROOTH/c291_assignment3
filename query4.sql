SELECT COUNT(DISTINCT Sellers.seller_postal_code)
FROM Customers, Orders, Order_items, Sellers
WHERE Customers.customer_id = Orders.customer_id
AND Orders.order_id = Order_items.order_id
AND Order_items.seller_id = Sellers.seller_id
AND Customers.customer_id = (
    SELECT Customers.customer_id
    FROM Customers, Orders
    WHERE Customers.customer_id = Orders.customer_id
    GROUP BY Customers.customer_id
    HAVING COUNT(DISTINCT Orders.order_id) > 1
    ORDER BY RANDOM()
    LIMIT 1
)
GROUP BY Orders.order_id;
