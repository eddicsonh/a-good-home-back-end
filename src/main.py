"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, json, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from werkzeug.wrappers import response
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Real_state
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/real_state/all', methods=['GET'])
def handle_real_state_get_all():
    get_real_state = Real_state.query.all()
    all_real_state_serialize = []
    for real_state in get_real_state:
        all_real_state_serialize.append(real_state.serialize())
    response_body = {
        "status": "OK",
        "response": all_real_state_serialize
    }
    headers = {
        "Content-Type": "application/json"
    }
    return jsonify(response_body), 200

@app.route('/real_state', methods=['POST'])
def handled_real_state_create():

    body = request.json
    new_real_state = Real_state(
        body["name"],
        body["description"],
        body["location"],
        body["total_area"],
        body["builded_surface"],
        body["rooms"],
        body["bathrooms"],
        body["parkings"]
    )
    db.session.add(new_real_state)
    db.session.commit()

    response_body = {
        "status": "ok"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
