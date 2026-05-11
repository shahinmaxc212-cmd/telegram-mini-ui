from datetime import datetime, timedelta
from database.db import get_db
from config import VIP_CONFIG


# ── VIP helpers ──────────────────────────────────────────────────────────────

def get_vip_level(balance: float) -> int:
    for level in sorted(VIP_CONFIG.keys(), reverse=True):
        if balance >= VIP_CONFIG[level][0]:
            return level
    return 0


def get_vip_bonus(level: int) -> float:
    return VIP_CONFIG.get(level, (0, 0))[1]


# ── Daily profit ─────────────────────────────────────────────────────────────

def process_daily_profit(uid: str) -> None:
    """Add daily profit to a user's balance if 24 h have passed."""
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT balance, daily_profit_percent, last_daily_profit_timestamp "
        "FROM users WHERE id=?", (uid,)
    )
    user = c.fetchone()
    if not user or user["daily_profit_percent"] <= 0:
        conn.close()
        return

    last_time = user["last_daily_profit_timestamp"]
    if last_time:
        elapsed = datetime.now() - datetime.fromisoformat(last_time)
        if elapsed < timedelta(hours=24):
            conn.close()
            return

    daily = round(user["balance"] * (user["daily_profit_percent"] / 100), 2)
    if daily > 0:
        c.execute(
            "UPDATE users SET balance=balance+?, total_profit=total_profit+?, "
            "last_daily_profit_timestamp=? WHERE id=?",
            (daily, daily, datetime.now().isoformat(), uid),
        )
    conn.commit()
    conn.close()
