import requests
import json
from datetime import datetime, timezone
now = datetime.now(timezone.utc)


URL = "https://www.hackerearth.com/api/community/challenges/hackathon/"

def hackerearth(live_only=True,challenge_type=None): # added challenge type if later on i need to only pull hackathon data and not competitve

    r = requests.get(URL)
    r.raise_for_status()
    rows= r.json()["data"]
    if not live_only:
        return rows
    now = datetime.now(timezone.utc)
    return [x for x in rows
            if datetime.fromisoformat(x["end"]).replace(tzinfo=timezone.utc) > now]



if __name__ == "__main__":
    data = hackerearth()
    print(type(data))
    with open("tests/hackerearth_test.json",'w') as file:
        json.dump(data , file,indent=2)