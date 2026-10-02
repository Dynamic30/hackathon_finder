from playwright.sync_api import sync_playwright
import json
import time

URL = "https://devfolio.co/hackathons/open"

def scroll_to_bottom(page):
    initial_height = page.evaluate("document.body.scrollHeight")
    n=0
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        new_height = page.evaluate("document.body.scrollHeight")
        n+=1
        print("reached ?>>")
        if new_height == initial_height:
            print("yes reached")
            break   

        if n==10:
            print("Maxed Scroll Limit reached (system set)")
            break
    
    return

def devfolio():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        # with page.expect_response("**")
        page.goto(URL)

        scroll_to_bottom(page)
        print("scroll done")
        time.sleep(10)
    return


if __name__ == "__main__":
    devfolio()