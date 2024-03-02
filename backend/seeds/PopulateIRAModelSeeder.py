from flask_seeder import Seeder
from flask_security.utils import hash_password
from datetime import datetime
import pandas as pd

from common.Utilities import ( strip, getDataPath, generate_random_string,isNotEmpty)
from models import *
import os.path

# All seeders inherit from Seeder


class PopulateIRAModelSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        pathDB = getDataPath()
        # print(pathDB)
        excel_book = pathDB / 'IRA_data.xlsx'
        file_exists = os.path.isfile(excel_book)

        if file_exists:
            # .-.-.-.-.-.-.-.-.-.-.--.- CREA/CARGA IRA_Cycles

            cyclesXL = pd.read_excel(excel_book, sheet_name='Periodo')

            cyclesXL.rename(columns={
                'Nombre_es': 'Cycle_es',
                'Nombre_en': 'Cycle_en',
                'Fecha_ini': 'Initial_date',
                'Fecha_fin': 'End_date',
                'activo': 'Is_active'
            }, inplace=True)

            cyclesXL.to_sql(name='IRA_Cycles', con=db.engine,
                            if_exists='append', index=False)

            print('Cargó IRA_CICLO...')

            # .-.-.-.-.-.-.-.-.-.-.--.- CREA/CARGA AREAS

            areasXL = pd.read_excel(excel_book, sheet_name='Areas')

            areasXL.rename(columns={'id': 'id_organization_area',
                                    'Nombre_es': 'Organization_area_es',
                                    'Nombre_en': 'Organization_area_en'
                                    }, inplace=True)
            # areasXL.rename(columns={
            #                         'Nombre_es': 'Organization_area_es',
            #                         'Nombre_en': 'Organization_area_en'
            #                         }, inplace=True)
            areasXL.to_sql(name='IRA_Organization_areas',
                        con=db.engine, if_exists='append', index=False)

            # ira_org_areas = IRA_Organization_areas.query.all()

            # df_from_records = pd.DataFrame.from_records(ira_org_areas, index='id_organization_area')

            # print(df_from_records)

            print('Cargó IRA_AREAS...')

            # .-.-.-.-.-.-.-.-.-.-.--.- CARGA FUNCIONARIOS
            funcionariosXL = \
                pd.read_excel(excel_book, sheet_name='Funcionarios')

            funcionariosXL['Nombre'] = funcionariosXL['Nombre'].apply(strip)
            funcionariosXL['UsuarioRedmine'] = funcionariosXL['UsuarioRedmine'].apply(
                strip)
            funcionariosXL['password'] = hash_password(generate_random_string())
            # funcionariosXL['password'] = hash_password('12345')
            funcionariosXL['active'] = True
            funcionariosXL['image_file'] = 'default.jpg'

            now = datetime.now()
            funcionariosXL['created_at'] = now.strftime("%Y-%m-%d %H:%M:%S")

            funcionariosXL.rename(
                columns={'Area': 'Organization_area_es'}, inplace=True)

            funcionariosXL = funcionariosXL.merge(areasXL, left_on='Organization_area_es',
                                                right_on='Organization_area_es',
                                                how='left')

            funcionariosXL.rename(columns={'id': 'id',
                                        'Nombre': 'username',
                                        'UsuarioRedmine': 'id_redmine',
                                        'DocumentID':'documentID'
                                        },
                                inplace=True)
            funcionariosXL.drop(
                columns=['Organization_area_es', 'Organization_area_en'], inplace=True)

            funcionariosXL.to_sql(name='users', con=db.engine,
                                if_exists='append', index=False)

            print('Cargó Users...')

            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA IRA_Networks

            networks_XL = \
                pd.read_excel(excel_book,
                            sheet_name='Networks')

            networks_XL.rename(columns={'id': 'id',
                                        'code': 'code',
                                        'Nombre_es': 'name_es',
                                        'Nombre_en': 'name_en'},
                            inplace=True)

            networks_XL.to_sql(name='IRA_Networks', con=db.engine,
                            if_exists='append', index=False)

            print('Cargó IRA_Networks...')

            # .-.-.-.-.-.-.-.-.-.-.--.- CARGA IRA_Nodes_segments_categories

            categorías_segmentos_nodos_df = pd.read_excel(
                excel_book, sheet_name='Node_segment_categories')
            categorías_segmentos_nodos_df.rename(columns={'id': 'id_node_segment_category',
                                                        'Nombre': 'Node_segment_category'},
                                                inplace=True)

            categorías_segmentos_nodos_df.to_sql(name='IRA_Nodes_segments_categories',
                                                con=db.engine, if_exists='append',
                                                index=False)

            # print(categorías_segmentos_nodos_df)
            
            print('Cargó IRA_Nodes_segments_categories...')
            
            
            #Lee IRA Nodes Segments
            
            ira_nodes_segments_XL = pd.read_excel(excel_book, sheet_name='ira_nodes_segments')
            for index, row in ira_nodes_segments_XL.iterrows():
                # print(row)
                node_segment_category = IRA_Nodes_segments_categories.query.filter_by(Node_segment_category=row['node_segment_category']).first()
                if (node_segment_category):
                    new_node_segment = IRA_Nodes_segments(
                        Node_segment=row['Node_segment'],
                        node_segment_category=node_segment_category
                    )
                    db.session.add(new_node_segment)

                db.session.commit()
            print('Cargó IRA_node_segments...')
            
        
            #Lee Data de Bimodales (Conocimientos , Tareas , Recursos)
        
            nodes_XL = pd.read_excel(excel_book, sheet_name='Nodes')
            for index, row in nodes_XL.iterrows():
                # print(row)
                node_segment = IRA_Nodes_segments.query.filter_by(Node_segment=row['Tipo']).first()
                if (node_segment):
                    new_node = IRA_Nodes(
                        Node_es=row['Nombre_es'],
                        Node_en=row['Nombre_en'],
                        theme_es=row['Tema_es'],
                        theme_en=row['Tema_en'],
                        origin_es=row['Origen_es'],
                        origin_en=row['Origen_en'],
                        node_segment=node_segment
                    )
                    db.session.add(new_node)

                db.session.commit()
            print('Cargó IRA_nodes...')
        
        
            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA IRA_Networks_modes_themes
            categorias_preguntasXL = \
                pd.read_excel(excel_book,
                            sheet_name='ira_networks_modes_themes')

            categorias_preguntasXL.rename(columns={'id': 'id_network_mode_theme',
                                                'code': 'code',
                                                'Nombre_es': 'Network_mode_theme_es',
                                                'Nombre_en': 'Network_mode_theme_en'},
                                        inplace=True)

            categorias_preguntasXL.to_sql(name='IRA_Networks_modes_themes', con=db.engine,
                                        if_exists='append', index=False)

            print('Cargó IRA_Networks_modes_themes...')

            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE LEE  IRA_Networks_modes

            networks_modesXL = pd.read_excel(excel_book, sheet_name='ira_networks_modes')
            
            for index, row in networks_modesXL.iterrows():
                # print(row)
                node_segment = None
                network_mode_theme = None
                
                network = IRA_Networks.query.filter_by(code=row['network_code']).first()
                if isNotEmpty(row['node_segment']):
                    node_segment = IRA_Nodes_segments.query.filter_by(Node_segment=row['node_segment']).first()
                if isNotEmpty(row['network_mode_theme_code']):
                    network_mode_theme = IRA_Networks_modes_themes.query.filter_by(code=row['network_mode_theme_code']).first()
                # if (network):
                new_network_mode = IRA_Networks_modes(
                    network=network,
                    node_segment=node_segment,
                    network_mode_theme=network_mode_theme
                )
                db.session.add(new_network_mode)

                db.session.commit()
                
            print('Cargó IRA_Networks_modes...')


            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA  IRA_Questions_possible_answers

            posibles_rtasXL = pd.read_excel(excel_book, sheet_name='Posibles_rtas')
            
            for index, row in posibles_rtasXL.iterrows():
                # print(row)
                Question_possible_answers_es = ''
                Question_possible_answers_en = ''
                use_external_source = None
                source_name = None
                
                if isNotEmpty(row['Descripcion_es']):
                    Question_possible_answers_es = row['Descripcion_es']
                if isNotEmpty(row['Descripcion_en']):
                    Question_possible_answers_en = row['Descripcion_en']
                if isNotEmpty(row['use_external_source']):
                    use_external_source = row['use_external_source']
                if isNotEmpty(row['source_name']):
                    source_name = row['source_name']
            
                new_possible_answers = IRA_Questions_possible_answers(
                    Question_possible_answers_es = Question_possible_answers_es,
                    Question_possible_answers_en = Question_possible_answers_en,
                    multiple = row['multiple'],
                    use_external_source = use_external_source,
                    source_name = source_name
                )
                db.session.add(new_possible_answers)

                db.session.commit()

            print('Cargó IRA_Questions_possible_answers...')

            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA  IRA_Questions

            preguntasXL = pd.read_excel(excel_book, sheet_name='Preguntas')
            preguntasXL.rename(columns={'id': 'id_question',
                                        'Descripcion_es': 'Question_es',
                                        'Descripcion_en': 'Question_en',
                                        'Descripcion_corta_es': 'short_question_es',
                                        'Descripcion_corta_en': 'short_question_en',
                                        'Explicacion_es': 'help_es',
                                        'Explicacion_en': 'help_en',
                                        'Siglas_es': 'acronym_es',
                                        'Siglas_en': 'acronym_en',
                                        'Posibles_rtas_id': 'id_question_possible_answers'},
                            inplace=True)
            # preguntasXL['Question_en'] = \
            #     preguntasXL.apply(lambda row: questions_en_dict.get(row.id_question),
            #                       axis=1)

            preguntasXL.to_sql(name='IRA_Questions', con=db.engine, if_exists='append',
                            index=False)

            print('Cargó IRA_Questions...')

            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA questions_vs_networks_modes PIVOT TABLE

            questions_vs_networks_modes_df = pd.read_excel(
                excel_book, sheet_name='Preg-NetworkMode')
            
            questions_vs_networks_modes_df.rename(
                columns={'id_pregunta': 'id_question'}, inplace=True)

            questions_vs_networks_modes_df.to_sql(name='questions_vs_networks_modes',
                                                con=db.engine, if_exists='append', index=False)

            print('Cargó questions_vs_networks_modes PIVOT TABLE...')

            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA cycles_vs_networks_modes PIVOT TABLE

            
            current_cycle = IRA_Cycles.query.get(1)
            network_modes = IRA_Networks_modes.query.all()
        
            for network_mode in network_modes:
                current_cycle.networks_modes.append(network_mode)
            

            print('Cargó cycles_vs_networks_modes PIVOT TABLE...')

            # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA nodes_vs_networks_modes PIVOT TABLE
        
            nodes = IRA_Nodes.query.all()
            
            for node in nodes:
                
                node_segment= node.node_segment
                network_mode = IRA_Networks_modes.query.filter_by(id_node_segment=node_segment.id_node_segment).first()
                network_mode.nodes.append(node)
                

            print('Cargó nodes_vs_networks_modes PIVOT TABLE...')

            db.session.commit()

            # :_:_:_:_:_:_:_:_:_:_:_:_:_:_: Hasta aquí el cargue del modelo IRA
        else:
            print(f'{excel_book} no existe!!!')