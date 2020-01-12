from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import hashlib
import random
import uuid
#from models import User, db #susitvarkyti


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
db = SQLAlchemy(app)


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(200), nullable=False)
	surname = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(200), default="")
	email = db.Column(db.String(200), nullable=False)
	lvl = db.Column(db.Integer, default=0)
	password = db.Column(db.String(200), nullable=False)
	image = db.Column(db.String(300), default="")
	info = db.Column(db.String(1000), default="")
	show = db.Column(db.String(10), default="False")

if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
	print(app.config['SQLALCHEMY_DATABASE_URI'])
	db.create_all()



	

@app.route("/")
def index():
	session_token = request.cookies.get("session_token")
	print(session_token)
	if session_token:
		#user = db.query(User).filter_by(session_token=session_token).first() # kas per
		user = "Valdas"
	else:
		user = None

	return render_template("index.html", user=user)
	

@app.route("/registracija/", methods=["POST","GET"])

def registration():
	if request.method == 'POST':
		print("="*20)
		print(request.form)
		user = User()
		user.name = request.form.get('user_name')
		user.surname = request.form['surname']
		user.phone = request.form['phone']
		user.email = request.form['email']
		user.lvl = 0
		password = request.form['password']
		user.password = hashlib.sha256(password.encode()).hexdigest()
		passwordr = request.form['passwordr']
		#user.image = format(request.form['image'])
		user.info = request.form['info']
		user.show = "False"
		try:
			db.session.add(user)
			db.session.commit()
			return render_template("registration_sucess.html")
			return redirect('/')
			
		except:
			
			return 'buvo problema dedant i db'
	else:
		return render_template("registration.html")
		
		



	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
if __name__=="__main__":
	app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)





















