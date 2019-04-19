#! /usr/bin/python3

import modals
import csv
import datetime


#! /usr/bin/python3

import modals
import csv
import datetime



#
# def main():
#
#     db = modals.CloudDB()
#
#     modals.create_table(db.engine)
#
#     list_of_data = []
#     first_pass = True
#     rows = 0
#     junk_in_csv = "()"
#     date_bound_lower = datetime.datetime(2014, 1, 1)
#     date_bound_upper = datetime.datetime(2016, 1,1)
#     cnt = 0
#     with open("cityoftacoma5960") as f:
#         baltimore_crime_data = csv.reader(f)
#         for row in baltimore_crime_data:
#             rows += 1
#             if first_pass:
#                 first_pass = False
#                 continue
#
#             dt = row[2]
#             loc_data = row[4]
#             crime_type = row[1]
#             try:
#                 _, lat_lon_pair = loc_data.split("(")
#                 lat, lon = lat_lon_pair.split(",")
#
#             except:
#                 cnt += 1
#                 continue
#
#             for junk in junk_in_csv:
#                 lat = lat.replace(junk, "")
#                 lon = lon.replace(junk, "")
#             try:
#                 lat = float(lat)
#                 lon = float(lon)
#             except:
#                 cnt += 1
#                 continue
#             data_to_enter = modals.get_location_schematic()
#
#             dt = datetime.datetime.strptime(dt, "%m/%d/%Y")
#
#             data_to_enter["date"] = dt
#             try:
#                 data_to_enter["longitude"] = float(lon)
#                 data_to_enter["latitude"] = float(lat)
#
#             except Exception as e:
#                 print(e, row)
#                 continue
#
#             if "assault" in crime_type.lower():
#                 data_to_enter["assault"] += 1
#
#             elif "murder" in crime_type.lower():
#                 data_to_enter["murder"] += 1
#
#             elif "theft" in crime_type.lower() or "larceny" in crime_type.lower()\
#                          or "burglary" in crime_type.lower():
#                 data_to_enter["theft"] += 1
#
#             elif "rape" in crime_type.lower():
#                 data_to_enter["rape"] += 1
#
#             elif "grand" in crime_type.lower() and \
#                  "theft" in crime_type.lower() and \
#                  "auto"  in crime_type.lower():
#                 data_to_enter["gta"] += 1
#
#             elif "robbery" in crime_type.lower():
#                 data_to_enter["robbery"] += 1
#
#             else:
#                 data_to_enter["other"] += 1
#             try:
#                 db_entry = add_data_to_db(data_to_enter, db)
#                 list_of_data.append(db_entry)
#             except:
#                 cnt += 1
#                 continue
#
#     print(cnt)
#     print(rows)
#     db.Session.bulk_save_objects(list_of_data)
#     db.Session.commit()
#     db.Session.close()
#

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

    db.Session.bulk_save_objects(list_of_data)
    db.Session.commit()
    db.Session.close()


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
