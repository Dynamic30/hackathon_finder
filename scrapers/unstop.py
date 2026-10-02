import requests
import json
import time

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
        data += batch
        page_num+=1

    return data

if __name__ == "__main__":
    unstop_hackathons = unstop()
    # print(unstop_hackathons)
    with open("unstop_test_data.json",'w') as file:
        json.dump(unstop_hackathons,file,indent=2)