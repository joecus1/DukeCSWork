from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import random, math, string
from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, addr, balance):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.addr = addr
        self.balance = balance

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, addr, CAST(balance AS numeric(36, 2))
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return 0,"Non-existent email"
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return 0,'Wrong password' 
        else:
            return 1,User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname,addr):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname,addr,balance)
VALUES(:email, :password, :firstname, :lastname,:addr, 0) --inserting a default balance of 0
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  addr=addr)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and
            # reporting needed
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, addr, CAST(balance AS numeric(36, 2))
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    # below method updates user info
    @staticmethod
    def updateInfo(id, new_email, new_firstname, new_lastname, new_addr):
        try:
            
            rows = app.db.execute("""
            UPDATE Users
            SET email = :new_email,
                firstname = :new_firstname,
                lastname = :new_lastname,
                addr = :new_addr
            WHERE id = :id
            """,
                          new_email = new_email,
                          new_firstname = new_firstname,
                          new_lastname = new_lastname,
                          new_addr = new_addr,
                          id = id
            )
            return True
        except Exception as e:
            print(e)
            return False

    # below method updates user password
    @staticmethod
    def updatePassword(id, new_password):
        try:
            
            rows = app.db.execute("""
            UPDATE Users
            SET password = :new_password
            WHERE id = :id
            """,
                          new_password = generate_password_hash(new_password),
                          id = id
            )
            return True
        except Exception as e:
            print(e)
            return False

    # below method updates user balance
    @staticmethod
    def updateBalance(id, new_balance):
        try:
            
            rows = app.db.execute("""
            UPDATE Users
            SET balance = :new_balance
            WHERE id = :id
            """,
                          new_balance = new_balance,
                          id = id
            )
            return True
        except Exception as e:
            print(e)
            return False

    # below method returns true if user is a seller and false if they are not a seller
    @staticmethod
    def isSeller(id):
        rows = app.db.execute("""
SELECT id
FROM Sellers
WHERE id = :id       
""",
                              id=id)
        return True if rows else False


    # below method adds user to list of sellers
    @staticmethod
    def makeSeller(id):
        try:
            rows = app.db.execute("""
            INSERT INTO Sellers(id)
            VALUES(:id)
            RETURNING id
            """,
                          id = id
            )
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def setUpUser(n):
        count = 0
        for i in range(n):
            try:
                rows = app.db.execute("""
                INSERT INTO Users(email, password, firstname, lastname, addr, balance)
                VALUES(:email, :password, :firstname, :lastname, :addr, :balance)
                RETURNING id
                """,
                              email = ''.join((random.choice(string.ascii_lowercase) for x in range(16))),
                              password = generate_password_hash("password"),
                              firstname = ''.join((random.choice(string.ascii_lowercase) for x in range(10))),
                              lastname = ''.join((random.choice(string.ascii_lowercase) for x in range(10))),
                              addr = ''.join((random.choice(string.ascii_lowercase) for x in range(20))),
                              balance = random.randint(0, 500)
                )
                id = rows[0][0]
                count = id
            except Exception as e:
                print(e)