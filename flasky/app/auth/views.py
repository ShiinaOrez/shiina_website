from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,login_required
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm,RegisterForm

@auth.route('/')
def index():
	return render_template('index.html')

@auth.route('/login',methods=['GET','POST'])
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
    return render_template("auth/login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.shiina_website'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
    	if form.validate_on_submit():
        	usr=User.query.filter_by(username=form.username.data).first()
        	if usr is None:
            		usr=User(username=form.username.data,
                		password=form.password.data,
                		useremail=form.useremail.data)
#           		 db.session.add(usr)
 #         		  db.session.commit()
            		if app.config['FLASKY_ADMIN']:
                		send_email(app.config['FLASKY_ADMIN'],
                        		            'NewUser',
                                		    'mail/new_user',
                                   			user=usr)
            		return render_template("register_create_s.html",name=form.username.data)
        	else:
            		return render_template("register_create_f.html") 
    	return render_template("auth/register.html",form=form)
