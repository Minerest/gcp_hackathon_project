#! /usr/bin/python3

import modals
import csv
import datetime


#! /usr/bin/python3

import modals
import csv
import datetime


def add_data_to_db(new_entry, db):
    data_to_enter = modals.DatedLocation(latitude=new_entry["latitude"], longitude=new_entry["longitude"],
                                         assaults=new_entry['assault'], date=new_entry["date"],
                                         murders=new_entry["murder"], rapes=new_entry["rape"],
                                         thefts=new_entry["theft"], gta=new_entry["gta"],
                                         robberies=new_entry["robbery"], other=new_entry["other"]
                                         )
    return data_to_enter




def main():

    db = modals.CloudDB()
    Session = db.get_session()
    list_of_data = []
    first_pass = True
    rows = 0
    with open("baltimorecity3335") as f:
        baltimore_crime_data = csv.reader(f)
        for row in baltimore_crime_data:
            rows += 1
            if rows > 50000:  # approx 1 year of data
                break
            if first_pass:
                first_pass = False
                continue
            dt = row[0]
            lon = row[10]
            lat = row[11]
            crime_type = row[4]
            data_to_enter = dict()
            data_to_enter["description"] = crime_type[:39] if len(crime_type) > 39 else crime_type
            dt = datetime.datetime.strptime(dt, "%m/%d/%Y")

            data_to_enter["date"] = dt
            try:
                data_to_enter["longitude"] = float(lon)
                data_to_enter["latitude"] = float(lat)

            except Exception as e:
                print(e, row)
                continue

            entry = modals.feed_master(data_to_enter)
            list_of_data.append(entry)

    Session.bulk_save_objects(list_of_data)
    Session.commit()
    Session.close()


def add_data_to_db(new_entry, db):
    data_to_enter = modals.DatedLocation(latitude=new_entry["latitude"], longitude=new_entry["longitude"],
                                         assaults=new_entry['assault'], date=new_entry["date"],
                                         murders=new_entry["murder"], rapes=new_entry["rape"],
                                         thefts=new_entry["theft"], gta=new_entry["gta"],
                                         robberies=new_entry["robbery"], other=new_entry["other"]
                                         )

    return data_to_enter
    # db.Session.add(data_to_enter)
    # db.Session.flush()
    # db.Session.close()


main()
