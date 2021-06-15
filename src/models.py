from enum import unique
from operator import truediv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Real_state(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)
    location = db.Column(db.String(500), unique=False, nullable=True)
    total_area = db.Column(db.Integer, unique=False, nullable=True)
    builded_surface = db.Column(db.Integer, unique=False, nullable=True)
    rooms = db.Column(db.Integer, unique=False, nullable=True)
    bathrooms = db.Column(db.Integer, unique=False, nullable=True)
    parkings = db.Column(db.Integer, unique=False, nullable=True)

    def __init__ (self, name, description, location, total_area, builded_surface, rooms, bathrooms, parkings):
        self.name = name,
        self.description = description,
        self.location = location,
        self.total_area = total_area,
        self.builded_surface = builded_surface,
        self.rooms = rooms,
        self.bathrooms = bathrooms,
        self.parkings = parkings

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
            "parkings": self.parkings
        }

