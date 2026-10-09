import requests
import json
import time
from datetime import datetime, timezone
now = datetime.now(timezone.utc)


URL = "https://api.devfolio.co/api/search/hackathons"

def per_card_strucure(r : dict) -> dict:
    hs = r.get("hackathon_setting") or {}

    return {
    "source": "devfolio",
    "source_id": r["uuid"],
    "source_url": f"https://{r['slug']}.devfolio.co",
    "scraped_at": now,

    "title": r["name"],
    "organizer": r.get("hosted_by"),
    "description": r.get("desc"),
    "description_format": "text" if r.get("desc") else None,

    "start_at": r.get("starts_at"),
    "end_at": r.get("ends_at"),
    "reg_start_at": hs.get("reg_starts_at"),
    "reg_end_at": hs.get("reg_ends_at"),
    "date_confidence": "exact",

    "mode": "online" if r.get("is_online") else "offline",
    "city": r.get("city"),
    "state": r.get("state"),
    "country": r.get("country"),
    "location_raw": r.get("location"),

    "prize_amount": None,               # prizes[] has names only, no cash amounts
    "prize_currency": None,
    "prize_is_total": None,

    "team_min": r.get("team_min"),
    "team_max": r.get("team_size"),
    "registrations": r.get("participants_count"),
    "is_paid": None,

    "tags": [t["name"] for t in (r.get("themes") or [])],
    "image_url": r.get("cover_img"),

    "raw": r
    }



def devfolio_data():
    r = requests.post(URL,
              json={"type": "application_open", "from": 0, "size": 200})
    r.raise_for_status()
    return [per_card_strucure(h["_source"]) for h in r.json()["hits"]["hits"]]


if __name__ == "__main__":
    data = devfolio_data()
    print(len(data))
    print(type(data))
    with open("tests/devfolio_test.json",'w') as file:
        json.dump(data,file,indent=2,default=str)
        file.close()

