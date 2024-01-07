from flask import render_template, redirect, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, SelectField, TextAreaField
from wtforms.validators import NumberRange, InputRequired, ValidationError
from flask_babel import _, lazy_gettext as _l
import os

from .models.inventory import Inventory
from .models.user import User
from .models.product import Product

from flask import Blueprint
bp = Blueprint('inventory', __name__)

class SearchForm(FlaskForm):
    search = IntegerField(_l("Search by Product ID"))
    submit2 = SubmitField(_l("Search"))

class SortForm(FlaskForm):
    sort = SelectField(_l("Sort All Inventory By"), choices=[('p', 'Product ID'), ('n', "Product Name"), ("q", "Quantity"), ('pr', 'Price')])
    submit = SubmitField(_l("Sort"))

# inventory page
@bp.route('/inventory', methods=['GET', 'POST'])
def inventory():
    # if user is not logged in or not a seller they are redirected to main page
    if not current_user.is_authenticated:
        return redirect(url_for('index.index', page_number = 1))
    if not User.isSeller(current_user.id):
        return redirect(url_for('index.index', page_number = 1))

    # get Inventory of current user
    inventory = Inventory.get(current_user.id)
    if(not inventory):
        hasInventory = False
    else:
        hasInventory = True

    print(Inventory.getSearch(current_user.id, 18)[0].product_name)

    #sorting and searching options
    form = SortForm()
    form2 = SearchForm()
    if form.submit.data and form.validate():
        inventory = Inventory.getOrder(current_user.id, form.sort.data)
        return render_template('inventory.html',
                            inventory=inventory,
                            isSeller=User.isSeller(current_user.id),
                            hasInventory=hasInventory, 
                            form=form,
                            form2=form2)
    if form2.submit2.data and form2.validate():
        inventory = Inventory.getSearch(current_user.id, form2.search.data)
        if(not inventory):
            hasInventory = False
        else:
            hasInventory = True
        return render_template('inventory.html',
                            inventory=inventory,
                            isSeller=User.isSeller(current_user.id),
                            hasInventory=hasInventory, 
                            form=form,
                            form2=form2)

    # render page by adding information to inventory.html
    return render_template('inventory.html',
                            inventory=inventory,
                            isSeller=User.isSeller(current_user.id),
                            hasInventory=hasInventory,
                            form=form,
                            form2=form2)


class ProductForm(FlaskForm):
    productname = StringField(_l('Product Name'), validators=[InputRequired()])
    category = SelectField(_l('Category'))
    price = DecimalField(_l('Price'), validators=[InputRequired(), NumberRange(min=0, message="Price Must be At Least 0")])
    quantity = IntegerField(_l('Quantity'), validators=[InputRequired(), NumberRange(min=0, message="Quantity Must be At Least 0")])
    description = TextAreaField(_l('Description'), validators=[InputRequired()])
    submit = SubmitField(_l('Add Product'))

    def __init__(self, names, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.names = names
        
    def validate_productname(self, field):
        for name in self.names:
            if field.data == name[0]:
                raise ValidationError("Product name must be unique.")

    

# add an item to inventory/product db
@bp.route('/addproduct', methods=['GET', 'POST'])
def addProduct():
    form = ProductForm(Product.getNames())
    form.category.choices = [(cat[0], cat[0]) for cat in Product.getCat()]
    if form.validate_on_submit():
        productid=Product.add(form.productname.data, form.category.data)
        Inventory.add(current_user.id, productid, form.price.data, form.quantity.data)
        print(form.description.data)
        if os.path.exists("./db/data/descriptions/" + str(productid) + ".txt"):
            os.remove("./db/data/descriptions/" + str(productid) + ".txt")
        file1 = open("./db/data/descriptions/" + str(productid) + ".txt", "w")
        file1.write(form.description.data)
        file1.close
        return redirect(url_for('inventory.inventory'))
    return render_template('addproduct.html',
                            form=form)


class InventoryForm(FlaskForm):
    productid = IntegerField(_l('Product ID'), validators=[InputRequired()])
    price = DecimalField(_l('Price'), validators=[InputRequired(), NumberRange(min=0, message="Price Must be At Least 0")])
    quantity = IntegerField(_l('Quantity'), validators=[InputRequired(), NumberRange(min=0, message="Quantity Must be At Least 0")])
    submit = SubmitField(_l('Add Inventory'))

    def __init__(self, ids, ids2, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)
        self.ids = ids
        self.ids2 = ids2

    def validate_productid(self, field):
        found = False
        for id in self.ids:
            if field.data == id[0]:
                found = True
                break
        if(not found):
            raise ValidationError("Must input valid Product ID.")
        for id in self.ids2:
            if field.data == id[0]:
                raise ValidationError("Product is already in inventory.")


# add an item to inventory/product db
@bp.route('/addinventory/<int:pid>/<int:fill>', methods=['GET', 'POST'])
def addInventory(pid, fill):
    form = InventoryForm(Product.getID(), Inventory.getPID(current_user.id))
    if fill == 1:
        form.productid.data = pid
    if form.validate_on_submit():
        if(Inventory.add(current_user.id, form.productid.data, form.price.data, form.quantity.data)):
            return redirect(url_for('inventory.inventory'))
    return render_template('addinventory.html',
                            form=form)

class QuantityForm(FlaskForm):
    quantity = IntegerField(_l('Fill in New Quantity'), validators=[InputRequired(),
                                NumberRange(min=0, message="Quanitity Must be At Least 0")])
    submit = SubmitField(_l('Save Changes'))

# page for editing quantity of inventory
@bp.route('/editquantity/<int:pid>', methods=['GET', 'POST'])
def editQuantity(pid):
    form = QuantityForm()
    if form.validate_on_submit():
        Inventory.editQuantity(current_user.id, pid, form.quantity.data)
        return redirect(url_for('inventory.inventory'))
    return render_template('editquantity.html',
                            form=form)

class PriceForm(FlaskForm):
    price = DecimalField(_l('Fill in New Price'), validators=[InputRequired(),
                                NumberRange(min=0, message="Price Must be At Least 0")])
    submit = SubmitField(_l('Save Changes'))

# page for editing price of inventory
@bp.route('/editprice/<int:pid>', methods=['GET', 'POST'])
def editPrice(pid):
    form = PriceForm()
    if form.validate_on_submit():
        Inventory.editPrice(current_user.id, pid, form.price.data)
        return redirect(url_for('inventory.inventory'))
    return render_template('editprice.html',
                            form=form)

# remove item from inventory
@bp.route('/removeinventory/<int:pid>')
def removeInventory(pid):
    Inventory.removeInventory(current_user.id, pid)
    return redirect(url_for('inventory.inventory'))
    