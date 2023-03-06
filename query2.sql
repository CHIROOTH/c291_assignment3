CREATE VIEW OrderSize AS
SELECT order_id AS oid, COUNT(*) AS size
FROM Order_items
GROUP BY order_id;

SELECT COUNT(DISTINCT Orders.order_id)
FROM Orders
WHERE Orders.customer_id IN (
    SELECT Customers.customer_id
    FROM Customers
    WHERE Customers.customer_postal_code = [random postal code]
)
AND Orders.order_id IN (
    SELECT Order_items.order_id
    FROM Order_items
    GROUP BY Order_items.order_id
    HAVING COUNT(DISTINCT Order_items.order_item_id) > 1
)
AND Orders.order_id IN (
    SELECT OrderSize.oid
    FROM OrderSize
    WHERE OrderSize.size > (
        SELECT AVG(size)
        FROM OrderSize
    )
);
