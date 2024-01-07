from flask import render_template, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from flask_babel import _, lazy_gettext as _l

from .models.orders import Order
from .models.user import User

from flask import Blueprint
bp = Blueprint('orders', __name__)

class SortForm(FlaskForm):
    sort = SelectField(_l('Sort All Orders By'), choices=[('t', 'Time'), ('q', "Quantity"), ("p", "Product Name"), ('b', 'Buyer Name')])
    submit = SubmitField(_l('Sort'))

class SearchForm(FlaskForm):
    search = IntegerField(_l("Search By Order ID"))
    submit2 = SubmitField(_l('Search'))

# orders page
@bp.route('/currentorders/<int:status>', methods=['GET', 'POST'])
def currentOrders(status):
    # if user is not logged in or not a seller they are redirected to main page
    if not current_user.is_authenticated:
        return redirect(url_for('index.index', page_number = 1))
    if not User.isSeller(current_user.id):
        return redirect(url_for('index.index', page_number = 1))
    x = Order.get(current_user.id, status)
    if(x):
        hasOrders = True
    else:
        hasOrders = False
    form = SortForm()
    form2 = SearchForm()
    if form.submit.data and form.validate():
        x = Order.getOrder(current_user.id, status, form.sort.data)
    if form2.submit2.data and form2.validate():
        x = Order.getSearch(current_user.id, status, form2.search.data)
        if(x):
            hasOrders = True
        else:
            hasOrders = False
    return render_template('currentorders.html',
                            x=x, 
                            hasOrders=hasOrders,
                            form=form,
                            form2=form2,
                            status=status)

# pulls up graph of top sellers
@bp.route('/topsellers')
def topSellers():
    top3 = Order.topSellers(current_user.id)
    labels = [x[0] for x in top3]
    values = [x[1] for x in top3]
    return render_template("topsellers.html",
                            labels=labels,
                            values=values)

# remove item from inventory
@bp.route('/fulfill/<int:oid>/<int:pid>/<int:sid>')
def fulfill(oid, pid, sid):
    Order.fulfill(oid, pid, sid)
    return redirect(url_for('orders.currentOrders', status=0))