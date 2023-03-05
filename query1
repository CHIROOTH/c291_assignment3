SELECT Oi1.order_id
FROM Customers C, Orders O, Order_items Oi1
WHERE C.customer_id = O.customer_id
AND O.order_id = Oi1.order_id
AND C.customer_postal_code = (?)
GROUP BY Oi1.order_id
HAVING COUNT(Oi1.order_item_id) > 1
-- ? - is some postal code which is given 
