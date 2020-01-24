from flask import Flask, render_template, url_for, request, redirect,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import os
import hashlib
import random
import uuid
#from flask_uploads 
#from models import User, db #susitvarkyti


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data_base.db'
db = SQLAlchemy(app)

#============================ Lentutes ============================
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
	session_token = db.Column(db.String, default="")
	
	
	
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
	

class Document(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(4000), default="")
	

	
class News(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(4000), default="")
	title_en = db.Column(db.String(4000), default="")
	date = db.Column(db.String(4000), default="")
	location = db.Column(db.String(4000), default="")
	
	
class News_in_LT(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(4000), default="")
	title_en = db.Column(db.String(4000), default="")
	date = db.Column(db.String(4000), default="")
	location = db.Column(db.String(4000), default="")
	

class News_in_World(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	title = db.Column(db.String(4000), default="")
	title_en = db.Column(db.String(4000), default="")
	date = db.Column(db.String(4000), default="")
	location = db.Column(db.String(4000), default="")

class History(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
class Officer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")

class Comision(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
#	
class Recruit(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
class Purpose(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	text = db.Column(db.String(400000), default="")
	text_en = db.Column(db.String(400000), default="")
	
#============================ Duomenu Baze ============================	
	
	
if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI']):
	#print(app.config['SQLALCHEMY_DATABASE_URI'])
	db.create_all()
	users_ = list(User.query.all())
	if len(users_)== 0:
		super_admin = User()
		super_admin.name = "SuperAdmin"
		super_admin.surname = "SuperAdmin"
		super_admin.phone = 88888888
		super_admin.email = "admin@demo.lt"
		super_admin.lvl = 2
		password = "demo"
		super_admin.password = hashlib.sha256(password.encode()).hexdigest()
		super_admin.info = "Pradinis administratorius"
		super_admin.show = "False"
		super_admin.confirmed = "True"
		db.session.add(super_admin)
		db.session.commit()

		
		
#============================ Base ============================
		
def guest_user():
	current_user = User()
	current_user.name="G"
	current_user.surname="Svecias"
	current_user.email="gg@gg.gg"
	current_user.lvl=0
	current_user.id=-1
	return current_user
	
def current_user():
	email = request.cookies.get("current-user-email")
	current_user = User.query.filter_by(email=email).first()
	if current_user == None:
		current_user = guest_user()
	return current_user


		
@app.route("/prisijungti/",  methods=["POST","GET"])
def login():
	message = ""
	email=""
	fokus ='autofocus=""'
	if request.method == 'POST':
		email = request.form.get("login")
		password = request.form.get("password")
		hashed_password = hashlib.sha256(password.encode()).hexdigest()
		user = User.query.filter_by(email=email).first()		
		if not user:
			user = guest_user()
			user.password = hashed_password

		if hashed_password != user.password:
			message =  "WRONG PASSWORD! / Klaidingas Slaptažodis"
			return render_template("login.html", email = email, message = message,fokus="", current_user=current_user())
			
		elif hashed_password == user.password:
			user.session_token = str(uuid.uuid4())
			response = make_response(redirect(url_for('index')))
			response.set_cookie("session-token", user.session_token)  #  consider adding httponly=True on production
			response.set_cookie("current-user-name", user.name) 
			response.set_cookie("current-user-lvl", str(user.lvl)) 
			response.set_cookie("current-user-id", str(user.id)) 
			response.set_cookie("current-user-email", str(user.email)) 
			return response
	else:
		return render_template("login.html", email = email, message = message,fokus=fokus, current_user=current_user())
		
		
@app.route("/logout/")
def logout():
	response = make_response(redirect(url_for('index')))
	response.set_cookie('session-token', '', expires=0)
	response.set_cookie('current-user-name', '', expires=0)
	response.set_cookie('current-user-lvl', '', expires=0)
	response.set_cookie('current-user-id', '', expires=0)
	response.set_cookie('current-user-email', '', expires=0)
	
	return response
	


@app.route("/")
def index():
	return render_template("index.html", current_user = current_user())
	
#============================ Registracija ============================

@app.route("/registracija/", methods=["POST","GET"])
def registration():
	if request.method == 'POST':
		user = User()
		user.name = request.form.get('user_name')
		user.surname = request.form['surname']
		user.phone = request.form['phone']
		user.email = request.form['email']
		user.lvl = 0
		password = request.form['password']
		user.password = hashlib.sha256(password.encode()).hexdigest()
		#passwordr = request.form['passwordr']
		#user.image = format(request.form['image'])
		user.info = request.form['info']
		user.show = "False"
		user.confirmed = "False"
		try:
			db.session.add(user)
			db.session.commit()
			return render_template("registration_sucess.html", current_user=current_user())
			
		except:
			
			return 'buvo problema dedant i db'
	else:
		return render_template("registration.html", current_user=current_user())
		

	
#============================ Zinutes ============================
	
@app.route("/sms/")
def messages_users():
	messages_ = list(reversed(Messages.query.order_by(Messages.date_created).all()))
	return render_template("sms.html", messages=messages_, current_user=current_user())
	
#============================ Vartotojai ============================

@app.route("/vartotojai/", methods=["POST","GET"])
def control_users():
	users = reversed(User.query.order_by(User.date_created).all())
	return render_template("vartotojai.html", users=users, current_user=current_user())
	


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
		user.name = request.form.get('user_name')
		user.surname = request.form['surname']
		user.phone = request.form['phone']
		user.email = request.form['email']
		#user.lvl = 0
		password = request.form['password']
		user.password = hashlib.sha256(password.encode()).hexdigest()
		#passwordr = request.form['passwordr']
		#user.image = format(request.form['image'])
		user.info = request.form['info']
		#user.show = "False"
		try:
			db.session.commit()
			return redirect('/vartotojai/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("profilis.html",user=user, current_user=current_user())

	
	
	
	
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

	
#============================ kontaktai ============================
	
@app.route("/kontaktai/", methods=["POST","GET"])
def contacts_of_users():
	if request.method == 'POST':
		message = Messages()
		message.name = request.form['name']
		message.email = request.form['email']
		message.sms = request.form['message']
		db.session.add(message)
		db.session.commit()
		return render_template("zinute_priimta.html", current_user=current_user())
	else:
		users_ = reversed(User.query.order_by(User.date_created).all())
		users = []
		
		try:
			contact_main = Contact_text.query.get_or_404(1)
		except:
			contact_main = Contact_text()
			contact_main.info = "Kontaktai pilnai neužpildyti"
			contact_main.info_en = "Main info need to fill"
			db.session.add(contact_main)
			db.session.commit()
		
		
		for user in users_:
			if user.show == "True":
				users.append(user)
		return render_template("kontaktai.html", users=users, contact_main=contact_main, current_user=current_user())
	
	
	
	
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
		return render_template("redaguoti_kontaktus.html",contact_main=main_info, current_user=current_user())
	
	
#============================ dokumentai ============================	
	
@app.route("/dokumentai/", methods=["GET", "POST"])
def documents():
	if request.method == "POST":
		return "file"
	return render_template("dokumentai.html", current_user=current_user())
	
#============================ naujienos ============================
	
@app.route("/Naujienos/", methods=["GET", "POST"])
def news():
	news_ = list(reversed(News.query.order_by(News.date_created).all()))
	return render_template("Naujienos.html",news = news_ , current_user=current_user())
	

@app.route("/create_news/", methods=["GET", "POST"])	
def create_news():
	new_ = News()
	new_.title = ""
	new_.title_en =""
	new_.date =""
	new_.location =""
	if request.method == "POST":
		new_.title = request.form['title']
		new_.title_en = request.form['title_en']
		new_.date = request.form['date']
		new_.location = request.form['location']
		try:
			db.session.add(new_)
			db.session.commit()
			return redirect('/Naujienos/')
		except:
			return "nepavyko prideti naujienos i db"
	else:
		return render_template("Naujienos_create.html",new = new_, current_user=current_user())
	
	
	
@app.route("/edit_new/<int:id>", methods=["GET", "POST"])
def edit_new(id):
	new_ = News.query.get_or_404(id)
	if request.method == "POST":
		new_.title = request.form['title']
		new_.title_en = request.form['title_en']
		new_.date = request.form['date']
		new_.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/Naujienos/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("Naujienos_create.html",new = new_, current_user=current_user())
	
	
@app.route("/delete_new/<int:id>", methods=["GET", "POST"])
def delete_new(id):
	new_ = News.query.get_or_404(id)
	try:
		db.session.delete(new_)
		db.session.commit()
		return redirect('/Naujienos/')
	except:
		return 'problema trinant naujiena'
	
	
# ================== events #=====================


	
@app.route("/Renginiai_lietuvoje/", methods=["GET", "POST"])
def events():
	events = list(reversed(News_in_LT.query.order_by(News_in_LT.date_created).all()))
	return render_template("Renginiai_lietuvoje.html",events = events , current_user=current_user())
	

@app.route("/create_event/", methods=["GET", "POST"])	
def create_event():
	event = News_in_LT()
	event.title = ""
	event.title_en =""
	event.date =""
	event.location =""
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.add(event)
			db.session.commit()
			return redirect('/Renginiai_lietuvoje/')
		except:
			return "nepavyko prideti naujienos i db"
	else:
		return render_template("Renginiai_lietuvoje_create.html",event = event, current_user=current_user())
	
	
	
@app.route("/edit_event/<int:id>", methods=["GET", "POST"])
def edit_event(id):
	event = News_in_LT.query.get_or_404(id)
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/Renginiai_lietuvoje/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("Renginiai_lietuvoje_create.html",event = event, current_user=current_user())
	
	
@app.route("/delete_event/<int:id>", methods=["GET", "POST"])
def delete_event(id):
	event = News_in_LT.query.get_or_404(id)
	try:
		db.session.delete(event)
		db.session.commit()
		return redirect('/Renginiai_lietuvoje/')
	except:
		return 'problema trinant naujiena'
	
	
	
	
# ================== tarptautiniai events #=====================


	
@app.route("/Tarptautiniai_renginiai/", methods=["GET", "POST"])
def tevents():
	events = list(reversed(News_in_World.query.order_by(News_in_World.date_created).all()))
	return render_template("Tartautiniai_renginiai.html",events = events , current_user=current_user())
	

@app.route("/create_tevent/", methods=["GET", "POST"])	
def tcreate_event():
	event = News_in_World()
	event.title = ""
	event.title_en =""
	event.date =""
	event.location =""
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.add(event)
			db.session.commit()
			return redirect('/Tarptautiniai_renginiai/')
		except:
			return "nepavyko prideti naujienos i db"
	else:
		return render_template("Tartautiniai_renginiai_create.html",event = event, current_user=current_user())
	
	
	
@app.route("/edit_tevent/<int:id>", methods=["GET", "POST"])
def tedit_event(id):
	event = News_in_World.query.get_or_404(id)
	if request.method == "POST":
		event.title = request.form['title']
		event.title_en = request.form['title_en']
		event.date = request.form['date']
		event.location = request.form['location']
		try:
			db.session.commit()
			return redirect('/Tarptautiniai_renginiai/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("Tartautiniai_renginiai_create.html",event = event, current_user=current_user())
	
	
@app.route("/delete_tevent/<int:id>", methods=["GET", "POST"])
def tdelete_event(id):
	event = News_in_World.query.get_or_404(id)
	try:
		db.session.delete(event)
		db.session.commit()
		return redirect('/Tarptautiniai_renginiai/')
	except:
		return 'problema trinant naujiena'
	
	
	
#============================ History ============================
	
	
	
@app.route("/history/")
def history():
	try:
		data = History.query.get_or_404(1)
	except:
		data = History()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	data.text = data.text.replace(" ","&nbsp")
	data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("History.html", data=data, current_user=current_user())
	

@app.route("/edit_history/<int:id>", methods=["GET", "POST"])
def edit_history(id):
	data = History.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/history/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user())
	
	
	
#============================ Officer ============================	
	
	
@app.route("/officer/")
def officer():
	try:
		data = Officer.query.get_or_404(1)
	except:
		data = Officer()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	data.text = data.text.replace(" ","&nbsp")
	data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Officer.html", data=data, current_user=current_user())
	

@app.route("/edit_officer/<int:id>", methods=["GET", "POST"])
def edit_officer(id):
	data = Officer.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/officer/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user())
	
	

	
#============================ Comision ============================	
	
	
@app.route("/comision/")
def comision():
	try:
		data = Comision.query.get_or_404(1)
	except:
		data = Comision()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	data.text = data.text.replace(" ","&nbsp")
	data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Comision.html", data=data, current_user=current_user())
	

@app.route("/edit_comision/<int:id>", methods=["GET", "POST"])
def edit_comision(id):
	data = Comision.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/comision/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user())
	
	
	
	

	
#============================ Recruit ============================	
	
	
@app.route("/recruit/")
def recruit():
	try:
		data = Recruit.query.get_or_404(1)
	except:
		data = Recruit()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	data.text = data.text.replace(" ","&nbsp")
	data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Recruit.html", data=data, current_user=current_user())
	

@app.route("/edit_recruit/<int:id>", methods=["GET", "POST"])
def edit_recruit(id):
	data = Recruit.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/recruit/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user())
	
	
	
	
#============================ Purpose ============================	
	
	
@app.route("/purpose/")
def purpose():
	try:
		data = Purpose.query.get_or_404(1)
	except:
		data = Purpose()
		data.text = "Teksto nėra adminas turi pridėti"
		data.text_en = "Admin have to add text"
		db.session.add(data)
		db.session.commit()
	data.text = data.text.replace(" ","&nbsp")
	data.text_en = data.text_en.replace(" ","&nbsp")
	return render_template("Purpose.html", data=data, current_user=current_user())
	

@app.route("/edit_purpose/<int:id>", methods=["GET", "POST"])
def edit_purpose(id):
	data = Purpose.query.get_or_404(id)
	if request.method == "POST":
		data.text = request.form['text']
		data.text_en = request.form['text_en']
		try:
			db.session.commit()
			return redirect('/purpose/')
		except:
			return "nepavyko atnaujinti"
	else:
		return render_template("APIE_create.html",data=data, current_user=current_user())
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
if __name__=="__main__":
	app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
