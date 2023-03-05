SELECT Oi1.order_id
FROM Customers C, Orders O, Order_items Oi1
WHERE C.customer_id = O.customer_id
AND O.order_id = Oi1.order_id
AND C.customer_postal_code = (
    SELECT C2.customer_postal_code
    FROM Customers C2 LIMIT 1
    ORDER BY RANDOM()

)
GROUP BY Oi1.order_id
HAVING COUNT(Oi1.order_item_id) > 1
;
