import requests
import json
from datetime import datetime, timezone
now = datetime.now(timezone.utc)


def per_card_strucure(r : dict) -> dict:
    return {
    "source": "hack2skill",
    "source_id": r["_id"],
    "source_url": r.get("link") or (f"https://hack2skill.com/event/{r['eventUrl']}" if r.get("eventUrl") else None),
    "scraped_at": now,

    "title": r["title"],
    "organizer": None,
    "description": None,
    "description_format": None,

    "start_at": r.get("submissionStart"),
    "end_at": r.get("submissionEnd"),
    "reg_start_at": r.get("registrationStart"),
    "reg_end_at": r.get("registrationEnd"),
    "date_confidence": "exact" if r.get("submissionStart") else "none",

    "mode": {"VIRTUAL": "online", "ONLINE": "online", "IN_PERSON": "offline",
             "OFFLINE": "offline", "HYBRID": "hybrid"}.get(r.get("mode"), "unknown"),
    "city": None,
    "state": None,
    "country": None,
    "location_raw": None,

    "prize_amount": None,
    "prize_currency": None,
    "prize_is_total": None,

    "team_min": 1 if r.get("participation") == "Individual" else None,
    "team_max": 1 if r.get("participation") == "Individual" else None,
    "registrations": None,
    "is_paid": r.get("ticket") == "PAID",

    "tags": [r["flag"]],
    "image_url": r.get("thumbnail"),

    "raw": r
    }

URL = "https://hack2skill.com/api/v1/innovator/public/event/public-list?page=1&records=1000"

def hack2skill_data():

    response = requests.get(URL)
    response.raise_for_status()
    return [per_card_strucure(i) for i in response.json()["data"]]

if __name__ == "__main__":
    data = hack2skill_data()
    with open("tests/hack2skills.json",'w') as file:
        json.dump(data,file,indent=2,default=str)
