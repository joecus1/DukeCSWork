from flask import current_app as app

from .cart_product import Cart_Product
class Cart:
    def __init__(self, id, pid, quantity):
        self.id = id
        self.pid = pid
        self.quantity = quantity

    @staticmethod
    def get(id):
        try: 
            rows = app.db.execute('''
            SELECT p.id, c.seller_id, CONCAT(u.firstname, u.lastname), p.name, CAST((c.quantity * i.price) AS numeric(36, 2)), c.quantity
            FROM Cart c, Products p, Inventory i, Users u
            WHERE c.id = :id AND c.pid = p.id AND p.id = i.product_id AND c.seller_id = i.seller_id AND c.seller_id = u.id;
            ''',
                                id=id)
            print([Cart_Product(*row) for row in rows])
            #eturn [Product(*row) for row in rows]
            return [Cart_Product(*row) for row in rows] #if rows is not None else None
        except Exception as e: 
            print(e)
            return None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Cart
        ''')
        return [Cart(*row) for row in rows]
    @staticmethod
    def checkIfProductInCart(id, uid, sid):
        try:
            rows = app.db.execute('''
            SELECT * 
            FROM Cart
            WHERE id = :uid AND pid = :pid AND seller_id = :sid
            ''',
                                uid = uid, 
                                pid = id,
                                sid = sid

            )
            if len(rows) == 0:
                return False
            else:
                return True 
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def update_product(id, uid, sid, state):
        try:
            rows = app.db.execute(
                    '''
                    SELECT quantity
                    FROM Cart
                    WHERE id = :uid AND pid = :pid AND seller_id = :sid
                    ''', 
                                        uid = uid,
                                        pid = id,
                                        sid = sid
                    )
            curr_quantity = int(rows[0][0])
            if state == "add":
                new_quantity = curr_quantity + 1
            else:
                new_quantity = curr_quantity - 1
            if new_quantity == 0:
                app.db.execute('''
                DELETE FROM Cart WHERE pid = :pid AND id = :uid AND seller_id = :sid
                ''',
                                                  uid = uid,
                                                  pid = id,
                                                  sid = sid
                )
            else:
                app.db.execute(
                        '''
                        UPDATE Cart
                        SET quantity = :new_quantity
                        WHERE id = :uid AND pid = :pid AND seller_id= :sid

                        ''',
                                        new_quantity = new_quantity,
                                        uid = uid,
                                        pid = id,
                                        sid = sid
                    )
        except Exception as e:
            print(e)

    @staticmethod
    def add_product(id, uid, sid):
        #quantity = request.args.get("quantity")
        try:
            app.db.execute(
                '''
                INSERT INTO Cart VALUES(:uid, :id, :sid, 1)
                ''',                            
                                      id = id, 
                                      uid = uid, 
                                      sid = sid
            )
        except Exception as e:
            print(e)
    @staticmethod
    def remove_product(pid, uid, seller_id):
        try: 
            app.db.execute(
                '''
                DELETE FROM Cart WHERE pid = :pid AND id = :uid AND seller_id = :sid
                ''',
                                                  uid = uid,
                                                  pid = pid, 
                                                  sid = seller_id
            )
        except Exception as e:
            print(e)

    @staticmethod
    def save_for_later(uid, pid, seller_id, quantity):
        try:
            rows = app.db.execute(
                '''
                DELETE FROM Cart c WHERE c.pid = :pid AND c.id = :uid AND c.seller_id = :sid
                RETURNING c.quantity
                ''',
                                                  uid = uid,
                                                  pid = pid, 
                                                  sid = seller_id
            )
            app.db.execute(
                '''
                INSERT INTO Saved_Cart VALUES(:id, :pid, :sid, :quantity)
                ''',
                                id = uid,
                                pid = pid,
                                sid = seller_id,
                                quantity = quantity
            )
        except Exception as e:
            print(e)

    @staticmethod
    def get_saved(uid):
        try:
            rows = app.db.execute('''
            SELECT p.id, s.seller_id, CONCAT(u.firstname, u.lastname), p.name, CAST((s.quantity * i.price) AS numeric(36, 2)), s.quantity
            FROM Saved_Cart s, Products p, Inventory i, Users u
            WHERE s.id = :id AND s.pid = p.id AND p.id = i.product_id AND s.seller_id = i.seller_id AND s.seller_id = u.id;
            ''',
                                id=uid)
            print([Cart_Product(*row) for row in rows])
            #eturn [Product(*row) for row in rows]
            return [Cart_Product(*row) for row in rows] #if rows is not None else None
        except Exception as e: 
            print(e)
            return None
    @staticmethod
    def get_total(uid):
        try: 
            rows = app.db.execute(
                '''
                SELECT CAST(SUM(c.quantity * i.price) as numeric(36,2)) AS total 
                FROM Cart c, Inventory i
                WHERE c.pid = i.product_id AND c.id = :uid AND c.seller_id = i.seller_id
                ''', 
                                                  uid = uid
            )
            return rows[0][0]
        except Exception as e:
            print(e)
    @staticmethod
    def remove_from_saved(uid, pid, sid):
        try: 
            app.db.execute(
                '''
                DELETE FROM Saved_Cart WHERE pid = :pid AND id = :uid AND seller_id = :sid
                ''',
                                                  uid = uid,
                                                  pid = pid, 
                                                  sid = sid
            )
        except Exception as e:
            print(e)

    @staticmethod
    def move_to_cart(uid, pid, sid, quantity):
        try:
            rows = app.db.execute(
                '''
                DELETE FROM Saved_Cart WHERE pid = :pid AND id = :uid AND seller_id = :sid
                RETURNING pid
                ''',
                                                  uid = uid,
                                                  pid = pid, 
                                                  sid = sid
            )
            pid = rows[0][0]
            app.db.execute(
                '''
                INSERT INTO Cart VALUES(:id, :pid, :sid, :quantity)
                ''',
                                id = uid,
                                pid = pid,
                                sid = sid,
                                quantity = quantity
            )
        except Exception as e:
            print(e)


            
                
