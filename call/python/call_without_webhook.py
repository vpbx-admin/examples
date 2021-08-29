import requests


#Number to call in international format (E164)
number = ""
#Number to be presented in international format (E164)
from_number = "48224723555"
api_url = "https://api.vpbx.pl/api/v1"
#API Username
username = ""
#API Password
password = ""


reqToken = requests.post(api_url + "/login", json={"username": username, "password": password})

if reqToken.status_code != 200:
    print("Failed to authenticate. Status : " + reqToken.json()["result"] + ",  Error: " + reqToken.json()["error"])
    exit(1)

token = reqToken.json()["token"]


call_object = {
    "from": from_number,
    "to": number,
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
                "text": "Twój jednorazowy kod to: 1. 2. 3. 4.",
                "lang": "pl-PL/Maja"
                }
            },
        {
            "type": "tts",
            "params": {
                "text": "Powtarzam: Twój jednorazowy kod to: 1. 2. 3. 4.",
                "lang": "pl-PL/Maja"
                }
            }
        ]
}

respObject = requests.post(api_url + "/callobject", json=call_object, headers={"authorization": "Bearer " + token})

if respObject.status_code != 200:
    print("Failed to send the call. Status : " + respObject.json()["result"] + ",  Error: " + respObject.json()["error"])
    exit(1)

print("Status : " + respObject.json()["result"] + ",  Call-ID : " + respObject.json()["call_id"])



