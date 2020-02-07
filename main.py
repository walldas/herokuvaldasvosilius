from flask import Flask, render_template, url_for, request, redirect,make_response, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import os
import hashlib
import random
import uuid
#from flask_uploads 
#from models import User, db #susitvarkyti


app = Flask(__name__)



	
@app.route("/")
def index():
	return render_template("base.html")
	


	
if __name__=="__main__":
	app.run(debug=True, host="0.0.0.0", port=5000 , threaded=True)
	#80 http
	#https 443
