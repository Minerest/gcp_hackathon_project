from sqlalchemy import String, Column, Integer, Float, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.automap import automap_base

metadata = MetaData()
Base = declarative_base()
# url = dialect + '://' + user + ':' + paswd + '@' + server + ":" + port + '/android_backend'
# engine = create_engine(url)
# session = sessionmaker()
# session.configure(bind=engine)
# Session = session()


def create_table(db):
    locs = Table('user_interface', metadata,
                 Column('id',Integer, primary_key=True, autoincrement=True),
                 Column("latitude", Float),
                 Column("longitude", Float),
                 Column("gta", Integer),
                 Column("assault", Integer),
                 Column("murder", Integer),
                 Column("theft", Integer),
                 Column("sexual_assault", Integer),
                 Column("robbery", Integer),
                 Column("other", Integer),
                 )

    db.metadata.create_all(db.engine)

    return locs


def get_location_schematic():
    data_to_enter = dict()
    data_to_enter["gta"] = 0
    data_to_enter["assaults"] = 0
    data_to_enter["murders"] = 0
    data_to_enter["thefts"] = 0
    data_to_enter["rapes"] = 0
    data_to_enter["robberies"] = 0
    data_to_enter["other"] = 0
    data_to_enter["date"] = 0
    data_to_enter["latitude"] = 0.0
    data_to_enter["longitude"] = 0.0
    return data_to_enter

def get_user_interface_schematic():
    data_to_enter = dict()
    data_to_enter["gta"] = 0
    data_to_enter["assault"] = 0
    data_to_enter["murder"] = 0
    data_to_enter["theft"] = 0
    data_to_enter["sexual_assault"] = 0
    data_to_enter["robbery"] = 0
    data_to_enter["other"] = 0
    data_to_enter["date"] = 0
    data_to_enter["latitude"] = 0.0
    data_to_enter["longitude"] = 0.0
    return data_to_enter


class CloudDB:

    user = 'webuser'
    paswd = 'mysqlPass909'
    dialect = 'mysql+pymysql' # db_type + python_driver
    server = '127.0.0.1'
    port = '3306'
    db = 'android_backend' # database created via googles UI

    def __init__(self):
        self.metadata = metadata
        self.base = Base
        self.url = self.dialect + '://' + self.user + ':' + self.paswd + '@' + self.server + ":" + self.port + '/' + self.db
        self.engine = create_engine(self.url, echo=False, pool_recycle=3600, pool_size=20, max_overflow=0)


    def get_session(self):

        session = sessionmaker()
        session.configure(bind=self.engine)
        Session = session()
        return Session

    def make_scoped_session(self):

        session = sessionmaker()
        session.configure(bind=self.engine)
        return scoped_session(session)


class Location(Base):

    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "locations2"
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    assaults = Column(Integer)
    murders = Column(Integer)
    thefts = Column(Integer)
    rapes = Column(Integer)
    gta = Column(Integer)
    robberies = Column(Integer)
    other = Column(Integer)


class UserInterface(Base):

    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "user_interface"
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    assault = Column(Integer)
    murder = Column(Integer)
    theft = Column(Integer)
    sexual_assault = Column(Integer)
    gta = Column(Integer)
    robbery = Column(Integer)
    other = Column(Integer)


class DatedLocation(Base):
        '''
            This is the main data we store
            Since it's inherited from the sqlalchemy Base class,
            we can access this variable directly to create and store data
        '''

        __tablename__ = "dated_locations"
        id = Column(Integer, autoincrement=True, primary_key=True)
        latitude = Column(Float)
        longitude = Column(Float)
        date = Column(Date)
        assaults = Column(Integer)
        murders = Column(Integer)
        thefts = Column(Integer)
        rapes = Column(Integer)
        gta = Column(Integer)
        robberies = Column(Integer)
        other = Column(Integer)


class MasterCrimeTable(Base):
    '''
        This is the main data we store
        Since it's inherited from the sqlalchemy Base class,
        we can access this variable directly to create and store data
    '''

    __tablename__ = "master_crime_table"
    id = Column(Integer, autoincrement=True, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    date = Column(Date)
    description = Column(String(40))


def add_data_to_db(new_entry, db):
    data_to_enter = DatedLocation(latitude=new_entry["latitude"], longitude=new_entry["longitude"],
                                  assaults=new_entry['assault'], date=new_entry["date"],
                                  murders=new_entry["murder"], rapes=new_entry["rape"],
                                  thefts=new_entry["theft"], gta=new_entry["gta"],
                                  robberies=new_entry["robbery"], other=new_entry["other"]
                                  )
    return data_to_enter


def feed_master(entry):
    data_to_enter = MasterCrimeTable(latitude=entry["latitude"], longitude=entry["longitude"],
                                     date=entry["date"], description=entry["description"])
    return data_to_enter


