from database.config import settings
from sqlalchemy import create_engine, text,MetaData,Table
from models.users import Base
import os
ur_s = settings.POSTGRES_DATABASE_URLS
print(ur_s)
engine_s = create_engine(ur_s,echo= True)
def create_algorithms():
    conn = engine_s.connect()
    metadata = MetaData()
    algorithms = Table('algoritms',metadata,autoload_with=engine_s)
    values_insert = [
        {'algoritm_name':"Информация получена из заявления потерпевшего"},
        {'algoritm_name':"Сведения получены по результатам оперативно-розыскной деятельности"},
        {'algoritm_name':"Установлен способ совершения преступления, потерпевшие и свидетели, выявлены цифровые следы, данные о преступнике имеются"},
        {'algoritm_name':"Установлен способ совершения преступления, потерпевшие и свидетели, выявлены цифровые следы, данные о преступнике отсутсвуют"},
        {'algoritm_name':"Установлен способ совершения преступления, цифровые следы, потерпевшие, данные о преступнике отсутсвуют"},
        {'algoritm_name':"Не установлен способ совершения преступления, данные о преступнике отсутсвуют"},
    ]
    insert_query = algorithms.insert().values(values_insert)
    conn.execute(insert_query)
    conn.commit()
    conn.close()
def create_roles():
    conn = engine_s.connect()
    metadata = MetaData()
    roles = Table('user_roles',metadata,autoload_with=engine_s)
    values_insert = [
        {'name_role':"Администратор","user_rights":"Добавление пользователей"},
        {'name_role':"Следователь","user_rights":"Ведение дел"},
        {'name_role':"Оперативный сотрудник","user_rights":"Выполнение поручений"},
        {'name_role':"Начальник отдела","user_rights":"Просмотр всех дел"},
    ]
    insert_query = roles.insert().values(values_insert)
    conn.execute(insert_query)
    conn.commit()
    conn.close()
def create_procedural_position():
    conn = engine_s.connect()
    metadata = MetaData()
    procedural_position = Table('procedural_position',metadata,autoload_with=engine_s)
    values_insert = [
        {'name_position':"Потерпевший"},
        {'name_position':"Эксперт"},
        {'name_position':"Специалист"},
        {'name_position':"Понятой"},
        {'name_position':"Защитник"},
        {'name_position':"Подозреваемый"},
    ]
    insert_query = procedural_position.insert().values(values_insert)
    conn.execute(insert_query)
    conn.commit()
    conn.close()
def create_first_department():
    conn = engine_s.connect()
    metadata = MetaData()
    procedural_position = Table('departments',metadata,autoload_with=engine_s)
    values_insert = [
        {'city':"Засекречено",'postal_code':"--//--",'street':"--//--",'house_number':"--//--",'name_department':"--//--"},
    ]
    insert_query = procedural_position.insert().values(values_insert)
    conn.execute(insert_query)
    conn.commit()
    conn.close()
def create_tables():
    Base.metadata.drop_all(bind= engine_s)
    Base.metadata.create_all(bind= engine_s)
    create_algorithms()
    create_roles()
    create_procedural_position()
    create_first_department()
