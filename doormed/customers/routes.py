from doormed import app, db, bcrypt
from flask import render_template,redirect,url_for,request,flash
from flask_login import login_user, current_user,login_required, logout_user
import secrets
from datetime import datetime
from doormed.models import Register_seller, Products, Register_user, CartItem, Order




@app.route('/reg_user', methods=['GET', 'POST'])
def reg_user():
    if request.method == "POST":
        name = request.form.get("Name")
        email = request.form.get("EmailID")
        address = request.form.get("Address")
        city = request.form.get("City")
        pin = request.form.get("PinCode")
        number = request.form.get("MobileNumber")
        password = request.form.get("Password")

        hash_password = bcrypt.generate_password_hash(password)
        
        email1 = Register_user.query.filter_by(email = email).first()
        no1 = Register_user.query.filter_by(number = number).first()
        if email1 or no1:
            flash(f'This email or phone number is already taken....Change that one')
            return redirect(url_for('reg_user'))


        entry = Register_user(name=name, email=email, address = address, city=city.lower(), pincode=pin, number=number, password=hash_password)
        db.session.add(entry)
        db.session.commit()
        flash(f'{name} you are registered successfully. Now You are able to login!', 'success')
        return redirect(url_for('user_login'))
    return render_template("customers/register.html")


@app.route('/user_login', methods = ['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email1 = request.form.get("email1")
        password1 = request.form.get("password1")
        customer = Register_user.query.filter_by(email = email1).first()
        
        # form.email.data = ""
        if customer and bcrypt.check_password_hash(customer.password,password1):
            # return redirect(url_for('shops', id = seller.id))
            # return redirect(url_for('main', id = customer.id))
            login_user(customer)
            # print(customer.name)
            return redirect(url_for('main',id=customer.id))

        elif customer is None:
            flash(f"You haven't registered yet! Register first!")
              
        else:
            flash(f'Login Unsuccessful. Please check email or password','danger')     
            return redirect(url_for('user_login')) 

    return render_template("customers/login_user.html")



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('customer_page'))



@app.route('/customer_page')

def customer_page():
    shops = Register_seller.query.all()
    
    return render_template('customers/shops.html', shops = shops)  




@app.route('/main/<int:id>')
@login_required
def main(id):
    user = Register_user.query.filter_by(id = id).first()
    pros = []
    shop1 = []
    q = request.args.get('q')
    if q:
        shops1 = Register_seller.query.filter_by(city=user.city).all()
        for sho in shops1:
            prod = Products.query.filter_by(shop_id=sho.id).all()           
            for p in prod:
                if q.lower() in p.name.lower():
                    pros.append(p)
                    shop1.append(sho)
                # pros = Products.query.filter(Products.name.contains(q))
                # shops.append(shops1)
        return render_template('customers/searchmed.html', shop_and_prod = zip(shop1,pros), products=pros,shop=shop1,q=q, id = id)
    else:
        shops = Register_seller.query.filter_by(city= user.city)
        # print(shops)
    return render_template('customers/index.html', shops = shops, user = user)    
    



@app.route('/main/<int:id>/search',methods=['GET','POST'])
def search(id):
    user = Register_user.query.filter_by(id = id).first()
    pros = []
    shop1 = []
    q = request.args.get('q')
    if q:
        shops1 = Register_seller.query.filter_by(city=user.city).all()
        for sho in shops1:
            prod = Products.query.filter_by(shop_id=sho.id).all()           
            for p in prod:
                if q.lower() in p.name.lower():
                    pros.append(p)
                    shop1.append(sho)
                # pros = Products.query.filter(Products.name.contains(q))
                # shops.append(shops1)
        return render_template('customers/searchmed.html', shop_and_prod = zip(shop1,pros), products=pros,shop=shop1,q=q,id=id)
    return redirect(url_for('main',id=id))


@app.route('/<int:id>')
@login_required
def shop_details(id):
    if current_user.is_authenticated:
        user = Register_user.query.filter_by(id = current_user.id).first()
    medlist = []
    shop = Register_seller.query.filter_by(id = id).first()
    products = Products.query.filter_by(shop_id = shop.id)
    q = request.args.get('q')
    if q:
        for product in products:
            if q.lower() in product.name.lower():
                medlist.append(product)            
    return render_template('customers/details.html', shop = shop, products = products, medlist = medlist, user = user)
    

# hbjsdesghdsjdnbjs

@app.route('/main/<int:id>/account', methods= ['GET', 'POST'])
@login_required
def account(id):
    user = Register_user.query.filter_by(id = id).first()
    return render_template('customers/account.html', user = user)


@app.route('/main/<int:id>/account/update', methods= ['GET', 'POST'])
@login_required
def update(id):
    user = Register_user.query.filter_by(id = id).first() 
    if request.method == "POST":
        
        user.email = request.form.get("email")
        user.number = request.form.get("number")
        user.address = request.form.get("address")
        user.city = request.form.get("city").lower()
        db.session.commit()
        flash(f'Your account has been updated!')
        return redirect(url_for('account', id = user.id))
    return render_template('customers/account.html', user = user)    



@app.route('/main/<int:id>/account/delete', methods= ['GET', 'POST'])
@login_required
def delete(id):
    user = Register_user.query.filter_by(id = id).first() 
    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('customer_page'))
    return render_template('customers/account.html', user = user)   
        
@app.route('/main/<int:id>/order', methods= ['GET', 'POST'])
@login_required
def order(id):
    if request.method == 'POST':
        products = []
        sum = 0
        carts1 = []
        user = Register_user.query.filter_by(id = id).first() 
        invoice = secrets.token_hex(5)
        carts = CartItem.query.filter_by(customer_id = user.id).all()
        for cart in carts:
            product = Products.query.filter_by(id = cart.product_id).first()
            sum += cart.quantity * product.price
            products.append(product)
            carts1.append(cart)
            db.session.delete(cart)
            db.session.commit()
        entry = Order(invoice = invoice, cust_id = user.id, total = sum, order_date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        orders = Order.query.filter_by(cust_id = user.id).order_by(Order.order_date.desc()).first()
        flash(f'Your order has been accepted!')
        return render_template('customers/order.html', user = user, order = orders, carts = carts, products = products , ord_and_prod = zip(products,carts1)) 





    
    



























# @app.route('/search')
# def search():
#     shops = []
#     q = request.args.get('q')
#     if q:
#         pros = Products.query.filter(Products.name.contains(q))
#         for p in pros:

#             shops1 = Register_seller.query.filter_by(id = p.shop_id).first()
#             shops.append(shops1)
#     else:
       
#         pros = Products.query.all()
#         shops = Register_seller.query.all()
