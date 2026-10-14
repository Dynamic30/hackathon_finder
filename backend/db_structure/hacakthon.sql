-- Hackathon Finder — table for DB_STRUCTURE (scrapers/orchestrator.py)
-- Postgres. Run once.

CREATE TABLE IF NOT EXISTS hackathons (
    id                  BIGSERIAL PRIMARY KEY,

    source              TEXT        NOT NULL,
    source_id           TEXT        NOT NULL,
    source_url          TEXT        NOT NULL,
    scraped_at          TIMESTAMPTZ NOT NULL,

    title               TEXT        NOT NULL,
    organizer           TEXT,
    description         TEXT,
    description_format  TEXT,

    start_at            TIMESTAMPTZ,
    end_at              TIMESTAMPTZ,
    reg_start_at        TIMESTAMPTZ,
    reg_end_at          TIMESTAMPTZ,
    date_confidence     TEXT        NOT NULL,
    is_active           BOOLEAN     NOT NULL DEFAULT TRUE,

    mode                TEXT        NOT NULL,
    city                TEXT,
    state               TEXT,
    country             TEXT,
    location_raw        TEXT,

    prize_amount        BIGINT,
    prize_currency      TEXT,
    prize_is_total      BOOLEAN,

    team_min            SMALLINT,
    team_max            SMALLINT,
    registrations       INTEGER,
    is_paid             BOOLEAN,

    tags                TEXT[]      NOT NULL DEFAULT '{}',
    image_url           TEXT,
    raw                 JSONB       NOT NULL,

    UNIQUE (source, source_id)
);

CREATE INDEX IF NOT EXISTS hackathons_reg_end_idx ON hackathons (reg_end_at) WHERE is_active;
CREATE INDEX IF NOT EXISTS hackathons_mode_idx    ON hackathons (mode)       WHERE is_active;
