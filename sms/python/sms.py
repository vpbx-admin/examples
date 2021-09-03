import requests


#Number to call in international format (E164)
number = "48500000000"
#Sender's number
from_number = "callapi.pl"
api_url = "https://api.vpbx.pl/api/v1"
#API Username
username = ""
#API Password
password = ""
text = "wiadomosc testowa wyslana z callapi.pl"

reqToken = requests.post(api_url + "/login", json={"username": username, "password": password})

if reqToken.status_code != 200:
    print("Failed to authenticate. Status : " + reqToken.json()["result"] + ",  Error: " + reqToken.json()["error"])
    exit(1)

token = reqToken.json()["token"]


sms = {
    "from": from_number,
    "to": number,
    "text": text
}

respObject = requests.post(api_url + "/sms", json=sms, headers={"authorization": "Bearer " + token})

if respObject.status_code != 200:
    print("Failed to send the sms. Status : " + respObject.json()["result"] + ",  Error: " + respObject.json()["error"])
    exit(1)

print("Status : " + respObject.json()["result"] + ",  SMS-ID : " + respObject.json()["sms_id"])



