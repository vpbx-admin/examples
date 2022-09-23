#!/usr/bin/python3
import requests, sys, json, tempfile
from dateutil.parser import parse
from datetime import datetime, timezone

#Number to call in international format (E164)
#Sender's number
from_number = "48447330000"
api_url = "https://api.vpbx.pl/api/v1"
#API Username
username = ""
#API Password
password = ""


#voice name. See https://callapi.pl/docs/

voice="pl-PL/Maja"

# Number of digits to be removed from the recipent number. 
# API expect the number in E164 form  - for example 48601000000. If the number you want to use is in +E164 form (for example +48601000000), the '+' characters needs to be removed.
stripPrefix=0

# Characters to be added in front of the number. 
# API expect the number in E164 form  - for example 48601000000. If the number you want to use is in a local form (for example 601000000), the '48' has to be added in front of the number.
addPrefix=''

# Temporary file to store a valid token
tempFile = "/tmp/sendsmstoken"

call_object = {
    "from": from_number,
    "to": addPrefix + sys.argv[1][stripPrefix:],
    "ring_timeout": 30,
    "objects": [
        {
            "type": "answer"
            },
        {
            "type": "wait",
            "params": {
                "time": 2
                }
            },
        {
            "type": "tts",
            "params": {
                "text": sys.argv[2],
                "lang": "pl-PL/Maja"
                }
            },
        {
            "type": "tts",
            "params": {
                "text": sys.argv[2],
                "lang": "pl-PL/Maja"
                }
            }
        ]
}


def requestToken():
    reqToken = requests.post(api_url + "/login", json={"username": username, "password": password})
    if reqToken.status_code != 200:
        print("Could not request token. Are credentials good?")
        exit(1)
    return reqToken

def getToken():

    try:
        with open(tempFile, 'r') as tfile:
            tmpToken = json.load(tfile)
            tmpTokenDate = parse(tmpToken["expire"]).replace(tzinfo=timezone.utc)
            nowDate = datetime.now(timezone.utc)
        if tmpTokenDate > nowDate:
            print("Token from the futre  - all good")
            return tmpToken["token"]
    except:
        print("could not read from file")
    print("Token is expired - requesting a new one")
    tmpReqToken = requestToken()
    tfileW = open(tempFile, 'w')
    try:
        tfileW.write(tmpReqToken.text)
    except:
        print("could not write to file")
    tfileW.close()
    return tmpReqToken.json()["token"]

print("Sending SMS to: " + call_object["to"])
token = getToken()
respObject = requests.post(api_url + "/callobject", json=call_object, headers={"authorization": "Bearer " + token})

if respObject.status_code != 200:
    print("Failed to send the sms. Status : " + respObject.json()["result"] + ",  Error: " + respObject.json()["error"])
    exit(1)

print("Status : " + respObject.json()["result"] + ",  Call-ID : " + respObject.json()["call_id"])

