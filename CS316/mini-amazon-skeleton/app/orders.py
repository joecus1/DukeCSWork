from flask import render_template, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from flask_babel import _, lazy_gettext as _l

from .models.orders import Order
from .models.user import User

from flask import Blueprint
bp = Blueprint('orders', __name__)

# current orders page
@bp.route('/currentorders')
def currentOrders():
    # if user is not logged in or not a seller they are redirected to main page
    if not current_user.is_authenticated:
        return redirect(url_for('index.index', page_number = 1))
    if not User.isSeller(current_user.id):
        return redirect(url_for('index.index', page_number = 1))
    x = Order.getCurrent(current_user.id)
    if(x):
        hasOrders = True
    else:
        hasOrders = False
    
    return render_template('currentorders.html',
                            x=x, 
                            hasOrders=hasOrders)