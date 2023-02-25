import requests


api_url = "https://api.vpbx.pl/api/v1"
#API Username
username = ""
#API Password
password = ""

#SMS ID 
sms_id = ""

reqToken = requests.post(api_url + "/login", json={"username": username, "password": password})

if reqToken.status_code != 200:
    print("Failed to authenticate. Status : " + reqToken.json()["result"] + ",  Error: " + reqToken.json()["error"])
    exit(1)

token = reqToken.json()["token"]


respObject = requests.get(api_url + "/sms/" + sms_id, headers={"authorization": "Bearer " + token})

if respObject.status_code != 200:
    print("Failed to send the sms. Status : " + respObject.json()["result"] + ",  Error: " + respObject.json()["error"])
    exit(1)

print("Status : " + respObject.json()["result"] + ",  Status : " + respObject.json()["status"])



