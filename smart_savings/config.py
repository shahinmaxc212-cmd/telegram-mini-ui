import os

# ── Bot & Admin Config ──────────────────────────────────────────────────────
ADMIN_ID        = "8671125457"          # আপনার Telegram User ID
BOT_USERNAME    = "siyamDemo12_bot"   # আপনার Bot Username (@ছাড়া)

# ── Wallet Addresses ────────────────────────────────────────────────────────
TRC_WALLET      = "TNWvYkycZFUfWzADKUQRjiZmRJWRhbU7Hm"   # TRC20 (USDT)
ERC_WALLET      = "0xFc9B81aa8e1921A2A4cd2ca7B46489c446F6c059"  # ERC20 (USDT)

# ── Database ─────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DB_PATH     = os.path.join(BASE_DIR, "database", "users.db")

# ── VIP Levels: {level: (min_balance, bonus_reward, color1, color2)} ─────────
VIP_CONFIG = {
    1: (500,   50,   "#6366f1", "#8b5cf6"),
    2: (1000,  100,  "#06b6d4", "#0284c7"),
    3: (2000,  200,  "#10b981", "#059669"),
    4: (5000,  500,  "#f59e0b", "#d97706"),
    5: (10000, 1000, "#f97316", "#ea580c"),
    6: (20000, 2000, "#ef4444", "#dc2626"),
    7: (50000, 5000, "#8b5cf6", "#6d28d9"),
}

VIP_COLORS = {
    0: "#64748b", 1: "#6366f1", 2: "#06b6d4",
    3: "#10b981", 4: "#f59e0b", 5: "#f97316",
    6: "#ef4444", 7: "#8b5cf6"
}
