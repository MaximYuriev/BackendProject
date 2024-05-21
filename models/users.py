from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Identity, ForeignKey, Date
from sqlalchemy.orm import declarative_base
import datetime
Base = declarative_base()
class UserRoles(Base):
    __tablename__ = 'user_roles'
    user_role_id = Column(Integer, Identity(start= 1),primary_key=True)
    name_role = Column(String, nullable=False)
    user_rights = Column(String, nullable=False)

class Passport(Base):
    __tablename__ = 'passports'
    passports_id = Column(Integer,Identity(start= 1),primary_key=True)
    passport_serial = Column(String,nullable=False)
    passport_number = Column(String,nullable=False)
    issued_by_whom = Column(String,nullable=False)
    place_of_birth = Column(String,nullable=False)
    birthdate = Column(Date, nullable=False)
    passport_date_of_issue = Column(Date,nullable=False)
    sex = Column(String,nullable=False)
    place_of_residence = Column(String,nullable=False)

class Department(Base):
    __tablename__ = 'departments'
    departments_id = Column(Integer, Identity(start= 1),primary_key=True)
    city = Column(String, nullable=False)
    postal_code = Column(String,nullable= False) 
    street = Column(String, nullable=False)
    house_number = Column(String,nullable=False)
    name_department = Column(String,nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Identity(start= 1),primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String,nullable= False) 
    password = Column(String, nullable=False)
    FK_user_roles_id = Column(Integer,ForeignKey(UserRoles.user_role_id),nullable=False)
    first_name = Column(String,nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String,nullable=True)
    phone = Column(String, nullable=False)
    users_rank = Column(String, nullable=False)
    appointment = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    fk_passports_id = Column(Integer,ForeignKey(Passport.passports_id) , nullable=False)
    fk_department_id = Column(Integer,ForeignKey(Department.departments_id) , nullable=False)

class New_Respons(BaseModel):
    message:str
class createRole(BaseModel):
    name:str
    rights:str
class Register_User(BaseModel):
    name: str
    email: str
    password: str
    role: int
    firstname: str
    middlename: str
    lastname: str
    users_rank: str
    appointment: str
    datebirthday: datetime.date
    phone: str
    passport_serial: str
    passport_number: str
    issued_by_whom: str
    place_of_birth: str
    passport_date_of_issue: datetime.date
    sex: str
    place_of_residence: str
    fk_department_id:int

class Main_Roles(BaseModel):
    name: str
    user_rights: str

class SignIn_User(BaseModel):
    name: str
    password: str
class getSignInUser(BaseModel):
    id:int
    FK_user_roles_id:int
class getUser(BaseModel):
    email: str
    firstname: str
    middlename: str
    lastname: str
    phone: str
    sex: str
    passport_serial: str
    passport_number: str
    datebirthday: datetime.date

class changeDataUser(BaseModel):
    old_data: str
    new_data: str

class changePasswordUser(BaseModel):
    old_password: str
    new_password: str

class createDepartment(BaseModel):
    city: str
    postal_code: str
    street: str
    house_number: str
    name_department: str

class getDepartments(BaseModel):
    id:int
    NameDepartments:str
    Adress:str
    NachFIO:str