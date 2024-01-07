from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l
import datetime
from .models.reviews import Reviews

from .models.user import User
from .models.cart import Cart
from .models.purchase import Purchase
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index', page_number = 1))
    form = LoginForm()
    if form.validate_on_submit():
        bool,user = User.get_by_auth(form.email.data, form.password.data)
        if not bool:
            flash(user)
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index', page_number = 1)

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):

    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    addr = StringField(_l('Address'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'  ) )


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index', page_number = 1))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.addr.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index', page_number = 1))

@bp.route('/cart')
def cart():
    my_cart = Cart.get(current_user.id)
    cart_total = Cart.get_total(current_user.id)
    saved = Cart.get_saved(current_user.id)
    cart_length = len(my_cart)
    return render_template('cart.html', my_cart = my_cart, cart_total = cart_total, saved = saved, cart_length = cart_length)

@bp.route('/addToCart/<int:id>/<int:uid>/<int:sid>')
def addToCart(id, uid, sid):
    try:
        inCart = Cart.checkIfProductInCart(id, uid, sid)
        if (inCart):
            Cart.update_product(id, uid, sid, 'add')
        else: 
            Cart.add_product(id, uid, sid)
        return redirect(url_for('users.cart'))
    except Exception as e:
        return 'There was an issue adding this product to your cart'
@bp.route('/removeSingleQuantFromCart/<int:pid>/<int:uid>/<int:sid>')
def removeSingleQuantFromCart(pid, uid, sid):
    try:
        Cart.update_product(pid, uid, sid, 'sub')
        return redirect(url_for('users.cart'))
    except Exception as e:
        print(e)
        return "There was an issue removing a single of that item from your cart"
@bp.route('/removeFromCart/<int:pid>/<int:uid>/<int:sid>')
def removeFromCart(pid, uid, sid):
    try: 
        Cart.remove_product(pid, uid, sid)
        return redirect(url_for('users.cart'))
    except Exception as e:
        print(e)
        return 'There was an issue removing this product from your cart'
@bp.route('/saveForLater/<int:pid>/<int:uid>/<int:sid>/<int:quantity>')
def saveForLater(pid, uid, sid, quantity):
    try:
        Cart.save_for_later(uid, pid, sid, quantity)
        return redirect(url_for('users.cart'))
    except Exception as e:
        print(e)
        return 'There was an issue saving this product for later'
@bp.route('/removeFromSaved/<int:pid>/<int:uid>/<int:sid>')
def removeFromSaved(pid, uid, sid):
    try:
        Cart.remove_from_saved(uid, pid, sid)
        return redirect(url_for('users.cart'))
    except Exception as e:
        print(e)
        return 'There was an issue removing from saved'

@bp.route('/moveToCart/<int:pid>/<int:uid>/<int:sid>/<int:quantity>')
def moveToCart(pid, uid, sid, quantity):
    try:
        Cart.move_to_cart(uid, pid, sid, quantity)
        return redirect(url_for('users.cart'))
    except Exception as e:
        print(e)
        return 'There was an issue adding to cart'

class SortForm(FlaskForm):
    sort = SelectField(_l("Sort By:"), choices = [('n', 'Product Name'), ('timeA', "Date: Oldest to Newest"), ('timeD', "Date: Newest to Oldest"), ('priceL', "Price: Lowest to Highest"), ('priceH', "Price: Highest to Lowest")])
    submit = SubmitField(_l("Sort"))

class SearchForm(FlaskForm):
    search = StringField(_l("Search By Product Name"))
    submit2 = SubmitField(_l("Search"))

@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = SortForm()
    form2 = SearchForm()
    if form.submit.data and form.validate():
        purchases = Purchase.get_all_by_uid_sort(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0), form.sort.data)
        return render_template('profile.html',
                                isSeller=User.isSeller(current_user.id),auth = True, purchases=purchases, form=form, form2=form2)
    if form2.submit2.data and form2.validate():
        purchases = Purchase.get_all_by_uid_search(current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0), form2.search.data)
        return render_template('profile.html',
                                isSeller=User.isSeller(current_user.id),auth = True, purchases=purchases, form=form, form2=form2)
    if current_user.is_authenticated:
    # find the products current user has bought:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        return render_template('profile.html',
                                isSeller=User.isSeller(current_user.id),auth = True, purchases=purchases, form=form, form2=form2)
    else:
        return render_template('profile.html',
                                isSeller=0, auth= False)

