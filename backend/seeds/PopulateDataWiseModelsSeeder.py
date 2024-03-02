# from datetime import datetime
import pandas as pd
from flask_security.utils import hash_password
from flask_seeder import Seeder

from common.Utilities import getDataPath, isNotEmpty
from models import (db, User, DW_Areas, DW_Grades, DW_Roles, DW_Schools, DW_Sections,
                    DW_ServiceUnits, DW_Subjects, DW_Tools, DW_Topics, DW_UsersGradesSectionsSubjectsPivot,
                    DW_GradesSectionsPivot, DW_GradesSubjectsPivot,  DW_UsersSchoolRolesPivot,
                    DW_ToolsGradesPivot, DW_ToolsRolesPivot, DW_ToolsAreasPivot,
                    DW_Options,
                    # DW_ToolsOptionsPivot,
                    IRA_Networks, IRA_Nodes_segments, IRA_Networks_modes,
                    IRA_Questions, IRA_Questions_possible_answers, IRA_Cycles)
import os.path

# All seeders inherit from Seeder
class PopulateDataWiseModelsSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 4

    # run() will be called by Flask-Seeder
    def run(self):
        
        pathDB = getDataPath()
        excel_data = pathDB / 'DataWise_data.xlsx'
        file_exists = os.path.isfile(excel_data)

        if file_exists:

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

            # area_director = DW_Roles.query.filter_by(
            #     name_es='Jefe de Area').first()
            # coordinator = DW_Roles.query.filter_by(name_es='Coordinador').first()
            # learning_center = DW_Roles.query.filter_by(
            #     name_es='Learning Center').first()
            # human_development = DW_Roles.query.filter_by(
            #     name_es='Desarrollo Humano').first()

            # dw_association_XL = pd.read_excel(
            #     excel_data, sheet_name='Staff-Roles-Areas-Schools')
            # for index, row in dw_association_XL.iterrows():
            
            #     user = User.query.get(row['StaffID'])
            #     if (user):

            #         if (row['Jefe de Area'] is not None and pd.notnull(row['Jefe de Area'])):
            #             new_association = DW_UsersSchoolRolesPivot(
            #                 user=user,
            #                 school_role=area_director,
            #                 areas=row['Jefe de Area']
            #             )
            #             db.session.add(new_association)
            #         if (row['Coordinador'] is not None and pd.notnull(row['Coordinador'])):
            #             new_association = DW_UsersSchoolRolesPivot(
            #                 user=user,
            #                 school_role=coordinator,
            #                 schools=row['Coordinador']
            #             )
            #             db.session.add(new_association)
            #         if (row['Learning Center'] is not None and pd.notnull(row['Learning Center'])):

            #             new_association = DW_UsersSchoolRolesPivot(
            #                 user=user,
            #                 school_role=learning_center,
            #                 schools=row['Learning Center']
            #             )
            #             db.session.add(new_association)
            #         if (row['Desarrollo Humano'] is not None and pd.notnull(row['Desarrollo Humano'])):
            #             new_association = DW_UsersSchoolRolesPivot(
            #                 user=user,
            #                 school_role=human_development,
            #                 schools=row['Desarrollo Humano']
            #             )
            #             db.session.add(new_association)

            # db.session.commit()

            # print('Cargó Asociación DW_Staff-Roles-Areas-Schools PIVOT ...')

            # Asociación Users-Grades-Sections-Subjects PIVOT
            teacher_role = DW_Roles.query.filter_by(name_en='Teacher').first()
            dw_association_XL = pd.read_excel(
                excel_data, sheet_name='Profesor-Grado-Seccion-Materia')
            for index, row in dw_association_XL.iterrows():
                # print(row)
                user = User.query.get(row['StaffID'])
                if (user):

                    grades_sections = row['Grado-Seccion'].strip().split()
                    subject_code = row['Materia']

                    # print(f"'{grade_name}'-'{section_name}'-'{subject_code}'")

                    subject = DW_Subjects.query.filter_by(
                        code=subject_code).first()

                    if (grades_sections is not None and subject is not None):

                        for grade_section in grades_sections:
                            grade_name = grade_section[:2]
                            section_name = grade_section[-1]
                            grade = DW_Grades.query.filter_by(
                                name_es=grade_name).first()
                            section = DW_Sections.query.filter_by(
                                name_es=section_name).first()

                            if (grade is not None and section is not None):
                                new_association = DW_UsersGradesSectionsSubjectsPivot(
                                    user=user,
                                    grade=grade,
                                    section=section,
                                    subject=subject
                                )
                                db.session.add(new_association)

                                lista_roles = list(
                                    map(lambda x: x.school_role.name_en, user.school_roles))

                                if ("Teacher" not in lista_roles):

                                    new_user_role = DW_UsersSchoolRolesPivot(
                                        user=user,
                                        school_role=teacher_role,
                                        schools=grade.school.code,
                                        areas=subject.area.code
                                    )
                                    db.session.add(new_user_role)
                                else:
                                    user_teacher = [
                                        x for x in user.school_roles if x.school_role.name_en == 'Teacher'][0]
                                    schools_list = user_teacher.schools.split(',')
                                    areas_list = user_teacher.areas.split(',')

                                    if (grade.school.code not in schools_list):
                                        user_teacher.schools = user_teacher.schools+","+grade.school.code
                                    if (subject.area.code not in areas_list):
                                        user_teacher.areas = user_teacher.areas+","+subject.area.code

            print('Cargó Asociación DW_Users-Grades-Sections-Subjects PIVOT...')

            # Asociaciones Tools-Grades Tools-Areas y Tools-Roles
            dw_XL = pd.read_excel(excel_data, sheet_name='Herramientas')
        # se selecciona 1 Tema/Topic por defecto ya que no hay clasificacion aún por este criterio
            topic = DW_Topics.query.get(1)
            # se convierten las columnas a string forzosamente
            dw_XL['Areas'] = dw_XL['Areas'].astype(str)
            dw_XL['Roles'] = dw_XL['Roles'].astype(str)
            dw_XL['Grados'] = dw_XL['Grados'].astype(str)

            for index, row in dw_XL.iterrows():
                # print(row)
                new_tool = DW_Tools(
                    name_es=row['name_es'].strip(),
                    name_en=row['name_en'].strip(),
                    # code=row['name_en'],
                    topic=topic
                )
                db.session.add(new_tool)
                db.session.commit()
                print(f"Creó  DW_Tools= '{row['name_es']}'")

                if isNotEmpty(row['Grados']):
                    if (row['Grados'] == 'All'):

                        grades = DW_Grades.query.with_entities(DW_Grades.id).all()
                        grades_ids = [idx for idx, in grades]
                        for grade_id in grades_ids:
                            new_association = DW_ToolsGradesPivot(
                                grade_id=grade_id,
                                tool=new_tool
                            )
                            # print('crea asociación subject-grade')
                            db.session.add(new_association)
                        print('Cargó Asociación DW_ToolsGrades PIVOT- ALL case')

                    else:
                        grade_names = row['Grados'].strip().split(',')
                        for grade_name in grade_names:
                            grade = DW_Grades.query.filter_by(
                                name_es=grade_name.strip()).first()
                            new_association = DW_ToolsGradesPivot(
                                grade=grade,
                                tool=new_tool
                            )
                            db.session.add(new_association)
                        print('Cargó Asociación DW_ToolsGrades PIVOT- LIST case')

                if isNotEmpty(row['Areas']):

                    if (row['Areas'].strip() == 'All'):

                        areas = DW_Areas.query.with_entities(DW_Areas.id).all()
                        areas_ids = [idx for idx, in areas]
                        for area_id in areas_ids:
                            new_association = DW_ToolsAreasPivot(
                                area_id=area_id,
                                tool=new_tool
                            )
                            # print('crea asociación subject-grade')
                            db.session.add(new_association)
                        print('Cargó Asociación DW_ToolsAreas PIVOT- ALL case')

                    else:
                        area_codes = row['Areas'].strip().split(',')

                        for area_code in area_codes:
                            area = DW_Areas.query.filter_by(
                                code=area_code.strip()).first()
                            new_association = DW_ToolsAreasPivot(
                                area=area,
                                tool=new_tool
                            )
                            db.session.add(new_association)
                        print('Cargó Asociación DW_ToolsAreas PIVOT- LIST case')

                if isNotEmpty(row['Roles']):

                    if (row['Roles'].strip() == 'All'):

                        roles = DW_Roles.query.with_entities(DW_Roles.id).all()
                        roles_ids = [idx for idx, in roles]
                        for role_id in roles_ids:
                            new_association = DW_ToolsRolesPivot(
                                role_id=role_id,
                                tool=new_tool
                            )
                            # print('crea asociación subject-grade')
                            db.session.add(new_association)
                        print('Cargó Asociación DW_ToolsRoles PIVOT- ALL case')

                    else:
                        roles = row['Roles'].strip().split(',')
                        print(f'Roles to associate = {roles}')

                        for role_name in roles:
                            role = DW_Roles.query.filter_by(
                                name_es=role_name.strip()).first()
                            if (role):
                                new_association = DW_ToolsRolesPivot(
                                    role=role,
                                    tool=new_tool
                                )
                                db.session.add(new_association)
                            else:
                                print(f'Rol ={role} no existe!')
                        print('Cargó Asociación DW_ToolsRoles PIVOT- LIST case')

            db.session.commit()

            print('Cargó Tools-Grades Tools-Areas y Tools-Roles...')

            dw_areas_XL = pd.read_excel(excel_data, sheet_name='Opciones')
            dw_areas_XL.to_sql(name='DW_Options', con=db.engine,
                            if_exists='append', index=False)
            print('Cargó DW_Options...')

            # Asociacion Herramientas-Opciones
            dw_XL = pd.read_excel(excel_data, sheet_name='Herramientas-Opciones')
            # usos = ['Uso1', 'Uso2', 'Uso3', 'Uso4',
            #         'Uso5', 'Uso6', 'Uso7', 'Uso8']
            usos = ['Uso1', 'Uso2', 'Uso3', 'Uso4','Uso5']
            for index, row in dw_XL.iterrows():
                tool = DW_Tools.query.filter_by(
                    name_en=row['Tool'].strip()).first()
                if (tool):
                    for uso in usos:
                        if isNotEmpty(row[uso]):
                            option = DW_Options.query.filter_by(
                                name_es=row[uso].strip()).first()
                            if (option):
                                # new_association = DW_ToolsOptionsPivot(
                                #             option=option,
                                #             tool=tool
                                #         )
                                # db.session.add(new_association)
                                # db.session.commit()
                                tool.options.append(option)
                                print(
                                    f'se creó asociación {row["Tool"]}-{row[uso]}')
                            else:
                                print(f'No existe opcion={row[uso]}')
                else:
                    print(f'No existe tool={row["Tool"]}')

            # print('Cargó DW_ToolsOptions Pivot...')
            print('Cargó DW_tools_vs_options Pivot...')

        else:
            print(f'{excel_data} no existe!!!')