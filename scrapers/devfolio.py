import requests
import json
import time
from datetime import datetime, timezone
now = datetime.now(timezone.utc)


URL = "https://api.devfolio.co/api/search/hackathons"

def per_card_strucure(r : dict) -> dict:
    return



def devfolio():
    r = requests.post(URL,
              json={"type": "application_open", "from": 0, "size": 200})
    r.raise_for_status()
    return [h["_source"] for h in r.json()["hits"]["hits"]]


if __name__ == "__main__":
    devfolio_data = devfolio()
    live = [h for h in devfolio_data
        if datetime.fromisoformat(h["hackathon_setting"]["reg_ends_at"]) > now]

    print(live)
    print(len(live))
    print(len(devfolio_data))
    print(type(devfolio_data))
    with open("tests/devfolio_test.json",'w') as file:
        json.dump(devfolio_data,file,indent=2)
        file.close()

