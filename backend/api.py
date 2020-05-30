import flask
from flask import request, jsonify
from retrieve_parameters import pollen_level, humidity_level, elevation_level, airquality, temperature
import pickle
from flask_pymongo import PyMongo
from alert_algorithm import alert
from predictions import makeHistogram, mostLikely

app = flask.Flask(__name__)
app.config["DEBUG"] = True

KEY = "mongodb+srv://dbUser:jCx!zG3X6HzqsT*@asthmaalert-q46ku.mongodb.net/test?retryWrites=true&w=majority"

app.config["MONGO_URI"] = KEY
client = PyMongo(app)
db = client.db.users
EMAIL = ""

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Welcome to the Asthma Alert Backend</h1>'''

@app.route('/alert', methods=['GET'])
def api_id():
    global EMAIL
    # x = db.find_one_or_404({"email": EMAIL})
    # print(x)

    lat = lon = 0

    if 'user' in request.args:
        EMAIL = (request.args['user'])
    else:
        return "No Email Provided. Please Provide an Email"
    if 'lat' in request.args:
        lat = float(request.args['lat'])
    else:
        return "No latitude field provided. Please specify a latitude."

    if 'lon' in request.args:
        lon = float(request.args['lon'])
    else:
        return "No longitude field provided. Please specify a longitude."
    
    x = db.find_one_or_404({"email": EMAIL})
    trigs = x['triggers']
    trained = x['trained']

    results = alert(lat, lon, trigs, trained)

    if trained == False:
        x["trained"] = True
        x = {"$set": x}
        db.update_one(db.find_one_or_404({"email": EMAIL}), x)

    return results


'''
Adds a user: user and triggers
'''


@app.route("/newUser", methods=["GET"])
def createUser():
    global EMAIL
    if 'user' in request.args:
        EMAIL = (request.args['user'])
    else:
        return "No Email Provided. Please Provide an Email"
    if 'triggers' in request.args:
        trig = (request.args['triggers'])
    else:
        return "No Triggers Provided. Please Provide a Trigger"
    
    print(EMAIL, trig)
    trig = trig.split(",")
    user = {"email": EMAIL, "trained": False, "triggers": trig, "past_attacks": []}
    db.insert_one(user)
    return "Added user to the database"


'''
Adds new trigger data given input
'''


@app.route("/newAttack", methods=["GET"])
def addAttack():
    global EMAIL
    if 'user' in request.args:
        EMAIL = (request.args['user'])
    else:
        return "No Email Provided. Please Provide an Email"
    if 'lat' in request.args:
        lat = float(request.args['lat'])
    else:
        return "No latitude field provided. Please specify a latitude."

    if 'lon' in request.args:
        lon = float(request.args['lon'])
    else:
        return "No longitude field provided. Please specify a longitude."
    
    x = db.find_one_or_404({"email": EMAIL})

    pollen = pollen_level(lat, lon)
    humidity = humidity_level(lat, lon)
    elevation = elevation_level(lat, lon)
    aq = airquality(lat, lon)
    temp = temperature(lat, lon)

    pollen_val = 0
    if pollen != None:
        for plant in pollen:
            if pollen[plant] > pollen_val:
                pollen_val = pollen[plant]

    param = [pollen_val, humidity, elevation, aq, temp]

    x["past_attacks"].append(param)
    x = {"$set": x}
    db.update_one(db.find_one_or_404({"email": EMAIL}), x)
    return "Added data for new attack"

@app.route("/histogram")
def makeHistogram():
    global EMAIL
    if 'user' in request.args:
        EMAIL = (request.args['user'])
    else:
        return "No Email Provided. Please Provide an Email"
    if 'data' in request.args:
        trig = (request.args['data'])
    x = db.find_one_or_404({"email": EMAIL})
    return makeHistogram(x["past_attacks"])

@app.route('/possibleNewTriggers')
def possibleNewTriggers():
    global EMAIL
    if 'user' in request.args:
        EMAIL = (request.args['user'])
    else:
        return "No Email Provided. Please Provide an Email"
    x = db.find_one_or_404({"email": EMAIL})
    if len(x["past_attacks"]) != 0:
        likely_String = mostLikely(x["past_attacks"])
        likely_String = likely_String[2:-2]
        return likely_String
    else:
        return "No past attack data available"

app.run()
