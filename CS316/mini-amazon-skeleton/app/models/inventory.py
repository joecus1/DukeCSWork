from flask import current_app as app
from .seller import Seller
class Inventory:
    def __init__(self, seller_id, product_id, quantity, product_name, price):
        self.seller_id = seller_id,
        self.product_id = product_id,
        self.quantity = quantity,
        self.product_name = product_name,
        self.price = price,

    # gets inventory based off seller's id
    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
SELECT Inventory.seller_id, Inventory.product_id, Inventory.quantity, Products.name, Inventory.price
FROM Inventory, Products
WHERE Inventory.seller_id = :seller_id
AND Products.id = Inventory.product_id
''',
                              seller_id=seller_id)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def getSearch(seller_id, pid):
        try:
            rows = app.db.execute('''
            SELECT Inventory.seller_id, Inventory.product_id, Inventory.quantity, Products.name, Inventory.price
            FROM Inventory, Products
            WHERE Inventory.seller_id = :seller_id
            AND Products.id = Inventory.product_id
            AND Products.id = :pid
            ORDER BY Inventory.product_id
            ''',
                            seller_id = seller_id,
                            pid=pid)
            return [Inventory(*row) for row in rows]
        except Exception as e:
            print(e)
            return None 


    @staticmethod
    def getOrder(seller_id, order):
        if order == 'p':
            try:
                rows = app.db.execute('''
                SELECT Inventory.seller_id, Inventory.product_id, Inventory.quantity, Products.name, Inventory.price
                FROM Inventory, Products
                WHERE Inventory.seller_id = :seller_id
                AND Products.id = Inventory.product_id
                ORDER BY Inventory.product_id
                ''',
                                seller_id = seller_id)
                return [Inventory(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'n':
            try:
                rows = app.db.execute('''
                SELECT Inventory.seller_id, Inventory.product_id, Inventory.quantity, Products.name, Inventory.price
                FROM Inventory, Products
                WHERE Inventory.seller_id = :seller_id
                AND Products.id = Inventory.product_id
                ORDER BY Products.name
                ''',
                                seller_id = seller_id)
                return [Inventory(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'q':
            try:
                rows = app.db.execute('''
                SELECT Inventory.seller_id, Inventory.product_id, Inventory.quantity, Products.name, Inventory.price
                FROM Inventory, Products
                WHERE Inventory.seller_id = :seller_id
                AND Products.id = Inventory.product_id
                ORDER BY Inventory.quantity
                ''',
                                seller_id = seller_id)
                return [Inventory(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'pr':
            try:
                rows = app.db.execute('''
                SELECT Inventory.seller_id, Inventory.product_id, Inventory.quantity, Products.name, Inventory.price
                FROM Inventory, Products
                WHERE Inventory.seller_id = :seller_id
                AND Products.id = Inventory.product_id
                ORDER BY Inventory.price
                ''',
                                seller_id = seller_id)
                return [Inventory(*row) for row in rows]
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def add(seller_id, product_id, price, quantity):
        try:
            rows = app.db.execute("""
            INSERT INTO Inventory(seller_id, product_id, price, quantity)
            VALUES(:seller_id, :product_id, :price, :quantity)
            RETURNING product_id""",
                seller_id=seller_id,
                product_id=product_id,
                price=price,
                quantity=quantity)
            return True if rows else False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def editQuantity(seller_id, product_id, quantity):
        try:
            rows = app.db.execute("""
            UPDATE Inventory
            SET quantity = :quantity
            WHERE product_id = :product_id
            AND seller_id = :seller_id
            RETURNING product_id""",
                seller_id=seller_id,
                product_id=product_id,
                quantity=quantity)
            return True if rows else False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def editPrice(seller_id, product_id, price):
        try:
            rows = app.db.execute("""
            UPDATE Inventory
            SET price = :price
            WHERE product_id = :product_id
            AND seller_id = :seller_id
            RETURNING product_id""",
                seller_id=seller_id,
                product_id=product_id,
                price=price)
            return True if rows else False
        except Exception as e:
            print(e)
            return False
    
    @staticmethod
    def getPID(uid):
        try:
            rows = app.db.execute("""
            SELECT product_id
            FROM Inventory
            WHERE seller_id = :uid
            """,
                uid = uid)
            return rows if rows else None
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_seller_info(pid):
        try:
            rows = app.db.execute('''
            SELECT i.seller_id, i.product_id, u.firstname, u.lastname, i.price 
            FROM Inventory i, Users u
            WHERE i.product_id = :pid AND i.seller_id = u.id AND i.quantity > 0
            ''',
                            pid = pid)
            return [Seller(*row) for row in rows]
        except Exception as e:
            print(e)
            return [] 

    @staticmethod
    def removeInventory(seller_id, product_id):
        try:
            rows = app.db.execute("""
            DELETE FROM INVENTORY
            WHERE seller_id = :seller_id
            AND product_id = :product_id""",
                seller_id=seller_id,
                product_id=product_id)
            return True if rows else False
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def enough_for_order(uid):
        enough = True
        items = app.db.execute(
            '''
            SELECT pid, seller_id, quantity
            FROM Cart
            WHERE id = :uid
            ''',
                                    uid = uid
        )
        for item in items:
            pid = item[0]
            seller_id = item[1]
            quant = item[2]
            rows = app.db.execute(
                '''
                SELECT quantity FROM Inventory WHERE product_id = :pid AND seller_id = :seller_id
                ''',
                                    pid = pid,
                                    seller_id = seller_id
            )
            actual_quant = int(rows[0][0])
            if actual_quant < quant:
                enough = False
        return enough



        
        