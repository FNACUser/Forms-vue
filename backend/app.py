from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_security import Security
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource


from config import Config
#from defaultapp.miscelaneous import mail, bcrypt, security
from models import db,ma, user_datastore,Role
from models import User,IRA_Cycles,IRA_Networks, IRA_Organization_areas             
from models import users_schema,cycles_schema,networks_schema, networkmodes_schema,areas_schema


DEBUG=True

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resources={r"/api/*": {"origins": [Config.CORS_ORIGINS]}})

db.init_app(app)
Bcrypt().init_app(app)
Security().init_app(app, datastore=user_datastore)
ma.init_app(app)
#api = Api(app)


@app.route('/', methods=['GET'])
def home():
    return jsonify('Hello World!')


@app.route('/api/v1/users', methods=['GET'])
def users():
    resp = User.query.order_by(User.username).all()
    return jsonify(users_schema.dump(resp))

@app.route('/api/v1/cycles', methods=['GET'])
def cycles():
    resp = IRA_Cycles.query.all()
    return jsonify(cycles_schema.dump(resp))

@app.route('/api/v1/networks', methods=['GET'])
def network():
    resp = IRA_Networks.query.order_by(IRA_Networks.name).all()
    return jsonify(networks_schema.dump(resp))

@app.route('/api/v1/cycle/<int:cycle_id>/network_modes', methods=['GET'])
def cycle_network_modes(cycle_id):
    cycle = IRA_Cycles.query.get(cycle_id)
    
    resp = cycle.networks_modes
    return jsonify(networkmodes_schema.dump(resp))

@app.route('/api/v1/areas', methods=['GET'])
def areas():
    resp = IRA_Organization_areas.query.order_by(IRA_Organization_areas.Organization_area).all()
    return jsonify(areas_schema.dump(resp))


if __name__ == '__main__':
    app.run()