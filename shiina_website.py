from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required,Email,Length

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
		name=session.get('username')
		pasw=session.get('password')
		if name is not None and pasw is not None:
			flash('database is building!')
	return render_template("shiina_website_login.html",form=form)

@app.route('/shiina_website/register',methods=['GET','POST'])
def shiina_website_register():
	return render_template("shiina_website_register.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

class LoginForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
	password=StringField('Password:',validators=[Length(3,20)])
	submit=SubmitField('Login')


if __name__=="__main__":
	app.run(debug=True)
