from doormed import app, db, mail, admin
from flask import render_template,redirect,url_for,request,flash
from flask_login import login_user, current_user,login_required, logout_user
from threading import Thread
from flask_mail import Mail, Message
from datetime import datetime
from doormed.models import Contact, Register_user, Register_seller, Products
from flask_admin.contrib.sqla import ModelView



admin.add_view(ModelView(Register_seller, db.session))
admin.add_view(ModelView(Register_user, db.session))
admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Contact, db.session))



@app.route('/')
def home():
    if current_user.is_authenticated:
        user = Register_user.query.filter_by(id = current_user.id).first()
        if user:
            return render_template('main/home.html', id = user.id)
    return render_template('main/home.html')

  
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to,subject,template,**kwargs):
    msg=Message(app.config['MAIL_SUBJECT_PREFIX']+subject,sender=app.config['MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr




@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        query = request.form.get('query')
    
        details = Contact(name=name, email=email, phone=phone, query=query, date=datetime.now())
        db.session.add(details)
        db.session.commit()
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'],'New Query/Message','mail/query',name=name,email=email,phone=phone,query=query)
            flash(f'{name}, Your query is submitted...we will get back to you soon!!', 'success')
            return redirect(request.referrer)
    return render_template("main/contact.html")
