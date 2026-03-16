
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(255))
    purchase_price = db.Column(db.Float)

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer)
    unit_number = db.Column(db.String(50))
    rent = db.Column(db.Float)
    status = db.Column(db.String(20))

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    category = db.Column(db.String(100))
    amount = db.Column(db.Float)
    type = db.Column(db.String(20))
    notes = db.Column(db.String(255))
    date = db.Column(db.String(20))
