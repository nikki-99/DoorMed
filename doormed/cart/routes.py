from doormed import app,db
from flask import render_template, url_for, request, redirect
from doormed.models import Register_seller, Register_user, Products, CartItem



@app.route('/main/<int:id>/cart')
def cart(id):
    items = []
    cart1 = []
    user = Register_user.query.filter_by(id=id).first()
    carts = CartItem.query.filter_by(customer_id=id).all()
    for cart in carts:
        item = Products.query.filter_by(id=cart.product_id).first()
        items.append(item)
        cart1.append(cart)
    # cart = Cartitem.query.filter
    return render_template("carts/cart.html",user=user,carts=carts,items=zip(items,cart1))    


@app.route('/main/<int:id>/addcart', methods = ['GET','POST'])
def addcart(id): 
    user = Register_user.query.filter_by(id = id).first()
    product_id = request.form.get('product_id')
    product = Products.query.filter_by(id = product_id).first()
    quantity = request.form.get('quantity')
    if request.method == 'POST' and quantity and product_id:
        
        entry = CartItem(quantity = quantity, customer_id = user.id, product_id = product.id )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('cart', id = user.id))
    return render_template('carts/cart.html', user = user)    
    

        



