from datetime import datetime

from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

db = SQLAlchemy()
ma = Marshmallow()

########################################################################################################################################################################              
#                               SQLAlchemy Models            
######################################################################################################################################################################## 


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    id_redmine = db.Column(db.String(30), nullable=True)
    active = db.Column(db.Boolean)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )
    id_organization_area = db.Column(db.Integer,
                                     db.ForeignKey('IRA_Organization_areas.id_organization_area'),
                                     nullable=True)
    
    adjacency_forms = db.relationship('IRA_Adjacency_input_form',
                                      backref=db.backref('users', lazy=True))

    culture_input_forms = db.relationship('CVF_Culture_input_form',
                                          backref=db.backref('users', lazy=True))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def has_role(self, role):
        return role in self.roles

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    
class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))
    
    def toJson(self):
        return json.dumps({'role': self.name}).decode('utf-8')
        
    
    
    

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    

questions_vs_networks_modes = \
    db.Table('questions_vs_networks_modes',
             db.Column('id_question', db.Integer,
                       db.ForeignKey('IRA_Questions.id_question')),
             db.Column('id_network_mode', db.Integer,
                       db.ForeignKey('IRA_Networks_modes.id_network_mode')))

cycles_vs_networks_modes = \
    db.Table('cycles_vs_networks_modes',
             db.Column('id_cycle', db.Integer,
                       db.ForeignKey('IRA_Cycles.id_cycle')),
             db.Column('id_network_mode', db.Integer,
                       db.ForeignKey('IRA_Networks_modes.id_network_mode')))

nodes_vs_networks_modes = \
    db.Table('nodes_vs_networks_modes',
             db.Column('id_node', db.Integer,
                       db.ForeignKey('IRA_Nodes.id_node')),
             db.Column('id_network_mode', db.Integer,
                       db.ForeignKey('IRA_Networks_modes.id_network_mode')))


class IRA_Adjacency_input_form(db.Model):
    __tablename__ = 'IRA_Adjacency_input_form'
    id_adjacency_input_form = db.Column(db.String(15), primary_key=True)
    id_employee = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=False)
    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=False)

    id_network_mode = \
        db.Column(db.Integer,
                  db.ForeignKey('IRA_Networks_modes.id_network_mode'),
                  nullable=False)

    Is_concluded = db.Column(db.Boolean, nullable=False)

    responses = db.relationship('IRA_Responses',
                                backref=db.backref('adjacency_input_form',
                                                   lazy=True))

    db.UniqueConstraint('id_employee', 'id_cycle', 'id_network_mode',
                        name='uix_1')

    def __repr__(self):
        return f"IRA_Adjacency_input_form('{self.id_adjacency_input_form}'," \
               f"'{self.id_employee}','{self.id_cycle}','{self.id_network_mode}'," \
               f"'{self.Is_concluded}')"
               

class IRA_Cycles(db.Model):
    __tablename__ = 'IRA_Cycles'
    id_cycle = db.Column(db.Integer, primary_key=True)
    Cycle = db.Column(db.String(100), nullable=False)
    Initial_date = db.Column(db.DateTime, nullable=False)
    End_date = db.Column(db.DateTime, nullable=False)
    Is_active = db.Column(db.Boolean, nullable=False)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     secondary=cycles_vs_networks_modes,
                                     backref=db.backref('cycles',
                                                        lazy='dynamic'))

    adyacency_forms = db.relationship('IRA_Adjacency_input_form',
                                      backref=db.backref('cycle', lazy=True))

    culture_input_forms = db.relationship('CVF_Culture_input_form',
                                          backref=db.backref('cycle', lazy=True))

    # responses=db.relationship('IRA_Responses',
    #                             backref=db.backref('cycle',lazy=True))

    def __repr__(self):
        return f"IRA_Cycles('{self.id_cycle}', '{self.Cycle},'" \
               f"'{self.Initial_date}','{self.End_date}','{self.Is_active}')"


        
