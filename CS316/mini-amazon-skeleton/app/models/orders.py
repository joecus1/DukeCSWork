from os import name
from flask import current_app as app

class Order:
    def __init__(self, id, product_id, product_name, seller_id, buyer_id, price, quantity, status, fulfillment_time):
        self.id = id
        self.product_id = product_id
        self.product_name = product_name,
        self.seller_id = seller_id
        self.buyer_id = buyer_id,
        self.price = price
        self.quantity = quantity
        self.status = status
        self.fulfillment_time = fulfillment_time
    
    @staticmethod
    def getCurrent(seller_id):
        try:
            rows = app.db.execute('''
            SELECT o.id, io.product_id, p.name, io.seller_id, o.uid, io.price, io.quantity, io.status, io.fulfillment_time
            FROM Items_ordered io, Orders o, Users u, Products p
            WHERE io.seller_id = :seller_id
            AND o.id = io.order_id
            AND io.product_id = p.id
            AND o.uid = u.id
            ''',
                            seller_id = seller_id)
            return [Order(*row) for row in rows]
        except Exception as e:
            print(e)
            return None 