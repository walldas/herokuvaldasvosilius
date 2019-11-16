from flask import Flask, render_template



app = Flask("hi")

@app.route("/")
def index():
	return render_template("index.html")

	
	
	
@app.route("/about")
def about():
	return render_template("about.html")

	
	
@app.route("/porfolio")
def porfolio():
	return render_template("porfolio.html")
	
	
	
	
	

app.run()