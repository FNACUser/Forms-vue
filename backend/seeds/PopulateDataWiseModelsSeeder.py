# from datetime import datetime
import pandas as pd
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import getDataPath
from models import (db, User, DW_Areas, DW_Grades, DW_Roles, DW_Schools, DW_Sections,
                    DW_ServiceUnits, DW_Subjects, DW_Tools, DW_Topics,DW_UsersGradesSectionsSubjectsPivot,
                    DW_GradesSectionsPivot, DW_GradesSubjectsPivot, DW_ToolsGradesSubjectsPivot, DW_UsersSchoolRolesPivot, User)


# All seeders inherit from Seeder
class PopulateDataWiseModelsSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    # run() will be called by Flask-Seeder
    def run(self):
        pathDB = getDataPath()

        excel_data = pathDB / 'DataWise_data.xlsx'

        dw_roles_XL = pd.read_excel(excel_data, sheet_name='Roles')
        dw_roles_XL.to_sql(name='DW_Roles', con=db.engine,
                           if_exists='append', index=False)
        print('Cargó DW_Roles...')

        dw_unidadesservicio_XL = pd.read_excel(
            excel_data, sheet_name='UnidadesServicio')
        dw_unidadesservicio_XL.to_sql(
            name='DW_ServiceUnits', con=db.engine, if_exists='append', index=False)
        print('Cargó DW_Service_Units...')

        dw_escuelas_XL = pd.read_excel(excel_data, sheet_name='Escuelas')
        dw_escuelas_XL.to_sql(name='DW_Schools', con=db.engine,
                              if_exists='append', index=False)
        print('Cargó DW_Schools...')

        dw_grades_XL = pd.read_excel(excel_data, sheet_name='Grades')
        for index, row in dw_grades_XL.iterrows():
            # print(row)
            school = DW_Schools.query.filter_by(
                code=row['school_code']).first()
            if (school):
                new_grade = DW_Grades(
                    name_es=row['name_es'],
                    name_en=row['name_en'],
                    school=school
                )
                db.session.add(new_grade)

            db.session.commit()
        print('Cargó DW_Grades...')

        dw_areas_XL = pd.read_excel(excel_data, sheet_name='Areas')
        dw_areas_XL.to_sql(name='DW_Areas', con=db.engine,
                           if_exists='append', index=False)
        print('Cargó DW_Areas...')

        dw_temas_XL = pd.read_excel(excel_data, sheet_name='Temas')
        dw_temas_XL.to_sql(name='DW_Topics', con=db.engine,
                           if_exists='append', index=False)
        print('Cargó DW_Topics...')

        dw_secciones_XL = pd.read_excel(excel_data, sheet_name='Secciones')
        dw_secciones_XL.to_sql(
            name='DW_Sections', con=db.engine, if_exists='append', index=False)
        print('Cargó DW_Sections...')

        dw_subjects_XL = pd.read_excel(excel_data, sheet_name='Materias')
        for index, row in dw_subjects_XL.iterrows():
            # print(row)
            area = DW_Areas.query.filter_by(code=row['area_id']).first()
            if (area):
                new_subject = DW_Subjects(
                    name_es=row['name_es'],
                    name_en=row['name_en'],
                    code=row['code'],
                    area=area
                )
                db.session.add(new_subject)

            db.session.commit()
        print('Cargó DW_Subjects...')

        # Asociación Grades-Sections
        dw_association_XL = pd.read_excel(
            excel_data, sheet_name='Grades_Sections')
        for index, row in dw_association_XL.iterrows():
            # print(row)
            grade = DW_Grades.query.filter_by(name_es=row['grado']).first()
            section = DW_Sections.query.filter_by(
                name_es=row['seccion']).first()
            if (grade and section):
                new_association = DW_GradesSectionsPivot(
                    grade=grade,
                    code=row['code'],
                    section=section,

                )
               # print('crea asociación grado-seccion')
                db.session.add(new_association)

            db.session.commit()
        print('Cargó Asociación DW_Grades-Sections PIVOT...')

        # Asociación Subjects-Grades
        dw_association_XL = pd.read_excel(
            excel_data, sheet_name='Subjects_Grades')
        for index, row in dw_association_XL.iterrows():
            # print(row)
            grade = DW_Grades.query.filter_by(name_es=row['grade']).first()
            subject = DW_Subjects.query.filter_by(
                name_es=row['subject']).first()
            if (grade and subject):
                new_association = DW_GradesSubjectsPivot(
                    grade=grade,
                    subject=subject
                    # code=row['code']
                )
               # print('crea asociación subject-grade')
                db.session.add(new_association)

            db.session.commit()
        print('Cargó Asociación DW_Grades-Subjects PIVOT...')
        
        
         # Asociación Staff-Roles-Areas-Schools PIVOT
         
        
        area_director=DW_Roles.query.filter_by(name_es='Director de Area').first()
        coordinator=DW_Roles.query.filter_by(name_es='Coordinador').first()
        learning_center=DW_Roles.query.filter_by(name_es='Learning Center').first()
        human_development=DW_Roles.query.filter_by(name_es='Desarrollo Humano').first()
        
        
        dw_association_XL = pd.read_excel(excel_data, sheet_name='Staff-Roles-Areas-Schools')
        for index, row in dw_association_XL.iterrows():
            # print(row)
            user=User.query.get(row['StaffID'])
            if(user):

                if(row['Director de Area'] is not None and pd.notnull(row['Director de Area'])):
                    new_association = DW_UsersSchoolRolesPivot(
                        user=user,
                        school_role=area_director,
                        areas=row['Director de Area']
                    )
                    db.session.add(new_association)
                if(row['Coordinador'] is not None and pd.notnull(row['Coordinador'])):
                    new_association = DW_UsersSchoolRolesPivot(
                        user=user,
                        school_role=coordinator,
                        schools=row['Coordinador']
                    )
                    db.session.add(new_association)
                if(row['Learning Center'] is not None and pd.notnull(row['Learning Center'])):
                    
                    new_association = DW_UsersSchoolRolesPivot(
                        user=user,
                        school_role=learning_center,
                        schools=row['Learning Center']
                    )
                    db.session.add(new_association)
                if(row['Desarrollo Humano'] is not None and pd.notnull(row['Desarrollo Humano'])):
                    new_association = DW_UsersSchoolRolesPivot(
                        user=user,
                        school_role=human_development,
                        schools=row['Desarrollo Humano']
                    )
                    db.session.add(new_association)
        
        db.session.commit()
        
        print('Cargó Asociación DW_Staff-Roles-Areas-Schools PIVOT ...')
        
        
        
        
        # Asociación Users-Grades-Sections-Subjects PIVOT
         
    
        
        dw_association_XL = pd.read_excel(excel_data, sheet_name='Profesor-Grado-Seccion-Materia')
        for index, row in dw_association_XL.iterrows():
            # print(row)
            user=User.query.get(row['StaffID'])
            if(user):

                grades_sections=row['Grado-Seccion'].strip().split()
                subject_code=row['Materia']
                 
                #print(f"'{grade_name}'-'{section_name}'-'{subject_code}'")
                
                subject=DW_Subjects.query.filter_by(code=subject_code).first()
                
                if(grades_sections is not None and  subject is not None):
                    
                    for grade_section in grades_sections:
                        grade_name=grade_section[:2]
                        section_name=grade_section[-1]
                        grade=DW_Grades.query.filter_by(name_es=grade_name).first()
                        section=DW_Sections.query.filter_by(name_es=section_name).first()
                        
                        if(grade is not None and section is not None):
                            new_association = DW_UsersGradesSectionsSubjectsPivot(
                                user=user,
                                grade=grade,
                                section=section,
                                subject=subject
                            )
                            db.session.add(new_association)
                
        
        db.session.commit()
        
        print('Cargó Asociación DW_Users-Grades-Sections-Subjects PIVOT...')

    