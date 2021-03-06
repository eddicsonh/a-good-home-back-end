from enum import unique
from operator import truediv
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.orm import backref, lazyload
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable = False)
    phone = db.Column(db.String(20), nullable=True)
    id_document = db.Column(db.Integer, unique=True, nullable=False)
    salt = db.Column(db.String(40), nullable=False)
    hashed_password = db.Column(db.String(240), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email, name, last_name, phone, id_document, password):
        self.email = email
        self.name = name
        self.last_name = last_name
        self.phone = phone
        self.id_document = id_document
        self.salt = os.urandom(16).hex()
        self.set_password(password)

    @classmethod
    def create(cls, **kwargs):
        user = cls(**kwargs)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return user
    
    def set_password(self, password):
        print(generate_password_hash(
            f"{password}{self.salt}"
        ))
        self.hashed_password = generate_password_hash(
            f"{password}{self.salt}"
        )

    def check_password(self, password):
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.salt}"
        )

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name" : self.name,
            "last_name" : self.last_name,
            "phone" : self.phone,
            "id_document" : self.id_document
            # do not serialize the password, its a security breach
        }

class RealState(db.Model):
    __tablename__ = 'realstate'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)
    city = db.Column(db.String(100), unique=False, nullable=True)
    address = db.Column(db.String(500), unique=False, nullable=True)
    total_area = db.Column(db.Integer, unique=False, nullable=True)
    builded_surface = db.Column(db.Integer, unique=False, nullable=True)
    rooms = db.Column(db.Integer, unique=False, nullable=True)
    bathrooms = db.Column(db.Integer, unique=False, nullable=True)
    parkings = db.Column(db.Integer, unique=False, nullable=True)
    price = db.Column(db.Integer, unique=False, nullable=True)
    contact_phone = db.Column(db.Integer, unique=True, nullable=True)
    contact_rrss = db.Column(db.String(50), unique=False, nullable=True)
    type_transaction = db.Column(db.String(50), unique=False, nullable=True)
    additional_information = db.Column(db.String(200), unique=False, nullable=True)
    image = db.Column(db.String(500), unique=True, nullable=True)
    transaction = db.relationship('Transaction', lazy=True)
    

    def __init__ (self, name, description, city, address, total_area, builded_surface, rooms, bathrooms, parkings, price, contact_phone, contact_rrss, type_transaction, additional_information,image):
        self.name = name,
        self.description = description,
        self.city = city,
        self.address = address
        self.total_area = total_area,
        self.builded_surface = builded_surface,
        self.rooms = rooms,
        self.bathrooms = bathrooms,
        self.parkings = parkings,
        self.price = price,
        self.contact_phone = contact_phone,
        self.contact_rrss = contact_rrss,
        self.type_transaction = type_transaction
        self.additional_information = additional_information,
        self.image = image
    
    def __repr__(self):
        return '<RealState %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.city + ' ' + self.address,
            "total_area": self.total_area,
            "builded_surface": self.builded_surface,
            "rooms": self.rooms,
            "bathrooms": self.bathrooms,
            "parkings": self.parkings,
            "price": self.price,
            "phone": self.contact_phone,
            "RRSS": self.contact_rrss,
            "transaction": self.transaction,
            "additional_information": self.additional_information,
            "image": self.image
            # "transaction": list(map(lambda x: x.serialize(), self.transaction))
        }

class Agent(db.Model):
    __tablename__ = 'agent'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(16), unique=True, nullable=False)
    description = db.Column(db.String(400), unique=False, nullable=False)
    city = db.Column(db.String(400), unique=False, nullable=True)
    salt = db.Column(db.String(40), nullable=False)
    hashed_password = db.Column(db.String(240), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        print(kwargs)
        self.email = kwargs.get('email')
        self.name = kwargs.get('name')
        self.last_name = kwargs.get('last_name')
        self.phone = kwargs.get('phone')
        self.description = kwargs.get('description')
        self.city = kwargs.get('city')
        self.salt = os.urandom(16).hex()
        self.set_password(kwargs.get('password'))
        

    @classmethod
    def create(cls, **kwargs):
        agent = cls(**kwargs)
        db.session.add(agent)
        try: 
            db.session.commit()
        except Exception as error:
            print(error.args)
            db.session.rollback()
            return False
        return agent 

    def set_password(self, password):
        print(generate_password_hash(
            f"{password}{self.salt}"
        ))
        self.hashed_password = generate_password_hash(
            f"{password}{self.salt}"
        )

    def check_password(self, password):
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.salt}"
        )   

    def __repr__(self):
        return '<Agent %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name" : self.last_name,
            "phone": self.phone,
            "city": self.city
            # do not serialize the password, its a security breach
        }
     



class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    id_realState = db.Column(db.Integer, db.ForeignKey('realstate.id'), nullable=True, unique=False)
    # realstate = db.relationship('RealState', backref='transaction', lazy=True)

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return{
            "id":self.id,
            "name": self.name
        }