from datetime import datetime
import pandas as pd
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import  getDataPath
from models import (db, DW_Areas,DW_Grades,DW_Roles,DW_Schools,DW_Sections,
                    DW_ServiceUnits,DW_Subjects,DW_Tools,DW_Topics,
                    DW_GradesSectionsPivot,DW_GradesSubjectsPivot,DW_ToolsGradesSubjectsPivot,DW_UsersSchoolRolesPivot,User)


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
        print('Cargó DW_Roles...')
       
        dw_unidadesservicio_XL = pd.read_excel(excel_data,sheet_name='UnidadesServicio')
        dw_unidadesservicio_XL.to_sql(name='DW_ServiceUnits',con=db.engine, if_exists='append',index=False)
        print('Cargó Unidades de Servicio...')

        dw_escuelas_XL = pd.read_excel(excel_data,sheet_name='Escuelas')
        dw_escuelas_XL.to_sql(name='DW_Schools',con=db.engine, if_exists='append',index=False)
        print('Cargó Schools...')
        
        dw_areas_XL = pd.read_excel(excel_data,sheet_name='Areas')
        dw_areas_XL.to_sql(name='DW_Areas',con=db.engine, if_exists='append',index=False)
        print('Cargó Areas...')
        
        dw_temas_XL = pd.read_excel(excel_data,sheet_name='Temas')
        dw_temas_XL.to_sql(name='DW_Topics',con=db.engine, if_exists='append',index=False)
        print('Cargó Temas...')
        
        dw_secciones_XL = pd.read_excel(excel_data,sheet_name='Secciones')
        dw_secciones_XL.to_sql(name='DW_Sections',con=db.engine, if_exists='append',index=False)
        print('Carga Secciones...')
        
        dw_grades_XL = pd.read_excel(excel_data,sheet_name='Grades')
        for index, row in dw_grades_XL.iterrows():
            # print(row)
            school=DW_Schools.query.filter_by(name_es=row['school']).first()
            if(school):
                new_grade=DW_Grades(
                        name_es=row['name_es'],
                        name_en=row['name_en'],
                        school=school      
                )
                db.session.add(new_grade)
        
            db.session.commit()
        print('Cargó Grados...')
        
        dw_subjects_XL = pd.read_excel(excel_data,sheet_name='Materias')
        for index, row in dw_subjects_XL.iterrows():
            # print(row)
            area=DW_Areas.query.filter_by(code=row['area_id']).first()
            if(area):
                new_subject=DW_Subjects(
                        name_es=row['name_es'],
                        name_en=row['name_en'],
                        code=row['code'],
                        area=area      
                )
                db.session.add(new_subject)
        
            db.session.commit()
        print('Cargó Materias...')
        
        #Asociación Grades-Sections
        dw_association_XL = pd.read_excel(excel_data,sheet_name='Grades_Sections')
        for index, row in  dw_association_XL.iterrows():
            # print(row)
            grade=DW_Grades.query.filter_by(name_es=row['grado']).first()
            section=DW_Sections.query.filter_by(name_es=row['seccion']).first()
            if(grade and section ):
                new_association=DW_GradesSectionsPivot(
                        grade=grade,
                        section=section,
                        code=row['code']  
                )
               # print('crea asociación grado-seccion')
                db.session.add(new_association)
        
            db.session.commit()
        print('Cargó Asociación Grados-Secciones...')
        
        #Asociación Subjects-Grades
        dw_association_XL = pd.read_excel(excel_data,sheet_name='Subjects_Grades')
        for index, row in  dw_association_XL.iterrows():
            # print(row)
            grade=DW_Grades.query.filter_by(name_es=row['grade']).first()
            subject=DW_Subjects.query.filter_by(name_es=row['subject']).first()
            if(grade and subject ):
                new_association=DW_GradesSubjectsPivot(
                        grade=grade,
                        subject=subject
                       # code=row['code']  
                )
               # print('crea asociación subject-grade')
                db.session.add(new_association)
        
            db.session.commit()
        print('Cargó Asociación Grados-Materias...')
        
       
        
        # dw_tools_XL = pd.read_excel(excel_data,sheet_name='Herramientas')
        # dw_tools_XL.to_sql(name='DW_Tools',con=db.engine, if_exists='append',index=False)
        
       


        