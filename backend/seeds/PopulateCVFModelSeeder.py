# from datetime import datetime
import pandas as pd
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import  getDataPath
from models import db


# All seeders inherit from Seeder
class PopulateCVFModelSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    # run() will be called by Flask-Seeder
    def run(self):
        pathDB = getDataPath()
        print(pathDB)

    
        # .-.-.-.-.-.-.- questions

        excel_preguntas = pathDB /'CVF_data.xlsx'

        cvf_questions_XL = pd.read_excel(excel_preguntas,
                                         sheet_name='Preguntas')


        # .-.-.-.-.-.-.-.-.-.-.-.- prefijos
        cvf_prefijos_XL = pd.read_excel(excel_preguntas,
                                        sheet_name='Prefijos')


        # .-.-.-.-.-.-.-.-.-.-- cuadrantes
        cvf_cuadrantes_XL = pd.read_excel(excel_preguntas,
                                          sheet_name='Cuadrantes')


        cvf_quadrants_df = cvf_cuadrantes_XL.reset_index()
        cvf_quadrants_df.rename(columns={'index': 'id',
                                         'Cuadrante_es': 'Culture_quadrant_es',
                                         'Cuadrante_en': 'Culture_quadrant_en'},
                                inplace=True)
        cvf_quadrants_df['id'] = 1 + cvf_quadrants_df['id']
       

        cuadrantes_dict = \
            cvf_quadrants_df.set_index('Culture_quadrant_es')['id'].to_dict()
       

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes
        cvf_culture_modes_df = pd.DataFrame({'id': [1],
                                             'Culture_mode_es': ['Colegio'],
                                             'Culture_mode_en': ['School']
                                             })
        cvf_culture_modes_df.to_sql(name='CVF_Culture_modes', con=db.engine,
                                    if_exists='append',
                                    index=False)
        
        print('Cargó CVF_Culture_modes...')
       
        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes_themes
        themes_es = list(cvf_prefijos_XL['Tema_es'])
        prefixes_es = list(cvf_prefijos_XL['Prefijo_es'])

        themes_en = list(cvf_prefijos_XL['Tema_en'])
        prefixes_en = list(cvf_prefijos_XL['Prefijo_en'])


        cvf_culture_modes_dict = \
            {'id': [i for i in range(1, 1 + len(themes_es))],
             'Culture_mode_theme_es': themes_es,
             'Culture_mode_theme_en': themes_en,
             'Questions_prefix_es': prefixes_es,
             'Questions_prefix_en': prefixes_en,
             'id_culture_mode': [1 for i in range(1, 1 + len(themes_es))]}
        cvf_culture_modes_themes_df = pd.DataFrame(cvf_culture_modes_dict)
        # cvf_culture_modes_themes_df.columns

        cvf_culture_modes_themes_df.to_sql(name='CVF_Culture_modes_themes',
                                           con=db.engine, if_exists='append',
                                           index=False)
        print('Cargó CVF_Culture_modes_themes...')

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_quadrants
        cvf_quadrants_df.to_sql(name='CVF_Culture_quadrants', con=db.engine,
                                if_exists='append', index=False)
        
        print('Cargó CVF_Culture_quadrants...')

        # .-.-.-.-.-.-.-.-.-.-.- CVF_Culture_modes_themes_questions
        def FD_create_CSV_question(xcvf_questions_XL, xcvf_culture_modes_themes_df,
                                   xcuadrantes_dict):
            def add_row(xculture_mode_theme_question_id, xtheme,
                        xquestion_es, xquestion_en, xquadrant, xquestions_df):
                # print(xtheme)
                culture_mode_theme_id = themes_dict.get(xtheme)
                culture_quadrant_id = xcuadrantes_dict.get(xquadrant)
                xquestions_df = xquestions_df.append(
                    pd.DataFrame({'id': [xculture_mode_theme_question_id],
                                  'Culture_mode_theme_question_es': [xquestion_es],
                                  'Culture_mode_theme_question_en': [xquestion_en],
                                  'id_culture_mode_theme': [culture_mode_theme_id],
                                  'id_culture_quadrant': [culture_quadrant_id]}))
                return xquestions_df

            themes_dict = xcvf_culture_modes_themes_df.set_index('Culture_mode_theme_es')['id'].to_dict()
            # print(themes_dict)

            questions_df = pd.DataFrame()
            culture_mode_theme_question_id = 1

            xcvf_questions_XL = xcvf_questions_XL.reset_index()

            for index, row in xcvf_questions_XL.iterrows():
                questions_df = add_row(culture_mode_theme_question_id, row['Tema_es'],
                                       row['Pregunta_es'], row['Pregunta_en'],
                                       row['Cuadrante_es'], questions_df)
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
            
        print('Cargó CVF_Culture_modes_themes_questions...')
