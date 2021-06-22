"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, make_response, session
from flask.typing import StatusCode
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from sqlalchemy.orm import query
from werkzeug.wrappers import response
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, RealState, Agent, Transaction
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "01cdeef14f0a17d28d723f35a2ba3670"
app.config.from_mapping(
    CLOUDINARY_URL=os.environ.get("CLOUDINARY_URL")
)
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
        request_body["id_document"],
        request_body["password"])
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
    user.name = request_body["name"]
    user.last_name = request_body["last_name"]
    user.phone = request_body["phone"]
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
def handle_get_all_real_state():
    get_real_state = RealState.query.all()
    all_real_state_serialize = []
    for real_state in get_real_state:
        all_real_state_serialize.append(real_state.serialize())

    response_body = {
        "status": "OK",
        "count_real_states": len(all_real_state_serialize),
        "response": all_real_state_serialize,
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
def handled_post_real_state():
    data = request.json
    if data is None:
        raise APIException('Bad Request: el servidor no pudo interpretar la solicitud dada una sintaxis inválida.', status_code=400)

    if data["name"] == "":
        return jsonify({"message":"El nombre no puede ser vacio"}), 400
    if data["location"] == "":
        return jsonify({"message":"Debes ingresar la localizacion del inmueble"}), 400
    new_real_state = RealState(
        data["name"],
        data["description"],
        data["location"],
        data["total_area"],
        data["builded_surface"],
        data["rooms"],
        data["bathrooms"],
        data["parkings"]
    )
    db.session.add(new_real_state)
    db.session.commit()

    response_body = {
        "status": "OK",
        "result": f"Inmueble {new_real_state.name} ha sido creado con exito."
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

@app.route("/real_state/<realState_id>", methods=["DELETE"])
def handled_delete_real_state(realState_id):
    real_state = RealState.query.get(realState_id)
    db.session.delete(real_state)
    db.session.commit()

    response_body = {
        "status": "OK",
        "result": f"Inmueble {real_state.name} ha sido borrado de la lista."
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

@app.route("/real_state/change/<realState_id>", methods=["PUT"])
def handled_update_real_state(realState_id):
    data = request.json
    if data is None:
        raise APIException('Bad Request: el servidor no pudo interpretar la solicitud dada una sintaxis inválida.', status_code=400)

    real_state = RealState.query.get(realState_id)
    real_state.name = data["name"]
    real_state.description = data["description"]
    real_state.locatio = data["location"]
    real_state.total_area = data["total_area"]
    real_state.builded_surface = data["builded_surface"]
    real_state.rooms = data["rooms"]
    real_state.bathrooms = data["bathrooms"]
    real_state.parkings = data["parkings"]
    db.session.commit()

    response_body = {
        "status": "OK",
        "result": f"Inmueble {real_state.name} ha sido actualizado de la lista."
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

@app.route('/real_state/seach/<realState_id>', methods=['GET'])
def handled_get_real_state(realState_id):
    real_state = RealState.query.get(realState_id)
    response_body = {
        "status": "OK",
        "response": real_state.serialize()
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

@app.route('/real_state/seach_rs/<location>', methods=['GET'])
def handled_src_location_real_state(location):
    search = "%{}%".format(location)
    print(search)
    rs_by_name = RealState.query.filter(RealState.location.like(search)).all()
    all_rs_serialize = []
    for real_state in rs_by_name:
        all_rs_serialize.append(real_state.serialize())
    response_body = {
        "status": "OK",
        "count": len(all_rs_serialize),
        "response": all_rs_serialize
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
    
@app.route("/signup/agent", methods=['POST', 'GET'])
def sign_up_agent():
    data = request.json

    if data is None:
        raise APIException("Los campos no pueden estart vacios", status_code=400)
    if 'email' not in data:
        raise APIException('Necesita especificar un email', status_code=400)
    if 'password' not in data:
        raise APIException('Necesita especificar una contraseña', status_code=400)
    if 'name' not in data:
        raise APIException('Necesita especificar su nombre', status_code=400)
    if 'last_name' not in data:
        raise APIException('Necsita especificar su apellido', status_code=400)
    if 'phone' not in data:
        raise APIException('Necesita colocar su número telefónico', status_code=400)
    
    agent = Agent.create(email=data.get('email'), password=data.get('password'), name=data.get('name'), last_name=data.get('last_name'), phone=data.get('phone'), description=data.get('description'))
    if not isinstance(agent, Agent):
        return jsonify({"msg": "tuve problemas, lo siento"}), 500
    return jsonify(agent.serialize()), 201

@app.route("/log-in/agent", methods=['POST'])
def log_in_agent():
    print(request.data)
    print(request.json)
    data = request.json
    agent = Agent.query.filter_by(email=data['email']).one_or_none()
    if agent is None: 
        return jsonify({"msg": "sin registrar"}), 404
    if not agent.check_password(data.get('password')):
        return jsonify({"msg": "bad credentials"}), 400
    token = create_access_token(identity=agent.id)
    return jsonify({
        "agent": agent.serialize(),
        "token": token
    }), 200

@app.route('/agent/profile', methods=['POST'])
def create_agent():
    data = request.json

    new_agent =Agent(
        data["email"],
        data["name"],
        data["last_name"],
        data["phone"],
        data["description"])
    db.session.add(new_agent)
    db.session.commit()
    response_body ={
          "status": "Perfil creado exitosamente"
    }
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

@app.route('/agent/profile/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    agent = Agent.query.get(agent_id)
    data= request.json
    agent.email = data["email"]
    agent.name = data["name"]
    agent.last_name = data["last_name"]
    agent.phone = data["phone"]
    agent.password = data["password"]
    agent.description = data["description"]
    db.session.commit()
    
    response_body = {
        "status": " actualizado"
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

@app.route('/agent/<agent_id>', methods=['GET'])
def get_agent_id(agent_id):
    agent = Agent.query.get(agent_id)
    response_body = {
        "status": "OK",
        "response": agent.serialize()
    
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

@app.route('/agent/all', methods=['GET'])
def get_agents():
    all_agents = Agent.query.all()
    all_agents_serialize = []
    for agent in all_agents:
        all_agents_serialize.append(agent.serialize())
    response_body = {
        "status": "OK",
        "response": all_agents_serialize
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

@app.route('/agent/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.get(agent_id)
    db.session.delete(agent)
    db.session.commit()
    response_body = {
        "status": "Agente borrado exitosamente"
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

@app.route('/realStateAgency', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/company-sign-up', methods=['POST'])
def company_sign_up():
    data=request.getjson()


@app.route('/transaction', methods=["GET","POST"])
def handled_transaction():

    headers={
        "Content-type":"application/json"
    }

    if request.method == 'GET':
        all_transaction = Transaction.query.all()
        all_transaction_serialize = []
        for transaction in all_transaction:
            all_transaction_serialize.append(transaction.serialize())
        response_body = {
            "status" : "OK",
            "results": all_transaction_serialize
        }
        status_code = 200

    elif request.method == 'POST':
        data = request.json

        new_transaction = Transaction(
            name = data["name"]
        )
        db.session.add(new_transaction)
        db.session.commit()
        response_body = {
            "status" : "OK",
            "results": f"Se ha creado correctamente {new_transaction.name}"
        }
        status_code = 200
    else:
        response_body={
            "status":"400_NO_EXISTE_EL_METODO_SELECCIONADO"
        }
        status_code = 404
    
    return make_response(
        jsonify(response_body),
        status_code,
        headers
    )


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
