from flask import Flask, jsonify, request, make_response
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_seeder import FlaskSeeder
from flask_bcrypt import Bcrypt
from flask_security import Security
from flask_mail import Mail
from flask import url_for, current_app
from flask_mail import Message
#from flask_marshmallow import Marshmallow
# from flask_restful import Api, Resource
# from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import json
#import jsonpickle
import datetime
from functools import wraps
import itertools
import click
import os
import logging
import random
import string

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


def setLogger(app):
    
    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')

    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format = logFormatStr, filename = log_file, level=logging.ERROR)
    formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler(log_file)
    fileHandler.setLevel(logging.ERROR)
    fileHandler.setFormatter(formatter)

    app.logger.addHandler(fileHandler)
    app.logger.info("Logging is set up.")
    
    

DEBUG=True



app = Flask(__name__)

setLogger(app)
app.config.from_object(Config)
cors = CORS(app, resources={r"/api/*": {"origins": [Config.CORS_ORIGINS]}})
#app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)
Bcrypt().init_app(app)
Security().init_app(app, datastore=user_datastore)
Mail().init_app(app)
ma.init_app(app)

seeder = FlaskSeeder()
seeder.init_app(app, db)
#api = Api(app)


# custom commands

def generate_random_string(N = 7):
    
    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return str(res)


@click.command(name="crear_usuario")
@with_appcontext
@click.argument("name", nargs=1)
@click.argument("email", nargs=1)
@click.argument("area", nargs=1)
@click.argument("roles", nargs=-1)
def crear_usuario(name, email, area, roles):
    try:

        model_area = IRA_Organization_areas.query.filter_by(Organization_area=area).first()

        if model_area:
            id_area = model_area.id_organization_area
        else:
            id_area = None

        new_user = user_datastore.create_user(username=name, email=email, id_organization_area=id_area,
                                                password=hash_password(generate_random_string()))
        db.session.add(new_user)
        for role in roles:
            click.echo(f"role {role}")
            r = Role.query.filter_by(name=role).first()
            user_datastore.add_role_to_user(new_user, r)

        db.session.commit()
    except exc.IntegrityError as ei:
        print('Duplicidad de Email, usuario ya existe!')

    except Exception as ee:
        print('Se presentó un problema con la creación del usuario!')
        print(ee)

@click.command(name="eliminar_usuario")
@with_appcontext
@click.argument("email", nargs=1)
def eliminar_usuario(email):
    user = User.query.filter_by(email=email).first()
    user_datastore.delete_user(user)
    db.session.commit()

@click.command(name="agregar_roles_usuario")
@with_appcontext
@click.argument("email", nargs=1)
@click.argument("roles", nargs=-1)
def agregar_roles_usuario(email, roles):
    user = User.query.filter_by(email=email).first()
    if (user):
        for role in roles:
            click.echo(f"role {role} fue agregado al usuario")
            r = Role.query.filter_by(name=role).first()
            user_datastore.add_role_to_user(user, r)

        db.session.commit()
    else:
        print('usuario no existe!')

@click.command(name="remover_roles_usuario")
@with_appcontext
@click.argument("email", nargs=1)
@click.argument("roles", nargs=-1)
def remover_roles_usuario(email, roles):
    user = User.query.filter_by(email=email).first()
    if (user):
        for role in roles:
            click.echo(f"role {role} fue removido del usuario")
            r = Role.query.filter_by(name=role).first()
            user_datastore.remove_role_from_user(user, r)

        db.session.commit()
    else:
        print('usuario no existe!')

# CLI User/Role management
app.cli.add_command(crear_usuario)
app.cli.add_command(eliminar_usuario)
app.cli.add_command(agregar_roles_usuario)
app.cli.add_command(remover_roles_usuario)



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
            return jsonify({'message' : 'login.missing_token'}), 401

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # print(' data  decoded es...')
            # print(data)
            current_user = User.query.filter_by(email=data['email']).first()
        except Exception as e:
            app.logger.error(f" jwt decode error= {e}")
            print(e)

            return jsonify({'message' : 'login.invalid_token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def home():
    return jsonify('Hello World!')

@app.route('/api/v1/login', methods=['POST'])
def login():
    
    auth = request.get_json()
    #print(auth['email'])
   # app.logger.info("Entra a Login")

    if not auth or not auth['email'] or not auth['password']:
       # app.logger.info("missing credentials")
       #return make_response('login.missing_credentials', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return make_response('login.missing_credentials', 401)

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
       # app.logger.info("user_not_registered")
        return make_response('login.user_not_registered', 401)


    # if check_password_hash(user.password, auth['password']):
    if verify_password(auth['password'],user.password):
        
        roles = roles_schema.dump(user.roles)
       # app.logger.info(f'password si coincide!! Roles=> {roles}')
        try:
            token = jwt.encode({'id':user.id, 
                                'username' : user.username, 
                                'email':user.email, 
                                'roles': roles, 
                                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, 
                               app.config['SECRET_KEY'])
           # app.logger.info(f'token {token}')
            return jsonify({'token' : token})
        except Exception as e:
            app.logger.error(f'Error=> {e}')
        

    return make_response('login.bad_credentials', 401)


def send_reset_email(user,language='es'):
    token = user.get_reset_token()
    app.logger.info(f"reset token= {token}")
    app.logger.info(f"username= {app.config['MAIL_USERNAME']}")
    msg = Message('Password Reset Request',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[user.email])
    href_url=f"{app.config['APP_URL']}/reset-password/{user.email}/{token}"
    if(language=='es'):
        msg.html = f'''
        <h3> Hola {user.username} </h3>
        <p>Para cambiar su contaseña, haga click en el siguiente enlace: <a href='{href_url}'>Reiniciar contraseña</a></p>
        <p>Si usted no realizó esta solicitud por favor ignore este mensaje, ninguna modificación a su contraseña será realizada.<p>
        '''
    else:
        msg.html = f'''
        <h3> Hello {user.username} </h3>
        <p>To reset your password, visit the following link: <a href='{href_url}'>Reset password</a></p>
        <p>If you did not make this request then simply ignore this email and no changes will be made.<p>
        '''
        
    Mail().send(msg)



@app.route('/api/v1/request_password_reset', methods=['POST'])
def request_password_reset():
    
    data = request.get_json()
    # print(data['email'])
    # app.logger.info("Entra a request_password_reset")

    if not data or not data['email']:
        app.logger.info("missing email")
       #return make_response('login.missing_credentials', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return make_response('login.missing_email', 401)

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        app.logger.info("user_not_registered")
        return make_response('login.user_not_registered', 401)
    
    try:
        send_reset_email(user,data['lang'])
        return make_response('login.reset_password.email_sent', 200)
    except Exception as e:
        app.logger.error(f'Error=> {e}')
        return make_response('login.reset_password.email_error', 500)
    

@app.route("/api/v1/reset_password", methods=['POST'])
def reset_password():
    
    data = request.get_json()
    app.logger.info(f"data={data}")
    
    user = User.verify_reset_token(data['token'])
    if user is None:
        return make_response('login.reset_password.invalid_or_expired_token', 401)
       
    if (data['password'] == data['confirmation_password']):
        hashed_password = hash_password(data['password'])
        user.password = hashed_password
        db.session.commit()
        return make_response('login.reset_password.pwd_reset_successful', 200)
    else:
        return make_response('login.confirmation_pwd_not_match', 401)
    

    
   

@app.route('/api/v1/users', methods=['GET'])
@token_required
def users(current_user):
#def users():
    resp = User.query.order_by(User.username).all()
    return jsonify(users_schema.dump(resp))


@app.route('/api/v1/cycles', methods=['GET'])
@token_required
def cycles(current_user):
#def cycles():
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
 
      #  print(f"New Ids={new_ids}")
    
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
        
        actor_interaction = IRA_Employees_interactions.query.filter_by(id_cycle=data['cycle_id'],id_responding_employee=current_user.id,id_interacting_employee=data['item_id']).first()
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
                        existing_actor=next(filter(lambda x: x['item_id'] == data['item_id'],current_response),None)
                        if( existing_actor is not  None):
                            current_response = list(filter(lambda x: x['item_id'] != data['item_id'], current_response))
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
            "item_id":data['item_id'],
            "valor":data["selected_option"]
        }
        
        # print(data["selected_option"])
        adjacency_input_form_code=str(data['cycle_id']) +'-'+ str(current_user.id) + '-' + str(data['network_mode_id'])
        #print(adjacency_input_form_code)
        existing_response = IRA_Responses.query.filter_by(id_question = data['question_id'],id_adjacency_input_form=adjacency_input_form_code).first()
       # print(existing_response)
        if(existing_response):
            current_responses=json.loads(existing_response.Response)
           # print(current_responses)
            existing_actor=next(filter(lambda x: x['item_id'] == data['item_id'],current_responses),None)
            if(data["selected_option"] is not None and existing_actor is None):
                current_responses.append(new_response)        
            elif(data["selected_option"] is not None and existing_actor is not  None):
                current_responses = list(filter(lambda x: x['item_id'] != data['item_id'], current_responses))
                current_responses.append(new_response)
            elif(data["selected_option"] is None and existing_actor is not  None):
                current_responses = list(filter(lambda x: x['item_id'] != data['item_id'], current_responses))
            
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
        
            
          
    return jsonify("main_page.answer_saved")



if __name__ == '__main__':
    app.run()