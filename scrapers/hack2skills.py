import requests
import json

def per_card_strucure(r : dict) -> dict:
    return

URL =  "https://hack2skill.com/api/v1/innovator/public/event/public-list?page=1&records=1000"

response = requests.get(URL)

print(response.content)

with open("tests/hack2skills.json",'w') as file:
    json.dump(response.json(),file,indent=2)
