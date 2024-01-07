# from flask import current_app as app

class Cart_Product: 
    def __init__(self, id, seller_id, seller_name, name, price, quantity):
        # self.pid = pid
        self.id = id
        self.seller_id = seller_id
        self.seller_name = seller_name
        self.name = name
        self.price = price
        self.quantity = quantity 

