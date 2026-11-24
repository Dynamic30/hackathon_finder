<div align="center">

<img src="frontend/static/favicon.svg" width="88" alt="Hackathon Finder logo">

# Hackathon Finder

Upcoming hackathons in India, from every major source, ranked by deadline, prize and priority.

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.162-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-cache-DC382D?logo=redis&logoColor=white)

</div>

## What it does

There are a lot of hackathons and you can find them, but there was no dedicated place that scrapes all the sources, sorts them by region, online or offline mode etc., and shows what is upcoming and what matters most.

Hackathon Finder scrapes Unstop, Devpost, Devfolio, HackerEarth and Hack2Skill, puts them in one list and ranks them. Region is currently India, more regions will be added later.

## Features

- Priority ranking: every hackathon gets a score and a High, Medium or Low tier.
- Sort by urgency, prize or recent, and filter by tier.
- Active, past or all hackathons.
- Search by name, organizer, location or theme.
- Detail page for each hackathon with dates, prize, team size, entry and a link to the source.
- Light and dark theme, and card or list layout.
- Infinite scroll, no build step.

## How it works

Scrapers pull hackathons from the five sources. The orchestrator pushes them to postgres (supabase). FastAPI serves them and also serves the frontend, which is plain html, css and js.

    scrapers/   scrapers + orchestrator
    backend/    fastapi api
    frontend/   index.html, error.html, static/

### Priority

Priority is not stored in the db, it is calculated on every request. Every hackathon gets a score out of 100.

| Part | Max | Based on |
|---|---|---|
| Deadline | 55 | how soon registration closes |
| Prize | 35 | cash value, converted to INR |
| Registrations | 10 | how many have registered |

60 or more is high, 35 or more is medium, the rest is low. The code is in `priority()` in `backend/routes/home.py`.

## Run it

You need a postgres db and a redis (upstash works). Make a `.env` in the root, see `.env.example`.

    sql_db=postgresql://...
    REDIS_URL=rediss://...

With docker

    docker compose up --build

then open localhost:8000. Compose starts its own redis so the REDIS_URL in .env is not used there.

Without docker

    pip install -r requirements.txt
    playwright install chromium
    fastapi dev backend/main.py

To get data, run the orchestrator. It creates the tables first (`backend/db_structure/hacakthon.sql`), then scrapes and pushes. Run it again whenever you want fresh data, it updates the dates and marks old ones inactive.

    python -m scrapers.orchestrator

or in docker

    docker compose run --rm scraper

## API

    GET /v1/all_cards
    sort_by = Prize | Urgency | Recent | Priority
    tier    = high | medium | low
    status  = active | inactive | all
    q, skip, limit

    GET /v1/cards/{source}/{source_id}

    GET /v1/last_updated

The second one gives the full details of one hackathon. 120 requests per minute per ip, and the list is cached for 2 minutes.

## Future

- Sign in, with a paid plan that gives insights on each hackathon, like reddit and other source reviews which we scrape and show on a dashboard. A good addition but a bit tricky.
- Organizer or company tags (Google, Meta etc.) to filter by and to rank higher.
- More regions.
