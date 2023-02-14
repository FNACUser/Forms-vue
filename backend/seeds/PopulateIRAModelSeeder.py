from flask_seeder import Seeder
from datetime import datetime
import pandas as pd
from common.Utilities import (UT_String_to_datetime, strip, getDataPath, generate_random_string)
from flask_security.utils import hash_password
from models import (db, IRA_Networks_modes, IRA_Nodes_segments_categories)

# All seeders inherit from Seeder
class PopulateIRAModelSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        pathDB = getDataPath()
        #print(pathDB)

        excel_book = pathDB / 'IRA_data.xlsx'
        
        
        # .-.-.-.-.-.-.-.-.-.-.--.- CREA/CARGA IRA_Cycles
        
        cyclesXL = pd.read_excel(excel_book, sheet_name='Periodo')
        
       
        
        cyclesXL.rename(columns={
                                    'Nombre_es' : 'Cycle_es',
                                    'Nombre_en': 'Cycle_en',
                                    'Fecha_ini' : 'Initial_date',
                                    'Fecha_fin': 'End_date',
                                    'activo' : 'Is_active'
                                }, inplace=True)
        

        cyclesXL.to_sql(name='IRA_Cycles', con=db.engine, if_exists='append', index=False)
        
        print('Carga CICLO...')
        
        # .-.-.-.-.-.-.-.-.-.-.--.- CREA/CARGA AREAS

        areasXL = pd.read_excel(excel_book, sheet_name='Areas')

        areasXL.rename(columns={'id': 'id_organization_area',
                                'Nombre_es': 'Organization_area_es',
                                'Nombre_en': 'Organization_area_en'
                                }, inplace=True)
        areasXL.to_sql(name='IRA_Organization_areas', con=db.engine, if_exists='append',index=False)
        
        print('Carga AREAS...')
        

        # .-.-.-.-.-.-.-.-.-.-.--.- CARGA FUNCIONARIOS
        funcionariosXL = \
            pd.read_excel(excel_book, sheet_name='Funcionarios')

        funcionariosXL['Nombre'] = funcionariosXL['Nombre'].apply(strip)
        funcionariosXL['UsuarioRedmine'] = funcionariosXL['UsuarioRedmine'].apply(strip)
        funcionariosXL['password'] = hash_password(generate_random_string())
        # funcionariosXL['password'] = hash_password('12345')
        funcionariosXL['active'] = True
        funcionariosXL['image_file'] = 'default.jpg'

        now = datetime.now()
        funcionariosXL['created_at'] = now.strftime("%Y-%m-%d %H:%M:%S")

        funcionariosXL.rename(columns={'Area': 'Organization_area_es'}, inplace=True)

        funcionariosXL = funcionariosXL.merge(areasXL, left_on='Organization_area_es',
                                              right_on='Organization_area_es',
                                              how='left')

        funcionariosXL.rename(columns={'id': 'id', 'Nombre': 'username', 'UsuarioRedmine': 'id_redmine'},
                              inplace=True)
        funcionariosXL.drop(columns=['Organization_area_es', 'Organization_area_en','Area_id'], inplace=True)
        
        

        funcionariosXL.to_sql(name='users', con=db.engine,
                              if_exists='append', index=False)
        
        print('Carga Funcionarios...')
        
        
        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA IRA_Networks
        
        networks_XL = \
            pd.read_excel(excel_book,
                          sheet_name='Networks')


        networks_XL.rename(columns={'id': 'id',
                                               'code':'code',
                                               'Name_es': 'name_es',
                                               'Name_en': 'name_en'},
                                      inplace=True)
        
        
        networks_XL.to_sql(name='IRA_Networks', con=db.engine,
                                     if_exists='append', index=False)
        
        print('Carga IRA_Networks...')       


        # .-.-.-.-.-.-.-.-.-.-.--.- CARGA IRA_Nodes_segments_categories

        categorías_segmentos_nodos_df = pd.read_excel(excel_book, sheet_name='Nodos')
        categorías_segmentos_nodos_df.rename(columns={'id': 'id_node_segment_category',
                                                      'Nombre': 'Node_segment_category'},
                                             inplace=True)
        
        categorías_segmentos_nodos_df.to_sql(name='IRA_Nodes_segments_categories',
                                             con=db.engine, if_exists='append',
                                             index=False)

        print('Carga IRA_Nodes_segments_categories...')
        
      
        
        
            
        # .-.-.-.-.-.-.-.-. LEE CONOCIMIENTOS
        segmentos_nodosXL = pd.read_excel(excel_book,sheet_name='Conocimientos')
        segmentos_nodosXL.rename(columns={'Tipo-Conocimiento': 'Node_segment',
                                          'Nombre_es': 'Node_es',
                                          'Nombre_en': 'Node_en'},inplace=True)
        #segmentos_nodosXL['id_node_segment_category'] = 2
        segmentos_nodosXL['id_node_segment_category'] = categorías_segmentos_nodos_df.loc[categorías_segmentos_nodos_df["Node_segment_category"]== 'Aspectos modelo educativo','id_node_segment_category'].squeeze()
        
        # print('hola')
        # print(segmentos_nodosXL['id_node_segment_category'])
        
       # print(categorías_segmentos_nodos_df.query("Node_segment_category == 'Aspectos modelo educativo'")['id_node_segment_category'])

        # .-.-.-.-.-.-.-.-. LEE RECURSOS
        segmentos_nodos_recursosXL = pd.read_excel(excel_book, sheet_name='Recursos')
        segmentos_nodos_recursosXL.rename(columns={'Tipo-Recurso': 'Node_segment',
                                                   'Recursos_es': 'Node_es',
                                                   'Recursos_en': 'Node_en'}, inplace=True)
        #segmentos_nodos_recursosXL['id_node_segment_category'] = 3
        segmentos_nodos_recursosXL['id_node_segment_category'] = categorías_segmentos_nodos_df.loc[categorías_segmentos_nodos_df["Node_segment_category"]== 'Recursos','id_node_segment_category'].squeeze()
       # print(categorías_segmentos_nodos_df.query("Node_segment_category == 'Recursos'")['id_node_segment_category'])

        segmentos_nodosXL = \
            segmentos_nodosXL.append(segmentos_nodos_recursosXL, ignore_index=True)


        # index
        segmentos_nodosXL.drop(columns=['id'], inplace=True)
        segmentos_nodosXL.reset_index(level=0, inplace=True)
        segmentos_nodosXL.rename(columns={'index': 'id_node'}, inplace=True)
        segmentos_nodosXL['id_node'] = segmentos_nodosXL['id_node'] + 1


        segmentos_nodosXL = \
            segmentos_nodosXL.merge(categorías_segmentos_nodos_df,
                                    left_on='id_node_segment_category',
                                    right_on='id_node_segment_category', how='left')
        segmentos_nodosXL['node_segment_and_category'] = \
            segmentos_nodosXL.Node_segment + '-' + segmentos_nodosXL.Node_segment_category

        set(segmentos_nodosXL['id_node'])
        set(segmentos_nodosXL['id_node_segment_category'])
        # segmentos_df
        segmentos_df = \
            segmentos_nodosXL.groupby(['Node_segment',
                                       'node_segment_and_category',
                                       'id_node_segment_category']).size().reset_index(name='Freq')
        segmentos_df.reset_index(level=0, inplace=True)
        segmentos_df.rename(columns={'index': 'id_node_segment'}, inplace=True)
        segmentos_df.drop(columns=['Freq'], inplace=True)
        segmentos_df['id_node_segment'] = segmentos_df['id_node_segment'] + 1

        # merge segmentos_nodosXL con segmentos_df
        segmentos_nodosXL.drop(columns=['id_node_segment_category', 'Node_segment'],
                               inplace=True)
        segmentos_nodosXL = segmentos_nodosXL.merge(segmentos_df,
                                                    left_on='node_segment_and_category',
                                                    right_on='node_segment_and_category',
                                                    how='left')

        set(segmentos_nodosXL['id_node'])
        set(segmentos_nodosXL['id_node_segment_category'])
        set(segmentos_nodosXL['id_node_segment'])

        # quitar columns innecesarias
        segmentos_df.drop(columns=['node_segment_and_category'], inplace=True)

        segmentos_nodosXL.drop(columns=['Node_segment_category',
                                        'node_segment_and_category', 'Node_segment',
                                        'id_node_segment_category'], inplace=True)

        
        
        # .-.-.-.-.-.-.-.-. SE CREA/CARGA IRA_Nodes_segments
        segmentos_df.to_sql(name='IRA_Nodes_segments', con=db.engine,
                            if_exists='append', index=False)
        
        print('Carga IRA_Nodes_segments...')
        
        
        
         # .-.-.-.-.-.-.-.-. SE CREA/CARGA IRA_Nodes
        segmentos_nodosXL.to_sql(name='IRA_Nodes', con=db.engine, if_exists='append',
                                 index=False)
        
        print('Carga IRA_Nodes...')



        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA IRA_Networks_modes_themes
        categorias_preguntasXL = \
            pd.read_excel(excel_book,
                          sheet_name='Categorias_preguntas')


        categorias_preguntasXL.rename(columns={'id': 'id_network_mode_theme',
                                               'code':'code',
                                               'Nombre_es': 'Network_mode_theme_es',
                                               'Nombre_en': 'Network_mode_theme_en'},
                                      inplace=True)


        categorias_preguntasXL.to_sql(name='IRA_Networks_modes_themes', con=db.engine,
                                      if_exists='append', index=False)
        
        print('Carga IRA_Networks_modes_themes...')

        
    
         # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA  IRA_Networks_modes
        networks_modes_df = pd.DataFrame({'id_network_mode': [1, 2, 3, 4, 5, 6],
                                          'id_network': [1,2,3,3,3,3],
                                          'id_node_segment_category': [2, 3, None, None,
                                                                       None, None],
                                          'id_network_mode_theme': [None, None, 1, 2, 3, 4]})

        networks_modes_df.to_sql(name='IRA_Networks_modes', con=db.engine,
                                 if_exists='append', index=False)
        
        
        print('Carga IRA_Networks_modes...')     

        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA  IRA_Questions_possible_answers
        

        posibles_rtasXL = pd.read_excel(excel_book, sheet_name='Posibles_rtas')

        posibles_rtasXL.rename(columns={'id': 'id_question_possible_answers',
                                        'Descripcion_es': 'Question_possible_answers_es',
                                        'Descripcion_en': 'Question_possible_answers_en'
                                        },
                               inplace=True)
       

        posibles_rtasXL.to_sql(name='IRA_Questions_possible_answers',
                               con=db.engine, if_exists='append', index=False)

        
        print('Carga IRA_Questions_possible_answers...')   
         
         
           
         # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA  IRA_Questions
        

        preguntasXL = pd.read_excel(excel_book, sheet_name='Preguntas')

        preguntasXL.drop(columns=['Modalidad'], inplace=True)
        preguntasXL.rename(columns={'id': 'id_question', 
                                    'Descripcion_es': 'Question_es',
                                    'Descripcion_en': 'Question_en',
                                    'Posibles_rtas_id': 'id_question_possible_answers'},
                           inplace=True)
        # preguntasXL['Question_en'] = \
        #     preguntasXL.apply(lambda row: questions_en_dict.get(row.id_question),
        #                       axis=1)

        preguntasXL.to_sql(name='IRA_Questions', con=db.engine, if_exists='append',
                           index=False)
        
        
        print('Carga IRA_Questions...')   
        
    
        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA questions_vs_networks_modes PIVOT TABLE
        questions_vs_networks_modes_df = \
            pd.DataFrame({'id_question': [1, 1, 1,
                                          2, 2, 2,
                                          3, 3,
                                          4, 4,
                                          5, 5,
                                          6,
                                          7, 8,
                                          9, 10, 11, 12],
                          'id_network_mode': [3, 4, 6,
                                              3, 4, 6,
                                              3, 4,
                                              3, 4,
                                              5, 6,
                                              5,
                                              2, 2,
                                              1, 1, 1, 1]})

        questions_vs_networks_modes_df.to_sql(name='questions_vs_networks_modes',
                                              con=db.engine, if_exists='append', index=False)



        print('Carga questions_vs_networks_modes PIVOT TABLE...') 
        
        

        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA cycles_vs_networks_modes PIVOT TABLE
        
        def FD_IRA_cycle_vs_networks_modes_to_DF(xira_networks_modes, xcycle,xcycle_modes):
            r = [(xcycle, nm.id_network_mode,) for nm in xira_networks_modes if
                 nm.id_network_mode in xcycle_modes]
            df = pd.DataFrame.from_records(r, columns=['id_cycle', 'id_network_mode'])

            return df

        cycle_vs_networks_modes_df = \
            FD_IRA_cycle_vs_networks_modes_to_DF(IRA_Networks_modes.query.all(), 1,
                                                 [1, 2, 3, 4, 5, 6])
        

        cycle_vs_networks_modes_df.to_sql(name='cycles_vs_networks_modes',
                                          con=db.engine, if_exists='append', index=False)


        print('Carga cycles_vs_networks_modes PIVOT TABLE...') 
        
        

         # .-.-.-.-.-.-.-.-.-.-.-.-.-.- SE CREA/CARGA  nodes_vs_networks_modes
        def FD_segments_DF(xsegments):
            r = [(n.id_node_segment, n.Node_segment, n.id_node_segment_category) \
                 for n in xsegments]
            df = pd.DataFrame.from_records(r, columns=['id_node_segment',
                                                       ' n.node_segment',
                                                       'id_node_segment_category'])
            return df

        def FD_nodes_segments_categories_DF(xnodes_segments_categories):
            r = [(n.id_node_segment_category, n.Node_segment_category) \
                 for n in xnodes_segments_categories]
            df = pd.DataFrame.from_records(r, columns=['id_node_segment_category',
                                                       'node_segment_category'])
            return df

        def FD_IRA_Nodes_to_DF(xira_nodes, xcategory):
            r = [(n.id_node, xcategory) for n in xira_nodes]
            df = pd.DataFrame.from_records(r, columns=['id_node', 'id_network_mode'])

            return df

        def FD_nodes_vs_networks_modes(xcategory):
            category = IRA_Nodes_segments_categories. \
                query.filter_by(id_node_segment_category=xcategory)
            category_df = FD_nodes_segments_categories_DF(category)
            category_df = category_df.merge(networks_modes_df,
                                            left_on='id_node_segment_category',
                                            right_on='id_node_segment_category',
                                            how='left')
            _id_network_mode = category_df['id_network_mode'][0]
            segments = category.first().nodes_segments
            nodes_flat = [node for segment in segments for node in segment.nodes]
            return FD_IRA_Nodes_to_DF(nodes_flat, _id_network_mode)

        nodes_vs_networks_modes_df = FD_nodes_vs_networks_modes(2)
        nodes_vs_networks_modes_df

        nodes_vs_networks_modes_df = \
            nodes_vs_networks_modes_df.append(FD_nodes_vs_networks_modes(3),
                                              ignore_index=True)
        nodes_vs_networks_modes_df

        nodes_vs_networks_modes_df.to_sql(name='nodes_vs_networks_modes',
                                          con=db.engine, if_exists='append', index=False)
        
        
        print('Carga nodes_vs_networks_modes PIVOT TABLE...') 

        db.session.commit()

        #:_:_:_:_:_:_:_:_:_:_:_:_:_:_: Hasta aquí el cargue del modelo IRA
       
        