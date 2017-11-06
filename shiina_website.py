from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required,EqualTo,Regexp,Email,Length

app=Flask(__name__)

bootstrap=Bootstrap(app)

app.config['SECRET_KEY']="mashiro"

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
	return render_template("shiina_website_login.html",form=form)

@app.route('/shiina_website/register',methods=['GET','POST'])
def shiina_website_register():
	form=RegisterForm()
	if form.validate_on_submit():
		flash('database is building!')
	return render_template("shiina_website_register.html",form=form)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

class LoginForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
	password=StringField('Password:',validators=[Length(3,20)])
	submit=SubmitField('Login')

class RegisterForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
#	password=PasswordField('Password:',validators=[Length(3,20)],EqualTo('password2',message='Passwords must match!'))
	password=PasswordField('Password:',[Required(),EqualTo('password2',message='Passwords must match!')])
	password2=StringField('Password again:',validators=[Length(3,20)])
	email=StringField('Your email:',validators=[Email()])
	submit=SubmitField('Register now')

if __name__=="__main__":
	app.run(debug=True)
