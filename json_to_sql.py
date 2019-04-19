#!/usr/bin/python3

import json
from sqlalchemy import String, Column, Integer, Table, create_engine, Float, Date
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import MetaData

import modals


def create_table(engine):
    locs = Table('dated_locations', modals.metadata,
          Column('id',Integer, primary_key=True, autoincrement=True),
          Column("date", Date),
          Column('latitude', Float),
          Column('longitude', Float),
          Column('assaults', Integer),
          Column('murders', Integer),
          Column('thefts', Integer),
          Column('rapes', Integer),
          Column('gta', Integer),
          Column('robberies', Integer),
          Column('other', Integer)
          )

    modals.Base.metadata.create_all(engine)

    return locs

def convert_json_to_db(key ,data, session):

    ''' Takes the latlon key from the JSON file, the data associated with it, and the session from main to create entries into the database. '''

    try:
        lat, lon = key.split('-')
    except:
        print(key)
        return
    lat = float(lat)
    lon = float(lon)
    lon *= -1
    data_to_input = modals.UserInterface(latitude=lat, longitude=lon, assault=data['ASSAULT'],
                                    murder=data["MURDER"], sexual_assault=data["RAPE"],
                                    theft=data["THEFT"], gta=data["GTA"],
                                    robbery=data["ROBBERY"], other=data["OTHER"]
                                    )
    session.add(data_to_input)
    session.flush()
    session.commit()

def main():

    db = modals.CloudDB()
    create_table(db.engine)
    with open("json_updated.json") as f:
        json_data = f.read()

    loc_vals = json.loads(json_data)

    for keys in loc_vals:
        convert_json_to_db(keys, loc_vals[keys], db.get_session())


main()