class IRA_Employees_interactions(db.Model):
    __tablename__ = 'IRA_Employees_interactions'
    id_employee_interaction = db.Column(db.Integer, primary_key=True)
    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=True)
    id_responding_employee = \
        db.Column(db.Integer,
                  db.ForeignKey('users.id'),
                  nullable=True)
    id_interacting_employee = \
        db.Column(db.Integer,
                  db.ForeignKey('users.id'),
                  nullable=True)

    def __repr__(self):
        return f"IRA_Employees_interactions('{self.id_employee_interaction}'," \
               f"'{self.id_cycle}','{self.id_responding_employee}'," \
               f"'{self.id_interacting_employee}')"


class IRA_Networks(db.Model):
    __tablename__ = 'IRA_Networks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    networks_modes = db.relationship('IRA_Networks_modes',
                                      backref=db.backref('network', lazy=True))
    
    def __repr__(self):
        return f"IRA_Networks('{self.name}')"
    

class IRA_Networks_modes(db.Model):
    __tablename__ = 'IRA_Networks_modes'
    id_network_mode = db.Column(db.Integer, primary_key=True)
    id_network = db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Networks.id'),
                  nullable=False)
    id_node_segment_category = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Nodes_segments_categories.id_node_segment_category'),
                  nullable=True)

    id_network_mode_theme = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Networks_modes_themes.id_network_mode_theme'),
                  nullable=True)

    adyacency_forms = db.relationship('IRA_Adjacency_input_form',
                                      backref=db.backref('network_mode', lazy=True))

    # responses=db.relationship('IRA_Responses',
    #                             backref=db.backref('network_mode',lazy=True))

    def __repr__(self):
        return f"IRA_Networks_modes('{self.id_network_mode}', \
            '{self.Network_mode}', \
            '{self.id_node_segment_category}','{self.id_network_mode_theme}')"


class IRA_Networks_modes_themes(db.Model):
    __tablename__ = 'IRA_Networks_modes_themes'
    id_network_mode_theme = db.Column(db.Integer, primary_key=True)
    Network_mode_theme = db.Column(db.String(100), nullable=False)

    network_modes = db.relationship('IRA_Networks_modes',
                                    backref=db.backref('network_mode_theme', lazy=True))

    def __repr__(self):
        return f"IRA_Networks_modes_themes('{self.id_network_mode_theme}', \
            '{self.Network_mode_theme}')"


class IRA_Nodes(db.Model):
    __tablename__ = 'IRA_Nodes'
    id_node = db.Column(db.Integer, primary_key=True)
    Node = db.Column(db.String(100), nullable=False)
    Node_en = db.Column(db.String(100), nullable=False)
    id_node_segment = db.Column(db.Integer,
                                db.ForeignKey(
                                    'IRA_Nodes_segments.id_node_segment'),
                                nullable=False)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     secondary=nodes_vs_networks_modes,
                                     backref=db.backref('nodes',
                                                        lazy='dynamic'))

    def __repr__(self):
        return f"IRA_Nodes('{self.id_node}', '{self.Node},'" \
               f"'{self.id_node_segment}')"


class IRA_Nodes_segments(db.Model):
    __tablename__ = 'IRA_Nodes_segments'
    id_node_segment = db.Column(db.Integer, primary_key=True)
    Node_segment = db.Column(db.String(100), nullable=False)
    id_node_segment_category = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Nodes_segments_categories.id_node_segment_category'),
                  nullable=False)

    nodes = db.relationship('IRA_Nodes',
                            backref=db.backref('node_segment', lazy=True))

    def __repr__(self):
        return f"IRA_Nodes_segments('{self.id_node_segment}', \
            '{self.Node_segment}','{self.id_node_segment_category}')"


class IRA_Nodes_segments_categories(db.Model):
    __tablename__ = 'IRA_Nodes_segments_categories'
    id_node_segment_category = db.Column(db.Integer, primary_key=True)
    Node_segment_category = db.Column(db.String(100), nullable=False)

    nodes_segments = db.relationship('IRA_Nodes_segments',
                                     backref=db.backref('node_segment_category', lazy=True))

    networks_modes = db.relationship('IRA_Networks_modes',
                                     backref=db.backref('node_segment_category', lazy=True))

    def __repr__(self):
        return f"IRA_Nodes_segments_categories('{self.id_node_segment_category}', \
            '{self.Node_segment_category}')"


