import modals
from sqlalchemy import and_
import datetime

''' utilities to convert data from one database to another '''


db = modals.CloudDB()


def convert_master_to_user(interface_schematic):
    # first iteration of converting master_db entries to user_interface entries

    # create the sqlAlchemy object to be inserted into the new table
    usr_schema = modals.UserInterface(latitude=interface_schematic["latitude"], longitude=interface_schematic["longitude"],
                                      assault=interface_schematic["assaults"], murder=interface_schematic["murders"],
                                      theft=interface_schematic["thefts"], sexual_assault=interface_schematic["rapes"],
                                      gta=interface_schematic["gta"], robbery=interface_schematic["robberies"],
                                      other=interface_schematic["other"])
    return usr_schema


def add_to_user_interface(master_list, Session):
    # Iterates through a list of entries and then saves them in a database all at once.
    # Much faster than individual commits
    bulk_entries = []
    for entry in master_list:
        usr_entry = convert_master_to_user(entry)
        bulk_entries.append(usr_entry)

    Session.bulk_save_objects(bulk_entries)
    Session.commit()
    Session.close()


def transform():
    master = modals.MasterCrimeTable

    ''' Notes as of 3/9/2019
    lon lower: -122.59
    lon upper: -73.7088
    lat upper: 47.3116
    lat lower: 33.706
    
    Date recent: 03/31/2019
    date oldest: 01/01/2001 ; There are older dates, but I figure they're not relevant
    '''
    # the bounds of the current data set.
    # TODO: make a function to do this automatically
    start_yr = 2010
    start_month = 1
    start_day = 1
    end_yr = 2019
    end_month = 3
    end_day = 31

    cur_yr = start_yr
    cur_mnth = 2
    cur_day = 1

    oldest_dt = datetime.datetime(start_yr, start_month, start_day)
    newest_dt = datetime.datetime(end_yr, end_month, end_day)

    dt_rng_old = oldest_dt
    dt_rng_new = datetime.datetime(start_yr, start_month + 1, start_day)

    master_object_dict = dict()

    done = False
    cnt = 0

    # TODO: I need to make a dictionary that contains a dictionary DB entry, and a month counter to divide each
    # entry by the amount of months of data it has

    Session = db.get_session()


    while not done:

        master_list = []

        # get entries based on the month.
        for entry in Session.query(master).filter(and_(master.date < dt_rng_new,
                                                          master.date >= dt_rng_old)):

            master_list.append(entry.__dict__)

        for i in master_list:
            local_lat = round(i['latitude'], 2)
            local_lon = round(i['longitude'], 2)
            object_key = str(local_lat) + str(local_lon)

            if not object_key in master_object_dict:
                master_object_dict[object_key] = modals.get_location_schematic()
                master_object_dict[object_key]["cnt"] = 0
                master_object_dict[object_key]["bool"] = True

            desc = i["description"].lower()
            master_object_dict[object_key]['latitude'] = local_lat
            master_object_dict[object_key]['longitude'] = local_lon

            if master_object_dict[object_key]["bool"]:
                master_object_dict[object_key]["cnt"] += 1
                master_object_dict[object_key]["bool"] = False

            if "assault" in desc:
                master_object_dict[object_key]["assaults"] += 1
            elif "murder" in desc:
                master_object_dict[object_key]["murders"] += 1
            elif "theft" in desc or "larceny" in desc:
                master_object_dict[object_key]["thefts"] += 1
            elif "rape" in desc:
                master_object_dict[object_key]["rapes"] += 1
            elif "grand" in desc and "theft" in desc and "auto" in desc:
                master_object_dict[object_key]["gta"] += 1
            elif "robbery" in desc:
                master_object_dict[object_key]["robberies"] += 1
            else:
                master_object_dict[object_key]["other"] += 1


        # if len(master_list) != 0:
        #     add_to_user_interface(master_list)
        #     print(len(master_list))

        for k, v in master_object_dict.items():
            master_object_dict[k]["bool"] = True

        cur_mnth += 1

        if cur_mnth > 12:
            cur_mnth = 1
            cur_yr += 1

        if cur_yr == 2019:
            done = True

        dt_rng_old = dt_rng_new
        dt_rng_new = datetime.datetime(cur_yr, cur_mnth, cur_day)
    master_list = []
    for k, v in master_object_dict.items():
        for sub_k, sub_v in master_object_dict[k].items():
            if sub_k != "latitude" and sub_k != "longitude" and master_object_dict[k]["cnt"] != 0:
                print(master_object_dict[k]["cnt"])
                master_object_dict[k][sub_k] /= master_object_dict[k]["cnt"]
                master_object_dict[k][sub_k] = int(master_object_dict[k][sub_k])
        master_list.append(master_object_dict[k])

    add_to_user_interface(master_list, Session)

if __name__ == "__main__":
    transform()
