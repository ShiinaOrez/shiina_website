from flask import render_template,session,redirect,url_for,request,flash

from . import main
from .forms import LoginForm,RegisterForm,PostForm
from .. import db
from ..models import User

@main.route('/shiina_website',methods=['GET','POST'])
def shiina_website():
    return render_template("shiina_website_index.html")

@main.route('/shiina_website/profile',methods=['GET','POST'])
def shiina_website_profile():
	form=PostForm()
	name=request.args.get("name")
	usr=User.query.filter_by(username=name).first()
	if form.validate_on_submit():
		txt=Text(topic=form.topic.data,date=form.date.data,incl=form.main_txt.data,user_id=usr.id)
		db.session.add(txt)
		db.session.commit()
		return redirect(url_for('main.post_succ',userid=usr.id,txtid=txt.id))
	return render_template("shiina_website_profile.html",name=name,form=form)

@main.route('/shiina_website/profile/post_succ/',methods=['GET','POST'])
def post_succ():
	usr=User.query.filter_by(id=request.args.get('userid')).first()
	return render_template('post_succ.html',name=usr.username)

@main.route('/shiina_website/login',methods=['GET','POST'])
def shiina_website_login():
    form=LoginForm()
    if form.validate_on_submit():
        usr=User.query.filter_by(username=form.username.data).first()
        if usr is None:
        	flash('The user is not registed!')
        	return redirect(url_for('main.shiina_website_login'))
        else:
        	if form.password.data == usr.password:
        		return redirect(url_for('main.shiina_website_profile',name=form.username.data))
        	else:
        		flash('username or password is wrong!')
        		return redirect(url_for('main.shiina_website_login'))
    return render_template("shiina_website_login.html",form=form)

@main.route('/shiina_website/register',methods=['GET','POST'])
def shiina_website_register():
    form=RegisterForm()
    if form.validate_on_submit():
        usr=User.query.filter_by(username=form.username.data).first()
        if usr is None:
            usr=User(username=form.username.data,
                	password=form.password.data,
                	useremail=form.useremail.data)
            db.session.add(usr)
            db.session.commit()
#            if app.config['FLASKY_ADMIN']:
 #               send_email(app.config['FLASKY_ADMIN'],
  #                                  'NewUser',
   #                                 'mail/new_user',
    #                                user=usr)
            return render_template("shiina_website_register_create_s.html",name=form.username.data)
        else:
            return render_template("shiina_website_register_create_f.html") 
    return render_template("shiina_website_register.html",form=form)
