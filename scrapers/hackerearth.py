import requests
import json
from datetime import datetime
now = datetime.utcnow()

URL = "https://www.hackerearth.com/api/community/challenges/hackathon/"

def hackerearth():

    r = requests.get(URL)
    r.raise_for_status()
    return r.json()["data"]

if __name__ == "__main__":
    data = hackerearth()
    print(data.content)
    print(type(data))