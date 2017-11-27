from flask_wtf import Form
from wtforms import BooleanField,StringField,SubmitField,PasswordField
from wtforms import ValidationError
from wtforms.validators import Length,Email,EqualTo
from ..models import User

class LoginForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
 	password=PasswordField('Password:',validators=[Length(3,20)])
	remeber_me=BooleanField('Keep me login in')
 	submit=SubmitField('Login')

class PostForm(Form):
	topic=StringField('Topic:')
	date=StringField('Date:')
	main_txt=StringField('MainText:',validators=[Length(3,1000)])
	submit=SubmitField('POST')

class RegisterForm(Form):
	username=StringField('Username:',validators=[Length(3,20)])
 	password=PasswordField('Password:',validators=[Length(3,20),EqualTo('password2',message='Passwords do not match')])
	password2=StringField('Password again:',validators=[Length(3,20)])
	useremail=StringField('Your email:',validators=[Email()])
	submit=SubmitField('Register now')