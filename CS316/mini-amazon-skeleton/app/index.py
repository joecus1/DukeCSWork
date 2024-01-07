from flask import render_template
from flask_login import current_user
import datetime
from flask import request

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.cart import Cart
from flask import Blueprint, redirect
bp = Blueprint('index', __name__)

@bp.route('/')
@bp.route('/<int:page_number>')
def index(page_number=1):
    setUpDB(False)
    # get all available products for sale:
    # products = Product.get_all(True)
    products = Product.get_paginated(True, page_number)
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           current_page = page_number,
                           search = False)

def setUpDB(val): 
    if (val):
        User.setUpUser(1000)

@bp.route('/search')
@bp.route('/search/<string:search>/<int:page_number>')
def get_search(page_number = 1,search = ""):
    setUpDB(False)
    if "q" in request.args:
        name = request.args.get("q",default=None,type=str)
        if name == "":
            return redirect('/')
        return redirect('/search/'+name+'/1')
    if search is None:
        return redirect('/')
    products = Product.search(True, search,page_number)
    return render_template('index.html',
                        
                           avail_products=products,
                           current_page = page_number,
                           search = True,
                           query = search)
