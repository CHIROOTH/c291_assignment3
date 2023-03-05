import sqlite3
import pandas as pd

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()


def drop_tables():
    global connection, cursor
    
    drop_Customers_table = """
        DROP TABLE IF EXISTS Customers;
    """

    drop_Sellers_table = """
        DROP TABLE IF EXISTS Sellers;
    """ 

    drop_Orders_table = """
        DROP TABLE IF EXISTS Orders;
    """

    drop_Order_items_table = """
        DROP TABLE IF EXISTS Order_items;
    """

    cursor.execute(drop_Customers_table)
    cursor.execute(drop_Sellers_table)
    cursor.execute(drop_Orders_table)
    cursor.execute(drop_Order_items_table)



def create_tables():
    global connection, cursor

    Customers_table = """
        CREATE TABLE "Customers"(
        "customer_id" TEXT,
        "customer_postal_code" INTEGER,
        PRIMARY KEY ("customer_id")
        );
        """

    Sellers_table = """
        CREATE TABLE "Sellers"(
        "seller_id" TEXT,
        "seller_postal_code" INTEGER,
        PRIMARY KEY ("seller_id")
        );
        """

    Orders_table = """
        CREATE TABLE "Orders" (
        "order_id" TEXT,
        "customer_id" TEXT,
        PRIMARY KEY("order_id"),
        FOREIGN KEY("customer_id") REFERENCES "Customers"("customer_id")
        );
        """

    Order_items_table =  """
        CREATE TABLE "Order_items" (
        "order_id" TEXT,
        "order_item_id" INTEGER,
        "product_id" TEXT,
        "seller_id" TEXT,
        PRIMARY KEY("order_id","order_item_id","product_id","seller_id"),
        FOREIGN KEY("seller_id") REFERENCES "Sellers"("seller_id")
        FOREIGN KEY("order_id") REFERENCES "Orders"("order_id")
        );
        """

    cursor.execute(Customers_table)
    cursor.execute(Sellers_table)
    cursor.execute(Orders_table)
    cursor.execute( Order_items_table)

    connection.commit()

    return


#insert data into Customers
def insert_data_Customers(n):
    global connection, cursor

    data = pd.read_csv('olist_customers_dataset.csv')
    df = pd.DataFrame(data)
    shuffled_df = df.sample(frac=1)

    count = 0
    for row in shuffled_df.itertuples():
        if count <= n:
            cursor.execute("""
                INSERT INTO Customers (customer_id, customer_postal_code)
                VALUES (?, ?)
                """,
                (row.customer_id, row.customer_zip_code_prefix)
                )
            count = count + 1
        else:
            break

    connection.commit()

    return


#insert data into Sellers
def insert_data_Sellers(n):
    global connection, cursor

    data = pd.read_csv('olist_sellers_dataset.csv')
    df = pd.DataFrame(data)
    shuffled_df = df.sample(frac=1)

    count = 0
    for row in shuffled_df.itertuples():
        if count <= n:
            cursor.execute("""
            INSERT INTO Sellers (seller_id, seller_postal_code)
            VALUES (?, ?)
            """,
            (row.seller_id, row.seller_zip_code_prefix)
            )
            count = count + 1
        else:
            break

    connection.commit()

    return


#insert data into Orders
def insert_data_Orders(n):
    global connection, cursor

    data = pd.read_csv('olist_orders_dataset.csv')
    df = pd.DataFrame(data)

    shuffled_df = df.sample(frac=1)

    count = 0
    for row in shuffled_df.itertuples():
        if count <= n:
            try:
                cursor.execute("""
                INSERT INTO Orders (order_id, customer_id)
                VALUES (?, ?)
                """,
                (row.order_id, row.customer_id)
                )
                count = count + 1
            except:
                pass
        else:
            break

    connection.commit()

    return


#insert data into Order_items
def insert_data_Order_items(n):
    global connection, cursor

    data = pd.read_csv('olist_order_items_dataset.csv')
    df = pd.DataFrame(data)

    shuffled_df = df.sample(frac=1)

    count = 0
    for row in shuffled_df.itertuples():
        if count <= n:
            try:
                cursor.execute("""
                INSERT INTO Order_items (order_id, order_item_id, product_id, seller_id)
                VALUES (?, ?, ?, ?)
                """,
                (row.order_id, row.order_item_id, row.product_id, row.seller_id)
                )
                count = count + 1
            except:
                pass
        else:
            break

    connection.commit()

    return


def database(name, customers, sellers, orders, order_items):
    connect(name)
    drop_tables()
    create_tables()
    insert_data_Customers(customers)
    insert_data_Sellers(sellers)
    insert_data_Orders(orders)
    insert_data_Order_items(order_items)

    # print(connection)

    return


def main():
    database("A3Small.db", 10000, 500, 10000, 2000)
    database("A3Medium.db", 20000, 750, 20000, 4000)
    database("A3Large.db", 33000, 1000, 33000, 10000)

if __name__ == '__main__':
    main()

