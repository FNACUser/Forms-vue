# from datetime import datetime
import pandas as pd
import os.path
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import getDataPath
from models import (db,
                    IRA_Networks, IRA_Nodes_segments,
                    IRA_Networks_modes, IRA_Cycles, User)


# All seeders inherit from Seeder
class PopulateNarrativeModelsSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 5

    # run() will be called by Flask-Seeder
    def run(self):
        
        pathDB = getDataPath()
        # print(pathDB)
        excel_book = pathDB / 'IRA_data.xlsx'
        file_exists = os.path.isfile(excel_book)

        if file_exists:
            # .-.-.-.-.-.-.-.-.-.-.--.- CREA/CARGA IRA_Narrative_topics

            topicosXL = pd.read_excel(excel_book, sheet_name='Narrativas_topicos')

            topicosXL.to_sql(name='IRA_Narrative_topics', con=db.engine,
                            if_exists='append', index=False)

            print('Cargó IRA_Narrative_topics...')

        
        narrative_network = IRA_Networks.query.filter_by(
                            code="narrative").first()
        
        narrative_node_segment = IRA_Nodes_segments.query.filter_by(
                            Node_segment="Narrative").first()

        narrative_ira_network_mode = IRA_Networks_modes.query.filter_by(
            id_network=narrative_network.id, id_node_segment=narrative_node_segment.id_node_segment).first()

        # Se lee el Ciclo actual IRA_Cycles

        current_cycle = IRA_Cycles.query.get(1)

        # Se asocia el nuevo IRA Network MOde con el ciclo

        current_cycle.networks_modes.append(narrative_ira_network_mode)

        print(f'Se  asocia Narrative definida en IRA Network_Mode con el Current Cycle...')

