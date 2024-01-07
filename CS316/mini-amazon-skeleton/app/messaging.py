import nltk
from nltk.stem.porter import PorterStemmer
import re
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from nltk.corpus import stopwords
from .toke_porter import tokenizer_porter as tokenizer_porter





from flask import render_template, Flask, flash,request
from flask_wtf import FlaskForm
from wtforms import StringField,  SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.__init__ import create_app
from flask_babel import _, lazy_gettext as _l
from flask_login import current_user
from .models.reviews import Reviews


from flask import Blueprint
bp = Blueprint('messaging', __name__)
app = create_app()

def preprocessor(txt):
    txt+= ' ' 
    txt = re.sub('<[^>]*>',' ', txt) 
    em_reg = '(\:\w+\:|\<[\/\\]?3|[\(\)\\\D|\*\$][\-\^]?[\:\;\=]|[\:\;\=B8][\-\^]?[3DOPp\@\$\*\\\)\(\/\|])(?=\s|[\!\.\?]|$)'
    emoticons = re.findall(em_reg,txt)
    txt = re.sub(em_reg ,' ', txt.lower() ) + ' '.join(emoticons)
    return txt



stop = stopwords.words('english')
filename = './app/LR_model.sav'
porter = PorterStemmer()
nltk.download('stopwords') 
tokenizer_porter("bal")


def pipeline(review,rating):
    if review == None or rating == None:
        return
    try:
        int(rating)
    except:
        return
    review = preprocessor(str(review))
    review = ' '.join(tokenizer_porter(review,stop))
    
    tfidf = pickle.load(open('./app/tfidf.sav','rb'))
    clf = pickle.load(open(filename,'rb'))
    
    plus = 0
    if int(rating) >2:
        plus +=.2
    else:
        plus -=.3
    xx_text = tfidf.transform([review])
    prediction_text = clf.predict(xx_text)[0]
    
    xx_word = tfidf.transform(review.split())
    prediction_word_by_word = np.mean(clf.predict(xx_word))

    prediction = np.mean([prediction_text, prediction_word_by_word])                   
    
    return  int((prediction +plus ) > .5)


class ReviewForm(FlaskForm):
    review = StringField(_l('Review', validators=[DataRequired()]) )
    rating = StringField(_l('Rating', validators=[DataRequired()]) )
    product_id = StringField(_l('pid') )
    submit = SubmitField(_l('Submit' ))

class ReviewForm_seller(FlaskForm):
    review = StringField(_l('Review', validators=[DataRequired()]) )
    rating = StringField(_l('Rating', validators=[DataRequired()]) )
    seller_id = StringField(_l('seller_id') )
    submit = SubmitField(_l('Submit' ))

class SelectorForm(FlaskForm):
    sort = StringField(_l('sort', validators=[DataRequired()]) )
    go = SubmitField(_l('Go' ))



def form_checks(form, product_id,polarity):


    if form.validate_on_submit() :

        if not Reviews.existing_product_check(product_id):
            flash("The product doesn't exist")
        elif not form.rating.data.isdigit():
            flash("The rating should be an integer comprised between 0 and 5")
        elif  not Reviews.rating_int_check(int(form.rating.data)):
            flash("The rating should be an integer comprised between 0 and 5")
        elif not Reviews.duplicate_key_check(current_user.id,product_id):
            upd = Reviews.update(current_user.id,product_id, form.review.data, form.rating.data,polarity)
            flash("Review Updated Successfully!") if upd else flash("Can't Update your review, please try again!")
        else:
            return True

class Delete_fct(FlaskForm):
    product_id = StringField(_l('product_id') )
    delete = SubmitField(_l('Delete' ))

class Edit_fct(FlaskForm):
    product_id = StringField(_l('product_id') )
    product_name = StringField(_l('product_name') )
    edit = SubmitField(_l('Select product to edit' ))

class Delete_fct_seller(FlaskForm):
    seller_id = StringField(_l('seller_id') )
    delete = SubmitField(_l('Delete' ))

class Edit_fct_seller(FlaskForm):
    seller_id = StringField(_l('seller_id') )
    product_name = StringField(_l('product_name') )
    edit = SubmitField(_l('Select product to edit' ))

