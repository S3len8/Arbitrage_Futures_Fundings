import os
import logging
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values
PSYCOPG2_AVAILABLE = True


# ─── Connection settings ───────────────────────────────────────────────────────
# You can change these values directly or use environment variables
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME",     "funding_scanner"),
    "user":     os.getenv("DB_USER",     "postgres"),
    "password": os.getenv("DB_PASSWORD", "12345678"),
}

# Name of the table to store funding opportunities
TABLE_NAME = "funding_opportunities"

# ─── SQL ───────────────────────────────────────────────────────────────────────
CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id              SERIAL PRIMARY KEY,
    scanned_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    pair            VARCHAR(30)  NOT NULL,
    small_exchange  VARCHAR(30),
    small_ask       NUMERIC(20, 8),
    small_bid       NUMERIC(20, 8),
    small_volume_24h NUMERIC(30, 2),
    big_exchange    VARCHAR(30),
    big_ask         NUMERIC(20, 8),
    big_bid         NUMERIC(20, 8),
    big_volume_24h  NUMERIC(30, 2),
    funding_spread  NUMERIC(20, 8),
    profit          NUMERIC(20, 8)
);
"""

INSERT_SQL = f"""
INSERT INTO {TABLE_NAME} (
    scanned_at,
    pair, small_exchange, small_ask, small_bid, small_volume_24h,
    big_exchange, big_ask, big_bid, big_volume_24h,
    funding_spread, profit
) VALUES %s
"""


# ─── Public API ────────────────────────────────────────────────────────────────

def get_connection():
    """Opens and returns a new psycopg2 connection."""
    if not PSYCOPG2_AVAILABLE:
        raise RuntimeError("psycopg2 is not installed. Run: pip install psycopg2-binary")
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """
    Creates the funding_opportunities table if it does not exist.
    Call once at application startup.
    Returns True on success, False on error.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)
        logging.info(f"[DB] Table '{TABLE_NAME}' is ready.")
        return True
    except Exception as e:
        logging.error(f"[DB] init_db error: {e}")
        return False


def save_funding_results(rows: list[dict], scanned_at: datetime = None) -> int:
    """
    Saves a list of funding opportunity rows to PostgreSQL.

    Args:
        rows: list of dicts, each with keys:
              pair, small_ex, small_ask, small_bid,
              big_ex, big_ask, big_bid, spread, profit
        scanned_at: timestamp for the scan (defaults to now)

    Returns:
        Number of rows inserted, or -1 on error.
    """
    if not rows:
        return 0

    if scanned_at is None:
        scanned_at = datetime.now()

    # Build tuples for bulk insert
    values = []
    for r in rows:
        values.append((
            scanned_at,
            r.get("pair", ""),
            r.get("small_ex", ""),
            r.get("small_ask", 0),
            r.get("small_bid", 0),
            r.get("small_volume_24H") or r.get("small_volume_24h") or 0,
            r.get("big_ex", ""),
            r.get("big_ask", 0),
            r.get("big_bid", 0),
            r.get("big_volume_24H") or r.get("big_volume_24h") or 0,
            r.get("spread", 0),
            r.get("profit", 0),
        ))

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                execute_values(cur, INSERT_SQL, values)
        logging.info(f"[DB] Saved {len(values)} funding records (scanned_at={scanned_at}).")
        return len(values)
    except Exception as e:
        logging.error(f"[DB] save_funding_results error: {e}")
        return -1


def is_available() -> bool:
    """Quick check: can we connect to the database?"""
    if not PSYCOPG2_AVAILABLE:
        return False
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception:
        return False