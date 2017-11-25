import os
from flask import Flask,render_template,session,redirect,url_for,flash,request
from flask_bootstrap import Bootstrap
from flask_script import Manager,Shell
from flask_mail import Mail,Message
from flask_migrate import Migrate,MigrateCommand
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Required,EqualTo,Regexp,Email,Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']='smtp.qq.com'
app.config['MAIL_POST']=465
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX']='[Flasky]'
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <shiina_orez@qq.com>'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')
manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate=Migrate(app,db)
manager.add_command('db',MigrateCommand)
mail=Mail(app)

class User(db.Model):
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

@app.route('/shiina_website',methods=['GET','POST'])
def shiina_website():
    return render_template("shiina_website_index.html")

@app.route('/shiina_website/profile',methods=['GET','POST'])
def shiina_website_profile():
	form=PostForm()
	name=request.args.get("name")
	usr=User.query.filter_by(username=name).first()
	if form.validate_on_submit():
		txt=Text(topic=form.topic.data,date=form.date.data,incl=form.main_txt.data,user_id=usr.id)
		db.session.add(txt)
		db.session.commit()
		return redirect(url_for('post_succ',userid=usr.id,txtid=txt.id))
	return render_template("shiina_website_profile.html",name=name,form=form)

@app.route('/shiina_website/profile/post_succ/',methods=['GET','POST'])
def post_succ():
	usr=User.query.filter_by(id=request.args.get('userid')).first()
	return render_template('post_succ.html',name=usr.username)

@app.route('/shiina_website/login',methods=['GET','POST'])
def shiina_website_login():
    form=LoginForm()
    if form.validate_on_submit():
        usr=User.query.filter_by(username=form.username.data).first()
        if usr is None:
        	flash('The user is not registed!')
        	return redirect(url_for('shiina_website_login'))
        else:
        	if form.password.data == usr.password:
        		return redirect(url_for('shiina_website_profile',name=form.username.data))
        	else:
        		flash('username or password is wrong!')
        		return redirect(url_for('shiina_website_login'))
    return render_template("shiina_website_login.html",form=form)

@app.route('/shiina_website/register',methods=['GET','POST'])
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
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],
                                    'NewUser',
                                    'mail/new_user',
                                    user=usr)
            return render_template("shiina_website_register_create_s.html",name=form.username.data)
        else:
            return render_template("shiina_website_register_create_f.html") 
    return render_template("shiina_website_register.html",form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

def send_email(to,subject,template,**kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,
                            sender=app.config['FLASKY_MAIL_SENDER'],
                            recipients=[to])
    msg.body=render_template(template+'txt',**kwargs)
    msg.html=render_template(template+'html',**kwargs)
    mail.send(msg)

def make_shell_context():
    return dict(app=app,db=db,User=User,Text=Text)

manager.add_command("shell",Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
    app.run(debug=True)
