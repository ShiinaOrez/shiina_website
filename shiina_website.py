import os
from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required,EqualTo,Regexp,Email,Length
from flask_sqlalchemy import SQLAlchemy

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

app.config['SECRET_KEY']="mashiro"
app.config['SQLALCHEMY_DATABASE_URI']=\
	'SQLITE:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

bootstrap=Bootstrap(app)
manager=Manager(app)
db=SQLAlchemy(app)
migrate=Migrate(app,db)

manager.add_command('db',MigrateCommand)

class User(db.Model):
	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True)
	password=db.Column(db.String(20))

class LoginForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
	password=StringField('Password:',validators=[Length(3,20)])
	submit=SubmitField('Login')

class RegisterForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
	password=PasswordField('Password:',validators=[Length(3,20),EqualTo('password2',message='Passwords do not match')])
#	password=PasswordField('Password:',[Required(),EqualTo('password2',message='Passwords must match!')])
	password2=StringField('Password again:',validators=[Length(3,20)])
	email=StringField('Your email:',validators=[Email()])
	submit=SubmitField('Register now')

@app.route('/shiina_website',methods=['GET','POST'])
def shiina_website():
	return render_template("shiina_website_index.html")

@app.route('/shiina_website/login',methods=['GET','POST'])
def shiina_website_login():
	form=LoginForm()
	if form.validate_on_submit():
		name=request.form('username')
		pasw=request.form('password')
		if name is not None and pasw is not None:
			flash('database is building!')
		#return render_template("building.html")	
	return render_template("shiina_website_login.html",form=form)

@app.route('/shiina_website/register',methods=['GET','POST'])
def shiina_website_register():
	form=RegisterForm()
	if form.validate_on_submit():
		usr=User.query.filter_by(username=form.username.data).first()
		if usr is None:
			usr=User(username=form.username.data,
				password=form.password.data)
			db.session.add(usr)
			return render_template("shiina_website_register_create_s.html",name=form.username.data)
		else:
			return render_template("shiina_website_register_create_f.html")	
	return render_template("shiina_website_register.html",form=form)

@app.route('/shiina_website/usershare',methods=['GET','POST'])
def shiina_website_usershare():
	render_template("shiina_website_usershare.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

if __name__=="__main__":
	manager.run()
	app.run(debug=True)
