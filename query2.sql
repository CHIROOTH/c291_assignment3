-- CREATE VIEW OrderSize (orderid, size)
-- AS SELECT O.order_id, COUNT(DISTINCT Oi1.order_item_id)
-- FROM Orders O, Order_items Oi1
-- WHERE O.order_id = Oi1.order_id
-- GROUP BY Oi1.order_id
-- ;

SELECT COUNT(DISTINCT Oi1.order_id)
FROM Customers C, Orders O, Order_items Oi1
WHERE C.customer_id = O.customer_id
AND O.order_id = Oi1.order_id
AND C.customer_postal_code = (
    SELECT C2.customer_postal_code
    FROM Customers C2
    GROUP BY C2.customer_postal_code
    ORDER BY RANDOM()
)
AND (
SELECT COUNT(Os.size) FROM OrderSize Os) > (SELECT AVG(Os.size) FROM OrderSize Os )
GROUP BY Oi1.order_id
HAVING COUNT(Oi1.order_item_id) > 1
;