class IRA_Organization_areas(db.Model):
    __tablename__ = 'IRA_Organization_areas'
    id_organization_area = db.Column(db.Integer, primary_key=True)
    Organization_area = db.Column(db.String(100), nullable=False)

    employees = \
        db.relationship('User',
                        backref=db.backref('organization_area',
                                           lazy=True))

    def __repr__(self):
        return f"IRA_Organization_area('{self.id_organization_area}'," \
               f"'{self.Organization_area}')"


class IRA_Questions(db.Model):
    __tablename__ = 'IRA_Questions'
    id_question = db.Column(db.Integer, primary_key=True)
    Question = db.Column(db.String(250), nullable=False)
    Question_en = db.Column(db.String(250), nullable=False)
    id_question_possible_answers = \
        db.Column(db.Integer,
                  db.ForeignKey(
                      'IRA_Questions_possible_answers.id_question_possible_answers'),
                  nullable=True)

    networks_modes = db.relationship('IRA_Networks_modes',
                                     secondary=questions_vs_networks_modes,
                                     backref=db.backref('questions',
                                                        lazy='dynamic'))

    responses = db.relationship('IRA_Responses',
                                backref=db.backref('question', lazy=True))

    def __repr__(self):
        return f"IRA_Questions('{self.id_question}'," \
               f"'{self.Question}','{self.id_question_possible_answers}')"


class IRA_Questions_possible_answers(db.Model):
    __tablename__ = 'IRA_Questions_possible_answers'
    id_question_possible_answers = db.Column(db.Integer, primary_key=True)
    Question_possible_answers = db.Column(db.String(1000), nullable=False)
    Question_possible_answers_en = db.Column(db.String(1000), nullable=False)

    questions = db.relationship('IRA_Questions',
                                backref=db.backref('question_possible_answers',
                                                   lazy=True))

    def __repr__(self):
        return f"IRA_Questions_possible_answers('{self.id_question_possible_answers}'," \
               f"'{self.Question_possible_answers}')"


class IRA_Responses(db.Model):
    __tablename__ = 'IRA_Responses'
    id_response = db.Column(db.Integer, primary_key=True)
    Response = db.Column(db.JSON, nullable=True)

    # id_employee = db.Column(db.Integer,
    #                             db.ForeignKey('IRA_Employees.id_employee'),
    #                             nullable=False)

    # id_cycle = db.Column(db.Integer,
    #                        db.ForeignKey('IRA_Cycles.id_cycle'),
    #                             nullable=False)

    id_question = db.Column(db.Integer,
                            db.ForeignKey('IRA_Questions.id_question'),
                            nullable=False)

    # id_network_mode = \
    #     db.Column(db.Integer,
    #               db.ForeignKey('IRA_Networks_modes.id_network_mode'),
    #                             nullable=False)

    id_adjacency_input_form = \
        db.Column(db.String(15),
                  db.ForeignKey(
                      'IRA_Adjacency_input_form.id_adjacency_input_form'),
                  nullable=True)

    def __repr__(self):
        return f"IRA_Responses('{self.id_response}','{self.Response}'," \
               f"'{self.id_question}','{self.id_adjacency_input_form}')"
               
#
# CVF models
#
class CVF_Culture_input_form(db.Model):
    __tablename__ = 'CVF_Culture_input_form'
    id = db.Column(db.Integer, primary_key=True)
    # id_culture_input_form = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_employee = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=False)
    id_cycle = db.Column(db.Integer,
                         db.ForeignKey('IRA_Cycles.id_cycle'),
                         nullable=False)

    id_culture_mode = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes.id'),
                  nullable=False)

    db.UniqueConstraint('id_employee', 'id_cycle', 'id_culture_mode',
                        name='uix_1')

    Is_concluded = db.Column(db.Boolean, nullable=False)

    themes_responses = db.relationship('CVF_Themes_responses',
                                       backref=db.backref('culture_input_form',
                                                          lazy=True))

    def __repr__(self):
        return f"CVF_Culture_input_form('{self.id}'," \
               f"'{self.id_employee}','{self.id_cycle}','{self.id_culture_mode}'," \
               f"'{self.Is_concluded}')"


