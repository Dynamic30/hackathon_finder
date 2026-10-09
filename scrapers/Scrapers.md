# Hackathon Finder — Scraper Priority

| Priority | Source      | Type       | Status | Method         | Notes |
|----------|-------------|-----------|--------|----------------|-------|
| 1        | Devpost     | Aggregator | ✅     | Json Response (API)       | Public JSON endpoints, easiest to pull, structured |
| 2        | Unstop      | Aggregator | ✅     | Json Response (API)    | No official API, largest India college base, scrape listing pages |
| 3        | Devfolio    | Aggregator | ✅     | Json Response (API) | Strong India + web3, check for API before scraping |
| 4        | Reddit      | Community  | ⬜     | Reddit API     | r/hackathon, r/developersIndia, r/csMajors — search/filter posts |
| 5        | Telegram    | Community  | ⬜     | Bot listener   | Join hackathon-alert channels via bot, parse messages, start with 1 |
| 6        | HackerEarth | Aggregator | ✅     | HTML scrape    | Hiring-focused hackathons + assessments, overlaps with corporate listings |
| 7        | Reskilll    | Aggregator | ⬜     | HTML scrape    | India-scale (92k+ regs), newer platform, verify site structure |
| 8        | Hack2Skill  | Aggregator | ✅     | HTML scrape    | India-focused, hosts many corporate hackathons (Google etc.) |
| 9        | GitHub lists| Curated    | ⬜     | Markdown parse | Curated repos (e.g. hackathons-tracker) — use to cross-check coverage, not a core source |
| 10       | MLH         | Aggregator | ⬜     | HTML scrape    | Global standard but mostly US/Europe, some India-relevant online events |
| 11       | DoraHacks   | Aggregator | ⬜     | API            | Web3/open-source niche, has API (BUIDL platform), low relevance for general use |
| 12       | Instagram   | Community  | ⬜     | Low priority   | College tech-fest pages, rate-limited/risky, skip for v1 |

## Status Legend
⬜ Not started · 🟨 In progress · ✅ Working · ⚠️ Broken

## v1 Scope
1. Devpost
2. Unstop
3. Devfolio
4. Reddit
5. Telegram (1 channel)

## Per-Scraper Detail
### Devpost
- **Status:** ⬜
- **Endpoint/URL:**
- **Fields extracted:**
- **Dedup key:**
- **Known issues:**

<!-- duplicate block per source -->

## Pipeline Notes
- Dedup: hash(name + date + org) — catches same hackathon posted on multiple sources
- Alert trigger: new listing / registration closes in 48h (separate, louder alert)
- DB:
- Last run:
