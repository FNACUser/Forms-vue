
from flask import Flask, jsonify, request, make_response
from flask.cli import with_appcontext
from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_seeder import FlaskSeeder
from flask_bcrypt import Bcrypt
from flask_security import Security
from flask_security.utils import hash_password, verify_password
from flask_mail import Mail, Message
from flask_migrate import Migrate
# from flask_user import roles_required

# from flask_security import login_user, current_user, logout_user, login_required
# from flask import url_for, current_app
# from flask_marshmallow import Marshmallow
# from flask_restful import Api, Resource
# from werkzeug.security import generate_password_hash, check_password_hash
# import jsonpickle

import jwt
import json
from datetime import datetime, timedelta
from functools import wraps
import itertools
import click
import os
import logging
import random
import string

from config import Config
from models import *


def setLogger(app):

    root = os.path.dirname(os.path.abspath(__file__))
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'app.log')

    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=logFormatStr,
                        filename=log_file, level=logging.ERROR)
    formatter = logging.Formatter(logFormatStr, '%m-%d %H:%M:%S')
    fileHandler = logging.FileHandler(log_file)
    fileHandler.setLevel(logging.ERROR)
    fileHandler.setFormatter(formatter)

    app.logger.addHandler(fileHandler)
    app.logger.info("Logging is set up.")


DEBUG = True


app = Flask(__name__)

setLogger(app)
app.config.from_object(Config)
cors = CORS(app, resources={
            r"/api/*": {"origins": [app.config['CORS_ORIGINS']]}})
# app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)
Bcrypt().init_app(app)
Security().init_app(app, datastore=user_datastore)
Mail().init_app(app)
ma.init_app(app)
migrate = Migrate(app,db)

seeder = FlaskSeeder()
seeder.init_app(app, db)

# api = Api(app)

# seeder
# custom commands


def generate_random_string(N=7):

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
        model_area = IRA_Organization_areas.query.filter_by(
            Organization_area_es=area).first()

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


@click.command(name="drop_create_db")
@with_appcontext
def drop_create_db():
    db.drop_all()
    db.create_all()
    
@click.command(name="drop_db")
@with_appcontext
def drop_db():
    db.drop_all()


# CLI User/Role management
app.cli.add_command(crear_usuario)
app.cli.add_command(eliminar_usuario)
app.cli.add_command(agregar_roles_usuario)
app.cli.add_command(remover_roles_usuario)

# DB management
app.cli.add_command(drop_create_db)
app.cli.add_command(drop_db)


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
            return jsonify({'message': 'login.missing_token'}), 401

        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # print(' data  decoded es...')
            # print(data)
            current_user = User.query.filter_by(email=data['email']).first()
        except Exception as e:
            app.logger.error(f" jwt decode error= {e}")
            print(e)

            return jsonify({'message': 'login.invalid_token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def home():
    return jsonify('Hello World!')


@app.route('/api/v1/login', methods=['POST'])
def login():

    MAX_TOKEN_LIFE = 60

    auth = request.get_json()
    # print(auth['email'])
   # app.logger.info("Entra a Login")

    if not auth or not auth['email'] or not auth['password']:
       # app.logger.info("missing credentials")
       # return make_response('login.missing_credentials', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return make_response('login.missing_credentials', 401)

    user = User.query.filter_by(email=auth['email']).first()

    if not user:
       # app.logger.info("user_not_registered")
        return make_response('login.user_not_registered', 401)

    # if check_password_hash(user.password, auth['password']):
    if verify_password(auth['password'], user.password):

        roles = roles_schema.dump(user.roles)

       # app.logger.info(f'password si coincide!! Roles=> {roles}')
        try:

            token = jwt.encode({'id': user.id,
                                'username': user.username,
                                'email': user.email,
                                'roles': roles,
                                'exp': datetime.utcnow() + timedelta(minutes=MAX_TOKEN_LIFE)},
                               app.config['SECRET_KEY'])

            # app.logger.info(f'token {token}')
            return jsonify({'token': token})
        except Exception as e:
            print(e)
            app.logger.error(f'Error=> {e}')

    return make_response('login.bad_credentials', 401)


def send_reset_email(user, language='es'):
    token = user.get_reset_token()
    href_url = f"{app.config['APP_URL']}/reset-password/{user.email}/{token}"
    subject = ""
    body = ""

    if (language == 'es'):
        subject = "Restablecer contraseña"
        body = f'''
        <h3> Hola {user.username} </h3>
        <p>Para cambiar su contaseña, haga click en el siguiente enlace: <a href='{href_url}'>Reiniciar contraseña</a></p>
        <p>Si usted no realizó esta solicitud por favor ignore este mensaje, ninguna modificación a su contraseña será realizada.<p>
        '''
    else:
        subject = "Password reset"
        body = f'''
        <h3> Hello {user.username} </h3>
        <p>To reset your password, visit the following link: <a href='{href_url}'>Reset password</a></p>
        <p>If you did not make this request then simply ignore this email and no changes will be made.<p>
        '''
    msg = Message(
        subject, sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.html = body

    Mail().send(msg)


@app.route('/api/v1/request_password_reset', methods=['POST'])
def request_password_reset():

    data = request.get_json()
    # print(data['email'])
    # app.logger.info("Entra a request_password_reset")

    if not data or not data['email']:
        app.logger.info("missing email")
       # return make_response('login.missing_credentials', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        return make_response('login.missing_email', 401)

    user = User.query.filter_by(email=data['email']).first()

    if not user:
        app.logger.info("user_not_registered")
        return make_response('login.user_not_registered', 401)

    try:
        send_reset_email(user, data['lang'])
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
        return make_response('login.invalid_or_expired_token', 401)

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
    # def users():
    resp = User.query.order_by(User.username).all()
    users_to_remove_str=app.config['REMOVE_USERS_FROM_LIST']
    if( users_to_remove_str):
        users_to_remove_list=users_to_remove_str.split(',')
        for user_to_remove_str in users_to_remove_list:
            user=User.query.filter_by(email=user_to_remove_str).first()
            if(user and user in resp):
                resp.remove(user)
                   
    if(current_user in resp):
        resp.remove(current_user)
    return jsonify(users_schema.dump(resp))


@app.route('/api/v1/create_user', methods=['POST'])
@token_required
def create_user(current_user):

    if(current_user and current_user.has_role('admin')):
        try:
            data = request.json
            area=IRA_Organization_areas.query.filter_by(Organization_area_es=data['area']).first()
            role=Role.query.filter_by(name=data['role']).first()
            new_user=User(
                username=data['username'],
                email=data['email'],
                documentID=data['documentID'],
                id_redmine=data['id_redmine'],
                password=hash_password(generate_random_string()),
                id_organization_area=area.id_organization_area,
                active=1,
                
            )
            db.session.add(new_user)
            new_user.roles.append(role)
            db.session.commit()
            return jsonify("api_responses.user_created"),200
        except exc.IntegrityError as ei:
            print('Duplicidad de Email, usuario ya existe!')
            return jsonify("api_responses.duplicated_user"),409
        except Exception as ee:
            print('Se presentó un problema con la creación del usuario!')
            print(ee)
            return jsonify("api_responses.error_creating_user"),422
    else:
        return jsonify("api_responses.user_not_authorized"), 401
    
@app.route('/api/v1/delete_user', methods=['POST'])
@token_required
def delete_user(current_user):

    if(current_user and current_user.has_role('admin')):
        try:
            data = request.json
            # role=Role.query.filter_by(name=data['role']).first()
            target_user=User.query.filter_by(email=data['email']).first()
            roles=target_user.roles
            print(roles)
            target_user.roles.remove(roles[0])
            db.session.delete(target_user)
            db.session.commit()
            return jsonify("api_responses.user_deleted"),200
        except Exception as ee:
            print('Se presentó un problema con la eliminación del usuario!')
            print(ee)
            return jsonify("api_responses.error_deleting_user"),422
    else:
        return jsonify("api_responses.user_not_authorized"), 401

@app.route('/api/v1/cycles', methods=['GET'])
@token_required
def cycles(current_user):
    resp = IRA_Cycles.query.all()
    return jsonify(cycles_schema.dump(resp))


@app.route('/api/v1/networks/<lang>', methods=['GET'])
@token_required
def network(current_user, lang):
    attribute_name = 'name_'+lang
    resp = IRA_Networks.query.order_by(
        getattr(IRA_Networks, attribute_name)).all()
    return jsonify(networks_schema.dump(resp))


@app.route('/api/v1/cycle/<int:cycle_id>/network_modes', methods=['GET'])
@token_required
def cycle_network_modes(current_user, cycle_id):

    cycle = IRA_Cycles.query.get(cycle_id)
    resp = cycle.networks_modes
    return jsonify(network_mode_schema.dump(resp))


@app.route('/api/v1/user/<int:user_id>/cycle/<int:cycle_id>/adjacency_input_forms', methods=['GET'])
@token_required
def adjacency_input_forms(current_user, user_id, cycle_id):

    input_forms = IRA_Adjacency_input_form.query.filter_by(
        id_cycle=cycle_id, id_employee=user_id).all()
    return jsonify(adjacency_input_forms_schema.dump(input_forms))


@app.route('/api/v1/areas', methods=['GET'])
@token_required
def areas(current_user):

    resp = IRA_Organization_areas.query.all()
    return jsonify(areas_schema.dump(resp))


@app.route('/api/v1/nodes_segments_categories', methods=['GET'])
@token_required
def nodes_segments_categories(current_user):

    resp = IRA_Nodes_segments_categories.query.order_by(
        IRA_Nodes_segments_categories.Node_segment_category).all()
    return jsonify(node_segment_category_schema.dump(resp))


@app.route('/api/v1/networks_modes_themes', methods=['GET'])
@token_required
def networks_modes_themes(current_user):

    resp = IRA_Networks_modes_themes.query.all()
    return jsonify(network_mode_theme_schema.dump(resp))


@app.route('/api/v1/questions', methods=['GET'])
@token_required
def questions(current_user):

    resp = IRA_Questions.query.all()
    return jsonify(questions_schema.dump(resp))


@app.route('/api/v1/network_mode/<int:network_mode_id>/questions', methods=['GET'])
@token_required
def network_mode_questions(current_user, network_mode_id):

    network_mode = IRA_Networks_modes.query.get(network_mode_id)
    resp = network_mode.questions
    return jsonify(questions_schema.dump(resp))


@app.route('/api/v1/network_mode/<int:network_mode_id>/nodes', methods=['GET'])
@token_required
def network_mode_nodes(current_user, network_mode_id):

    network_mode = IRA_Networks_modes.query.get(network_mode_id)
    nodes = network_mode.nodes

    # print(current_user.id)
    filtered_nodes = []

    if nodes:
        filtered_nodes = [e for e in nodes if e.id_employee ==
                          None or e.id_employee == current_user.id]

    # print(filtered_nodes)

    return jsonify(nodes_schema.dump(filtered_nodes))


@app.route('/api/v1/questions_possible_answers', methods=['GET'])
@token_required
def possible_answer(current_user):

    resp = IRA_Questions_possible_answers.query.all()
    return jsonify(questions_possible_answers_schema.dump(resp))


@app.route('/api/v1/nodes', methods=['GET'])
@token_required
def nodes(current_user):

    resp = IRA_Nodes.query.all()
    # resp = IRA_Nodes.query.filter((IRA_Nodes.id_employee==None) | (IRA_Nodes.id_employee==current_user.id))
    # print(resp)

    return jsonify(nodes_schema.dump(resp))


@app.route('/api/v1/user/narrative/add', methods=['POST'])
@token_required
def add_narrative(current_user):

    data = request.json
    new_narrative = None
    if (data['user_email'] == current_user.email):

        adjacency_input_form_code = str(
            data['cycle_id']) + '-' + str(current_user.id) + '-' + str(data['network_mode_id'])

        adjacency_input_form = IRA_Adjacency_input_form.query.get(
            adjacency_input_form_code)
        if (adjacency_input_form is None):

            db.session.add(IRA_Adjacency_input_form(id_adjacency_input_form=adjacency_input_form_code,
                                                    id_employee=current_user.id, id_cycle=data['cycle_id'], id_network_mode=data['network_mode_id'], Is_concluded=0))

        new_narrative = IRA_Narratives(
            title=data['title'],
            narrative=data['narrative'],
            id_cycle=data["cycle_id"],
            id_employee=current_user.id)

        db.session.add(new_narrative)
        # db.session.flush()
        db.session.commit()

    return jsonify({'response': narrative_schema.dump(new_narrative), 'message': "api_responses.data_saved"})


@app.route('/api/v1/user/narrative/update', methods=['POST'])
@token_required
def update_narrative(current_user):

    data = request.json
    narrative = None
    if (data['user_email'] == current_user.email):

        narrative = IRA_Narratives.query.get(data['narrative_id'])
        narrative.title = data['title'],
        narrative.narrative = data['narrative'],
        db.session.commit()
        return jsonify("api_responses.data_updated")

    return jsonify("api_responses.data_not_updated"), 500


@app.route('/api/v1/user/narrative/delete', methods=['DELETE'])
@token_required
def delete_narrative(current_user):

    data = request.json
    if (data['user_email'] == current_user.email):

        narrative = IRA_Narratives.query.filter_by(
            id_cycle=data['cycle_id'], id_employee=current_user.id).first()
        db.session.delete(narrative)
        db.session.commit()
        return jsonify("api_responses.item_deleted")

    return jsonify("api_responses.item_not_deleted"), 500


@app.route('/api/v1/node/add', methods=['POST'])
@token_required
def add_node(current_user):

    data = request.json
    if (data['user_email'] == current_user.email):

        new_node = IRA_Nodes(
            Node_es=data['name_es'],
            Node_en=data['name_en'],
            id_node_segment=data["node_segment_id"],
            id_employee=current_user.id)

        db.session.add(new_node)
        db.session.flush()

        node_nwtmode = nodes_vs_networks_modes.insert().values(
            id_node=new_node.id_node, id_network_mode=data["network_mode_id"])
        db.session.execute(node_nwtmode)

        db.session.commit()

    network_mode = IRA_Networks_modes.query.get(data["network_mode_id"])
    nodes = network_mode.nodes

    return jsonify({'response': nodes_schema.dump(nodes), 'message': "api_responses.data_saved"})


@app.route('/api/v1/node', methods=['DELETE'])
@token_required
def delete_node(current_user):

    data = request.json
    # print(data)
    if (data['user_email'] == current_user.email):

        # deleted_relations = nodes_vs_networks_modes.delete().where(id_node = data['item_id'])
        # db.session.execute(deleted_relations)

        adjacency_input_forms_ids = IRA_Adjacency_input_form.query\
            .with_entities(IRA_Adjacency_input_form.id_adjacency_input_form)\
            .filter_by(id_cycle=data['cycle_id'], id_employee=current_user.id, id_network_mode=data['network_mode_id'])\
            .all()
        adjacency_codes = list(itertools.chain(*adjacency_input_forms_ids))

        if (adjacency_codes):
            for code in adjacency_codes:
                existing_responses = IRA_Responses.query.filter_by(
                    id_adjacency_input_form=code).all()
                for response in existing_responses:
                    if (response):
                        current_response = json.loads(response.Response)
                        # print(current_response)
                        existing_item = next(
                            filter(lambda x: x['item_id'] == data['item_id'], current_response), None)
                        if (existing_item is not None):
                            current_response = list(
                                filter(lambda x: x['item_id'] != data['item_id'], current_response))
                            response.Response = json.dumps(current_response)

        db.session.delete(IRA_Nodes.query.get(data['item_id']))

        db.session.commit()

        network_mode = IRA_Networks_modes.query.get(data["network_mode_id"])
        nodes = network_mode.nodes

        return jsonify({'response': nodes_schema.dump(nodes), 'message': "api_responses.item_deleted"})

    return jsonify("api_responses.item_not_deleted"), 500


@app.route('/api/v1/selected_tool', methods=['DELETE'])
@token_required
def delete_selected_tool(current_user):

    data = request.json
    # print(data)
    if (data['user_email'] == current_user.email):

        adjacency_input_forms_ids = IRA_Adjacency_input_form.query\
            .with_entities(IRA_Adjacency_input_form.id_adjacency_input_form)\
            .filter_by(id_cycle=data['cycle_id'], id_employee=current_user.id, id_network_mode=data['network_mode_id'])\
            .all()
        adjacency_codes = list(itertools.chain(*adjacency_input_forms_ids))

        if (adjacency_codes):
            for code in adjacency_codes:
                existing_responses = IRA_Responses.query.filter_by(
                    id_adjacency_input_form=code).all()
                for response in existing_responses:
                    if (response):
                        current_response = json.loads(response.Response)
                        # print(current_response)
                        existing_item = next(
                            filter(lambda x: x['item_id'] == data['item_id'], current_response), None)
                        if (existing_item is not None):
                            current_response = list(
                                filter(lambda x: x['item_id'] != data['item_id'], current_response))
                            response.Response = json.dumps(current_response)

        db.session.commit()
        existing_responses = IRA_Responses.query.filter_by(
            id_adjacency_input_form=code).all()

        return jsonify({'response': responses_schema.dump(existing_responses), 'message': "api_responses.item_deleted"})

    return jsonify("api_responses.item_not_deleted"), 500


@app.route('/api/v1/networks_modes', methods=['GET'])
@token_required
def networks_modes(current_user):

    resp = IRA_Networks_modes.query.all()
    return jsonify(network_mode_schema.dump(resp))


@app.route('/api/v1/user/<int:user_id>/cycle/<int:cycle_id>/interacting_actors', methods=['GET'])
@token_required
def get_interacting_actors(current_user, user_id, cycle_id):

    # data = request.json
    # print(data)
    actors_ids = []

    # if(data['user_email']==current_user.email):

    interactions = IRA_Employees_interactions.query.with_entities(
        IRA_Employees_interactions.id_interacting_employee).filter_by(id_cycle=cycle_id, id_responding_employee=user_id).all()
    actors_ids = list(itertools.chain(*interactions))

    return jsonify(actors_ids)


@app.route('/api/v1/user/<int:user_id>/cycle/<int:cycle_id>/responses', methods=['GET'])
@token_required
def get_user_responses(current_user, user_id, cycle_id):

    # data = request.json
    # print(data)
    existing_responses = []

    # if(data['user_email']==current_user.email):

    adjacency_input_forms_ids = IRA_Adjacency_input_form.query.with_entities(
        IRA_Adjacency_input_form.id_adjacency_input_form).filter_by(id_cycle=cycle_id, id_employee=user_id).all()
    adjacency_codes = list(itertools.chain(*adjacency_input_forms_ids))

    if (adjacency_codes):
        existing_responses = IRA_Responses.query.filter(
            IRA_Responses.id_adjacency_input_form.in_(adjacency_codes)).all()

    return jsonify(responses_schema.dump(existing_responses))


@app.route('/api/v1/user/<int:user_id>/cycle/<int:cycle_id>/narratives', methods=['GET'])
@token_required
def get_user_narratives(current_user, user_id, cycle_id):

    user_narratives = []

    # if(data['user_email']==current_user.email):

    user_narratives = IRA_Narratives.query.filter_by(
        id_cycle=cycle_id, id_employee=user_id).all()

    return jsonify(narratives_schema.dump(user_narratives))


@app.route('/api/v1/open_close_adjacency_input_form', methods=['POST'])
@token_required
def open_close_adjacency_input_form(current_user):

    data = request.json

    existing_form = IRA_Adjacency_input_form.query.filter_by(
        id_adjacency_input_form=data['id_adjacency_input_form']).first()

    if (existing_form):
        existing_form.Is_concluded = data['closed']
        db.session.commit()
        return jsonify("api_responses.form_closed") if data['closed'] else jsonify("api_responses.form_opened")

    return jsonify("api_responses.no_adjacency_input_form_found"), 404


@app.route('/api/v1/add_interacting_actor', methods=['POST'])
@token_required
def add_interacting_actor(current_user):

    data = request.json
    # print(data)
    if (data['user_email'] == current_user.email):

        existing_actor = IRA_Employees_interactions.query.filter_by(
            id_cycle=data['cycle_id'], id_responding_employee=current_user.id,id_interacting_employee=data['actor_id'] ).first()
        
    
        # already_saved = list(itertools.chain(*interactions))

        # new_ids = list(set(data['employee_ids']).difference(already_saved))  

        # if len(new_ids):
        #     for new_id in new_ids:
        #         db.session.add(IRA_Employees_interactions(
        #             id_cycle=data['cycle_id'], id_responding_employee=current_user.id, id_interacting_employee=new_id))

        #     db.session.commit()
        
        if (existing_actor is None):
        
            db.session.add(IRA_Employees_interactions(
                        id_cycle=data['cycle_id'], id_responding_employee=current_user.id, id_interacting_employee=data['actor_id']))

            db.session.commit()
            return jsonify("api_responses.new_interacting_actor_added")
        else:
            return jsonify("api_responses.new_interacting_actor_already_exists"),422
            
    else:
        return jsonify("api_responses.user_not_authorized"),403
        


@app.route('/api/v1/delete_interacting_actor', methods=['DELETE'])
@token_required
def delete_interacting_actor(current_user):

    data = request.json

    # if(data['user_email']==current_user.email and current_user.has_role("encuestado")):
    if (data['user_email'] == current_user.email):

        actor_interaction = IRA_Employees_interactions.query.filter_by(
            id_cycle=data['cycle_id'], id_responding_employee=current_user.id, id_interacting_employee=data['item_id']).first()

        actor_network = IRA_Networks.query.get(data['network_id'])

        if (actor_network.code == 'actor'):
            actor_network_modes = actor_network.networks_modes

            if (actor_network_modes):

                actor_network_mode_ids = [
                    anm.id_network_mode for anm in actor_network_modes]
                adjacency_input_forms_ids = IRA_Adjacency_input_form.query.with_entities(IRA_Adjacency_input_form.id_adjacency_input_form)\
                    .filter(IRA_Adjacency_input_form.id_cycle == data['cycle_id'], IRA_Adjacency_input_form.id_employee == current_user.id,
                            IRA_Adjacency_input_form.id_network_mode.in_(actor_network_mode_ids)).all()
                adjacency_codes = list(
                    itertools.chain(*adjacency_input_forms_ids))

                if actor_interaction:
                    db.session.delete(actor_interaction)

                if (adjacency_codes):
                    for code in adjacency_codes:
                        existing_responses = IRA_Responses.query.filter_by(
                            id_adjacency_input_form=code).all()
                        for response in existing_responses:
                            if (response):
                                current_response = json.loads(
                                    response.Response)
                                # print(current_response)
                                existing_actor = next(
                                    filter(lambda x: x['item_id'] == data['item_id'], current_response), None)
                                if (existing_actor is not None):
                                    current_response = list(
                                        filter(lambda x: x['item_id'] != data['item_id'], current_response))
                                    response.Response = json.dumps(
                                        current_response)
                db.session.commit()
                return jsonify("api_responses.interacting_actor_deleted")

    else:
        return jsonify("api_responses.user_not_authorized"),403


@app.route('/api/v1/save_answer', methods=['POST'])
@token_required
def save_answer(current_user):

    data = request.json
   # print(data)
    # print(current_user.has_role("admin"))
    # print(current_user.id)
    # if(data['user_email']==current_user.email and current_user.has_role("encuestado")):

    existing_responses = []

    if (data['user_email'] == current_user.email):

        new_response = {
            "item_id": data['item_id'],
            "valor": data["selected_option"]
        }

        # print((data["selected_option"] is None))
        # print(new_response)
        adjacency_input_form_code = str(
            data['cycle_id']) + '-' + str(current_user.id) + '-' + str(data['network_mode_id'])
        # print(adjacency_input_form_code)
        existing_response = IRA_Responses.query.filter_by(
            id_question=data['question_id'], id_adjacency_input_form=adjacency_input_form_code).first()

        if (existing_response):
            # print('Existen ya respuestas almacenadas =>')
            current_responses = json.loads(existing_response.Response)
            # print('current_responses 0=')
            # print(current_responses)
            existing_actor = next(
                filter(lambda x: x['item_id'] == data['item_id'], current_responses), None)
            #  print('existing_actor=')
            # print(existing_actor)
            # if actor/item does not exist and there is a new  valid response then append new_response
            if (not isResponseEmpty(data["selected_option"]) and existing_actor is None):
                current_responses.append(new_response)
            #    print('Agrega nueva respuesta e item no existe=> agrega nuevo elemento')
            #    print('current_responses 1=')
            #    print(current_responses)
            # if actor/item exists and there is a valid response
            elif (not isResponseEmpty(data["selected_option"]) and existing_actor is not None):
                #    print('Agrega nueva respuesta e item ya existe=> reemplaza los valores ya existentes')
                current_responses = list(
                    filter(lambda x: x['item_id'] != data['item_id'], current_responses))
            #    print('respuesta es valida y actor/item existe=')
                current_responses.append(new_response)
            #    print('current_responses 2=')
            #   print(current_responses)
            elif (isResponseEmpty(data["selected_option"]) and existing_actor is not None):
                #   print('Como la respuesta  es vacía y el  item ya  existe=> remueve el item presente de las respuestas totales')
                current_responses = list(
                    filter(lambda x: x['item_id'] != data['item_id'], current_responses))
            #   print('current_responses 3=')
            #   print(current_responses)
            existing_response.Response = json.dumps(current_responses)
            db.session.commit()
        else:
            if not isResponseEmpty(data["selected_option"]):
               # print('No existen respuestas previas y la nueva respuesta no esta vacía => se agrega la nueva respuesta')
                adjacency_input_form = IRA_Adjacency_input_form.query.get(
                    adjacency_input_form_code)
                if (adjacency_input_form is None):
                   # print('No existe numero de formulario, entonces se crea uno nuevo  =>')
                    db.session.add(IRA_Adjacency_input_form(id_adjacency_input_form=adjacency_input_form_code,
                                   id_employee=current_user.id, id_cycle=data['cycle_id'], id_network_mode=data['network_mode_id'], Is_concluded=0))
                    db.session.commit()
                response = []
                response.append(new_response)
                # print(response)
                db.session.add(IRA_Responses(
                    id_question=data['question_id'], id_adjacency_input_form=adjacency_input_form_code, Response=json.dumps(response)))
                db.session.commit()

        adjacency_input_forms_ids = IRA_Adjacency_input_form.query.with_entities(
            IRA_Adjacency_input_form.id_adjacency_input_form).filter_by(id_cycle=data['cycle_id'], id_employee=current_user.id).all()
        adjacency_codes = list(itertools.chain(*adjacency_input_forms_ids))

        if (adjacency_codes):
            existing_responses = IRA_Responses.query.filter(
                IRA_Responses.id_adjacency_input_form.in_(adjacency_codes)).all()

        return jsonify({'responses': responses_schema.dump(existing_responses), 'message': "api_responses.answer_saved"})
    
    else:
        return jsonify("api_responses.user_not_authorized"),403


def isResponseEmpty(response):

    if type(response) == list:
        return not response
    else:
        return response is None


# -----------------------------------------------------------------------------------------------------------
# CVF CULTURE api routes
# -----------------------------------------------------------------------------------------------------------


@app.route('/api/v1/culture/modes', methods=['GET'])
@token_required
def culture_modes(current_user):

    resp = CVF_Culture_modes.query.all()
    return jsonify(culture_mode_schema.dump(resp))


@app.route('/api/v1/culture/quadrants', methods=['GET'])
@token_required
def culture_quadrants(current_user):
    # def culture_quadrants():

    resp = CVF_Culture_quadrants.query.all()
    return jsonify(culture_quadrant_schema.dump(resp))


@app.route('/api/v1/culture/modes_themes', methods=['GET'])
@token_required
def culture_modes_themes(current_user):
    # def culture_modes_themes():

    resp = CVF_Culture_modes_themes.query.all()
    return jsonify(culture_mode_theme_schema.dump(resp))


@app.route('/api/v1/culture/modes_themes_questions', methods=['GET'])
@token_required
def culture_modes_themes_questions(current_user):
    # def culture_modes_themes_questions():

    resp = CVF_Culture_modes_themes_questions.query.all()
    return jsonify(culture_mode_theme_question_schema.dump(resp))


@app.route('/api/v1/culture/questions_responses', methods=['GET'])
@token_required
def culture_questions_responses(current_user):
    # def culture_questions_responses():

    resp = CVF_Questions_responses.query.all()
    return jsonify(culture_question_response_schema.dump(resp))


@app.route('/api/v1/culture/themes_responses', methods=['GET'])
@token_required
def culture_themes_responses(current_user):
    # def culture_themes_responses():

    resp = CVF_Themes_responses.query.all()
    return jsonify(culture_theme_response_schema.dump(resp))


@app.route('/api/v1/culture/mode/<int:mode_id>/themes', methods=['GET'])
@token_required
def get_culture_themes_by_mode(current_user, mode_id):

    themes = CVF_Culture_modes_themes.query.filter_by(
        id_culture_mode=mode_id).all()

    return jsonify(culture_mode_theme_schema.dump(themes))


@app.route('/api/v1/culture/theme/<int:theme_id>/questions', methods=['GET'])
@token_required
def get_culture_questions_by_theme(current_user, theme_id):

    questions = CVF_Culture_modes_themes_questions.query.filter_by(
        id_culture_mode_theme=theme_id).all()

    return jsonify(culture_mode_theme_question_schema.dump(questions))


@app.route('/api/v1/culture/save_answers', methods=['POST'])
@token_required
def culture_save_answers(current_user):

    data = request.json

    if (data['user_email'] == current_user.email):

        culture_input_form = CVF_Culture_input_form.query.filter_by(
            id_employee=current_user.id, id_cycle=data['cycle_id'], id_culture_mode=data['mode_id']).first()

        if not culture_input_form:
            db.session.add(CVF_Culture_input_form(id_employee=current_user.id,
                           id_cycle=data['cycle_id'], id_culture_mode=data['mode_id'], Is_concluded=0))
           # db.session.commit()
            culture_input_form = CVF_Culture_input_form.query.filter_by(
                id_employee=current_user.id, id_cycle=data['cycle_id'], id_culture_mode=data['mode_id']).first()

        theme_response = CVF_Themes_responses.query.filter_by(
            id_culture_input_form=culture_input_form.id, id_culture_mode_theme=data['theme_id']).first()

        if not theme_response:

            db.session.add(CVF_Themes_responses(id_culture_input_form=culture_input_form.id,
                           id_culture_mode_theme=data['theme_id'], Total_actual=0, Total_preferred=0, Is_concluded=0))
          #  db.session.commit()
            theme_response = CVF_Themes_responses.query.filter_by(
                id_culture_input_form=culture_input_form.id, id_culture_mode_theme=data['theme_id']).first()

        for question_answer in data['answers']:
            # print(question_answer)
            # question_answer=json.loads(answer)
            existing_response = CVF_Questions_responses.query.filter_by(
                id_theme_responses=theme_response.id, id_culture_mode_theme_question=question_answer['question_id']).first()

            if (existing_response):

                existing_response.Actual = question_answer['now']
                existing_response.Preferred = question_answer['preferred']
             #   db.session.commit()

            else:

                db.session.add(CVF_Questions_responses(id_theme_responses=theme_response.id,
                               id_culture_mode_theme_question=question_answer['question_id'], Actual=question_answer['now'], Preferred=question_answer['preferred']))
             #   db.session.commit()

        theme_response.Total_actual = 100
        theme_response.Total_preferred = 100
        db.session.commit()

    return jsonify({'message': "api_responses.answer_saved"})


@app.route('/api/v1/culture/user/<int:user_id>/cycle/<int:cycle_id>/mode/<int:mode_id>/theme/<int:theme_id>/answers', methods=['GET'])
@token_required
def get_culture_user_mode_theme_answers(current_user, user_id, cycle_id, mode_id, theme_id):

    culture_input_form = CVF_Culture_input_form.query.filter_by(
        id_employee=user_id, id_cycle=cycle_id, id_culture_mode=mode_id).first()

    if culture_input_form:

        theme_response = CVF_Themes_responses.query.filter_by(
            id_culture_input_form=culture_input_form.id, id_culture_mode_theme=theme_id).first()
        if theme_response:

            existing_answers = CVF_Questions_responses.query.filter_by(
                id_theme_responses=theme_response.id).all()
            return jsonify(culture_question_response_schema.dump(existing_answers))

    return jsonify({'message': "api_responses.no_results"})


@app.route('/api/v1/culture/user/<int:user_id>/cycle/<int:cycle_id>/mode/<int:mode_id>/themes_totals', methods=['GET'])
@token_required
def get_culture_user_mode_themes_totals(current_user, user_id, cycle_id, mode_id):

    culture_input_form = CVF_Culture_input_form.query.filter_by(
        id_employee=user_id, id_cycle=cycle_id, id_culture_mode=mode_id).first()

    if culture_input_form:

        themes_totals = CVF_Themes_responses.query.filter_by(
            id_culture_input_form=culture_input_form.id).all()
        return jsonify(culture_theme_response_schema.dump(themes_totals))

    return jsonify({'message': "api_responses.no_results"})


# -----------------------------------------------------------------------------------------------------------
# DataWise  api routes
# -----------------------------------------------------------------------------------------------------------

@app.route('/api/v1/datawise/user_tools', methods=['GET'])
@token_required
def get_user_tools(current_user):

    # school_roles = list(map(lambda x: x.school_role.name_en, current_user.school_roles))

    resp = DW_Tools.query.all()
    # print(resp)
    return jsonify(dw_tools_schema.dump(resp))


if __name__ == '__main__':
    app.run()
