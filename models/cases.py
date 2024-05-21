from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Identity, ForeignKey, Date
import datetime
from models.users import Base, User,Passport

class Algoritm(Base):
    __tablename__ = 'algoritms'
    algoritm_id = Column(Integer, Identity(start= 1),primary_key=True)
    algoritm_name = Column(String,nullable=False)

class Invidivual(Base):
    __tablename__ = 'individuals'
    individuals_id = Column(Integer, Identity(start= 1),primary_key=True)
    first_name = Column(String,nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String,nullable=True)
    phone = Column(String, nullable=False)
    FK_passports_id = Column(Integer,ForeignKey(Passport.passports_id), nullable=False)

class Statement(Base):
    __tablename__ = 'statements'
    statement_id = Column(Integer, Identity(start= 1),primary_key=True)
    statement_date = Column(Date, nullable=False)
    explanation_text = Column(String,nullable=True)
    fk_individuals_id = Column(Integer,ForeignKey(Invidivual.individuals_id), nullable=False)

class Case(Base):
    __tablename__ = 'active_cases'
    active_cases_id = Column(Integer, Identity(start= 1),primary_key=True)
    FK_statement_id = Column(Integer,ForeignKey(Statement.statement_id), nullable=False)
    fk_user_id = Column(Integer,ForeignKey(User.id), nullable=False)
    fk_algoritm_id = Column(Integer,ForeignKey(Algoritm.algoritm_id), nullable=False)
    number_cases = Column(String,nullable=False)
class Archive(Base):
    __tablename__ = 'arcive_cases'
    arcive_cases_id = Column(Integer, Identity(start= 1),primary_key=True)
    FK_active_cases_id = Column(Integer,ForeignKey(Case.active_cases_id), nullable=False)

class createAlgorithm(BaseModel):
    name:str
class createIndividual(BaseModel):
    firstname: str
    middlename: str
    lastname: str
    datebirthday: datetime.date
    phone: str
    passport_serial: str
    passport_number: str
    issued_by_whom: str
    place_of_birth: str
    passport_date_of_issue: datetime.date
    sex: str
    place_of_residence: str

class createStatement(BaseModel):
    statement_date: datetime.date
    explanation_text: str
    fk_individuals_id: int

class createCase(BaseModel):
    FK_statement_id: int
    fk_user_id: int
    fk_algoritm_id: int
    number_cases: str

class getCase(BaseModel):
    id: int
    number_cases: str
    StatementDate: datetime.date
    UserFio: str
    IndividualFio: str
    StatementText: str
    NameAlgoritm: str
    IdAlgoritm:int
    Status: str
class changeAlgorithm(BaseModel):
    algorithm_id:int
class findByPassport(BaseModel):
    passport_serial: str
    passport_number: str
class getFilterCases(BaseModel):
    id: int
    startDate: datetime.date
    endDate: datetime.date
class getCaseAllInfo(BaseModel):
    number_cases: str
    StatementDate: datetime.date
    UserFio: str
    IndividualFio: str
    StatementText: str
    NameAlgoritm: str
    IdAlgoritm:int
    Status: str
class getIndividual(BaseModel):
    datebirthday: datetime.date
    phone: str
    passport_serial: str
    passport_number: str
    sex: str
    place_of_residence: str