class CVF_Culture_modes(db.Model):
    __tablename__ = 'CVF_Culture_modes'
    id = db.Column(db.Integer, primary_key=True)
    Culture_mode = db.Column(db.String(100), nullable=False)

    culture_mode_themes = db.relationship('CVF_Culture_modes_themes',
                                          backref=db.backref('culture_mode',
                                                             lazy=True))

    culture_input_forms = db.relationship('CVF_Culture_input_form',
                                          backref=db.backref('culture_mode', lazy=True))

    def __repr__(self):
        return f"CVF_Culture_modes('{self.id}', \
            '{self.Culture_mode}')"


class CVF_Culture_modes_themes(db.Model):
    __tablename__ = 'CVF_Culture_modes_themes'
    id = db.Column(db.Integer, primary_key=True)
    Culture_mode_theme = db.Column(db.String(100), nullable=False)
    Questions_prefix = db.Column(db.String(100), nullable=False)

    id_culture_mode = db.Column(db.Integer,
                                db.ForeignKey('CVF_Culture_modes.id'),
                                nullable=False)

    themes_responses = db.relationship('CVF_Themes_responses',
                                       backref=db.backref('culture_mode_theme',
                                                          lazy=True))

    culture_mode_theme_questions = \
        db.relationship('CVF_Culture_modes_themes_questions',
                        backref=db.backref('culture_mode_theme', lazy=True))

    def __repr__(self):
        return f"CVF_Culture_modes_themes('{self.id}', \
            '{self.Culture_mode_theme}','{self.id_culture_mode}')"


class CVF_Culture_modes_themes_questions(db.Model):
    __tablename__ = 'CVF_Culture_modes_themes_questions'
    id = db.Column(db.Integer, primary_key=True)
    Culture_mode_theme_question = db.Column(db.String(200), nullable=False)

    id_culture_mode_theme = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes_themes.id'),
                  nullable=False)

    id_culture_quadrant = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_quadrants.id'),
                  nullable=False)

    questions_responses = \
        db.relationship('CVF_Questions_responses',
                        backref=db.backref('modes_themes_question', lazy=True))

    def __repr__(self):
        return f"CVF_Culture_modes_themes_questions('" \
               f"'{self.id}'," \
               f"'{self.Culture_mode_theme_question}'," \
               f"'{self.id_culture_mode_theme}'," \
               f"'{self.id_culture_quadrant}')"


class CVF_Culture_quadrants(db.Model):
    __tablename__ = 'CVF_Culture_quadrants'
    id = db.Column(db.Integer, primary_key=True)
    Culture_quadrant = db.Column(db.String(100), nullable=False)

    culture_modes_themes_questions = \
        db.relationship('CVF_Culture_modes_themes_questions',
                        backref=db.backref('culture_quadrant',
                                           lazy=True))

    def __repr__(self):
        return f"CVF_Culture_quadrants('{self.id}', \
            '{self.Culture_quadrant}')"


class CVF_Questions_responses(db.Model):
    __tablename__ = 'CVF_Questions_responses'
    id = db.Column(db.Integer, primary_key=True)

    id_theme_responses = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Themes_responses.id'),
                  nullable=False)

    id_culture_mode_theme_question = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes_themes_questions.id'),
                  nullable=False)

    Actual = db.Column(db.Integer, nullable=False)

    Preferred = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"CVF_Questions_responses('{self.id}'," \
               f"'{self.id_theme_responses}','{self.id_culture_mode_theme_question}'," \
               f"'{self.Actual}','{self.Preferred}')"


