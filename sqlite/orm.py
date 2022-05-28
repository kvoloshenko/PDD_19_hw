from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import desc

# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine('sqlite:///C:\\sqlitedbs\\school.db', echo=True)

def get_engine(connect_string):
    engine = create_engine(connect_string, echo=False)
    return engine

Base = declarative_base()


class Hh_Requests(Base):
    __tablename__ = 'hh_requests'
    id = Column(Integer, primary_key=True)
    keywords = Column(String, nullable=False)

    def __init__(self, keywords):
        self.keywords = keywords

    def __repr__(self):
        return "<Hh_Requests('%s')>" % (self.keywords)

    def set_requests(self, connect_string, requests):
        engine = get_engine(connect_string)
        # Создание сессии
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        keywords = Hh_Requests(requests)
        # Добавление данных
        session.add(keywords)
        # for r in session.query(Hh_Requests).order_by(Hh_Requests.id):
        #     print (r)
        # ids = session.query(func.max('hh_requests.id'))
        session.commit()
        last_request_id = 0
        for id in session.query(func.max(Hh_Requests.id)):
            # print (type(id), f'id={id}')
            last_request_id = id[0]
            # print(type(max_id), f'max_id={max_id}')
        # print (type(maxid), f'maxid={maxid}')
        return last_request_id

    def get_last_request_id(self, connect_string):
        engine = get_engine(connect_string)
        # Создание сессии
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        last_request_id = 0
        for id in session.query(func.max(Hh_Requests.id)):
            # print (type(id), f'id={id}')
            last_request_id = id[0]
            # print(type(max_id), f'max_id={max_id}')
        # print (type(maxid), f'maxid={maxid}')
        return last_request_id


class Hh_Responses(Base):
    __tablename__ = 'hh_responses'
    id = Column(Integer, primary_key=True)
    requests_id = Column(Integer, ForeignKey('hh_requests.id'), nullable=False)
    skill_name = Column(String, nullable=False)
    skill_count = Column(Integer, nullable=False)
    skill_persent = Column(Integer, nullable=False)

    def __init__(self, requests_id, skill_name, skill_count, skill_persent):
        self.requests_id = requests_id
        self.skill_name = skill_name
        self.skill_count = skill_count
        self.skill_persent = skill_persent

    def __repr__(self):
        return "<Hh_Responses('%s','%s', '%s')>" % (self.skill_name, self.skill_count, self.skill_persent)

    def set_responses(self, connect_string, last_request_id, responses):
        engine = get_engine(connect_string)
        # Создание сессии
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        for item in responses:
            # print (type(item),f'item={item}')
            i_name = item['name']
            i_count = item['count']
            i_persent = item['persent']
            responses = Hh_Responses(last_request_id, i_name, i_count, i_persent)
            # Добавление данных
            session.add(responses)
        session.commit()

    def get_responses(self, connect_string, last_request_id):
        engine = get_engine(connect_string)
        # Создание сессии
        # create a configured "Session" class
        Session = sessionmaker(bind=engine)
        # create a Session
        session = Session()
        # запрос с условием
        hh_responses = session.query(Hh_Responses)\
            .filter(Hh_Responses.requests_id == last_request_id)\
            .order_by(desc(Hh_Responses.skill_count)).all()
        # print(type(hh_responses), f'responses={hh_responses}')
        requirements = []
        for r in hh_responses:
            i_dic = {}
            # print(type(r),f'fow={r}')
            i_dic['name'] = r.skill_name
            i_dic['count'] = r.skill_count
            i_dic['persent'] = r.skill_persent
            # print(f'i_dic={i_dic}')
            requirements.append(i_dic)
        return requirements

# Создание таблицы
def create_db(connect_string):
    engine = get_engine(connect_string)
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    connect_string = 'sqlite:///hh_db_orm.sqlite'
    create_db(connect_string)
    keywords = Hh_Requests('')
    last_request_id = keywords.set_requests(connect_string, 'NAME:(C++)')
    # print(f'last_request_id={last_request_id}')
    responses = Hh_Responses(0,'',0,0)
    requirements = [{'name': 'net', 'count': 16, 'persent': 21}, {'name': 'c', 'count': 12, 'persent': 16}]
    responses.set_responses(connect_string, last_request_id, requirements)
    last_request_id = keywords.get_last_request_id(connect_string)
    print(f'last_request_id={last_request_id}')
    requirements = responses.get_responses(connect_string, last_request_id)
    print(type(requirements), f'requirements={requirements}')

    # s = keywords.get_requests()
    # print(type(s), f's={s}')
