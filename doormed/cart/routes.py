from doormed import app,db
from flask import render_template, url_for, request, redirect, flash
from doormed.models import Register_seller, Register_user, Products, CartItem



@app.route('/main/<int:id>/cart')
def cart(id):
    items = []
    cart1 = []
    user = Register_user.query.filter_by(id=id).first()
    carts = CartItem.query.filter_by(customer_id=id).all()
    if carts:
        for cart in carts:
            item = Products.query.filter_by(id=cart.product_id).first()
            items.append(item)
            cart1.append(cart)
            shop1 = Register_seller.query.filter_by(id = item.shop_id).first()
       
    # cart = Cartitem.query.filter
        return render_template("carts/cart.html",user=user,carts=carts,items=zip(items,cart1), shop = shop1) 
    return render_template("carts/cart.html",user=user,carts=carts,items=zip(items,cart1))        


@app.route('/main/<int:id>/addcart', methods = ['GET','POST'])
def addcart(id): 
    user = Register_user.query.filter_by(id = id).first()
    carts = CartItem.query.filter_by(customer_id = user.id).all()
    productId = request.form.get('product_id')
    product = Products.query.filter_by(id = productId).first()
    shop2 = Register_seller.query.filter_by(id = product.shop_id).first()
    quantity = request.form.get('quantity')
    if request.method == 'POST' and quantity and productId:
        if carts:
            for cart in carts:
                prodId = Products.query.filter_by(id = cart.product_id).first()
                if prodId.id == int(productId):
                    flash(f'You have already added this item in your cart!')
                    return redirect(url_for('cart', id = user.id))

                shopId = Register_seller.query.filter_by(id = prodId.shop_id).first()
                if shop2.id != shopId.id:
                    flash(f'You can not add this!')
                    return redirect(url_for('cart', id = user.id))


    
        
        entry = CartItem(quantity = quantity, customer_id = user.id, product_id = product.id )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('cart', id = user.id))
    return render_template('carts/cart.html', user = user, shop= shop2)    
    

        



@app.route('/main/<int:id>/cart/delete/<int:id2>', methods=['GET','POST'])
# @login_required
def deleteitem(id, id2):
    user = Register_user.query.filter_by(id = id).first()
    # seller = Register_seller.query.filter_by(id = current_user.id).first() 
    cart = CartItem.query.get_or_404(id2)
    if request.method == 'POST':
        db.session.delete(cart)
        db.session.commit()
        flash(f'Item has been deleted successfully from your cart!')
        return redirect(url_for('cart', id = user.id))
    return redirect(url_for('cart', id = user.id))    
  
      

   


