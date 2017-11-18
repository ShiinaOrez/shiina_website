from . import db

class User(db.Model):
 	__tablename__='users'
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(20),unique=True)
    	password=db.Column(db.String(20))
	useremail=db.Column(db.String(30),unique=True)
	texts=db.relationship('Text',backref='user')

class Text(db.Model):
	__tablename__='texts'
	id=db.Column(db.Integer,primary_key=True)
	topic=db.Column(db.String(20))
	date=db.Column(db.String(20))
	incl=db.Column(db.String(1000))
	user_id=db.Column(db.Integer,db.ForeignKey('users.id'))