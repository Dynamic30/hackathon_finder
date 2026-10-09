from playwright.sync_api import sync_playwright
import time
import curl_cffi
import json
import re
from datetime import datetime, timezone
now = datetime.now(timezone.utc)


# uses devpost api to fetch data

URL = "https://devpost.com/hackathons?status[]=upcoming&status[]=open"

CURRENCY = {"$": "USD", "₹": "INR", "$CAD": "CAD", "€": "EUR", "£": "GBP", "MEX$": "MXN"}
MONTHS = {m: i for i, m in enumerate(
    ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)}


def parse_dates(s : str):
    # devpost only gives a display string: "Aug 31 - Oct 23, 2026", "Oct 01 - 10, 2026",
    # "Oct 10, 2026", "Sep 29, 2026 - Oct 14, 2026". the year is printed once, at the end.
    parts = []
    for p in (s or "").split(" - "):
        m = re.match(r"(?:([A-Z][a-z]{2})\w*\s+)?(\d{1,2})(?:,\s*(\d{4}))?$", p.strip())
        if not m:
            return None, None
        parts.append([m.group(1), int(m.group(2)), m.group(3)])

    month = next((p[0] for p in parts if p[0]), None)
    year = next((p[2] for p in reversed(parts) if p[2]), None)
    if not month or not year:
        return None, None

    dates = [datetime(int(p[2] or year), MONTHS[p[0] or month], p[1], tzinfo=timezone.utc)
             for p in parts]
    start, end = dates[0], dates[1] if len(dates) > 1 else None
    if end and start > end:          # "Dec 15 - Jan 10, 2027" -> start is the prior year
        start = start.replace(year=start.year - 1)
    return start, end


def parse_prize(s : str):
    # '$<span data-currency-value>138,000</span>' -> (138000, "USD")
    txt = re.sub(r"<[^>]+>", "", s or "").strip()
    m = re.search(r"[\d,]+", txt)
    if not m:
        return None, None
    return int(m.group().replace(",", "")), CURRENCY.get(txt[:m.start()].strip())


def per_card_strucure(r : dict) -> dict:
    loc = r.get("displayed_location") or {}
    thumb = r.get("thumbnail_url") or ""
    start, end = parse_dates(r.get("submission_period_dates"))
    prize, currency = parse_prize(r.get("prize_amount"))

    return {
    "source": "devpost",
    "source_id": str(r["id"]),
    "source_url": r["url"],
    "scraped_at": now,

    "title": r["title"],
    "organizer": r.get("organization_name"),
    "description": None,
    "description_format": None,

    "start_at": start,
    "end_at": end,
    "reg_start_at": None,               # devpost has no registration window
    "reg_end_at": None,
    "date_confidence": "parsed" if start else "none",

    "mode": {"globe": "online", "map-marker-alt": "offline"}.get(loc.get("icon"), "unknown"),
    "city": None,
    "state": None,
    "country": None,
    "location_raw": loc.get("location"),

    "prize_amount": prize,
    "prize_currency": currency,
    "prize_is_total": True if prize else None,

    "team_min": None,
    "team_max": None,
    "registrations": r.get("registrations_count"),
    "is_paid": None,

    "tags": [t["name"] for t in (r.get("themes") or [])],
    "image_url": ("https:" + thumb) if thumb.startswith("//") else (thumb or None),

    "raw": r
    }



def devpost_hackathon():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: print("<<", response.status, response.url))

        page.goto(URL,wait_until="networkidle")
        print("continue")        
        time.sleep(10)



    return

def devpost_data():

    hacakthon_list = []
    page = 1
    while True:
        # print(page)
        r = curl_cffi.get(
            f"https://devpost.com/api/hackathons?page={page}&status[]=upcoming&status[]=open",
            impersonate="chrome"
        )
        # print(r.status_code)
        data = r.json()
        hacakthon_list.extend(data.get("hackathons"))
        # print(data)
        
        page+=1
        

        if not data.get("hackathons"):
            # print("its false !!")
            break

    return [per_card_strucure(i) for i in hacakthon_list]
        

# devpost_hackathon()
if __name__=="__main__":
    data = devpost_data()
    with open("tests/devpost_text_data.json",'w',encoding="utf-8") as file:
        json.dump(data,file,indent=2,default=str)
        file.close()