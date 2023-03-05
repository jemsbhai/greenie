import os
import pymongo
import json
import random
import hashlib
import time

import requests

from hashlib import sha256





def sendsms(tonum, message):


    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/sendsms"

    payload = json.dumps({
    "receiver": tonum,
    "message": message,
    "token": "CEWIT"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

def hashthis(st):


    hash_object = hashlib.md5(st.encode())
    h = str(hash_object.hexdigest())
    return h



def dummy(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from origin https://mydomain.com with
        # Authorization header
        headers = {
            'Access-Control-Allow-Origin': ['*', 'localhost'],
            'Access-Control-Allow-Methods': ['POST', 'OPTIONS'],
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true'
        }
        return ('', 204, headers)

    # Set CORS headers for main requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': 'true'
    }

    request_json = request.get_json()



    receiver_public_key = os.environ.get('ownpublic')

    mongostr = os.environ.get('MONGOSTR')
    client = pymongo.MongoClient(mongostr)
    db = client["hackathon"]


    retjson = {}

    action = request_json['action']

    if action == "inperson":
        col = db.rooms



        found = 0
        id = "0" ##can change this

        for x in col.find():
            if x['id'] == id:
                found = 1
                id = x['id']
                pop = x['population']

            break
        if found == 0:
            retjson['status'] = "unknown  id"

            return json.dumps(retjson)
        


        col.update_one({"id": id}, {"$set":{"population":pop+1}})

        retjson['status'] = "population updated"

        return json.dumps(retjson)


    if action == "outperson":
        col = db.rooms



        found = 0
        id = "0" ##can change this

        for x in col.find():
            if x['id'] == id:
                found = 1
                id = x['id']
                pop = x['population']

            break
        if found == 0:
            retjson['status'] = "unknown  id"

            return json.dumps(retjson)
        


        col.update_one({"id": id}, {"$set":{"population":pop-1}})

        retjson['status'] = "population updated"

        return json.dumps(retjson)


    if action == "getpop" :
        col = db.baseparty



        found = 0
        id = "0" ##can change this

        for x in col.find():
            if x['id'] == id:
                found = 1
                id = x['id']
                pop = str(x['population'])

            break
        if found == 0:
            retjson['status'] = "unknown id"

            return json.dumps(retjson)
        


        retjson['pop'] = pop

        return json.dumps(retjson)



    if action == "startparty" :
        col = db.baseparty



        found = 0
        id = "0" ##can change this

        for x in col.find():
            if x['partyid'] == id:
                found = 1
                id = x['partyid']

            break
        if found == 0:
            retjson['status'] = "unknown party id"

            return json.dumps(retjson)
        
        col.update_one({"partyid": id}, {"$set":{"status":"1"}})

        retjson['status'] = "party mode updated"

        return json.dumps(retjson)




    if action == "stopparty" :
        col = db.baseparty



        found = 0
        id = "0" ##can change this

        for x in col.find():
            if x['partyid'] == id:
                found = 1
                id = x['partyid']

            break
        if found == 0:
            retjson['status'] = "unknown party id"

            return json.dumps(retjson)
        
        col.update_one({"partyid": id}, {"$set":{"status":"0"}})

        retjson['status'] = "party mode updated"

        return json.dumps(retjson)


    if action == "getparty" :
        col = db.baseparty



        found = 0
        id = "0" ##can change this

        for x in col.find():
            if x['partyid'] == id:
                found = 1
                id = x['partyid']
                status = x['status']

            break
        if found == 0:
            retjson['status'] = "unknown party id"

            return json.dumps(retjson)
        


        retjson['status'] = status

        return json.dumps(retjson)




    if action == "donate":
        tophone = request_json['phone']
        amount = float(request_json['amount'])

        col = db.users

        found = 0
        id = "0"
        for x in col.find():
            if x['phone'] == tophone:
                found = 1
                id = x['id']

            break
        if found == 0:
            retjson['status'] = "unknown number"

            return json.dumps(retjson)
        
        col.update_one({"id": id}, {"$inc":{"balance":amount}})

        retjson['status'] = "donation successful"

        return json.dumps(retjson)


    if action == "login":
        col = db.users
        for x in col.find():
            if x['email'] == request_json['email'] and x['password'] == request_json['password']:
                userid = x['id']
                name = x['name']
                retjson = {}

                # retjson['dish'] = userid
                retjson['status'] = "success"
                retjson['name'] = name
                retjson['userid'] = userid
                retjson['email'] = x['email']
                retjson['phone'] = x['phone']
                retjson['gender'] = x['gender']
                tags = []
                for t in x['tags']:
                    tags.append(t)
                retjson['tags'] = tags
                

                return json.dumps(retjson)
        retjson = {}

        # retjson['dish'] = userid
        retjson['status'] = "fail"
        retjson['userid'] = "-1"

        return json.dumps(retjson)


 

    retstr = "action not done"

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return retstr
