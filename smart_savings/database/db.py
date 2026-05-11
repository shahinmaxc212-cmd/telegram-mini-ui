import sqlite3
from config import DB_PATH


def get_db():
    """SQLite connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables on first run (safe to call multiple times)."""
    conn = get_db()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id                          TEXT PRIMARY KEY,
            type                        TEXT,
            balance                     REAL DEFAULT 0,
            profit                      REAL DEFAULT 0,
            total_profit                REAL DEFAULT 0,
            vip_level                   INTEGER DEFAULT 0,
            reward_balance              REAL DEFAULT 0,
            reward_timestamp            TEXT,
            daily_profit_percent        REAL DEFAULT 0,
            last_daily_profit_timestamp TEXT,
            username                    TEXT,
            first_name                  TEXT,
            name                        TEXT,
            email                       TEXT,
            phone                       TEXT,
            country_code                TEXT,
            address                     TEXT,
            referral_code               TEXT,
            registered                  INTEGER DEFAULT 0
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id      INTEGER PRIMARY KEY,
            user_id TEXT,
            message TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS support (
            id       INTEGER PRIMARY KEY,
            user_id  TEXT,
            username TEXT,
            sender   TEXT,
            msg      TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS deposits (
            id      INTEGER PRIMARY KEY,
            user_id TEXT,
            amount  REAL,
            network TEXT,
            txid    TEXT,
            status  TEXT,
            reason  TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS withdraws (
            id      INTEGER PRIMARY KEY,
            user_id TEXT,
            amount  REAL,
            address TEXT,
            network TEXT,
            status  TEXT,
            reason  TEXT
        )
    ''')

    # Migration: safely add new columns to existing databases
    migrations = [
        ("daily_profit_percent",        "REAL DEFAULT 0"),
        ("last_daily_profit_timestamp", "TEXT"),
        ("name",                        "TEXT"),
        ("email",                       "TEXT"),
        ("phone",                       "TEXT"),
        ("country_code",                "TEXT"),
        ("address",                     "TEXT"),
        ("referral_code",               "TEXT"),
        ("registered",                  "INTEGER DEFAULT 0"),
    ]
    for col, col_type in migrations:
        try:
            c.execute(f"ALTER TABLE users ADD COLUMN {col} {col_type}")
        except Exception:
            pass  # column already exists

    conn.commit()
    conn.close()
