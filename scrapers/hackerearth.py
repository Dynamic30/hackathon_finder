import requests
import json
from datetime import datetime, timezone
now = datetime.now(timezone.utc)


URL = "https://www.hackerearth.com/api/community/challenges/hackathon/"

def per_card_strucure(r : dict) -> dict:
    return {
    "source": "hackerearth",
    "source_id": r["slug"],
    "source_url": r["url"] if r["url"].startswith("http") else "https://www.hackerearth.com"+r["url"],
    "scraped_at": now,

    "title": r["title"],
    "organizer": r.get("company_name"),
    "description": None,
    "description_format": None,

    "start_at": datetime.fromisoformat(r["start"]).replace(tzinfo=timezone.utc),
    "end_at": datetime.fromisoformat(r["end"]).replace(tzinfo=timezone.utc),
    "reg_start_at": None,
    "reg_end_at": None,
    "date_confidence": "exact",

    "mode": "unknown",
    "city": None,
    "state": None,
    "country": None,
    "location_raw": None,

    "prize_amount": None,
    "prize_currency": None,
    "prize_is_total": None,

    "team_min": r.get("min_team_size"),
    "team_max": r.get("max_team_size"),
    "registrations": r.get("subscription_count"),
    "is_paid": None,

    "tags": [r["type"]],
    "image_url": r.get("listing_image"),

    "raw": r
    }


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