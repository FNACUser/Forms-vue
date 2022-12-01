from datetime import datetime

import pandas as pd
from flask_seeder import Seeder

from models import db

from common.Utilities import (UT_String_to_datetime, strip, getDataPath, generate_random_string)
from models import (IRA_Networks_modes, IRA_Nodes_segments_categories)
from flask_security.utils import hash_password


# All seeders inherit from Seeder
class PopulateNewIRAQuestionsSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        pathDB = getDataPath()
        print(pathDB)

        # %%
        excel_book = pathDB / 'Descripcion_informacion_alcaparros.xlsx'

        areasXL = pd.read_excel(excel_book, sheet_name='Areas')

        areasXL.rename(columns={'id': 'id_organization_area',
                                'Nombre_es': 'Organization_area_es',
                                'Nombre_en': 'Organization_area_en'
                                }, inplace=True)
        areasXL.to_sql(name='IRA_Organization_areas', con=db.engine, if_exists='append',
                       index=False)

        cycles_df = pd.DataFrame({'id_cycle': [1],
                                  'Cycle': ['junio-2022'],
                                  'Initial_date': [UT_String_to_datetime('2022-06-01',
                                                                         xstring="%Y-%m-%d")],
                                  'End_date': [UT_String_to_datetime('2022-06-30',
                                                                     xstring="%Y-%m-%d")],
                                  'Is_active': [True]})

        cycles_df.to_sql(name='IRA_Cycles', con=db.engine, if_exists='append',
                         index=False)

        # .-.-.-.-.-.-.-.-.-.-.--.- funcionarios
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
        
        funcionariosXL

        funcionariosXL.to_sql(name='users', con=db.engine,
                              if_exists='append', index=False)


        # .-.-.-.-.-.-.-.-.-.-.-.-. categorías nodos

        categorías_segmentos_nodos_df = pd.read_excel(excel_book, sheet_name='Nodos')
        categorías_segmentos_nodos_df.rename(columns={'id': 'id_node_segment_category',
                                                      'Nombre': 'Node_segment_category'},
                                             inplace=True)



        categorías_segmentos_nodos_df.to_sql(name='IRA_Nodes_segments_categories',
                                             con=db.engine, if_exists='append',
                                             index=False)

        # .-.-.-.-.-.-.-.-.-.-.--.- nodes y nodes_segments
        conocimientos_en = pd.read_excel(excel_book,
                                         sheet_name='Conocimientos_en')

        conocimientos_en_dict = \
            pd.Series(conocimientos_en.Nombre.values,
                      index=conocimientos_en.id).to_dict()
        # .-.-.-.-.-.-.-.-. Conocimientos
        segmentos_nodosXL = \
            pd.read_excel(excel_book,
                          sheet_name='Conocimientos')
        segmentos_nodosXL.rename(columns={'Tipo-Conocimiento': 'Node_segment',
                                          'Nombre': 'Node'}, inplace=True)
        segmentos_nodosXL['id_node_segment_category'] = 2

        segmentos_nodosXL['Node_en'] = \
            segmentos_nodosXL.apply(lambda row: \
                                        conocimientos_en_dict.get(row.id), axis=1)

        # .-.-.-.-.-.-.-.-.- Recursos
        recursos_en = pd.read_excel(excel_book,
                                    sheet_name='Recursos_en')
        recursos_en_dict = \
            pd.Series(recursos_en.Recursos.values,
                      index=recursos_en.id).to_dict()

        segmentos_nodos_recursosXL = pd.read_excel(excel_book, sheet_name='Recursos')
        segmentos_nodos_recursosXL.rename(columns={'Tipo-Recurso': 'Node_segment',
                                                   'Recursos': 'Node'}, inplace=True)
        segmentos_nodos_recursosXL['id_node_segment_category'] = 3
        segmentos_nodos_recursosXL['Node_en'] = \
            segmentos_nodos_recursosXL.apply(lambda row: \
                                                 recursos_en_dict.get(row.id), axis=1)

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

        # grabar
        segmentos_df.to_sql(name='IRA_Nodes_segments', con=db.engine,
                            if_exists='append', index=False)
        segmentos_nodosXL.to_sql(name='IRA_Nodes', con=db.engine, if_exists='append',
                                 index=False)

        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- inetwork_mode_theme
        categorias_preguntasXL = \
            pd.read_excel(excel_book,
                          sheet_name='Categorias_preguntas')


        categorias_preguntasXL.rename(columns={'id': 'id_network_mode_theme',
                                               'Nombre': 'Network_mode_theme'},
                                      inplace=True)


        categorias_preguntasXL.to_sql(name='IRA_Networks_modes_themes', con=db.engine,
                                      if_exists='append', index=False)

        # .-.-.-.-.-.-.-.-.- network modes
        networks_modes_df = pd.DataFrame({'id_network_mode': [1, 2, 3, 4, 5, 6],
                                          'Network_mode': ['Modelo educativo', 'Recurso',
                                                           'Actor', 'Actor', 'Actor',
                                                           'Actor'],
                                          'id_node_segment_category': [2, 3, None, None,
                                                                       None, None],
                                          'id_network_mode_theme': [None, None, 1, 2,
                                                                    3, 4]})

        networks_modes_df.to_sql(name='IRA_Networks_modes', con=db.engine,
                                 if_exists='append', index=False)


        # .-.-.-.-.-.-.-.-.- Questions_posible_answers
        possible_answers_en = pd.read_excel(excel_book,
                                            sheet_name='Posibles_rtas_en')

        possible_answers_en_dict = \
            pd.Series(possible_answers_en.Descripcion.values,
                      index=possible_answers_en.id).to_dict()

        posibles_rtasXL = pd.read_excel(excel_book, sheet_name='Posibles_rtas')

        posibles_rtasXL.rename(columns={'id': 'id_question_possible_answers',
                                        'Descripcion': 'Question_possible_answers'},
                               inplace=True)
        posibles_rtasXL = posibles_rtasXL[['id_question_possible_answers',
                                           'Question_possible_answers']]

        posibles_rtasXL['Question_possible_answers_en'] = \
            posibles_rtasXL.apply(lambda row: \
                                      possible_answers_en_dict. \
                                  get(row.id_question_possible_answers),
                                  axis=1)

        posibles_rtasXL.to_sql(name='IRA_Questions_possible_answers',
                               con=db.engine, if_exists='append', index=False)

        # .-.-.-.-.-.-.-.-.-.-.-. Questions
        questions_en = pd.read_excel(excel_book, sheet_name='Preguntas_en')

        questions_en_dict = \
            pd.Series(questions_en.Descripcion.values,
                      index=questions_en.id).to_dict()
        # questions_en_dict

        preguntasXL = pd.read_excel(excel_book, sheet_name='Preguntas')

        preguntasXL.drop(columns=['Modalidad'], inplace=True)
        preguntasXL.rename(columns={'id': 'id_question', 'Descripcion': 'Question',
                                    'Posibles_rtas_id': 'id_question_possible_answers'},
                           inplace=True)
        preguntasXL['Question_en'] = \
            preguntasXL.apply(lambda row: questions_en_dict.get(row.id_question),
                              axis=1)

        preguntasXL.to_sql(name='IRA_Questions', con=db.engine, if_exists='append',
                           index=False)

        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- questions_vs_networks_modes
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



        # .-.-.-.-.-.-. cycles_vs_networks_modes
        def FD_IRA_cycle_vs_networks_modes_to_DF(xira_networks_modes, xcycle,
                                                 xcycle_modes):
            r = [(xcycle, nm.id_network_mode,) for nm in xira_networks_modes if
                 nm.id_network_mode in xcycle_modes]
            df = pd.DataFrame.from_records(r, columns=['id_cycle', 'id_network_mode'])

            return df

        cycle_vs_networks_modes_df = \
            FD_IRA_cycle_vs_networks_modes_to_DF(IRA_Networks_modes.query.all(), 1,
                                                 [1, 2, 3, 4, 5, 6])
        # cycle_vs_networks_modes_df = \
        #     cycle_vs_networks_modes_df.\
        #         append(FD_IRA_cycle_vs_networks_modes_to_DF(IRA_Networks_modes.query.all(),2,
        #                                                     [1,2,3,4,5]),
        #                                       ignore_index=True)


        cycle_vs_networks_modes_df.to_sql(name='cycles_vs_networks_modes',
                                          con=db.engine, if_exists='append', index=False)

        # .-.-.-.-.-.-.-.-.-.-.-.-.-.- nodes_vs_networks_modes
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

        db.session.commit()

        #:_:_:_:_:_:_:_:_:_:_:_:_:_:_: Hasta aquí el cargue del modelo IRA
        #:_:_:_:_:_:_:_:_:_:_:_:_:_:_: Hasta aquí el cargue del modelo IRA
        #:_:_:_:_:_:_:_:_:_:_:_:_:_:_: Hasta aquí el cargue del modelo IRA

        # .-.-.-.-.-.-.-.-.-. cargue de CVF questions y respuestas simuladas
        # .-.-.-.-.-.-.-.-.-. cargue de CVF questions y respuestas simuladas
        # .-.-.-.-.-.-.-.-.-. cargue de CVF questions y respuestas simuladas



        # .-.-.-.-.-.-.- questions

        excel_preguntas = pathDB /'alcaparrosCVF_Preguntas.xlsx'

        cvf_questions_XL = pd.read_excel(excel_preguntas,
                                         sheet_name='Preguntas')


        cvf_questions_XL_en = pd.read_excel(excel_preguntas,
                                            sheet_name='Preguntas_en')
        cvf_questions_XL = pd.concat([cvf_questions_XL, cvf_questions_XL_en], axis=1)
        # cvf_questions_XL.to_dict('records')

        # .-.-.-.-.-.-.-.-.-.-.-.- prefijos
        cvf_prefijos_XL = pd.read_excel(excel_preguntas,
                                        sheet_name='Prefijos')
        # cvf_prefijos_XL.columns
        # cvf_prefijos_XL
        cvf_prefijos_XL_en = pd.read_excel(excel_preguntas,
                                           sheet_name='Prefijos_en')
        cvf_prefijos_XL = pd.concat([cvf_prefijos_XL, cvf_prefijos_XL_en], axis=1)


        # .-.-.-.-.-.-.-.-.-.-- cuadrantes
        cvf_cuadrantes_XL = pd.read_excel(excel_preguntas,
                                          sheet_name='Cuadrantes')
        # cvf_cuadrantes_XL.columns
        cvf_cuadrantes_XL_en = pd.read_excel(excel_preguntas,
                                             sheet_name='Cuadrantes_en')
        cvf_cuadrantes_XL = pd.concat([cvf_cuadrantes_XL, cvf_cuadrantes_XL_en], axis=1)

        cvf_quadrants_df = cvf_cuadrantes_XL.reset_index()
        cvf_quadrants_df.rename(columns={'index': 'id',
                                         'Cuadrante': 'Culture_quadrant',
                                         'Cuadrante_en': 'Culture_quadrant_en'},
                                inplace=True)
        cvf_quadrants_df['id'] = 1 + cvf_quadrants_df['id']
        # cvf_quadrants_df

        cuadrantes_dict = \
            cvf_quadrants_df.set_index('Culture_quadrant')['id'].to_dict()
        # cuadrantes_dict

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes
        cvf_culture_modes_df = pd.DataFrame({'id': [1],
                                             'Culture_mode': ['Colegio']})
        cvf_culture_modes_df.to_sql(name='CVF_Culture_modes', con=db.engine,
                                    if_exists='append',
                                    index=False)
        # cvf_culture_modes_df.columns

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes_themes
        themes = list(cvf_prefijos_XL['Tema'])
        prefixes = list(cvf_prefijos_XL['Prefijo'])

        themes_en = list(cvf_prefijos_XL['Tema_en'])
        prefixes_en = list(cvf_prefijos_XL['Prefijo_en'])


        cvf_culture_modes_dict = \
            {'id': [i for i in range(1, 1 + len(themes))],
             'Culture_mode_theme': themes,
             'Culture_mode_theme_en': themes_en,
             'Questions_prefix': prefixes,
             'Questions_prefix_en': prefixes_en,
             'id_culture_mode': [1 for i in range(1, 1 + len(themes))]}
        cvf_culture_modes_themes_df = pd.DataFrame(cvf_culture_modes_dict)
        # cvf_culture_modes_themes_df.columns

        cvf_culture_modes_themes_df.to_sql(name='CVF_Culture_modes_themes',
                                           con=db.engine, if_exists='append',
                                           index=False)

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_quadrants
        cvf_quadrants_df.to_sql(name='CVF_Culture_quadrants', con=db.engine,
                                if_exists='append', index=False)

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes_themes_questions
        def FD_create_CSV_question(xcvf_questions_XL, xcvf_culture_modes_themes_df,
                                   xcuadrantes_dict):
            def add_row(xculture_mode_theme_question_id, xtheme,
                        xquestion, xquestion_en, xquadrant, xquestions_df):
                # print(xtheme)
                culture_mode_theme_id = themes_dict.get(xtheme)
                culture_quadrant_id = xcuadrantes_dict.get(xquadrant)
                xquestions_df = xquestions_df.append(
                    pd.DataFrame({'id': [xculture_mode_theme_question_id],
                                  'Culture_mode_theme_question': [xquestion],
                                  'Culture_mode_theme_question_en': [xquestion_en],
                                  'id_culture_mode_theme': [culture_mode_theme_id],
                                  'id_culture_quadrant': [culture_quadrant_id]}))
                return xquestions_df

            themes_dict = \
                cvf_culture_modes_themes_df. \
                    set_index('Culture_mode_theme')['id'].to_dict()
            # print(themes_dict)

            questions_df = pd.DataFrame()
            culture_mode_theme_question_id = 1

            xcvf_questions_XL = xcvf_questions_XL.reset_index()

            for index, row in xcvf_questions_XL.iterrows():
                questions_df = add_row(culture_mode_theme_question_id, row['Tema'],
                                       row['Pregunta'], row['Pregunta_en'],
                                       row['Cuadrante'], questions_df)
                culture_mode_theme_question_id += 1

            return questions_df



        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes_themes_questions
        cvf_culture_modes_themes_questions_df = \
            FD_create_CSV_question(cvf_questions_XL, cvf_culture_modes_themes_df,
                                   cuadrantes_dict)
        cvf_culture_modes_themes_questions_df.to_dict('records')

        cvf_culture_modes_themes_questions_df. \
            to_sql(name='CVF_Culture_modes_themes_questions', con=db.engine,
                   if_exists='append', index=False)
