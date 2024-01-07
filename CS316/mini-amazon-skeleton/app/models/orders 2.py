from os import name
from flask import current_app as app

class Order:
    def __init__(self, id, product_id, product_name, seller_id, buyer_id, buyer_firstname, buyer_lastname, buyer_addr, price, quantity, status, fulfillment_time):
        self.id = id
        self.product_id = product_id
        self.product_name = product_name,
        self.seller_id = seller_id
        self.buyer_id = buyer_id,
        self.buyer_firstname = buyer_firstname,
        self.buyer_lastname = buyer_lastname,
        self.buyer_addr = buyer_addr,
        self.price = price
        self.quantity = quantity
        self.status = status
        self.fulfillment_time = fulfillment_time
    
    @staticmethod
    def get(seller_id, status):
        try:
            rows = app.db.execute('''
            SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, u.firstname, u.lastname, u.addr, io.price, io.quantity, io.status, io.fulfillment_time
            FROM Items_ordered io, Orders o, Users u, Products p
            WHERE io.seller_id = :seller_id
            AND o.id = io.order_id
            AND io.product_id = p.id
            AND o.uid = u.id
            AND io.status = :status
            ORDER BY io.fulfillment_time DESC
            ''',
                            seller_id = seller_id,
                            status = status)
            return [Order(*row) for row in rows]
        except Exception as e:
            print(e)
            return None 

    @staticmethod
    def getSearch(seller_id, status, oid):
        try:
            rows = app.db.execute('''
            SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, u.firstname, u.lastname, u.addr, io.price, io.quantity, io.status, io.fulfillment_time
            FROM Items_ordered io, Orders o, Users u, Products p
            WHERE io.seller_id = :seller_id
            AND io.order_id = :oid
            AND o.id = io.order_id
            AND io.product_id = p.id
            AND o.uid = u.id
            AND io.status = :status
            ORDER BY io.fulfillment_time DESC
            ''',
                            seller_id = seller_id,
                            status = status,
                            oid=oid)
            return [Order(*row) for row in rows]
        except Exception as e:
            print(e)
            return None 

    @staticmethod
    def getOrder(seller_id, status, order):
        if order == 'p':
            try:
                rows = app.db.execute('''
                SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, u.firstname, u.lastname, u.addr, io.price, io.quantity, io.status, io.fulfillment_time
                FROM Items_ordered io, Orders o, Users u, Products p
                WHERE io.seller_id = :seller_id
                AND o.id = io.order_id
                AND io.product_id = p.id
                AND o.uid = u.id
                AND io.status = :status
                ORDER BY p.name, io.fulfillment_time DESC
                ''',
                                seller_id = seller_id,
                                status = status)
                return [Order(*row) for row in rows]
            except Exception as e:
                print(e)
                return None 
        elif order == 't':
            try:
                rows = app.db.execute('''
                SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, u.firstname, u.lastname, u.addr, io.price, io.quantity, io.status, io.fulfillment_time
                FROM Items_ordered io, Orders o, Users u, Products p
                WHERE io.seller_id = :seller_id
                AND o.id = io.order_id
                AND io.product_id = p.id
                AND o.uid = u.id
                AND io.status = :status
                ORDER BY io.fulfillment_time DESC
                ''',
                                seller_id = seller_id,
                                status = status)
                return [Order(*row) for row in rows]
            except Exception as e:
                print(e)
                return None 
        elif order == 'q':
            try:
                rows = app.db.execute('''
                SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, u.firstname, u.lastname, u.addr, io.price, io.quantity, io.status, io.fulfillment_time
                FROM Items_ordered io, Orders o, Users u, Products p
                WHERE io.seller_id = :seller_id
                AND o.id = io.order_id
                AND io.product_id = p.id
                AND o.uid = u.id
                AND io.status = :status
                ORDER BY io.quantity, io.fulfillment_time DESC
                ''',
                                seller_id = seller_id,
                                status = status)
                return [Order(*row) for row in rows]
            except Exception as e:
                print(e)
                return None 
        elif order == 'b':
            try:
                rows = app.db.execute('''
                SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, u.firstname, u.lastname, u.addr, io.price, io.quantity, io.status, io.fulfillment_time
                FROM Items_ordered io, Orders o, Users u, Products p
                WHERE io.seller_id = :seller_id
                AND o.id = io.order_id
                AND io.product_id = p.id
                AND o.uid = u.id
                AND io.status = :status
                ORDER BY u.firstname, u.lastname, io.fulfillment_time DESC
                ''',
                                seller_id = seller_id,
                                status = status)
                return [Order(*row) for row in rows]
            except Exception as e:
                print(e)
                return None 

            

    @staticmethod
    def fulfill(oid, pid, uid):
        try:
            rows = app.db.execute('''
            UPDATE Items_ordered io
            SET status = :status
            WHERE order_id = :oid
            AND product_id = :pid
            AND seller_id = :uid
            RETURNING status
            ''',
                            status = 1,
                            oid=oid,
                            pid=pid,
                            uid=uid)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def topSellers(sid):
        try:
            rows = app.db.execute('''
            SELECT p.name, SUM(io.quantity)
            FROM Items_ordered io, Products p
            WHERE io.seller_id = :sid
            AND io.product_id = p.id
            GROUP BY p.name
            ORDER BY SUM(io.quantity) DESC
            LIMIT 5
            ''',
                            sid=sid)
            return rows
        except Exception as e:
            print(e)
            return None