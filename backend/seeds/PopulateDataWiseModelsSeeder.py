from datetime import datetime
import pandas as pd
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import  getDataPath
from models import db


# All seeders inherit from Seeder
class PopulateDataWiseModelsSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    # run() will be called by Flask-Seeder
    def run(self):
        pathDB = getDataPath()
       
        excel_data = pathDB /'DataWise_data.xlsx'

        dw_roles_XL = pd.read_excel(excel_data,sheet_name='Roles')
        dw_roles_XL.to_sql(name='DW_Roles',con=db.engine, if_exists='append',index=False)
        print('Carga DW_Roles...')
       
        dw_unidadesservicio_XL = pd.read_excel(excel_data,sheet_name='UnidadesServicio')
        dw_unidadesservicio_XL.to_sql(name='DW_ServiceUnits',con=db.engine, if_exists='append',index=False)
        print('Carga Unidades de Servicio...')

        dw_escuelas_XL = pd.read_excel(excel_data,sheet_name='Escuelas')
        dw_escuelas_XL.to_sql(name='DW_Schools',con=db.engine, if_exists='append',index=False)
        print('Carga Schools...')
        
        dw_areas_XL = pd.read_excel(excel_data,sheet_name='Areas')
        dw_areas_XL.to_sql(name='DW_Areas',con=db.engine, if_exists='append',index=False)
        print('Carga Areas...')
        
        dw_temas_XL = pd.read_excel(excel_data,sheet_name='Temas')
        dw_temas_XL.to_sql(name='DW_Topics',con=db.engine, if_exists='append',index=False)
        print('Carga Temas...')
        
        # dw_secciones_XL = pd.read_excel(excel_data,sheet_name='Secciones')
        # dw_secciones_XL.to_sql(name='DW_Sections',con=db.engine, if_exists='append',index=False)
        
        # dw_grades_XL = pd.read_excel(excel_data,sheet_name='Grades')
        # dw_grades_XL.to_sql(name='DW_Grades',con=db.engine, if_exists='append',index=False)
        
        # dw_subjects_XL = pd.read_excel(excel_data,sheet_name='Materias')
        # dw_subjects_XL.to_sql(name='DW_Subjects',con=db.engine, if_exists='append',index=False)
        
        # dw_tools_XL = pd.read_excel(excel_data,sheet_name='Herramientas')
        # dw_tools_XL.to_sql(name='DW_Tools',con=db.engine, if_exists='append',index=False)
        
       


        