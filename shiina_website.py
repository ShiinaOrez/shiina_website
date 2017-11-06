from flask import Flask,render_template,session

app=Flask(__name__)

@app.route('/shiina_website',methods=['GET','POST'])
def shiina_website():
	return render_template("shiina_website_index.html")

@app.route('/shiina_website/login',methods=['GET','POST'])
def shiina_website_login():
	return render_template("shiina_website_login.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

if __name__=="__main__":
	app.run(debug=True)
