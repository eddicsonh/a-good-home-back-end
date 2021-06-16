from flask_sqlalchemy import SQLAlchemy
import os
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


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(16), unique=True, nullable=False)
    salt = db.Column(db.String(40), nullable=False)
    hashed_password = db.Column(db.String(240), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, **kwargs):
        print(kwargs)
        self.email = kwargs.get('email')
        self.name = kwargs.get('name')
        self.last_name = kwargs.get('last_name')
        self.phone = kwargs.get('phone')
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