class CVF_Themes_responses(db.Model):
    __tablename__ = 'CVF_Themes_responses'
    id = db.Column(db.Integer, primary_key=True)

    id_culture_input_form = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_input_form.id'),
                  nullable=False)

    id_culture_mode_theme = \
        db.Column(db.Integer,
                  db.ForeignKey('CVF_Culture_modes_themes.id'),
                  nullable=False)

    Is_concluded = db.Column(db.Boolean, nullable=False)

    Total_actual = db.Column(db.Integer, nullable=False)

    Total_preferred = db.Column(db.Integer, nullable=False)

    questions_responses = \
        db.relationship('CVF_Questions_responses',
                        backref=db.backref('theme_responses', lazy=True))

    def __repr__(self):
        return f"CVF_Themes_responses('{self.id}'," \
               f"'{self.id_culture_input_form}','{self.id_culture_mode_theme}'," \
               f"'{self.Is_concluded}','{self.Total_actual}'," \
               f"'{self.Total_preferred}')"
               


####################################################################################################            
#                               Marshmallow Schemas             
####################################################################################################

class AreaSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Organization_areas
        fields = ("id_organization_area", "Organization_area")

areas_schema = AreaSchema(many=True)

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        fields = ("id","name")

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

class ResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IRA_Responses
        


class QuestionResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Questions_responses
        
class ThemeResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Themes_responses
        
    questions_responses = ma.List(ma.Nested(QuestionResponseSchema))
        
class AdjacencyFormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IRA_Adjacency_input_form
        
    responses = ma.List(ma.Nested(ResponseSchema))
        
class CultureFormSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CVF_Culture_input_form
        
    themes_responses = ma.List(ma.Nested(ThemeResponseSchema))
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "username", "email","id_redmine","roles","id_organization_area","organization_area")
    
    organization_area = ma.Nested(AreaSchema)
    # posts = ma.List(ma.Nested(PostSchema))
    roles = ma.List(ma.Nested(RoleSchema))
    # adjacency_forms = ma.List(ma.Nested(AdjacencyFormSchema))
    # culture_input_forms = ma.List(ma.Nested(CultureFormSchema))
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# class CycleSchema(ma.SQLAlchemyAutoSchema):
    
#     class Meta:
#         model = IRA_Cycles
        
#         network_modes = ma.Nested(NetworksModesSchema)

# cycles_schema = CycleSchema(many=True)

class NetworkSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Networks
        fields = ("id", "name")

networks_schema = NetworkSchema(many=True)

class NetworkModeSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Networks_modes
        fields = ("id_network_mode", "id_network","id_node_segment_category","id_network_mode_theme")

network_modes_schema = NetworkModeSchema(many=True)


class NetworkModeThemeSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Networks_modes_themes

network_mode_theme_schema = NetworkModeThemeSchema(many=True)


class NodeSegmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IRA_Nodes_segments
node_segment_schema = NodeSegmentSchema(many=True)


class NodeSegmentCategorySchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Nodes_segments_categories
        fields = ("id_node_segment_category", "Node_segment_category")
        
node_segment_category_schema = NodeSegmentCategorySchema(many=True)


class NodeSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Nodes
        fields = ("id_node", "Node","Node_en","id_node_segment","node_segment")
    
    node_segment = ma.Nested(NodeSegmentSchema)
        
nodes_schema = NodeSchema(many=True)



class QuestionsPossibleAnswersSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Questions_possible_answers
        fields = ("id_question_possible_answers", "Question_possible_answers", "Question_possible_answers_en")

questions_possible_answers_schema = QuestionsPossibleAnswersSchema(many=True)


class QuestionsSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Questions
        fields = ("id_question", "Question", "Question_en","id_question_possible_answers","question_possible_answers")
    
    question_possible_answers = ma.Nested(QuestionsPossibleAnswersSchema)

questions_schema = QuestionsSchema(many=True)


class NetworksModesSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Networks_modes
        fields = ("id_network_mode","id_network","network","id_node_segment_category","node_segment_category","id_network_mode_theme","network_mode_theme")
    
    network = ma.Nested(NetworkSchema)
    node_segment_category = ma.Nested(NodeSegmentCategorySchema)
    network_mode_theme = ma.Nested(NetworkModeThemeSchema)

networks_modes_schema = NetworksModesSchema(many=True)


class CycleSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = IRA_Cycles
        # fields = ("id_cycle","Cycle","Initial_date","End_date","Is_active","networks_modes")
        
        # network_modes = ma.Nested(NetworksModesSchema)

cycles_schema = CycleSchema(many=True)


