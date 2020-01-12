import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(app)
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	name = db.Column(db.String(200), nullable=False)
	surname = db.Column(db.String(200), nullable=False)
	phone = db.Column(db.String(200), default="")
	email = db.Column(db.String(200), nullable=False)
	lvl = db.Column(db.Integer, default=0)
	password = db.Column(db.String(200), nullable=False)
	image = db.Column(db.String(200), default="")
	info = db.Column(db.String(1000), default="")
	show = db.Column(db.String, default="False")
	
	
