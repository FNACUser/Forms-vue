from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_security import Security
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
#import jsonpickle
import datetime
from functools import wraps

from flask_security import login_user, current_user, logout_user, login_required
from flask_security.utils import hash_password,verify_password


from config import Config
#from defaultapp.miscelaneous import mail, bcrypt, security
from models import db,ma, user_datastore, Role
from models import User,IRA_Cycles,IRA_Networks, IRA_Organization_areas ,\
                    IRA_Nodes_segments_categories,IRA_Networks_modes_themes, IRA_Questions ,\
                    IRA_Questions_possible_answers, IRA_Nodes,IRA_Networks_modes       
from models import  users_schema, user_schema,cycles_schema, networks_schema, network_modes_schema, areas_schema,\
                    networks_modes_schema, roles_schema, role_schema,node_segment_category_schema,\
                    network_mode_theme_schema,questions_schema,questions_possible_answers_schema, nodes_schema


DEBUG=True

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resources={r"/api/*": {"origins": [Config.CORS_ORIGINS]}})

db.init_app(app)
Bcrypt().init_app(app)
Security().init_app(app, datastore=user_datastore)
ma.init_app(app)
#api = Api(app)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print('HOLA')
        # print(request.headers)

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            print('token es...')
            print("The variable type:", type(token))

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            print(' data  decoded es...')
            print(data)
            current_user = User.query.filter_by(email=data['email']).first()
        except Exception as e:
            print(e)

            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def home():
    return jsonify('Hello World!')

@app.route('/api/v1/login', methods=['POST'])
def login():
    
    auth = request.get_json()
    #print(auth['email'])

    if not auth or not auth['email'] or not auth['password']:
        return make_response('Could not verify 1', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
        return make_response('Could not verify 2', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


    # if check_password_hash(user.password, auth['password']):
    if verify_password(auth['password'],user.password):
        
        roles = roles_schema.dump(user.roles)
        print(f'password si coincide!! { roles}')
        token = jwt.encode({'username' : user.username, 'email':user.email, 'roles': roles, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token})

    return make_response('Could not verify 3', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
   

@app.route('/api/v1/users', methods=['GET'])
#@token_required
#def users(current_user):
def users():
    resp = User.query.order_by(User.username).all()
    return jsonify(users_schema.dump(resp))

@app.route('/api/v1/cycles', methods=['GET'])
#@token_required
#def cycles(current_user):
def cycles():
    resp = IRA_Cycles.query.all()
    return jsonify(cycles_schema.dump(resp))

@app.route('/api/v1/networks/<lang>', methods=['GET'])
#@token_required
#def network(current_user):
def network(lang):
    attribute_name = 'name_'+lang
    resp = IRA_Networks.query.order_by(getattr(IRA_Networks,attribute_name)).all()
    return jsonify(networks_schema.dump(resp))

@app.route('/api/v1/cycle/<int:cycle_id>/network_modes', methods=['GET'])
#@token_required
#def cycle_network_modes(current_user,cycle_id):
def cycle_network_modes(cycle_id):   
    cycle = IRA_Cycles.query.get(cycle_id)   
    resp = cycle.networks_modes
    return jsonify(networks_modes_schema.dump(resp))

@app.route('/api/v1/areas', methods=['GET'])
#@token_required
#def areas(current_user):
def areas():
    #resp = IRA_Organization_areas.query.order_by(IRA_Organization_areas.Organization_area).all()
    
    resp = IRA_Organization_areas.query.all()
    return jsonify(areas_schema.dump(resp))


@app.route('/api/v1/nodes_segments_categories', methods=['GET'])
#@token_required
#def nodes_segments_categories(current_user):
def nodes_segments_categories():
    resp = IRA_Nodes_segments_categories.query.order_by(IRA_Nodes_segments_categories.Node_segment_category).all()
    return jsonify(node_segment_category_schema.dump(resp))


@app.route('/api/v1/networks_modes_themes', methods=['GET'])
#@token_required
#def networks_modes_themes(current_user):
def networks_modes_themes():
    resp = IRA_Networks_modes_themes.query.order_by(IRA_Networks_modes_themes.Network_mode_theme).all()
    return jsonify(network_mode_theme_schema.dump(resp))


@app.route('/api/v1/questions', methods=['GET'])
#@token_required
#def questions(current_user):
def questions():
    resp = IRA_Questions.query.all()
    return jsonify(questions_schema.dump(resp))


@app.route('/api/v1/network_mode/<int:network_mode_id>/questions', methods=['GET'])
#@token_required
#def network_mode_questions(current_user,cycle_id):
def network_mode_questions(network_mode_id):   
    network_mode = IRA_Networks_modes.query.get(network_mode_id)   
    resp = network_mode.questions
    return jsonify(questions_schema.dump(resp))


@app.route('/api/v1/network_mode/<int:network_mode_id>/nodes', methods=['GET'])
#@token_required
#def network_mode_nodes((current_user,cycle_id):
def network_mode_nodes(network_mode_id):   
    network_mode = IRA_Networks_modes.query.get(network_mode_id)   
    resp = network_mode.nodes
    return jsonify(nodes_schema.dump(resp))


@app.route('/api/v1/questions_possible_answers', methods=['GET'])
#@token_required
#def possible_answer(current_user):
def possible_answers():
    resp = IRA_Questions_possible_answers.query.all()
    return jsonify(questions_possible_answers_schema.dump(resp))


@app.route('/api/v1/nodes', methods=['GET'])
#@token_required
#def nodes(current_user):
def nodes():
    resp = IRA_Nodes.query.all()
    return jsonify(nodes_schema.dump(resp))


@app.route('/api/v1/networks_modes', methods=['GET'])
#@token_required
#def networks_modes(current_user):
def networks_modes():
    resp = IRA_Networks_modes.query.all()
    return jsonify(networks_modes_schema.dump(resp))


if __name__ == '__main__':
    app.run()