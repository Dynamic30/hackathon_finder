from playwright.sync_api import sync_playwright
import time
import curl_cffi
import json

# uses devpost api to fetch data

URL = "https://devpost.com/hackathons?status[]=upcoming&status[]=open"

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

def api_endpoint_call():

    hacakthon_list = []
    page = 1
    while True:
        print(page)
        r = curl_cffi.get(
            f"https://devpost.com/api/hackathons?page={page}&status[]=upcoming&status[]=open",
            impersonate="chrome"
        )
        print(r.status_code)
        data = r.json()
        hacakthon_list.extend(data.get("hackathons"))
        # print(data)
        
        page+=1
        

        if not data.get("hackathons"):
            print("its false !!")
            break

    return (hacakthon_list)
        

# devpost_hackathon()
if __name__=="__main__":
    data = api_endpoint_call()
    with open("tests/devpost_text_data.json",'w',encoding="utf-8") as file:
        json.dump(data,file)
        file.close()