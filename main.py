from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
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
	info_en = db.Column(db.String(1000), default="")
	show = db.Column(db.String(10), default="False")
	confirmed = db.Column(db.String(10), default="False")
	
	
	
class Contact_text(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	info = db.Column(db.String(4000), default="")
	info_en = db.Column(db.String(4000), default="")

	
class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	sms = db.Column(db.String(4000), default="")
	
	
if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
	print(app.config['SQLALCHEMY_DATABASE_URI'])
	db.create_all()
	


	

@app.route("/")
def index():
	session_token = request.cookies.get("session_token")
	print(">"*20)
	print(session_token)
	print(">"*20)
	if session_token:
		#user = db.query(User).filter_by(session_token=session_token).first() # kas per
		user = "Valdas"
	else:
		user = None

	return render_template("index.html", user=user)
	

@app.route("/registracija/", methods=["POST","GET"])
def registration():
	if request.method == 'POST':
		#print("="*20)
		#print(request.form)
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
		user.confirmed = "False"
		try:
			db.session.add(user)
			db.session.commit()
			return render_template("registration_sucess.html")
			return redirect('/')
			
		except:
			
			return 'buvo problema dedant i db'
	else:
		return render_template("registration.html")
		

	
@app.route("/vartotojai/", methods=["POST","GET"])
def control_users():
	users = reversed(User.query.order_by(User.date_created).all())
	return render_template("vartotojai.html", users=users)
	

	
@app.route("/sms/")
def messages_users():
	messages_ = list(reversed(Messages.query.order_by(Messages.date_created).all()))
	return render_template("sms.html", messages=messages_)
	
	
@app.route('/confirm_user/<int:id>')
def confirm_user(id):
	user = User.query.get_or_404(id)
	user.confirmed = "True"
	user.lvl = 1
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema patvirtinant vartotoja'
	

@app.route('/show_user/<int:id>')
def show_user(id):
	user = User.query.get_or_404(id)
	if user.show == "False":
		user.show = "True"
	else:
		user.show = "False"
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema suteikiant vartotojuj rodymo statusa'
	
	
@app.route('/delete_user/<int:id>')
def delete_user(id):
	user = User.query.get_or_404(id)
	try:
		db.session.delete(user)
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema trinant vartotoja'

		
@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):
	user = User.query.get_or_404(id)
	if request.method == "POST":
		#user.content = request.form['content']
		user.name = request.form.get('user_name')
		user.surname = request.form['surname']
		user.phone = request.form['phone']
		user.email = request.form['email']
		#user.lvl = 0
		password = request.form['password']
		user.password = hashlib.sha256(password.encode()).hexdigest()
		passwordr = request.form['passwordr']
		#user.image = format(request.form['image'])
		user.info = request.form['info']
		#user.show = "False"
		try:
			db.session.commit()
			return redirect('/vartotojai/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("profilis.html",user=user)

	
	
	
	
@app.route('/down_user/<int:id>')
def down_user(id):
	user = User.query.get_or_404(id)
	user.lvl -= 1
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema mazinant vartotojo lvl'
	
	
	
@app.route('/up_user/<int:id>')
def up_user(id):
	user = User.query.get_or_404(id)
	user.lvl += 1
	try:
		db.session.commit()
		return redirect('/vartotojai/')
	except:
		return 'problema didinant vartotojo lvl'
	
	
	
	
@app.route('/remove_message/<int:id>')
def remove_message(id):
	message = Messages.query.get_or_404(id)
	try:
		db.session.delete(message)
		db.session.commit()
		return redirect('/sms/')
	except:
		return 'problema trinant zinute'

	
@app.route("/kontaktai/", methods=["POST","GET"])
def contacts_of_users():
	if request.method == 'POST':
		message = Messages()
		message.name = request.form['name']
		message.email = request.form['email']
		message.sms = request.form['message']
		db.session.add(message)
		db.session.commit()
		return render_template("zinute_priimta.html")
	else:
		users_ = reversed(User.query.order_by(User.date_created).all())
		users = []
		
		try:
			contact_main = Contact_text.query.get_or_404(1)
		except:
			contact_main = Contact_text()
			contact_main.info = "Kontaktai pilnai neužpildyti"
			contact_main.info_en = "Main info need to fill"
			db.session.set(contact_main)
			db.session.commit()
		
		
		for user in users_:
			if user.show == "True":
				users.append(user)
		return render_template("kontaktai.html", users=users, contact_main=contact_main)
	
	
	
	
@app.route("/edit_contact_info/<int:id>", methods=["GET", "POST"])
def edit_contact_info(id):
	main_info = Contact_text.query.get_or_404(id)
	if request.method == "POST":
		
		main_info.info = request.form['info']
		main_info.info_en = request.form['info_en']
		
		
		try:
			db.session.commit()
			return redirect('/kontaktai/')
		except:
			return "nepavyko atnaujinti"
	else:
		
		return render_template("redaguoti_kontaktus.html",contact_main=main_info)
	
	
	
	
@app.route("/prisijungti/")
def prisijungimas():
	
	return render_template("login.html")
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
if __name__=="__main__":
	app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)





















