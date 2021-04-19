
from datetime import datetime


from . import db, login_manager, login_seller
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    
    return Register_user.query.get(user_id)


class Register_user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120),  nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    pincode = db.Column(db.String(10), unique=False, nullable=False)
    number = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    cartitems1 = db.relationship('CartItem', backref='Customer')

    def _repr_(self):
        return '<Register_user %r>' % self.name


@login_seller.user_loader
def load_user(seller_id):
    return Register_seller.query.get(seller_id)


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    catagory = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Numeric(10,2), nullable = False)
    mfg = db.Column(db.String(60), nullable=True)
    description = db.Column(db.Text, nullable=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('register_seller.id'),nullable=False)
    pic = db.Column(db.String, nullable=False)
    cartitems = db.relationship('CartItem', backref='Product')

    def __repr__(self):
        return '<Products %r>' % self.name



class Register_seller(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),  nullable=False)
    number = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120),  nullable=False)
    city = db.Column(db.String(120),  nullable=False)
    state = db.Column(db.String(120),  nullable=False)
    pincode = db.Column(db.String(120),  nullable=False)
    shop_name = db.Column(db.String(120),  nullable=False)
    bio = db.Column(db.String(120),default= 'Best Shop')
    image = db.Column(db.String(120), nullable = False)
    products = db.relationship('Products', backref='shop', lazy=True, cascade="all,delete")

    def __repr__(self):
        return '<Register_seller %r>' % self.name

     
   



class CartItem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    quantity = db.Column(db.Integer, nullable = False, default = 1)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('register_user.id'))


































class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer,  nullable=False)
    query = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return f"Contact('{self.name}' , '{self.email}' , '{self.phone}' , '{self.query}')"

db.create_all()