#!/usr/bin/python3
import requests, sys, json, tempfile
from dateutil.parser import parse
from datetime import datetime, timezone

#Number to call in international format (E164)
#Sender's number
from_number = "callapi.pl"
api_url = "https://api.vpbx.pl/api/v1"
#API Username
username = ""
#API Password
password = ""


# Number of digits to be removed from the recipent number. 
# API expect the number in E164 form  - for example 48601000000. If the number you want to use is in +E164 form (for example +48601000000), the '+' characters needs to be removed.
stripPrefix=0

# Characters to be added in front of the number. 
# API expect the number in E164 form  - for example 48601000000. If the number you want to use is in a local form (for example 601000000), the '48' has to be added in front of the number.
addPrefix=''

# Temporary file to store a valid token
tempFile = "/tmp/sendsmstoken"



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

sms = {
    "from": from_number,
    "to": addPrefix + sys.argv[1][stripPrefix:],
    "text": sys.argv[2]
}
print("Sending SMS to: " + sms["to"])
token = getToken()
respObject = requests.post(api_url + "/sms", json=sms, headers={"authorization": "Bearer " + token})

if respObject.status_code != 200:
    print("Failed to send the sms. Status : " + respObject.json()["result"] + ",  Error: " + respObject.json()["error"])
    exit(1)

print("Status : " + respObject.json()["result"] + ",  SMS-ID : " + respObject.json()["sms_id"])


