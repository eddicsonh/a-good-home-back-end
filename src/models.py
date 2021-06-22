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
    location = db.Column(db.String(500), unique=False, nullable=True)
    total_area = db.Column(db.Integer, unique=False, nullable=True)
    builded_surface = db.Column(db.Integer, unique=False, nullable=True)
    rooms = db.Column(db.Integer, unique=False, nullable=True)
    bathrooms = db.Column(db.Integer, unique=False, nullable=True)
    parkings = db.Column(db.Integer, unique=False, nullable=True)
    transaction = db.relationship('Transaction', lazy=True)
    

    def __init__ (self, name, description, location, total_area, builded_surface, rooms, bathrooms, parkings):
        self.name = name,
        self.description = description,
        self.location = location,
        self.total_area = total_area,
        self.builded_surface = builded_surface,
        self.rooms = rooms,
        self.bathrooms = bathrooms,
        self.parkings = parkings,
    
    def __repr__(self):
        return '<RealState %r>' % self.name

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "total_area": self.total_area,
            "builded_surface": self.builded_surface,
            "rooms": self.rooms,
            "bathrooms": self.bathrooms,
            "parkings": self.parkings,
            "transaction": list(map(lambda x: x.serialize(), self.transaction))
        }


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(16), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=False)
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
            # do not serialize the password, its a security breach
        }
     
class real_state_agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(900), unique=True, nullable=False)
    location = db.Column(db.String(20), unique=True, nullable=False)
    team_agents = db.Column(db.Integer, nullable=False)
    listings = db.Column(db.Integer, unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, unique=False, nullable=False)


    def __init__(self, company, description, location, team_agents, listings, is_verified):
        self.company= company
        self.description= description
        self.location= location
        self.team_agents=team_agents
        self.listings=listings
        self.is_verified=is_verified

    def serialize(self):
        return {

            "company": self.company,
            "description": self.description,
            "location": self.description,
            "team_agents": self.team_agents,
            "listings": self.listings,
            "is_verified": self.is_verified 
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