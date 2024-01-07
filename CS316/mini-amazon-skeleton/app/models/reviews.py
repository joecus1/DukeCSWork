from flask import current_app as app
from flask_login import UserMixin
from flask_login import current_user




class Reviews(UserMixin):
    def __init__(self,uid,pid,product_name,review,rating,fname="",lname=""):
        self.pid = pid # includes sellers too
        self.product_name = product_name
        self.review = review
        self.rating = rating
        self.fname = fname
        self.lname = lname
        self.uid = uid
        if current_user.is_authenticated:
            self.current_user_id = current_user.id
    
    @staticmethod
    def duplicate_key_check(current_user_id,pid):
        rows = app.db.execute("""
                Select * from  product_ratings
                where product_id = :pid and buyer_id = :uid
                """,
                pid=pid,
                uid=current_user_id)
        return len(rows) == 0
    

    @staticmethod
    def duplicate_key_check_sell(current_user_id,sid):
        rows = app.db.execute("""
                Select * from  seller_ratings
                where seller_id = :sid and buyer_id = :uid
                """,
                sid=sid,
                uid=current_user_id)
        return len(rows) == 0

    @staticmethod
    def existing_product_check(pid):
        rows = app.db.execute("""
                Select * from  products
                where id = :pid 
                """,
                pid=pid)
        return len(rows) != 0

    @staticmethod
    def existing_seller_check(uid):
        rows = app.db.execute("""
                Select * from  sellers
                where id = :uid 
                """,
                uid=uid)
        return len(rows) != 0

    @staticmethod
    def rating_int_check(rating):
        
        return rating in [0,1,2,3,4,5]

    @staticmethod
    def return_reviews(pid):
        rows = app.db.execute("""
                Select buyer_id, product_id,products.name, review,rating, firstname,lastname 
                from  product_ratings, users, products
                where product_id = :pid and users.id =buyer_id and products.id = product_id
                ORDER BY review_time DESC
                """,
                pid=pid)
        return [Reviews(*row) for row in rows]
    
    @staticmethod
    def return_reviews_pol(pid,polarity):
        rows = app.db.execute("""
                Select buyer_id, product_id,products.name, review,rating, firstname,lastname 
                from  product_ratings, users, products
                where product_id = :pid and users.id =buyer_id and products.id = product_id and polarity = :polarity
                ORDER BY review_time DESC
                """,
                pid=pid,
                polarity=polarity)
        return [Reviews(*row) for row in rows]

    @staticmethod
    def return_reviews_user(uid):
        rows = app.db.execute("""
                Select buyer_id, product_id,products.name, review,rating, firstname,lastname from  product_ratings, users , products
                where users.id = :uid and users.id = buyer_id and products.id = product_id
                ORDER BY review_time DESC
                """,
                uid=uid)
        return [Reviews(*row) for row in rows]


    @staticmethod
    def return_reviews_user_pol(uid,polarity):
        rows = app.db.execute("""
                Select buyer_id, product_id,products.name, review,rating, firstname,lastname from  product_ratings, users , products
                where users.id = :uid and users.id = buyer_id and products.id = product_id and polarity = :polarity
                ORDER BY review_time DESC
                """,
                uid=uid,
                polarity=polarity)
        return [Reviews(*row) for row in rows]

    @staticmethod
    def return_reviews_user_sell(uid):
        # uid,pid,product_name,review,rating,fname="",lname=""
        rows = app.db.execute("""
                select t1.seller_id,t1.buyer_id,t3.seller_fn,t3.seller_ln , t1.rating, t1.review,t1.review_time from 
                (Select seller_id, buyer_id,review,rating,review_time from seller_ratings ) as t1,
                (select id,firstname as buyer_fn,lastname as buyer_ln from users where id = :uid) as t2,
                (select id, firstname as seller_fn , lastname as seller_ln from users  ) t3
                where t3.id = t1.seller_id and buyer_id = :uid
                ORDER BY review_time DESC
                """,
                uid=uid)
        return [Reviews(row[1],row[0],'',row[5],row[4],row[2],row[3] ) for row in rows]

    @staticmethod
    def return_reviews_user_sell_pol(uid,polarity):
        # uid,pid,product_name,review,rating,fname="",lname=""
        rows = app.db.execute("""
                select t1.seller_id,t1.buyer_id,t3.seller_fn,t3.seller_ln , t1.rating, t1.review,t1.review_time from 
                (Select seller_id, buyer_id,review,rating,review_time  from seller_ratings where polarity = :polarity ) as t1,
                (select id,firstname as buyer_fn,lastname as buyer_ln from users where id = :uid) as t2,
                (select id, firstname as seller_fn , lastname as seller_ln from users  ) t3
                where t3.id = t1.seller_id and buyer_id = :uid
                ORDER BY review_time DESC
                """,
                uid=uid,
                polarity=polarity)
        return [Reviews(row[1],row[0],'',row[5],row[4],row[2],row[3] ) for row in rows]

    @staticmethod
    def return_reviews_user_sell_Rat(uid):
        # uid,pid,product_name,review,rating,fname="",lname=""
        rows = app.db.execute("""
                select t1.seller_id,t1.buyer_id,t3.seller_fn,t3.seller_ln , t1.rating, t1.review from 
                (Select seller_id, buyer_id,review,rating from seller_ratings ) as t1,
                (select id,firstname as buyer_fn,lastname as buyer_ln from users where id = :uid) as t2,
                (select id, firstname as seller_fn , lastname as seller_ln from users  ) t3
                where t3.id = t1.seller_id and buyer_id = :uid
                ORDER BY rating DESC
                """,
                uid=uid)
        return [Reviews(row[1],row[0],'',row[5],row[4],row[2],row[3] ) for row in rows]


    @staticmethod
    def submit(current_user_id,pid, review, rating,polarity):
    # check for the conditions listed in the project description
        rows = app.db.execute("""
                INSERT INTO product_ratings(product_id,buyer_id, rating, review,polarity)
                VALUES(:pid, :uid, :rating, :review,:polarity) 
                RETURNING product_id
                """,
                pid=pid,
                uid=current_user_id,
                rating=rating,
                review=review,
                polarity=polarity)

        return True

    @staticmethod
    def ordered_check(current_user_id,sid):
        rows = app.db.execute("""
        select * from 
                (Select id as order_id from orders where uid = :uid) as t1,
                (Select order_id, seller_id from items_ordered ) as t2

                where t1.order_id = t2.order_id and t2.seller_id = :sid
        """, uid=current_user_id, sid=sid)
        return len(rows)!=0

    @staticmethod
    def submit_sell(current_user_id,sid, review, rating,polarity):
    # check for the conditions listed in the project description
        rows = app.db.execute("""
                INSERT INTO seller_ratings(seller_id,buyer_id, rating, review,polarity)
                VALUES(:sid, :uid, :rating, :review,:polarity) 
                RETURNING seller_id
                """,
                sid=sid,
                uid=current_user_id,
                rating=rating,
                review=review,
                polarity=polarity)

        return True


    @staticmethod
    def update(current_user_id,pid, review, rating,polarity):
    # check for the conditions listed in the project description
        rows = app.db.execute("""
                UPDATE product_ratings
                SET review = :review, rating = :rating, polarity= :polarity,review_time=CURRENT_TIMESTAMP
                WHERE buyer_id = :uid and product_id= :pid 
                RETURNING product_id
                """,
                pid=pid,
                uid=current_user_id,
                rating=rating,
                review=review,
                polarity=polarity)

        return True


    @staticmethod
    def update_sell(current_user_id,sid, review, rating,polarity):
    # check for the conditions listed in the project description
        rows = app.db.execute("""
                UPDATE seller_ratings
                SET review = :review, rating = :rating, polarity = :polarity ,review_time=CURRENT_TIMESTAMP
                WHERE buyer_id = :uid and seller_id= :sid 
                RETURNING seller_id
                """,
                sid=sid,
                uid=current_user_id,
                rating=rating,
                review=review,
                polarity=polarity)

        return True


    @staticmethod
    def delete(current_user_id,pid):
    # check for the conditions listed in the project description
        rows = app.db.execute("""
                DELETE FROM product_ratings
                WHERE buyer_id = :uid and product_id= :pid 
                RETURNING product_id
                """,
                pid=pid,
                uid=current_user_id)

        return True

    @staticmethod
    def delete_sell(current_user_id,sid):
    # check for the conditions listed in the project description
        rows = app.db.execute("""
                DELETE FROM seller_ratings
                WHERE buyer_id = :uid and seller_id= :sid 
                RETURNING seller_id
                """,
                sid=sid,
                uid=current_user_id)

        return True


    @staticmethod
    def num_ratings(pid):
        rows = app.db.execute("""
                Select * from  product_ratings
                where product_id = :pid 
                """,
                pid=pid)
        return len(rows)

    @staticmethod
    def num_ratings_sell(pid):
        rows = app.db.execute("""
                Select * from  seller_ratings
                where seller_id = :pid 
                """,
                pid=pid)
        return len(rows)

    @staticmethod
    def avg_rating(pid):
        rows = app.db.execute("""
                Select avg(rating) from  product_ratings
                where product_id = :pid 
                """,
                pid=pid)
        if rows[0][0] != None:
            return "%0.2f"%rows[0][0]
        else:
            return None

    @staticmethod
    def avg_rating_sell(pid):
        rows = app.db.execute("""
                Select avg(rating) from  seller_ratings
                where seller_id = :pid 
                """,
                pid=pid)
        if rows[0][0] != None:
            return "%0.2f"%rows[0][0]
        else:
            return None

    @staticmethod
    def return_reviews_rating(pid):
        rows = app.db.execute("""
                Select buyer_id, product_id,products.name, review,rating, firstname,lastname 
                from  product_ratings, users, products
                where product_id = :pid and users.id =buyer_id and products.id = product_id
                ORDER BY rating DESC
                """,
                pid=pid)
        return [Reviews(*row) for row in rows]
    @staticmethod
    def return_reviews_user_rating(uid):
        rows = app.db.execute("""
                Select buyer_id, product_id,products.name, review,rating, firstname,lastname from  product_ratings, users , products
                where users.id = :uid and users.id = buyer_id and products.id = product_id
                ORDER BY rating DESC
                """,
                uid=uid)
        return [Reviews(*row) for row in rows]

    @staticmethod
    def return_reviews_seller_rating(seller_uid):
        #self,uid,pid,product_name,review,rating,fname="",lname=""
        rows = app.db.execute("""
                Select buyer_id,seller_id ,review,rating, firstname as buyer_fn,lastname as buyer_ln 
                from  seller_ratings, users 
                where seller_id = :seller_uid  and users.id = buyer_id 

                ORDER BY rating DESC
                """,
                seller_uid=seller_uid)
        return [ Reviews(uid=row[0],pid=row[1],product_name="",review=row[2],rating=row[3],fname=row[4],lname=row[5]) for row in rows]

    @staticmethod
    def return_reviews_seller(seller_uid):
        rows = app.db.execute("""
                Select buyer_id,seller_id ,review,rating, firstname as buyer_fn,lastname as buyer_ln 
                from  seller_ratings, users 
                where seller_id = :seller_uid  and users.id = buyer_id 

                ORDER BY review_time DESC
                """,
                seller_uid=seller_uid)
        return [ Reviews(uid=row[0],pid=row[1],product_name="",review=row[2],rating=row[3],fname=row[4],lname=row[5]) for row in rows]


    @staticmethod
    def return_reviews_seller_pol(seller_uid,polarity):
        rows = app.db.execute("""
                Select buyer_id,seller_id ,review,rating, firstname as buyer_fn,lastname as buyer_ln 
                from  seller_ratings, users 
                where seller_id = :seller_uid  and users.id = buyer_id  and polarity = :polarity

                ORDER BY review_time DESC
                """,
                seller_uid=seller_uid,
                polarity=polarity)
        return [ Reviews(uid=row[0],pid=row[1],product_name="",review=row[2],rating=row[3],fname=row[4],lname=row[5]) for row in rows]

