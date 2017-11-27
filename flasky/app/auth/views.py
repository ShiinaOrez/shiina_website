from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login')
def login():
    form=LoginForm()
    if form.validate_on_submit():
        usr=User.query.filter_by(username=form.username.data).first()
        if usr is None:
        	flash('The user is not registed!')
        	return redirect(url_for('shiina_website_login'))
        else:
        	if usr.verify_password(form.password.data):
        		return redirect(url_for('shiina_website_profile',name=form.username.data))
        	else:
        		flash('username or password is wrong!')
        		return redirect(url_for('shiina_website_login'))
    return render_template("shiina_website_login.html",form=form)