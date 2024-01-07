from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased, name, price, quantity, status):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
FROM Items_ordered i, Orders o, Products p
WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
FROM Items_ordered i, Orders o, Products p
WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid_sort(uid, since, order):
        if order == 'n':
            try:
                rows = app.db.execute('''
                SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
                FROM Items_ordered i, Orders o, Products p
                WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
                AND time_purchased >= :since
                ORDER BY p.name
                ''',
                              uid=uid,
                              since=since)
                return [Purchase(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'timeD':
            try:
                rows = app.db.execute('''
                SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
                FROM Items_ordered i, Orders o, Products p
                WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
                AND time_purchased >= :since
                ORDER BY time_purchased DESC
                ''',
                              uid=uid,
                              since=since)
                return [Purchase(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'timeA':
            try:
                rows = app.db.execute('''
                SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
                FROM Items_ordered i, Orders o, Products p
                WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
                AND time_purchased >= :since
                ORDER BY time_purchased
                ''',
                              uid=uid,
                              since=since)
                return [Purchase(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'priceL':
            try:
                rows = app.db.execute('''
                SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
                FROM Items_ordered i, Orders o, Products p
                WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
                AND time_purchased >= :since
                ORDER BY i.price
                ''',
                              uid=uid,
                              since=since)
                return [Purchase(*row) for row in rows]
            except Exception as e:
                print(e)
                return None
        elif order == 'priceH':
            try:
                rows = app.db.execute('''
                SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
                FROM Items_ordered i, Orders o, Products p
                WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
                AND time_purchased >= :since
                ORDER BY i.price DESC
                ''',
                              uid=uid,
                              since=since)
                return [Purchase(*row) for row in rows]
            except Exception as e:
                print(e)
                return None

    @staticmethod
    def get_all_by_uid_search(uid, since, search):
        rows = app.db.execute('''
SELECT o.id, o.uid, i.product_id, o.time_purchased, p.name, i.price, i.quantity, i.status
FROM Items_ordered i, Orders o, Products p
WHERE o.id = i.order_id AND uid = :uid AND i.product_id = p.id
AND time_purchased >= :since AND p.name LIKE '%' || :search || '%'
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since,
                              search=search)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def place_order(uid):
        try:
            cost = app.db.execute(
                '''
                SELECT SUM(c.quantity * i.price) AS total 
                FROM Cart c, Inventory i
                WHERE c.pid = i.product_id AND c.seller_id = i.seller_id AND c.id = :uid;
                ''', 
                                                  uid = uid
            )
            totalcost = float(cost[0][0])
            balance = app.db.execute(
                '''
                SELECT balance FROM Users WHERE id = :uid
                ''', 
                                                  uid = uid
            )
            balance = float(balance[0][0])
            items = app.db.execute(
                '''
                SELECT c.pid, c.seller_id, c.quantity, i.price
                FROM Cart c, Inventory i
                WHERE id = :uid AND c.pid = i.product_id AND c.seller_id = i.seller_id
                ''',
                                        uid = uid
            )
            for item in items:
                pid = item[0]
                seller_id = item[1]
                quant = int(item[2])
                price = float(item[3])
                total_price = float(price * quant)
                rows = app.db.execute(
                    '''
                    UPDATE Inventory
                    SET quantity = quantity - :quant
                    WHERE product_id = :pid AND seller_id = :seller_id
                    RETURNING product_id
                    ''',
                                        pid = pid,
                                        seller_id = seller_id,
                                        quant = quant
                )
                rows1 = app.db.execute(
                    '''
                    UPDATE Users
                    SET balance = balance + :total_price
                    WHERE id = :seller_id
                    RETURNING id
                    ''',
                                        seller_id = seller_id,
                                        total_price = total_price
                )
            if balance >= totalcost:
                removeBalance = app.db.execute('''
                    UPDATE Users
                    SET balance = :new_balance
                    WHERE id = :uid
                    RETURNING balance
                
                ''', 
                                                  new_balance = balance - totalcost,
                                                  uid = uid
                
                )
                generateID = app.db.execute('''
                SELECT COUNT(id) FROM Orders
                ''')
                order_id = int(generateID[0][0]) + 1
                rows = app.db.execute('''
                INSERT INTO ORDERS(id, uid)
                VALUES(:id, :uid)
                RETURNING id
                ''',
                                                    id = order_id,
                                                    uid = uid
                )
                id = rows[0][0]
                rows = app.db.execute('''
                INSERT INTO Items_Ordered(order_id, product_id, seller_id, price, quantity, status)
                SELECT :order_id, c.pid, c.seller_id, i.price, c.quantity, :status
                FROM Inventory i, Cart c
                WHERE c.id = :uid AND c.pid = i.product_id AND c.seller_id = i.seller_id
                RETURNING order_id
                ''',
                                                    uid = uid,
                                                    order_id = id,
                                                    status = 0
                )

                app.db.execute('''
                DELETE FROM Cart WHERE id = :uid
                ''',
                                                    uid = uid
                )
        except Exception as e:
            print(e)
    @staticmethod
    def can_place_order(uid):
        try: 
            cost = app.db.execute(
                '''
                SELECT SUM(c.quantity * i.price) AS total 
                FROM Cart c, Inventory i
                WHERE c.pid = i.product_id AND c.seller_id = i.seller_id AND c.id = :uid;
                ''', 
                                                  uid = uid
            )
            totalcost = float(cost[0][0])
            balance = app.db.execute(
                '''
                SELECT balance FROM Users WHERE id = :uid
                ''', 
                                                  uid = uid
            )
            balance = float(balance[0][0])
            if balance >= totalcost:
                return True
            else:
                return False 
        except Exception as e:
                print(e)
