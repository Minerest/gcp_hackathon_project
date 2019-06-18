#!env/bin/python3
from flask import Flask, request, Response, render_template, send_from_directory
import json
from sqlalchemy import and_
import logging
import os
# user library that contains the format for table entries.
import modals

''' FEATURE:
    
    Safest route to location. 
    User picks place to go via map
    google maps api gives us path based on our own parameters <---- DO this first, fail faster
    Display the path
    
'''


app = Flask(__name__, static_folder='/home/paulina/Desktop/www/gcp_hackathon_project/static/build/')

db = modals.CloudDB()


@app.route("/user_interface")
def grab_from_user_interface():
    # ip.addr/testing?lat=12.34&lon=43.21
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    Session = db.get_session()
    schematic = modals.get_user_interface_schematic()
    data_array = [schematic.copy() for i in range(111)]

    # Thre's no reason we should take anything other than numbers as an input
    try:
        lat = float(lat)
        lon = float(lon)
    except Exception as e: # Can't give hackers any clues so same output as any other generic error.
        return "No data available"

    if lat is None or lon is None:
        return "No data available"

    # So this is a total difference of .1 lat/lon which is 7 miles
    upper_lat = float(lat + 0.05)
    upper_lon = float(lon + 0.05)
    lower_lat = float(lat - 0.05)
    lower_lon = float(lon - 0.05)

    for entry in Session.query(modals.UserInterface).filter(and_(
        modals.UserInterface.longitude <= upper_lon, modals.UserInterface.longitude >= lower_lon,
        modals.UserInterface.latitude <= upper_lat, modals.UserInterface.latitude >= lower_lat
                                                                    )):
        d = entry.__dict__
        entry_json = dict()
        for i, j in d.items():
            if i != "_sa_instance_state" and i != "id":
                entry_json[i] = j
        y = entry_json["longitude"]
        x = entry_json["latitude"]
        ydiff = int(((y - lon) + 0.05) * 100)
        xdiff = int(((x - lat) + 0.05) * 100)
        indx = 10 * ydiff + xdiff
        for k, v in entry_json.items():
            if k == "latitude" or k == "longitude":
                data_array[indx][k] = v
            else:
                data_array[indx][k] += v
    data_to_ret = json.dumps(data_array)

    try:
        Session.flush()
        Session.commit()
    finally:
        Session.close()

    return data_to_ret

@app.route('/testing')
def make_db_query():

    ''' hits the database based on url parameters '''
    schematic = modals.get_location_schematic()
    data_array = [schematic.copy() for i in range(111)] # initialize an array of 100 full of 0's
    # ip.addr/testing?lat=12.34&lon=43.21
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    Session = db.get_session()
    # Thre's no reason we should take anything other than numbers as an input
    try:
        lat = float(lat)
        lon = float(lon)
    except Exception as e: # Can't give hackers any clues so same output as any other generic error.
        return "No data available"

    if lat is None or lon is None:
        return "No data available"

    # So this is a total difference of .1 lat/lon which is 7 miles
    upper_lat = float(lat + 0.05)
    upper_lon = float(lon + 0.05)
    lower_lat = float(lat - 0.05)
    lower_lon = float(lon - 0.05)

    # The algorithm to actually append values to a data array of 100:
    # The dead center of the array a[49](?)
    # The further north the latitude, the smaller the y value
    # the further east the longitude, the larger the x value
    # data_array[ y * 10 + x] where x and y are less than 10.


    cnt = 0
    for entry in Session.query(modals.Location).filter(and_(
        modals.Location.longitude <= upper_lon, modals.Location.longitude >= lower_lon,
        modals.Location.latitude <= upper_lat, modals.Location.latitude >= lower_lat
                                                                    )):
        d = entry.__dict__
        entry_json = dict()
        cnt+=1
        for i, j in d.items():
            if i != "_sa_instance_state" and i != "id":
                entry_json[i] = j
        y = round(entry_json["longitude"], 2)
        x = round(entry_json["latitude"], 2)
        ydiff = int(((y - lon) + 0.05) * 100)
        xdiff = int(((x - lat) + 0.05) * 100)
        indx = 10 * ydiff + xdiff
        for k, v in entry_json.items():
            if k == "latitude" or k == "longitude":
                data_array[indx][k] = round(v, 2)
            else:
                data_array[indx][k] += round(v, 2)
    data_to_ret = json.dumps(data_array)

    try:
        Session.flush()
        Session.commit()
    finally:
        Session.close()

    print(cnt)
    return data_to_ret


@app.route('/testing/dump')
def dump_db():
    ''' Gets all the data from the db and print it as json '''

    def generate(t):
        for item in t:
            yield json.dumps(str(item))
    a = []
    Session = db.get_session()
    for entry in Session.query(modals.UserInterface).limit(2000):
        a.append(entry.__dict__)
    try:
        Session.commit()
        Session.flush()
    finally:
        Session.close()
    return Response(generate(a), mimetype="text")


@app.route("/single")
def get_single():

    schema = modals.get_user_interface_schematic()
    schema["rapes"] = 0
    lat = request.args.get('lat', None)
    lon = request.args.get('lon', None)
    # Thre's no reason we should take anything other than numbers as an input
    try:
        lat = float(lat)
        lon = float(lon)
    except Exception as e: # Can't give hackers any clues so same output as any other generic error.
        return "No data available"

    upper_lat = float(lat + 0.01)
    upper_lon = float(lon + 0.01)
    lower_lat = float(lat - 0.01)
    lower_lon = float(lon - 0.01)

    data_array = []

    Session = db.get_session()

    for entry in Session.query(modals.UserInterface).filter(and_(
        modals.UserInterface.longitude <= upper_lon, modals.UserInterface.longitude >= lower_lon,
        modals.UserInterface.latitude <= upper_lat, modals.UserInterface.latitude >= lower_lat
                                                                    )):
        d = entry.__dict__
        entry_json = dict()
        for i, j in d.items():
            if i != "_sa_instance_state" and i != "id":
                entry_json[i] = j

        data_array.append(entry_json)

    for i in data_array:
        for k, v in i.items():
            if k == "longitude" or k == "latitude":
                continue
            schema[k] += v
    try:
        Session.commit()
    finally:
        Session.close()
    print(schema)
    return json.dumps(schema)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return ""


@app.route("/main_db")
def get_police_reports():

    session = db.get_session()
    try:
        lat = float(request.args.get("lat", None))
        lon = float(request.args.get("lon", None))
    except:
        return ""

    upper_lat = float(lat + 1)
    upper_lon = float(lon + 1)
    lower_lat = float(lat - 1)
    lower_lon = float(lon - 1)

    entries = session.query(modals.MasterCrimeTable).filter(
        modals.MasterCrimeTable.longitude <= upper_lon, modals.MasterCrimeTable.longitude >= lower_lon,
        modals.MasterCrimeTable.latitude <= upper_lat, modals.MasterCrimeTable.latitude >= lower_lat)\
        .order_by(modals.MasterCrimeTable.date.desc()).limit(300)

    data = []

    for entry in entries:
        data.append(entry.__dict__)

    session.close()
    return json.dumps(data)



@app.route('/')
def ret_none():
    return render_template("index.html")

@app.route('/json')
def ret_json():
    with open("json_updated.json") as f:
        json_data = f.read()
    return json_data



if __name__ == "__main__":
    app.run("0.0.0.0", debug=False, port=80)
