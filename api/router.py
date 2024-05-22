from fastapi import APIRouter, Body, Depends, HTTPException,UploadFile,File
from fastapi.responses import JSONResponse
from starlette import status
from typing import Union, Annotated
from sqlalchemy.orm import Session
from database.db import engine_s
from models.users import *
from models.cases import *
from models.methods import *
import hashlib
import shutil
import os

def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()
app_router = APIRouter()

def check_email(email: str, DB: Session = Depends(get_session)): #Проверка почты
    email = DB.query(User).filter(User.email==email).first()
    if email == None:
        return True
    return email
def check_login(login: str, DB: Session = Depends(get_session)): #Проверка логина
    login = DB.query(User).filter(User.name==login).first()
    if login == None:
        return True
    return login
def check_password(login:str,password: str, DB: Session = Depends(get_session)): #Проверка пароля
    user = DB.query(User).filter(User.name==login).first()
    if password == user.password:
        return True
    return False
def check_passport(passport_serial:str,passport_number:str,DB: Session = Depends(get_session)):
    passport_check = DB.query(Passport).filter(Passport.passport_serial==passport_serial,Passport.passport_number==passport_number).first()
    if passport_check == None:
        return True
    return False
def create_passport(item:Register_User|createIndividual,DB: Session = Depends(get_session)):
    passport = Passport(passport_serial=item.passport_serial,passport_number=item.passport_number,issued_by_whom=item.issued_by_whom,place_of_birth=item.place_of_birth,birthdate=item.datebirthday,passport_date_of_issue=item.passport_date_of_issue,sex=item.sex,place_of_residence=item.place_of_residence)
    try:
        DB.add(passport)
        DB.commit()
        DB.refresh(passport)
        return(passport.passports_id)
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})

def delete_passport(passport_id:int,DB: Session = Depends(get_session)):
    passport =  DB.query(Passport).filter(Passport.passports_id == passport_id).first()
    if passport != None:
        try:
            DB.delete(passport)
            DB.commit()
        except HTTPException:
            return JSONResponse(status_code=404, content={"message":"Ошибка"})
        

