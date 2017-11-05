from flask import Flask,render_template

app=Flask(__name__)

@app.route('/shiina_website')
def shiina_website():
	return render_template("shiina_website_index.html")

if __name__=="__main__":
	app.run(debug=True)
