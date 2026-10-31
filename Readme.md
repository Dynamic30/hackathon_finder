# Hackathon Finder

## need

there are a lot of Hackathon that happen and we can find them but a deticated platform that scrapes all sources in any region, sorts them by region , online offlien mode etc. and people can see what is the upcomming hacakthon and can sour them based on priority 

for region, it is currently mapped to India but in future more regions will be added as well

## how it works

scrapers pull hackathons from unstop, devpost, devfolio, hackerearth and hack2skill. the orchestrator pushes them to postgres (supabase). fastapi serves them and also serves the frontend, which is plain html, css and js with no build step.

    scrapers/   scrapers + orchestrator
    backend/    fastapi api
    frontend/   index.html, error.html, static/

priority is not stored in the db, it is calculated on every request. every hackathon gets a score out of 100 (deadline 55, prize 35, registrations 10). 60 or more is high, 35 or more is medium, the rest is low. the code is in `priority()` in backend/routes/home.py

## run it

you need a postgres db and a redis (upstash works). make a `.env` in the root

    sql_db=postgresql://...
    REDIS_URL=rediss://...

with docker

    docker compose up --build

then open localhost:8000. compose starts its own redis so the REDIS_URL in .env is not used there.

without docker

    pip install -r requirements.txt
    playwright install chromium
    fastapi dev backend/main.py

to get data, run the orchestrator. it creates the tables first (backend/db_structure/hacakthon.sql), then scrapes and pushes. run it again whenever you want fresh data, it updates the dates and marks old ones inactive

    python -m scrapers.orchestrator

or in docker

    docker compose run --rm scraper

## api

    GET /v1/all_cards
    sort_by = Prize | Urgency | Recent | Priority
    tier    = high | medium | low
    status  = active | inactive | all
    skip, limit

    GET /v1/cards/{source}/{source_id}

second one gives the full details of one hackathon. 120 requests per minute per ip, and the list is cached for 2 minutes

## feature addition (for future)

if a user sign in in that case we can have a subscription where they will pay so we give them insights on hackathon as well 
like reddit and other sources reviews and insight which we scrape and get them on dashboard 
a good addition but a bit tricky
