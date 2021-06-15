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

class real_state_agency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(900), unique=True, nullable=False)
    location = db.Column(db.String(20), unique=True, nullable=False)
    team_agents = db.Column(db.Integer(10), nullable=False)
    listings = db.Column(db.Integer(10), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean(), unique=False, nullable=False)


    def __init__(self, company, description, location, team_agents, listings, is_verified):
        self.company= company
        self.description= description
        self.location= location
        self.team_agents=team_agents
        self.listings=listings
        self.is_verified=is_verified

    def serialize(self):
        return {
            "id": self.id,
            "company": self.company,
            "description": self.description,
            "location": self.description,
            "team_agents": self.team_agents,
            "listings": self.listings,
            "is_verified": self.is_verified 
        }
