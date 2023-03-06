SELECT COUNT(DISTINCT Orders.order_id)
FROM Customers, Orders, Order_items
WHERE Customers.customer_id = Orders.customer_id
AND Orders.order_id = Order_items.order_id
AND Customers.customer_postal_code = [random postal code]
AND Orders.order_id IN (
    SELECT Order_items.order_id
    FROM Order_items
    GROUP BY Order_items.order_id
    HAVING COUNT(DISTINCT Order_items.order_item_id) > 1
)
AND Orders.order_id IN (
    SELECT Orders.order_id
    FROM Order_items, Orders
    WHERE Order_items.order_id = Orders.order_id
    GROUP BY Orders.order_id
    HAVING COUNT(DISTINCT Order_items.order_item_id) > (
        SELECT AVG(size)
        FROM (
            SELECT Orders.order_id, COUNT(*) AS size
            FROM Order_items, Orders
            WHERE Order_items.order_id = Orders.order_id
            GROUP BY Orders.order_id
        )
    )
);
