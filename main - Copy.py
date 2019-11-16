from flask import Flask#, render_template



app = Flask("hi")

@app.route("/")
def index():
	return ("hello valdas")

	
	
	
	

	
	
	
	
	

app.run()