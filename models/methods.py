from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Identity, ForeignKey, Date
import datetime
from models.users import Base, User,Passport
from models.cases import Case

class Clarif(Base):
    __tablename__ = 'clarif'
    id_clarif = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    date_clarif = Column(Date, nullable=False)
    phone = Column(String,nullable=False)
    email = Column(String,nullable=False)
    information = Column(String,nullable=False)

class Reclaim(Base):
    __tablename__ = 'reclaim'
    id_reclaim = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    passport = Column(String,nullable=False)
    income = Column(String,nullable=False)
    detailing = Column(String,nullable=False)

class Track(Base):
    __tablename__ = 'track'
    id_track = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    account = Column(String,nullable=True)
    сorrespondence = Column(String,nullable=True)
    history = Column(String,nullable=True)
    track_money = Column(String,nullable=True)
    logfile = Column(String,nullable=True)
    antivirus = Column(String,nullable=True)

class Inspect(Base):
    __tablename__ = 'inspect'
    id_inspect = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False)
    date_inspect = Column(Date, nullable=False)
    begin_inspect = Column(String,nullable=False)
    end_inspect = Column(String,nullable=False)
    message_inspect = Column(String,nullable=False)
    from_message_inspect = Column(String,nullable=False)
    place_of_inspect = Column(String,nullable=False)
    inspect_exam = Column(String,nullable=False)
    technical_means = Column(String,nullable=False)
    conditions = Column(String,nullable=False)
    establish = Column(String,nullable=False)
    photography = Column(String,nullable=False)
    sized_items = Column(String,nullable=False)
    items_for_inspect = Column(String,nullable=False)
    familiarization = Column(String,nullable=False)

class ProceduralPosition(Base):
    __tablename__ = 'procedural_position'
    id_procedural_position = Column(Integer, Identity(start= 1),primary_key=True)
    name_position = Column(String, nullable=False)

class PersonsInvolved(Base):
    __tablename__ = 'persons_involved'
    id_persons_involved = Column(Integer, Identity(start= 1),primary_key=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    residence = Column(String, nullable=True)
    fk_procedural_position = Column(Integer,ForeignKey(ProceduralPosition.id_procedural_position),nullable=False)
    notes = Column(String, nullable=False)
    petition = Column(Integer,nullable=True)


class InspectPersonsInvolved(Base):
    __tablename__ = 'inspect_persons_involved'
    id_persons_involved = Column(Integer, ForeignKey(PersonsInvolved.id_persons_involved),primary_key=True)
    id_inspect = Column(Integer, ForeignKey(Inspect.id_inspect),primary_key=True)

class Check(Base):
    __tablename__ = 'check_comp'
    id_check = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    checks = Column(String,nullable=False)

class Expertise(Base):
    __tablename__ = 'expertise'
    id_expertise = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    app_comp = Column(String,nullable=True)
    prog_comp = Column(String,nullable=True)
    inf_comp = Column(String,nullable=True)
    comp_net = Column(String,nullable=True)

class Extract(Base):
    __tablename__ = 'extract_meth'
    id_extract = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    money_orders = Column(String,nullable=True)
    detailing = Column(String,nullable=True)
    screenshot = Column(String,nullable=True)

class Quest(Base):
    __tablename__ = 'quest'
    id_quest = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    have = Column(String,nullable=True)
    reg = Column(String,nullable=True)
    know = Column(String,nullable=True)
    have_bank = Column(String,nullable=True)
    connect_online = Column(String,nullable=True)
    know_cards = Column(String,nullable=True)
    pay_site = Column(String,nullable=True)

class Set(Base):
    __tablename__ = 'set_criminal'
    id_criminal = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    criminal = Column(String,nullable=False)

class Witnes(Base):
    __tablename__ = 'witnes'
    id_witnes = Column(Integer, Identity(start= 1),primary_key=True)
    fk_active_case_id = Column(Integer,ForeignKey(Case.active_cases_id),nullable=False )
    witnes = Column(String,nullable=False)

class createProceduralPosition(BaseModel):
    name: str
class createClarif(BaseModel):
    user_id:int
    case_id:int
    date_clarif:datetime.date
    phone:str
    email:str
    information:str
class createTrack(BaseModel):
    user_id:int
    case_id:int
    account:str
    сorrespondence:str
    history:str
    track_money:str
    logfile:str
    antivirus:str
class createInspect(BaseModel):
    user_id:int
    case_id:int
    date_inspect:datetime.date
    begin_inspect:str
    end_inspect:str
    message_inspect:str
    from_message_inspect:str
    inspect_exam:str
    place_of_inspect:str
    technical_means:str
    conditions:str
    establish:str
    photography:str
    sized_items:str
    items_for_inspect:str
    familiarization:str
class createCheck(BaseModel):
    user_id:int
    case_id:int
    checks:str
class createExpertise(BaseModel):
    user_id:int
    case_id:int
    app_comp:str
    prog_comp:str
    inf_comp:str
    comp_net:str
class createQuest(BaseModel):
    user_id:int
    case_id:int
    have:str
    reg:str
    know:str
    have_bank:str
    connect_online:str
    know_cards:str
    pay_site:str
class createSet(BaseModel):
    user_id:int
    case_id:int
    criminal:str
class createWitnes(BaseModel):
    user_id:int
    case_id:int
    witnes:str
class createPersonInvolved(BaseModel):
    first_name:str
    middle_name:str
    last_name:str
    residence:str
    fk_procedural_position:int
    notes:str
    petition: int
class createInspectPersonInvolved(BaseModel):
    idPerson:int
    idInspect:int
class updateClarif(BaseModel):
    date_clarif:datetime.date
    phone:str
    email:str
    information:str
class updateInspect(BaseModel):
    date_inspect:datetime.date
    begin_inspect:str
    end_inspect:str
    message_inspect:str
    from_message_inspect:str
    inspect_exam:str
    place_of_inspect:str
    technical_means:str
    conditions:str
    establish:str
    photography:str
    sized_items:str
    items_for_inspect:str
    familiarization:str
class updateTrack(BaseModel):
    сorrespondence:str
    account:str
    history:str
    track_money:str
    logfile:str
    antivirus:str
class updateCheck(BaseModel):
    checks:str
class updateExpertise(BaseModel):
    app_comp:str
    prog_comp:str
    inf_comp:str
    comp_net:str
class updateQuest(BaseModel):
    have:str
    reg:str
    know:str
    have_bank:str
    connect_online:str
    know_cards:str
    pay_site:str
class updateSet(BaseModel):
    criminal:str
class updateWitnes(BaseModel):
    witnes:str
class requestMobile(BaseModel):
    date_case: datetime.date
    date_incidient: datetime.date
    time: str
    duration: str
    phone: str
class requestBank(BaseModel):
    bank: str