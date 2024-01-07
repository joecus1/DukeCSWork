#imports
from flask import Blueprint
from flask.templating import render_template
from flask_login import current_user

from .models.product import Product
from .models.reviews import Reviews
from .models.inventory import Inventory
from .models.user import User

bp = Blueprint('products',__name__)

@bp.route('/viewProduct/<int:product_id>')
def viewProduct(product_id):
    num_ = Reviews.num_ratings(product_id)
    average_rating = Reviews.avg_rating(product_id)
    sellers = Inventory.get_seller_info(product_id)
    desc = ['Description unavailable']
    try:
        link = Product.get_link(product_id)
        with open('db/data/descriptions/'+str(link[0][0])+'.txt') as f:
            desc = f.readlines()
        f.close()
    except Exception as e:
        print(e)

    return render_template('./product.html', 
                            product= Product.get(product_id), 
                            number_ratings = num_,
                            average_rating=average_rating, 
                            sellers = sellers, 
                            desc_lines = desc,
                            isSeller= User.isSeller(current_user.id))
 
