# from datetime import datetime
import pandas as pd
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import getDataPath
from models import (db,
                    IRA_Networks, IRA_Nodes_segments_categories, IRA_Networks_modes,
                    IRA_Questions, IRA_Questions_possible_answers, IRA_Cycles, User)


# All seeders inherit from Seeder
class PopulateNarrativeModelsSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    # run() will be called by Flask-Seeder
    def run(self):

      ##
      # CARGA nuevos valores dentro de los modelos IRA para representar este nuevo tipo de formulario.
      ##
        new_ira_netowrk = IRA_Networks(
            code="narrative",
            name_es="Narrativa",
            name_en="Narrative"
        )
        db.session.add(new_ira_netowrk)
        db.session.commit()

        print(f'Se crea un nuevo tipo de IRA Network...{new_ira_netowrk}')

        new_ira_node_segment_category = IRA_Nodes_segments_categories(

            Node_segment_category="Narrative"

        )
        db.session.add(new_ira_node_segment_category)
        db.session.commit()

        print(
            f'Se crea un nuevo tipo de IRA Node Segment Category...{ new_ira_node_segment_category}')

        new_ira_network_mode = IRA_Networks_modes(

            network=new_ira_netowrk,
            node_segment_category=new_ira_node_segment_category

        )
        db.session.add(new_ira_network_mode)
        db.session.commit()

        print(
            f'Se crea un nuevo tipo de IRA Network Mode...{new_ira_network_mode}')

        # Se lee el Ciclo actual IRA_Cycles

        current_cycle = IRA_Cycles.query.get(1)

        # Se asocia el nuevo IRA Network MOde con el ciclo

        current_cycle.networks_modes.append(new_ira_network_mode)

        print(f'Se crea asociación  nuevo IRA NetworkMode con el Current Cycle...')

        new_question1 = IRA_Questions(

            Question_es='Título',
            Question_en='Titulo',
            question_possible_answers=None
        )
        new_question2 = IRA_Questions(

            Question_es='Narrativa',
            Question_en='Narrative',
            question_possible_answers=None
        )

        db.session.add(new_question1)
        db.session.add(new_question2)

        db.session.commit()

        print(f'Se crean nuevas IRA_Questions...')

        new_ira_network_mode.questions.append(new_question1)
        new_ira_network_mode.questions.append(new_question2)

        print(f'Se crean las relaciones entre el nuevo Network Mode y las  nuevas Questions...')
