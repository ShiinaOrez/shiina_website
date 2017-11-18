from flask import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Length,Email,EqualTo

class LoginForm(FlaskForm):
	username=StringField('Username:',validators=[Length(3,20)])
 	password=PasswordField('Password:',validators=[Length(3,20)])
 	submit=SubmitField('Login')

class PostForm(FlaskForm):
	topic=StringField('Topic:')
	date=StringField('Date:')
	main_txt=StringField('MainText:',validators=[Length(3,1000)])
	submit=SubmitField('POST')

class RegisterForm(FlaskForm):
	username=StringField('Username:',validators=[Length(3,20)])
 	password=PasswordField('Password:',validators=[Length(3,20),EqualTo('password2',message='Passwords do not match')])
	password2=StringField('Password again:',validators=[Length(3,20)])
	useremail=StringField('Your email:',validators=[Email()])
	submit=SubmitField('Register now')
