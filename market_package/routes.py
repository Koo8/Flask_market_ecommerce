from flask_bcrypt import check_password_hash, generate_password_hash
from flask import render_template, redirect, url_for, flash, request
from market_package import app, db
from market_package.models import Item, User
from market_package.form import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required,current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['POST', 'GET'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == 'POST':
        # purchase item
        purchased_item = request.form.get('purchase_item_name')
        thePurchasedItem = Item.query.filter_by(name=purchased_item).first()
        if thePurchasedItem:
            if current_user.budget >= thePurchasedItem.price:
                current_user.budget -= thePurchasedItem.price
                thePurchasedItem.owner = current_user.id
                db.session.commit()
                flash('You have purchased the item.', category='success')

            else:
                flash('You do not have enough budget to purchase this item.', category='danger')

        # sold item
        sold_item = request.form.get('sold_item_id')
        print(f'{sold_item} is the sold_item id')
        theSoldItem = Item.query.filter_by(id=sold_item).first()
        if theSoldItem in current_user.items:
            theSoldItem.owner = None
            current_user.budget +=theSoldItem.price
            db.session.commit()
            flash(f'You have sold {theSoldItem.name} for {theSoldItem.price} to the market', category='success')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        items =Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        print(owned_items)
        return render_template('market.html', items = items, purchase_form=purchase_form,sell_form=sell_form, owned_items = owned_items)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        # print('validate all register info')
        encrypt_password =generate_password_hash(form.password1.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        email_address=form.email_address.data,
                        password_hash = encrypt_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f'You have successfully registerd. Now you are logged in as {new_user.username}', category='success')
        return redirect(url_for('market_page'))
    if form.errors:
        for error_message in form.errors:
           flash(error_message, category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST','GET'])
def login_page():
    form=LoginForm()
   # print(f'username is {form.username.data}, password is {form.password.data}')
    if form.validate_on_submit():
        print('Login form is validated.')
        attempted_user = User.query.filter_by(username=form.username.data).first()
        print(f'attempted user is {attempted_user}')
        if attempted_user:
            if check_password_hash(attempted_user.password_hash, form.password.data):
                login_user(attempted_user)
                flash('You have logged in successfully.', category='success')
                return redirect(url_for('market_page'))
            else:
                flash('password does not match the username', category='danger')
        else:
            flash('The username is wrong.', category='danger')
    if form.errors:
        print('ERRORS ')
        for error_message in form.errors:
           flash(error_message, category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out.', category='info')
    return redirect(url_for('home_page'))