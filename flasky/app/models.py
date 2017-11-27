from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,LoginManager

class User(UserMixin,db.Model):
 	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True)
    	password=db.Column(db.String(20))
        password_hash=db.Column(db.String(128))
	useremail=db.Column(db.String(30),unique=True)
	texts=db.relationship('Text',backref='user')
        @property
        def password(self):
            raise AttributeError('password is not a readable attribute')
	@password.setter
        def password(self,password):
            self.password_hash=generate_password_hash(password)
        def verify_password(self,password):
            return check_password_hash(self.password_hash,password)

class Text(db.Model):
	__tablename__='texts'
	id=db.Column(db.Integer,primary_key=True)
	topic=db.Column(db.String(20))
	date=db.Column(db.String(20))
	incl=db.Column(db.String(1000))
	user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