class InfoForm(FlaskForm):
    email = StringField(_l('Email:'), validators=[DataRequired(), Email()])
    firstname = StringField(_l('First Name:'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name:'), validators=[DataRequired()])
    addr = StringField(_l('Address:'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

    def __init__(self, myEmail, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        self.myEmail = myEmail

    def validate_email(self, email):
        if User.email_exists(email.data) and email.data != self.myEmail:
            raise ValidationError(_('Already a user with this email.'  ) )

@bp.route('/editinfo', methods=['GET', 'POST'])
def editInfo():
    form = InfoForm(current_user.email)
    if form.validate_on_submit():
        User.updateInfo(current_user.id, form.email.data, form.firstname.data, form.lastname.data, form.addr.data)
        return redirect(url_for('users.profile'))
    return render_template('editinfo.html',
                            form=form)

class PasswordForm(FlaskForm):
    password = PasswordField(_l('New Password:'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password:'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Submit'))

@bp.route('/changepassword', methods=['GET', 'POST'])
def changePassword():
    form = PasswordForm()
    if form.validate_on_submit():
        User.updatePassword(current_user.id, form.password.data)
        return redirect(url_for('users.profile'))
    return render_template('changepassword.html',
                            form=form)

class BalanceForm(FlaskForm):
    balance = DecimalField(_l('How much do you want to add?'), validators=[InputRequired(),
                                                                            NumberRange(min=0, message="Must be At Least 0")])
    submit = SubmitField(_l('Add'))

@bp.route('/addbalance', methods=['GET', 'POST'])
def addBalance():
    form = BalanceForm()
    if form.validate_on_submit():
        User.updateBalance(current_user.id, float(current_user.balance) + float(form.balance.data))
        return redirect(url_for('users.profile'))
    return render_template('addbalance.html',
                            form=form)

class BalanceForm2(FlaskForm):
    balance = DecimalField(_l('How much do you want to withdraw?'), validators=[InputRequired(),
                                                                            NumberRange(min=0, max=100, message="Must be Between 0 and Current Balance")])
    submit = SubmitField(_l('Withdraw'))

@bp.route('/withdrawbalance', methods=['GET', 'POST'])
def withdrawBalance():
    form = BalanceForm2()
    form.balance.validators[1].max = current_user.balance
    print(form.balance.validators[1].max)
    if form.validate_on_submit():
        User.updateBalance(current_user.id, float(current_user.balance) - float(form.balance.data))
        return redirect(url_for('users.profile'))
    return render_template('withdrawbalance.html',
                            form=form)

@bp.route('/makeseller')
def makeSeller():
    if(not User.isSeller(current_user.id)):
        User.makeSeller(current_user.id)
    return redirect(url_for('users.profile'))

def setUpDB(val): 
    if (val):
        User.setUpUser(1000)

@bp.route('/place_order/<int:uid>')
def place_order(uid):
    if not Inventory.enough_for_order(uid):
        flash("An item in your cart is now out of stock")
        return redirect(url_for('users.cart'))
    if Purchase.can_place_order(uid):
        try:
            Purchase.place_order(uid)
            return redirect(url_for('index.index', page_number = 1))
        except Exception as e:
            print(e)
    else:
        flash('You do not have enough balance to place this order.')
        return redirect(url_for('users.cart'))

@bp.route('/seller_page/<int:uid>')
def sellerPage(uid):
    seller = User.get(uid)
    average_rating = Reviews.avg_rating_sell(uid)
    num_ = Reviews.num_ratings_sell(uid)
    return render_template('sellerpage.html',
                            number_ratings = num_,
                            average_rating=average_rating,
                            seller=seller)