@bp.route('/profile/<string:fname>/<string:lname>/user/<string:buyer_id>/<string:sellers>', methods=['GET', 'POST'])
def revPerUser(fname,lname,buyer_id,sellers):
    selector = SelectorForm()
    
    
    if  sellers == "0":
        form = ReviewForm()
        delete_ = Delete_fct()
        edit_ = Edit_fct()
        polarity = pipeline(form.review.data,form.rating.data)
        form_checks(form,form.product_id.data,polarity)
        if "delete" in request.form:
            Reviews.delete(current_user.id, delete_.product_id.data)
        if selector.sort.data == "time":
            reviews = Reviews.return_reviews_user(buyer_id)
        elif selector.sort.data == "positive":
            reviews = Reviews.return_reviews_user_pol(buyer_id,1)
        elif selector.sort.data == "negative":
            reviews = Reviews.return_reviews_user_pol(buyer_id,0)
        elif selector.sort.data == "ratings":
            reviews = Reviews.return_reviews_user_rating(buyer_id)
        else:
            reviews = Reviews.return_reviews_user(buyer_id)
    else:
        form = ReviewForm_seller()
        delete_ = Delete_fct_seller()
        edit_ = Edit_fct_seller()
        polarity = pipeline(form.review.data,form.rating.data)
        form_checks_sell(form,form.seller_id.data,polarity)

        if "delete" in request.form:
            Reviews.delete_sell(current_user.id, delete_.seller_id.data)

        if selector.sort.data == "time":
            reviews = Reviews.return_reviews_user_sell(buyer_id)
        elif selector.sort.data == "ratings":
            reviews = Reviews.return_reviews_user_sell_Rat(buyer_id)
        elif selector.sort.data == "positive":
            reviews = Reviews.return_reviews_user_sell_pol(buyer_id,1)
        elif selector.sort.data == "negative":
            reviews = Reviews.return_reviews_user_sell_pol(buyer_id,0)
        else:
            reviews = Reviews.return_reviews_user_sell(buyer_id)
        
    return render_template('./reviewsPUser.html',delete_=delete_,selector=selector,edit_=edit_,form=form ,reviews = reviews,name = " ".join([fname,lname]),buyer_id_ = int(buyer_id),sellers = int(sellers) )


@bp.route('/profile/<string:fname>/<string:lname>/<string:buyer_id>/divpage', methods=['GET', 'POST'])
def revPerUser_div(fname,lname,buyer_id):
    return render_template('./product_seller_reviews_div.html',fname = fname,lname = lname,buyer_id_ = int(buyer_id) )






@bp.route('/chat/<string:product_name>/<int:product_id>', methods=['GET', 'POST'])
def chat(product_name,product_id):
    selector = SelectorForm()
    if selector.sort.data == "time":
        reviews = Reviews.return_reviews(product_id)
    elif selector.sort.data == "ratings":
        reviews = Reviews.return_reviews_rating(product_id)
    elif selector.sort.data == "positive":
        reviews = Reviews.return_reviews_pol(product_id,1)
    elif selector.sort.data == "negative":
        reviews = Reviews.return_reviews_pol(product_id,0)
    else:
        reviews = Reviews.return_reviews(product_id)
    
    delete_ = Delete_fct()
    form = ReviewForm()
    polarity = pipeline(form.review.data,form.rating.data)

    if "delete" in request.form:
        Reviews.delete(current_user.id, product_id)
    
    if form_checks(form, product_id,polarity):
        Reviews.submit(current_user.id, product_id, form.review.data, form.rating.data,polarity) # TODO add polarity

    return render_template('./messaging.html',form = form,delete_ = delete_,selector=selector, reviews = reviews,product_name = product_name,polarity=polarity )


@bp.route('/profile/<string:fname>/<string:lname>/<string:seller_id>/seller', methods=['GET', 'POST'])
def revPerSeller(fname,lname,seller_id):
    selector = SelectorForm()
    delete_ = Delete_fct_seller()
    edit_ = Edit_fct_seller()
    form = ReviewForm_seller()
    
    #form_checks(form,form.seller_id.data)
    polarity = pipeline(form.review.data,form.rating.data)
    if "delete" in request.form:
        Reviews.delete_sell(current_user.id, seller_id)

    if selector.sort.data == "time":
        reviews = Reviews.return_reviews_seller(seller_id)
    elif selector.sort.data == "ratings":
        reviews = Reviews.return_reviews_seller_rating(seller_id)
    elif selector.sort.data == "positive":
        reviews = Reviews.return_reviews_seller_pol(seller_id,1)
    elif selector.sort.data == "negative":
        reviews = Reviews.return_reviews_seller_pol(seller_id,0)
    else:
        reviews = Reviews.return_reviews_seller(seller_id)
    try:
        if  int(current_user.id) == int(seller_id):
            flash("you can't rate yourself!")
        elif form_checks_sell(form, seller_id,polarity):
            Reviews.submit_sell(current_user.id, seller_id, form.review.data, form.rating.data,polarity)

    except:
        if form_checks_sell(form, seller_id,polarity):
            Reviews.submit_sell(current_user.id, seller_id, form.review.data, form.rating.data,polarity)


    return render_template('./reviewsPSeller.html',delete_=delete_,selector=selector,edit_=edit_,form=form ,reviews = reviews,name = " ".join([fname,lname]),seller_id_ = int(seller_id) )


def form_checks_sell(form, seller_id,polarity):


    if form.validate_on_submit() :

        if not Reviews.existing_seller_check(seller_id):
            flash("The product doesn't exist")
        elif not form.rating.data.isdigit():
            flash("The rating should be an integer comprised between 0 and 5")
        elif  not Reviews.rating_int_check(int(form.rating.data)):
            flash("The rating should be an integer comprised between 0 and 5")
        elif not Reviews.ordered_check(current_user.id,seller_id):
            flash("You need to order at least one item from the seller to be able to submit a review")
        elif not Reviews.duplicate_key_check_sell(current_user.id,seller_id):
            upd = Reviews.update_sell(current_user.id,seller_id, form.review.data, form.rating.data,polarity)
            flash("Review Updated Successfully!") if upd else flash("Can't Update your review, please try again!")
        else:
            return True