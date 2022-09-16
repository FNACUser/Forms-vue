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
import itertools

from flask_security import login_user, current_user, logout_user, login_required
from flask_security.utils import hash_password,verify_password


from config import Config
#from defaultapp.miscelaneous import mail, bcrypt, security
from models import db,ma, user_datastore, Role
from models import User,IRA_Cycles,IRA_Networks, IRA_Organization_areas ,\
                    IRA_Nodes_segments_categories,IRA_Networks_modes_themes, IRA_Questions ,\
                    IRA_Questions_possible_answers, IRA_Nodes,IRA_Networks_modes, IRA_Employees_interactions,IRA_Responses,\
                    IRA_Adjacency_input_form     
from models import  users_schema, user_schema,cycles_schema, networks_schema, network_mode_schema, areas_schema,\
                    roles_schema, role_schema,node_segment_category_schema,\
                    network_mode_theme_schema,questions_schema,questions_possible_answers_schema, nodes_schema,responses_schema


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
            # print('token es...')
            # print("The variable type:", type(token))

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # print(' data  decoded es...')
            # print(data)
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
        token = jwt.encode({'id':user.id, 'username' : user.username, 'email':user.email, 'roles': roles, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
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
    return jsonify(network_mode_schema.dump(resp))

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
    #resp = IRA_Networks_modes_themes.query.order_by(IRA_Networks_modes_themes.Network_mode_theme).all()
    resp = IRA_Networks_modes_themes.query.all()
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
#def network_mode_nodes(current_user,cycle_id):
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
    return jsonify(network_mode_schema.dump(resp))


@app.route('/api/v1/user/<int:user_id>/cycle/<int:cycle_id>/interacting_actors', methods=['GET'])
# @token_required
# def interacting_actors(current_user,user_id,cycle_id):
def get_interacting_actors(user_id,cycle_id):

    # data = request.json
    # print(data)
    actors_ids=[]

    # if(data['user_email']==current_user.email):
        
    interactions = IRA_Employees_interactions.query.with_entities(IRA_Employees_interactions.id_interacting_employee).filter_by(id_cycle=cycle_id,id_responding_employee=user_id).all()
    actors_ids = list(itertools.chain(*interactions))
        
    
    return jsonify(actors_ids)


@app.route('/api/v1/user/<int:user_id>/cycle/<int:cycle_id>/responses', methods=['GET'])
# @token_required
# def interacting_actors(current_user,user_id,cycle_id):
def get_user_responses(user_id,cycle_id):

    # data = request.json
    # print(data)
    existing_responses = []

    # if(data['user_email']==current_user.email):
    
    adjacency_input_forms_ids= IRA_Adjacency_input_form.query.with_entities(IRA_Adjacency_input_form.id_adjacency_input_form).filter_by(id_cycle=cycle_id,id_employee=user_id).all()
    adjacency_codes = list(itertools.chain(*adjacency_input_forms_ids))
         
    if (adjacency_codes):
        existing_responses = IRA_Responses.query.filter(IRA_Responses.id_adjacency_input_form.in_(adjacency_codes)).all()
    
    
    return jsonify(responses_schema.dump(existing_responses))



@app.route('/api/v1/add_interacting_actor', methods=['POST'])
@token_required
def add_interacting_actor(current_user):
# def add_interacting_person():
    data = request.json
    #print(data)

    if(data['user_email']==current_user.email):
        
        interactions = IRA_Employees_interactions.query.with_entities(IRA_Employees_interactions.id_interacting_employee).filter_by(id_cycle=data['cycle_id'],id_responding_employee=current_user.id).all()
       
        already_saved = list(itertools.chain(*interactions))
        
        new_ids=list(set(data['employee_ids']).difference(already_saved))
 
        print(f"New Ids={new_ids}")
    
        if len(new_ids):
            for new_id in new_ids:
                db.session.add(IRA_Employees_interactions(id_cycle=data['cycle_id'],id_responding_employee=current_user.id,id_interacting_employee=new_id))
            
            db.session.commit()

        # remove_ids=list(set(already_saved).difference(data['employee_ids']))

        # print(f"Remove Ids={remove_ids}")

        # if len(remove_ids):
        #     for remove_id in remove_ids:
        #         actor_interaction = IRA_Employees_interactions.query.filter_by(id_cycle=data['cycle_id'],id_responding_employee=current_user.id,id_interacting_employee=remove_id).first()
        #         if actor_interaction:
        #             db.session.delete(actor_interaction)
        #             db.session.commit()


         
          
    return jsonify("interacting actors updated correctly!!")



@app.route('/api/v1/delete_interacting_actor', methods=['DELETE'])
@token_required
def delete_interacting_actor(current_user):

    data = request.json
    
    #if(data['user_email']==current_user.email and current_user.has_role("encuestado")):
    if(data['user_email']==current_user.email):
        
        actor_interaction = IRA_Employees_interactions.query.filter_by(id_cycle=data['cycle_id'],id_responding_employee=current_user.id,id_interacting_employee=data['actor_id']).first()
        adjacency_input_forms_ids= IRA_Adjacency_input_form.query.with_entities(IRA_Adjacency_input_form.id_adjacency_input_form).filter_by(id_cycle=data['cycle_id'],id_employee=current_user.id).all()
        adjacency_codes = list(itertools.chain(*adjacency_input_forms_ids))
        
        if actor_interaction:
            db.session.delete(actor_interaction)
        
        if (adjacency_codes):
            for code in adjacency_codes:
                existing_responses = IRA_Responses.query.filter_by(id_adjacency_input_form=code).all()
                for response in existing_responses:
                    if(response):
                        current_response=json.loads(response.Response)
                        #print(current_response)
                        existing_actor=next(filter(lambda x: x['id_actor'] == data['actor_id'],current_response),None)
                        if( existing_actor is not  None):
                            current_response = list(filter(lambda x: x['id_actor'] != data['actor_id'], current_response))
                            response.Response=json.dumps(current_response)
        db.session.commit()
            
          
    return jsonify("interacting actor was deleted and all answers related to this actor !!")



@app.route('/api/v1/save_answer', methods=['POST'])
@token_required
def save_answer(current_user):

    data = request.json
    #print(data)
    #print(current_user.has_role("admin"))

    #if(data['user_email']==current_user.email and current_user.has_role("encuestado")):
    
    if(data['user_email']==current_user.email ):
        
        new_response={
            "id_actor":data['actor_id'],
            "valor":data["selected_option"]
        }
        
        # print(data["selected_option"])
        adjacency_input_form_code=str(data['cycle_id']) +'-'+ str(current_user.id) + '-' + str(data['network_mode_id'])
        #print(adjacency_input_form_code)
        existing_response = IRA_Responses.query.filter_by(id_question = data['question_id'],id_adjacency_input_form=adjacency_input_form_code).first()
        print(existing_response)
        if(existing_response):
            current_responses=json.loads(existing_response.Response)
            print(current_responses)
            existing_actor=next(filter(lambda x: x['id_actor'] == data['actor_id'],current_responses),None)
            if(data["selected_option"] is not None and existing_actor is None):
                current_responses.append(new_response)        
            elif(data["selected_option"] is not None and existing_actor is not  None):
                current_responses = list(filter(lambda x: x['id_actor'] != data['actor_id'], current_responses))
                current_responses.append(new_response)
            elif(data["selected_option"] is None and existing_actor is not  None):
                current_responses = list(filter(lambda x: x['id_actor'] != data['actor_id'], current_responses))
            
           # print(current_responses)
            existing_response.Response=json.dumps(current_responses)
            db.session.commit()
        else:
            if(data["selected_option"] is not None):
                adjacency_input_form = IRA_Adjacency_input_form.query.get(adjacency_input_form_code)
                if(adjacency_input_form is None):
                    db.session.add(IRA_Adjacency_input_form(id_adjacency_input_form = adjacency_input_form_code ,id_employee=current_user.id, id_cycle=data['cycle_id'], id_network_mode=data['network_mode_id'], Is_concluded=0))
                    db.session.commit()    
                response = []
                response.append(new_response)
                #print(response)
                db.session.add(IRA_Responses(id_question = data['question_id'],id_adjacency_input_form = adjacency_input_form_code ,Response = json.dumps(response)))
                db.session.commit()    
        
            
          
    return jsonify("answer was saved correctly!!")






if __name__ == '__main__':
    app.run()