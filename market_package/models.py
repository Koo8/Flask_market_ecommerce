from market_package import db, login_manager
from market_package import flask_bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    print('in the Loader method')
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address= db.Column(db.String(length=60), nullable=False, unique=True)
    budget =  db.Column(db.Integer(),nullable=False, default=1000)
    password_hash = db.Column(db.String(length=60), nullable=False)
    # this items is not a column in table
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def beautify_budget(self):
        b_str = str(self.budget)
        if len(b_str)>=4:
            return  f'{b_str[:-3]},{b_str[-3:]}'
        else:
            return self.budget


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    # this column with foreign key defined is a column
    owner =  db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'