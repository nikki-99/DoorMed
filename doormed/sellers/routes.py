from doormed import app, db, bcrypt
from flask import render_template,redirect,url_for,request,flash, send_file
from flask_login import login_user, current_user,login_required, logout_user
from doormed.models import Register_seller, Products, Order, Register_user
from io import BytesIO


@app.route('/seller_register', methods = ['GET','POST'])
def register_seller():
    if request.method == 'POST':
        name = request.form.get("Name")
        email = request.form.get("EmailID")
        password = request.form.get("Password")
        number = request.form.get("MobileNumber")
        address = request.form.get("Address")
        city = request.form.get("City")
        pin = request.form.get("PinCode")
        state = request.form.get("State")
        shop = request.form.get("shop")
        bio = request.form.get("Bio")
        
        img = request.files['fileupload']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        email1 = Register_seller.query.filter_by(email = email).first()
        no1 = Register_seller.query.filter_by(number = number).first()
        if email1 or no1:
            flash(f'This email or phone number is already taken....Change that one')
            return redirect(url_for('register_seller'))
        entry = Register_seller(name=name, email=email, password=hashed_password,
                                number=number, address=address, city=city.lower(),
                                pincode=pin, state=state, shop_name=shop, bio=bio, pic_name =img.filename, pic_data = img.read())
        db.session.add(entry)
        db.session.commit()
        flash(f'{shop} is registered successfully in our database. Now you are able to login!', 'success')
        return redirect(url_for('seller_login'))
        
    return render_template("sellers/register.html")




@app.route('/seller_login', methods = ['GET','POST'])
def seller_login():
    if request.method == 'POST':
        email = request.form.get("email")
        password1 = request.form.get("password")
        seller = Register_seller.query.filter_by(email = email ).first()
        
        # form.email.data = ""
        if seller and bcrypt.check_password_hash(seller.password,password1):
            login_user(seller)
            return redirect(url_for('shops'))
        elif seller is None:
            flash(f"You haven't registered yet! Register first!")
              
        else:
            flash(f'Login Unsuccessful. Please check email or password','danger')     
            return redirect(url_for('seller_login')) 

    return render_template('sellers/login.html')    



@app.route('/logout_seller')
def logout_seller():
    logout_user()
    return redirect(url_for('seller_login'))




@app.route('/shops')
@login_required
def shops():
    seller = Register_seller.query.filter_by(id =current_user.id ).first()
    products = Products.query.filter_by(shop_id = seller.id)
    users = []
    orders = Order.query.filter_by(sh_id = seller.id).all()
    if orders:
        for order in orders:
            user = Register_user.query.filter_by(id = order.cust_id).first()
            users.append(user)
    
        return render_template('sellers/shop.html', seller = seller, products = products, orders = orders, user_order = zip(orders, users), users = users)

    return render_template('sellers/shop.html', seller = seller, products = products)


@app.route('/shops/update', methods= ['GET', 'POST'])
@login_required
def accountupdate():
    seller = Register_seller.query.filter_by(id = current_user.id).first() 
    products = Products.query.filter_by(shop_id = seller.id)
    if request.method == "POST":
        
        seller.email = request.form.get("email")
        seller.number = request.form.get("number")
        seller.address = request.form.get("address")
        seller.city = request.form.get("city").lower()
        db.session.commit()
        return redirect(url_for('shops'))
    return render_template('sellers/shop.html', seller = seller, products = products)    




@app.route('/shops/delete', methods= ['GET', 'POST'])
@login_required
def shop_delete():
    seller = Register_seller.query.filter_by(id = current_user.id).first() 
    products = Products.query.filter_by(shop_id = seller.id)
    if request.method == "POST":
        db.session.delete(seller)
        db.session.commit()
        flash(f"Your account has successfully deleted!")
        return redirect(url_for('seller_login'))
    return render_template('sellers/shop.html', seller = seller, products = products)    
          
              





@app.route('/shops/addproduct', methods=['GET','POST'])
@login_required
def addproduct():
    seller = Register_seller.query.filter_by(id = current_user.id).first() 
    if request.method == "POST":
        name = request.form.get('Name')
        desc = request.form.get('Desc')
        
        catagory = request.form.get('Catagory')
        price = request.form.get('price')
        mfg = request.form.get('Mfg')
        img = request.files['Image']

        name1 = Products.query.filter_by(name = name, shop_id = seller.id).first()
        if name1:
            
            flash(f'You have already added this medicine!..')
            return redirect(url_for('addproduct'))
              

        entry = Products(name=name, shop_id=seller.id, catagory=catagory, price=price, mfg=mfg, description=desc, pic_name =img.filename, pic_data = img.read())
        db.session.add(entry)
        db.session.commit()
        flash(f'{name} is added successfully')
        return redirect(url_for('addproduct'))
    return render_template("products/add.html")
        


@app.route('/shops/deleteproduct/<int:id>', methods=['GET','POST'])
@login_required
def deleteproduct(id):
    seller = Register_seller.query.filter_by(id = current_user.id).first() 
    product = Products.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash(f'{product.name} has been deleted successfully')
        return redirect(url_for('shops'))
    return render_template('sellers/shop.html',  seller = seller,products = products)    
      

   
@app.route('/show/<int:id>')
def getimg(id):
    img = Products.query.filter_by(id = id).first()
    get = send_file(BytesIO(img.pic_data), attachment_filename = 'flask.jpg')
    return get


@app.route('/show1/<int:id>')
def getimg1(id):
    img = Register_seller.query.filter_by(id = id).first()
    get = send_file(BytesIO(img.pic_data), attachment_filename = 'flask.jpg')
    return get