@app_router.post("/api/department",tags=['Departments'])
def create_department(item:createDepartment,DB: Session = Depends(get_session)):
    department = DB.query(Department).filter(Department.city==item.city,Department.street==item.street,Department.house_number==item.house_number).first()
    if department is not None:
        return JSONResponse(status_code=400, content={"message":"Отдел с таким адресом уже присутствует в системе!"})
    department=Department(city=item.city,postal_code=item.postal_code,street=item.street,house_number=item.house_number,name_department=item.name_department)
    try:
        DB.add(department)
        DB.commit()
        DB.refresh(department)
        return JSONResponse(status_code= 200, content={"message": "Отдел добавлен!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта")

@app_router.get("/api/departments",tags=['Departments'])
def get_departments(DB: Session = Depends(get_session)):
    departments = DB.query(Department).filter(Department.departments_id!=1).all()
    if len(departments)==0:
        return JSONResponse(status_code=404, content={"message":"Отделы не найдены!"})
    get_departments = []
    for i in range(len(departments)):
        adress = departments[i].city+', '+ departments[i].street+', '+departments[i].house_number+', '+departments[i].postal_code
        user = DB.query(User).filter(User.FK_user_roles_id==4,User.fk_department_id==departments[i].departments_id).first()
        if user is None:
            userFIO = "Не указан"
        else:
            userFIO = user.first_name +' '+user.middle_name[0]+'.'+user.last_name[0]+'.'
        this_department = getDepartments(id=departments[i].departments_id,NameDepartments=departments[i].name_department,Adress=adress,NachFIO=userFIO)
        get_departments.append(this_department)
    return get_departments

@app_router.get("/api/user/{id}",tags=['Users']) #Поиск пользователя по id
def get_user(id:int ,DB: Session = Depends(get_session)):
    user =  DB.query(User).filter(User.id == id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    passport = DB.query(Passport).filter(Passport.passports_id == user.fk_passports_id).first()
    user = getUser(email=user.email,firstname=user.first_name,middlename=user.middle_name,lastname=user.last_name,phone=user.phone,sex=passport.sex,passport_serial=passport.passport_serial,passport_number=passport.passport_number,datebirthday=passport.birthdate)
    return user
@app_router.get("/api/users/roles",tags=['Users']) #Вывод всех ролей
def get_roles(DB: Session = Depends(get_session)):
    roles = DB.query(UserRoles).all()
    if roles == None:
        return JSONResponse(status_code= 404, content={"message": "Роли не найдены"})
    return roles

@app_router.post("/api/users/sign-up",tags=['Users']) #Регистрация нового пользователя
def create_user(item: Register_User,DB: Session = Depends(get_session)):
    try:
        department = DB.query(Department).filter(Department.departments_id==item.fk_department_id).first()
        if department is None:
            return JSONResponse(status_code= 404, content={"message": "Указанный отдел не найден!"})
        if item.role != 1:
            if department.departments_id == 1:
                return JSONResponse(status_code= 400, content={"message": "В этот отдел может быть добавлен только администартор!"})
            users_department = DB.query(User).filter(User.fk_department_id==item.fk_department_id).first()
            if (users_department is None) and (item.role!=4):
                return JSONResponse(status_code= 404, content={"message": "Начальник отдела не найден!"})
            if (users_department is not None) and (item.role==4):
                return JSONResponse(status_code= 400, content={"message": "Начальник отдела уже добавлен!"})
        else:
            item.fk_department_id = 1 
        email_checker = check_email(item.email,DB)
        if email_checker!=True:
            return JSONResponse(status_code= 400, content={"message": "Данный e-mail уже зарегистрирован в системе"})
        login_checker = check_login(item.name,DB)
        if login_checker!=True:
            return JSONResponse(status_code= 400, content={"message": "Пользователь с данным логином уже зарегистрирован в системе"})
        passport_checker = check_passport(item.passport_serial,item.passport_number,DB)
        if passport_checker == False:
            return JSONResponse(status_code= 400, content={"message": "Пользователь с данным паспортом уже зарегистрирован в системе"})
        add_passport = create_passport(item, DB)
        password_code = item.password.encode('utf-8')
        hash_password = hashlib.sha256(password_code)
        user = User(name=item.name,email=item.email,password=hash_password.hexdigest(),FK_user_roles_id=item.role,first_name=item.firstname,middle_name=item.middlename,last_name=item.lastname,users_rank=item.users_rank,appointment=item.appointment,phone=item.phone,fk_passports_id=add_passport,fk_department_id=item.fk_department_id)
        if user is None:
            return JSONResponse(status_code=404, detail="Объект не определен")
        DB.add(user)
        DB.commit()
        DB.refresh(user)
        
        os.mkdir(f'media/{user.id}')
        os.mkdir(f'media/{user.id}/profile')
        if item.role == 2:
            os.mkdir(f'media/{user.id}/cases')
        return JSONResponse(status_code= 200, content={"message": "Пользователь добавлен"})
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта")

@app_router.post("/api/users/sign-in",tags=['Users']) #Вход в аккаунт
def sign_in(item: SignIn_User,DB: Session = Depends(get_session)):
    try:
        login_checker = check_login(item.name,DB)
        if login_checker==True:
            return JSONResponse(status_code= 400, content={"message": "Пользователя с таким именем не существует"})
        password_code = item.password.encode('utf-8')
        hash_password = hashlib.sha256(password_code)
        password_checker = check_password(item.name,hash_password.hexdigest(),DB)
        if password_checker == False:
            return JSONResponse(status_code= 400, content={"message": "Неверный пароль"})
        user = getSignInUser(id=login_checker.id,FK_user_roles_id=login_checker.FK_user_roles_id)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта {user}")
    
@app_router.put("/api/edit_login/{id}",tags=['Users'])#Изменение логина
def edit_login(id:int,item:changeDataUser,DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id==id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    if user.name != item.old_data:
        return JSONResponse(status_code= 400, content={"message": "Текущий логин введен неверно"})
    login_checker = check_login(item.new_data,DB)
    if login_checker!=True and login_checker.name != user.name:
        return JSONResponse(status_code= 400, content={"message": "Логин занят другим пользователем"})
    user.name=item.new_data
    try:
        DB.commit()
        DB.refresh(user)
        return JSONResponse(status_code=200, content={"message": "Данные обновлены"})
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
@app_router.put("/api/edit_email/{id}",tags=['Users'])#Изменение почты
def edit_email(id:int,item:changeDataUser,DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id==id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    if user.email != item.old_data:
        return JSONResponse(status_code= 400, content={"message": "Текущая почта введена неверно"})
    email_checker = check_email(item.new_data,DB)
    if email_checker!=True and email_checker.name != user.email:
        return JSONResponse(status_code= 400, content={"message": "Почта занят другим пользователем"})
    user.email=item.new_data
    try:
        DB.commit()
        DB.refresh(user)
        return JSONResponse(status_code=200, content={"message": "Данные обновлены"})
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
@app_router.put("/api/edit_password_user/{id}",tags=['Users']) #Изменение пароля
def edit_password_user(id:int,item:changePasswordUser,DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id==id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    password_code = item.old_password.encode('utf-8')
    hash_password = hashlib.sha256(password_code)
    password_cheker = check_password(user.name,hash_password.hexdigest(),DB)
    if password_cheker == False:
        return JSONResponse(status_code=400, content={"message": "Старый пароль указан неверно"})
    password_code = item.new_password.encode('utf-8')
    hash_password = hashlib.sha256(password_code)
    user.password = hash_password.hexdigest()
    try:
        DB.commit()
        DB.refresh(user)
        return JSONResponse(status_code=200, content={"message": "Данные обновлены"})
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
    

@app_router.post("/api/create_individual",tags=['Individual']) #Добавление заявителя
def create_individual(item: createIndividual,DB: Session = Depends(get_session)):
    try:
        passport_checker = check_passport(item.passport_serial,item.passport_number,DB)
        if passport_checker == False:
            return JSONResponse(status_code= 400, content={"message": "Заявитель с данным паспортом уже зарегистрирован в системе"})
        add_passport = create_passport(item, DB)
        individual = Invidivual(first_name=item.firstname,middle_name=item.middlename,last_name=item.lastname,phone=item.phone,FK_passports_id=add_passport)
        if individual is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        DB.add(individual)
        DB.commit()
        DB.refresh(individual)
        return individual.individuals_id
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта")
@app_router.get("/api/get_individual/{id}",tags=['Individual'])
def get_individual_by_id(id:int,DB: Session = Depends(get_session)):
    cases = DB.query(Case).filter(Case.active_cases_id==id).first()
    if cases is None:
        return JSONResponse(status_code= 404, content={"message": "Дело не найдено"})
    individual_id = DB.query(Statement).filter(cases.FK_statement_id==Statement.statement_id).first().fk_individuals_id
    individual = DB.query(Invidivual).filter(Invidivual.individuals_id==individual_id).first()
    if individual is None:
        return JSONResponse(status_code= 404, content={"message": "Заявитель не найден"})
    passport = DB.query(Passport).filter(individual.FK_passports_id==Passport.passports_id).first()
    get_individ = getIndividual(datebirthday=passport.birthdate,phone=individual.phone,passport_serial=passport.passport_serial,passport_number=passport.passport_number,sex=passport.sex,place_of_residence=passport.place_of_residence)
    return get_individ
@app_router.post("/api/create_statement",tags=['Individual'])
def create_statement(item: createStatement,DB: Session = Depends(get_session)):
    individual = DB.query(Invidivual).filter(Invidivual.individuals_id == item.fk_individuals_id).first()
    if individual is None:
        return JSONResponse(status_code= 404, content={"message": "Заявитель не найден"})
    statement = Statement(statement_date=item.statement_date,explanation_text=item.explanation_text,fk_individuals_id=item.fk_individuals_id)
    if statement is None:
        return JSONResponse(status_code= 404, content={"message": "Объект не определен"})
    try:
        DB.add(statement)
        DB.commit()
        DB.refresh(statement)
        return statement.statement_id
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта")
@app_router.get("/api/algoritms",tags=['Algorithm'])
def get_algoritms(DB: Session = Depends(get_session)):
    algoritm = DB.query(Algoritm).all()
    return algoritm

def check_user(id:int,DB: Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user is None:
        return False
    return True
def check_statement(id:int,DB: Session = Depends(get_session)):
    statement = DB.query(Statement).filter(Statement.statement_id == id).first()
    if statement is None:
        return False
    return True
def check_algoritm(id:int,DB: Session = Depends(get_session)):
    algoritm = DB.query(Algoritm).filter(Algoritm.algoritm_id == id).first()
    if algoritm is None:
        return False
    return True
def check_unique_statement(id:int, DB: Session = Depends(get_session)):
    case = DB.query(Case).filter(Case.FK_statement_id==id).first()
    if case is None:
        return True
    return False
@app_router.post("/api/case",tags=['Case'])
def create_case(item:createCase,DB: Session = Depends(get_session)):
    if check_user(item.fk_user_id,DB) == False:
        return JSONResponse(status_code= 404, content={"message": "Следователь не найден в системе"})
    if check_statement(item.FK_statement_id,DB) == False:
        return JSONResponse(status_code= 404, content={"message": "Заявление не найдено в системе"})
    if check_algoritm(item.fk_algoritm_id,DB) == False:
        return JSONResponse(status_code= 404, content={"message": "Алгоритм не найден в системе"})
    if check_unique_statement(item.FK_statement_id,DB)==False:
        return JSONResponse(status_code= 400, content={"message": "Заявление должно быть уникально"})
    user = DB.query(User).filter(User.id==item.fk_user_id).first()
    if user.FK_user_roles_id != 2:
        return JSONResponse(status_code= 400, content={"message": "Только следователь может заводить дела!"})
    cases = Case(FK_statement_id=item.FK_statement_id,fk_user_id=item.fk_user_id,fk_algoritm_id=item.fk_algoritm_id,number_cases=item.number_cases)
    if cases is None:
        return JSONResponse(status_code= 404, content={"message": "Объект не определен"})
    try:
        DB.add(cases)
        DB.commit()
        DB.refresh(cases)
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/documents')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/reclaim')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/reclaim/detailing')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/reclaim/income')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/reclaim/passport')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/extract')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/extract/money_orders')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/extract/detailing')
        os.mkdir(f'media/{item.fk_user_id}/cases/{cases.active_cases_id}/extract/screenshot')
        return JSONResponse(status_code= 200, content={"message": "Дело сформировано"})
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Произошла ошибка при добавлении объекта")
@app_router.put("/api/case_edit_alg/{id}",tags=['Case'])
def edit_cases_algorithm(id:int,item:changeAlgorithm,DB:Session = Depends(get_session)):
    if check_algoritm(item.algorithm_id,DB) == False:
        return JSONResponse(status_code= 404, content={"message": "Алгоритм не найден в системе"})
    cases = DB.query(Case).filter(Case.active_cases_id==id).first()
    if cases is None:
        return JSONResponse(status_code= 404, content={"message": "Дело не найдено в системе"})
    if cases.fk_algoritm_id == item.algorithm_id:
        return JSONResponse(status_code= 400, content={"message": "Этот алгоритм уже используется в деле"})
    cases.fk_algoritm_id = item.algorithm_id
    try:
        DB.commit()
        DB.refresh(cases)
        return JSONResponse(status_code=200, content={"message": "Данные обновлены"})
    except HTTPException:
        return JSONResponse(status_code=404, content={"message":"Ошибка"})
@app_router.get("/api/case_all_info/{id}",tags=['Case'])
def get_case_all_info(id:int,DB:Session = Depends(get_session)):
    cases = DB.query(Case).filter(Case.active_cases_id == id).first()
    if cases is None:
        return JSONResponse(status_code= 404, content={"message": "Дело не найдено"})
    user = DB.query(User).filter(User.id==cases.fk_user_id).first()
    numberCases = cases.number_cases
    userFIO = user.first_name + ' ' + user.middle_name[0]+'. ' + user.last_name[0]+'.'
    statement = DB.query(Statement).filter(Statement.statement_id == cases.FK_statement_id).first()
    statementText = statement.explanation_text
    statementDate = statement.statement_date
    individual = DB.query(Invidivual).filter(Invidivual.individuals_id == statement.fk_individuals_id).first()
    individualFIO = individual.first_name + ' ' + individual.middle_name[0]+'. ' + individual.last_name[0]+'.'
    algoritm = DB.query(Algoritm).filter(Algoritm.algoritm_id == cases.fk_algoritm_id).first()
    algoritmName = algoritm.algoritm_name
    algoritmId = algoritm.algoritm_id
    archive = DB.query(Archive).filter(Archive.FK_active_cases_id == cases.active_cases_id).first()
    if archive is None:
        status = "В процессе"
    else:
        status = "Завершено"
    this_case = getCase(id=cases.active_cases_id,number_cases=numberCases,StatementDate=statementDate,UserFio=userFIO,IndividualFio=individualFIO,StatementText=statementText,NameAlgoritm=algoritmName,IdAlgoritm=algoritmId,Status=status)
    return this_case
@app_router.get("/api/user/{id}/cases",tags=['Case'])
def get_user_cases(id:int,DB:Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == id).first()
    if user is None:
        return JSONResponse(status_code= 404, content={"message": "Пользователь не найден в системе"})
    if int(user.FK_user_roles_id) == 1:
        cases = DB.query(Case).all()
    elif int(user.FK_user_roles_id) == 2:
        cases = DB.query(Case).filter(Case.fk_user_id == user.id).all()
    if cases is None:
        return JSONResponse(status_code= 404, content={"message": "Дел не найдено"})
    get_cases = []
    for i in range(len(cases)):
        user = DB.query(User).filter(User.id==cases[i].fk_user_id).first()
        numberCases = cases[i].number_cases
        userFIO = user.first_name + ' ' + user.middle_name[0]+'.' + user.last_name[0]+'.'
        statement = DB.query(Statement).filter(Statement.statement_id == cases[i].FK_statement_id).first()
        statementText = statement.explanation_text
        statementDate = statement.statement_date
        individual = DB.query(Invidivual).filter(Invidivual.individuals_id == statement.fk_individuals_id).first()
        individualFIO = individual.first_name + ' ' + individual.middle_name[0]+'.' + individual.last_name[0]+'.'
        algoritm = DB.query(Algoritm).filter(Algoritm.algoritm_id == cases[i].fk_algoritm_id).first()
        algoritmName = algoritm.algoritm_name
        algoritmId = algoritm.algoritm_id
        archive = DB.query(Archive).filter(Archive.FK_active_cases_id == cases[i].active_cases_id).first()
        if archive is None:
            status = "В процессе"
        else:
            status = "Завершено"
        this_case = getCase(id=cases[i].active_cases_id,number_cases=numberCases,StatementDate=statementDate,UserFio=userFIO,IndividualFio=individualFIO,StatementText=statementText,NameAlgoritm=algoritmName,IdAlgoritm=algoritmId,Status=status)
        get_cases.append(this_case)
    return get_cases
@app_router.get("/api/users/cases",tags=['Case'])
def get_cases(DB:Session = Depends(get_session)):
    cases = DB.query(Case).all()
    return cases
@app_router.get("/api/case/{id}",tags=['Case'])
def get_case(id:int,DB:Session = Depends(get_session)):
    case = DB.query(Case).filter(Case.active_cases_id == id).first()
    if case is None:
        return JSONResponse(status_code= 404, content={"message": "Дело не найдено"})
    return case
@app_router.post("/api/individual_prt",tags=['Individual'])
def get_individual(item:findByPassport,DB:Session = Depends(get_session)):
    passports = DB.query(Passport).filter(Passport.passport_serial==item.passport_serial,Passport.passport_number==item.passport_number).first()
    if passports is None:
        return JSONResponse(status_code= 404, content={"message": "Паспорт не найден в системе"})
    individual = DB.query(Invidivual).filter(Invidivual.FK_passports_id == passports.passports_id).first()
    if individual is None:
        return JSONResponse(status_code= 404, content={"message": "Заявитель не найден в системе"})
    return individual.individuals_id
@app_router.post("/api/user/cases/filter",tags=['Case'])
def get_filter_user_cases(item:getFilterCases,DB:Session = Depends(get_session)):
    user = DB.query(User).filter(User.id == item.id).first()
    if user is None:
        return JSONResponse(status_code= 404, content={"message": "Пользователь не найден в системе"})
    if int(user.FK_user_roles_id) == 1:
        cases = DB.query(Case).all()
    elif int(user.FK_user_roles_id) == 2:
        cases = DB.query(Case).filter(Case.fk_user_id == user.id).all()
    if cases is None:
        return JSONResponse(status_code= 404, content={"message": "Дел не найдено"})
    get_cases = []
    for i in range(len(cases)):
        statement = DB.query(Statement).filter(Statement.statement_id == cases[i].FK_statement_id).first()
        statementText = statement.explanation_text
        statementDate = statement.statement_date
        if statementDate >= item.startDate and statementDate <= item.endDate:
            user = DB.query(User).filter(User.id==cases[i].fk_user_id).first()
            userFIO = user.first_name + ' ' + user.middle_name[0]+'.' + user.last_name[0]+'.'
            numberCases=cases[i].number_cases
            individual = DB.query(Invidivual).filter(Invidivual.individuals_id == statement.fk_individuals_id).first()
            individualFIO = individual.first_name + ' ' + individual.middle_name[0]+'.' + individual.last_name[0]+'.'
            algoritm = DB.query(Algoritm).filter(Algoritm.algoritm_id == cases[i].fk_algoritm_id).first()
            algoritmName = algoritm.algoritm_name
            algoritmId = algoritm.algoritm_id
            archive = DB.query(Archive).filter(Archive.FK_active_cases_id == cases[i].active_cases_id).first()
            if archive is None:
                status = "В процессе"
            else:
                status = "Завершено"
            this_case = getCase(id=cases[i].active_cases_id,number_cases=numberCases,StatementDate=statementDate,UserFio=userFIO,IndividualFio=individualFIO,StatementText=statementText,NameAlgoritm=algoritmName,IdAlgoritm=algoritmId,Status=status)
            get_cases.append(this_case)
        else:
            continue
    return get_cases

