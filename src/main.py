"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response, session
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from werkzeug.wrappers import response
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Real_state
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "01cdeef14f0a17d28d723f35a2ba3670"
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

    # return jsonify(response_body), 200

@app.route("/sign-up", methods=["POST"])
def sign_up():
    data = request.get_json()
    if data is None:
        raise APIException('Los campos no pueden estar vacios', status_code=400)
    if 'email' not in data:
        raise APIException('Necesita introducir un email válido', status_code=400)
    if 'name' not in data:
        raise APIException('Por favor introduce tu nombre', status_code=400)
    if 'last_name' not in data:
        raise APIException('Por favor introduce tu apellido', status_code=400)
    if 'id_document' not in data:
        raise APIException('Por favor introduce tu numero de cedula', status_code=400)
    if 'password' not in data:
        raise APIException('Por favor introduce una clave', status_code=400)
    if data["email"]=="":
        return jsonify({"msg":"Los campos no pueden estar vacios"}), 500
    if data["name"]=="":
        return jsonify({"msg":"Los campos no pueden estar vacios"}), 500
    if data["last_name"]=="":
        return jsonify({"msg":"Los campos no pueden estar vacios"}), 500
    if data["id_document"]=="":
        return jsonify({"msg":"Los campos no pueden estar vacios"}), 500
    if data["password"]=="":
        return jsonify({"msg":"Los campos no pueden estar vacios"}), 500
    user = User.create(email=data.get('email'), name=data.get('name'), last_name=data.get('last_name'), phone=data.get('phone'), id_document=data.get('id_document'), password=data.get('password'))
    if not isinstance(user, User):
        return jsonify({"msg": "PROBLEMA"}), 500
    return jsonify(user.serialize()), 201


# this only runs if `$ python src/main.py` is executed

@app.route("/log-in", methods=["POST"])
def log_in():
    print(request.data)
    print(request.json)
    data = request.json
    user = User.query.filter_by(email=data['email']).one_or_none()
    if user is None:
        return jsonify({"msg":"No existe el usuario"}), 404
    if not user.check_password(data.get('password')):
        return jsonify({"msg": "Credenciales erroneas"}), 400
    token = create_access_token(identity=user.id)
    return jsonify({
        "user": user.serialize(),
        "token": token
    }), 200


@app.route('/user/profile', methods=['POST'])
def create_user():
    request_body = request.json
    new_user = User(
        request_body["email"],
        request_body["name"],
        request_body["last_name"],
        request_body["phone"],
        request_body["id_document"])
    db.session.add(new_user)
    db.session.commit()
    response_body ={
          "status": "Perfil creado exitosamente"
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

@app.route('/user/profie/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    request_body = request.json
    user.email = request_body["email"]
    user.name = request_body["name"]
    user.last_name = request_body["last_name"]
    user.phone = request_body["phone"]
    user.id_document = request_body["id_document"]
    user.password = request_body["password"]
    db.session.commit()
    
    response_body = {
        "status": "Usuario actualizado"
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    ) 

@app.route('/user/all', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users_serialize = []
    for user in all_users:
        all_users_serialize.append(user.serialize())
    response_body = {
        "status": "OK",
        "response": all_users_serialize
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

@app.route('/user/<user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    response_body = {
        "status": "OK",
        "response": user.serialize()
    
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )  


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    response_body = {
        "status": "User borrado exitosamente"
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

@app.route('/real_state/all', methods=['GET'])
def handle_real_state_get_all():
    get_real_state = Real_state.query.all()
    all_real_state_serialize = []
    for real_state in get_real_state:
        all_real_state_serialize.append(real_state.serialize())
    response_body = {
        "status": "OK",
        "count_real_states": len(all_real_state_serialize),
        "response": all_real_state_serialize
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )

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
