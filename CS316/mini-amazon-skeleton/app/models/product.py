from os import name
from flask import current_app as app
import functools

def compareFunction(product1,product2,search,price = 0,index1 = -1,index2 = -1):
    match1 = False
    match2 = False
    if(product1[1].upper() == search.upper()):
        match1 = True
    if(product2[1].upper() == search.upper()):
        match2 = True
    if(match1 and not match2):
        return -1
    if(match2 and not match1):
        return 1
    if(match1 and match2):
        if(price == 1):
            return product1[3]-product2[3]
        if(price == -1):
            return product2[3]-product1[3]
        else:
            return product1[0] - product2[0]
    #checks if there is an exact match in search name
    match1 = False
    match2 = False
    if(search.upper() in product1[1].upper() or product1[1].upper() in search.upper()):
        match1 = True
    if(search.upper() in product2[1].upper() or product1[1].upper() in search.upper()):
        match2 = True
    if(match1 and not match2):
        return -1
    if(match2 and not match1):
        return 1
    if(match1 and match2):
        if(price == 1):
            return product1[3]-product2[3]
        if(price == -1):
            return product2[3]-product1[3]
        else:
            return product1[0] - product2[0]
    #checks if search is a substring of original or original a substring of search
    if(index1 < index2):
        return 1
    if(index2 > index1):
        return -1
    if(price == 1):
            return product1[3]-product2[3]
    if(price == -1):
        return product2[3]-product1[3]
    else:
        return product1[0] - product2[0]
    return 0


class Product:
    def __init__(self, id, name, category, available,price = 0):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.available = available
        # self.quantity = quantity

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT p.id, p.name, p.category, p.available
FROM Products p
WHERE p.id = :id
''',
                              id=id)
        print(rows[0])
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT DISTINCT p.id, p.name, p.category, p.available
FROM Products p
WHERE p.available = True
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_paginated(available, page_number):
        offset = (20 * (page_number-1))
        rows = app.db.execute('''
SELECT DISTINCT p.id, p.name, p.category, p.available
FROM Products p
WHERE p.available = True 
ORDER BY p.id
LIMIT 20 OFFSET :offset
''',
                              available=available,
                              offset = offset)
        return [Product(*row) for row in rows]
        
    @staticmethod
    def add(name,category):
        try:
            lastid = app.db.execute("""
            SELECT MAX(p.id)
            FROM Products p
            """)
            print(lastid[0][0])
            rows = app.db.execute("""
            INSERT INTO Products(id, name, category, available, description_link)
            VALUES(:id, :name, :category, :available, :description_link)
            RETURNING id""",
                id=lastid[0][0] + 1,
                name=name,
                category=category,
                available=True,
                description_link=str(lastid[0][0] + 1))
            return rows[0][0]
        except Exception as e:
            print(e)
            return False
    @staticmethod
    def get_link(productid):
        return app.db.execute(
            '''
            SELECT DISTINCT p.description_link
            FROM products p
            WHERE p.id = :id
            ''', id = productid
        )

    @staticmethod
    def search(available,search,page_number):
        newsearch = search
        price = 0
        literal = False
        if('"' in search):
            newsearch = search.replace('"','')
            literal = True
        if('*p-' in search or ' *p-' in search):
            newsearch = newsearch.replace(' *p-', '').replace('*p-','')
            price = -1
        elif('*p' in search or ' *p' in search):
            newsearch = newsearch.replace(' *p', '').replace('*p','')
            price = 1
        cat = newsearch.strip()
        if('*c' in newsearch or ' *c' in newsearch):
            ind = newsearch.find('*c')
            fin = newsearch.find(' ', ind+3)+1
            if fin == 0:
                fin = len(newsearch)
            cat = newsearch[ind+2:fin].strip()
            
            newsearch = newsearch[0:ind]
        catsearch = app.db.execute(
            '''
SELECT DISTINCT c.name
FROM Product_Categories c, Products p, Inventory i
WHERE UPPER(c.name) = :cat and UPPER(p.category) = :cat and i.product_id = p.id and i.quantity > 0
            ''', cat = cat.upper())
        if(len(catsearch) > 0 and literal == False):
            rows = app.db.execute('''
SELECT DISTINCT p.id, p.name, p.category, p.available, MIN(i.price) AS price
FROM Products p, Inventory i
WHERE p.available = :available and i.product_id = p.id and i.quantity > 0 and UPPER(p.category) = :cat
GROUP BY p.id

''',
                              available=available, cat = cat.upper())
        else:
             rows = app.db.execute('''
SELECT DISTINCT p.id, p.name, p.category, p.available, MIN(i.price) AS price
FROM Products p, Inventory i
WHERE p.available = :available and i.product_id = p.id and i.quantity > 0
GROUP BY p.id

''',
                              available=available)
        indices = {}
        for row in rows:
            indices[row[0]] = -1
            if(Product.get_link(row[0])[0][0] != '!'):
                try:
                    link1 = Product.get_link(row[0])
                    with open('db/data/descriptions/'+str(link1[0][0])+'.txt') as f:
                        desc = f.readlines()
                    f.close()
                    for i in range(0,len(desc)):
                        if search.upper() in desc[len(desc) - i-1].upper() and indices[row[0]] == -1:
                            indices[row[0]] = i
                except Exception as e:
                    print(e)
    

        sortedrows = sorted(rows,key = functools.cmp_to_key(lambda x,y: compareFunction(x,y,newsearch.strip(),price,indices[x[0]],indices[y[0]])))
        selection = sortedrows[(page_number-1)*20:(page_number)*20]
        return [Product(*row) for row in selection]

    @staticmethod
    def getID():
        try:
            ids = app.db.execute('''
            SELECT id
            From Products
            ''')
            return ids
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def getNames():
        try:
            names = app.db.execute('''
            SELECT name
            From Products
            ''')
            return names
        except Exception as e:
            print(e)
            return None

    staticmethod
    def getCat():
        try:
            cats = app.db.execute('''
            SELECT DISTINCT name
            FROM Product_Categories
            ''')
            return cats
        except Exception as e:
            print(e)
            return None



