import requests
import json
import time
from datetime import datetime, timezone
now = datetime.now(timezone.utc)

def per_card_strucure(r : dict) -> dict:
    rq = r.get("regnRequirements") or {}
    addr = r.get("address_with_country_logo") or {}
    cash = [p for p in (r.get("prizes") or []) if p.get("cash")]

    return {
    "source": "unstop",
    "source_id": str(r["id"]),
    "source_url": r["seo_url"],
    "scraped_at": now,

    "title": r["title"],
    "organizer": (r.get("organisation") or {}).get("name"),
    "description": r.get("details"),
    "description_format": "html" if r.get("details") else None,

    "start_at": rq.get("start_regn_dt"),    # no event start date, reg start used instead
    "end_at": r.get("end_date"),
    "reg_start_at": rq.get("start_regn_dt"),
    "reg_end_at": rq.get("end_regn_dt"),
    "date_confidence": "inferred",

    "mode": r.get("region") or "unknown",   # already online / offline / hybrid
    "city": addr.get("city") or None,
    "state": addr.get("state") or None,
    "country": (addr.get("country") or {}).get("name"),
    "location_raw": addr.get("address") or None,

    "prize_amount": sum(p["cash"] for p in cash) or None,
    "prize_currency": {"fa-rupee": "INR", "fa-dollar": "USD"}.get(cash[0].get("currency")) if cash else None,
    "prize_is_total": True if cash else None,

    "team_min": rq.get("min_team_size"),
    "team_max": rq.get("max_team_size"),
    "registrations": r.get("registerCount"),
    "is_paid": r.get("isPaid"),

    "tags": [s["skill"] for s in (r.get("required_skills") or [])]
            + [w["name"] for w in (r.get("workfunction") or [])],
    "image_url": r.get("logoUrl2"),

    "raw": r
    }

def unstop():
    data = []
    page_num=1
    while True:

        r = requests.get(
        "https://unstop.com/api/public/opportunity/search-result",
        params={"opportunity": "hackathons", "oppstatus": "open",
                "per_page": 50, "page": page_num},
        headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        
        batch = r.json()["data"]["data"]
        if not batch:
            print("NO DATA FOUND! CHECK IT ONCE")
            break
        print(f"page_done : {page_num}")
        data += batch
        page_num+=1


    return data

if __name__ == "__main__":
    unstop_hackathons = unstop()
    # print(unstop_hackathons)
    with open("tests/unstop_test_data.json",'w') as file:
        json.dump(unstop_hackathons,file,indent=2)
        file.close()