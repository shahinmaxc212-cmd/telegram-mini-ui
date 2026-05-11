from datetime import datetime, timedelta
from flask import Blueprint, request, render_template_string
from database.db import get_db
from helpers import get_vip_level, get_vip_bonus, process_daily_profit
from config import ADMIN_ID, BOT_USERNAME, VIP_CONFIG, VIP_COLORS

home_bp = Blueprint("home", __name__)


# ── Reusable HTML snippets ────────────────────────────────────────────────────

def ticker_html():
    return """
    <div class="ticker-wrap animate-in">
        <div class="ticker-inner">
            <span class="ticker-item">
                <span class="ticker-symbol">BTC</span>
                <span class="ticker-price">Loading...</span>
            </span>
        </div>
    </div>
    """


def market_section():
    coins = [
        ("bitcoin",     "₿",  "Bitcoin",    "BTC"),
        ("ethereum",    "Ξ",  "Ethereum",   "ETH"),
        ("tether",      "₮",  "Tether",     "USDT"),
        ("binancecoin", "🔶", "BNB Chain",  "BNB"),
        ("solana",      "◎",  "Solana",     "SOL"),
        ("ripple",      "✕",  "XRP Ledger", "XRP"),
    ]
    cards = "".join(f"""
        <div class="market-card" data-coin="{cid}">
            <div class="market-coin-icon">{icon}</div>
            <div class="market-coin-name">{sym}</div>
            <div class="market-coin-full">{name}</div>
            <div class="market-coin-price">Loading...</div>
            <div class="market-coin-change pos">+0.00%</div>
        </div>
    """ for cid, icon, name, sym in coins)
    return f"""
    <div class="section-title animate-in delay-3">📊 Live Market</div>
    <div class="market-grid animate-in delay-3">{cards}</div>
    """


def base_head():
    """Shared <head> content."""
    return """
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="/static/css/main.css">
    <script>
    const tg = window.Telegram.WebApp;
    tg.expand(); tg.ready(); tg.setHeaderColor('#050816');
    const _tgUser = tg.initDataUnsafe?.user;
    if (window.location.pathname === '/' && _tgUser && !window.location.search.includes("id=")) {
        window.location.href = '/?id=' + _tgUser.id + '&username=' + (_tgUser.username||'') + '&first_name=' + encodeURIComponent(_tgUser.first_name||'');
    }
    </script>
    """


def page(content, scripts="", uid=""):
    nav = f'<div class="bottom-nav"><a href="/?id={uid}" class="nav-item active"><div class="nav-icon">🏠</div><div class="nav-label">Home</div></a><a href="/profile?id={uid}" class="nav-item"><div class="nav-icon">👤</div><div class="nav-label">Profile</div></a><a href="/deposit?id={uid}" class="nav-item"><div class="nav-icon">💳</div><div class="nav-label">Deposit</div></a><a href="/withdraw?id={uid}" class="nav-item"><div class="nav-icon">💸</div><div class="nav-label">Withdraw</div></a><a href="/settings?id={uid}" class="nav-item"><div class="nav-icon">⚙️</div><div class="nav-label">Settings</div></a></div>' if uid else ""
    return f"""<!DOCTYPE html><html lang="en">
    <head>{base_head()}</head>
    <body>
    {content}
    {nav}
    <script src="/static/js/crypto.js"></script>
    {scripts}
    </body></html>"""


def result_page(icon, title, subtitle, btn_href, btn_label):
    """Generic success / error full-page result."""
    return f"""<!DOCTYPE html><html lang="en">
    <head>{base_head()}</head>
    <body>
    <div class="page"><div class="result-page">
        <div class="result-icon animate-in">{icon}</div>
        <div class="result-title animate-in delay-1">{title}</div>
        <div class="result-sub animate-in delay-2">{subtitle}</div>
        <a href="{btn_href}" class="btn-primary animate-in delay-3" style="max-width:280px">{btn_label}</a>
    </div></div>
    </body></html>"""


# ── Routes ────────────────────────────────────────────────────────────────────

@home_bp.route("/")
def home():
    uid       = request.args.get("id")
    username  = request.args.get("username") or ""
    first_name = request.args.get("first_name") or ""

    if not uid:
        return f"""<!DOCTYPE html><html lang="en">
        <head>{base_head()}</head>
        <body>
        <div class="page"><div class="result-page">
            <div class="result-icon">🔒</div>
            <div class="result-title">Access Denied</div>
            <div class="result-sub">Open this app through Telegram Bot</div>
            <a href="https://t.me/{BOT_USERNAME}" target="_blank" class="btn-primary" style="max-width:280px">Open Bot →</a>
        </div></div>
        </body></html>"""

    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (id,type,username,first_name) VALUES(?,?,?,?)",
                  (uid, "user", username, first_name))
        conn.commit()
        c.execute("SELECT * FROM users WHERE id=?", (uid,))
        user = c.fetchone()

    process_daily_profit(uid)
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = c.fetchone()
    if user["balance"] < 0:       c.execute("UPDATE users SET balance=0 WHERE id=?",        (uid,))
    if user["reward_balance"] < 0: c.execute("UPDATE users SET reward_balance=0 WHERE id=?", (uid,))
    conn.commit()

    # ── Admin shortcut ──────────────────────────────────────────────────────
    if uid == ADMIN_ID:
        conn.close()
        return f"""<!DOCTYPE html><html lang="en">
        <head>{base_head()}</head>
        <body>
        <div class="page">
            <div class="app-logo animate-in">
                <div class="logo-icon">💰</div>
                <div><div class="logo-text">SMART SAVINGS</div><div class="logo-tag">ADMIN ACCESS</div></div>
            </div>
            <div class="admin-banner animate-in delay-1">🔐 Administrator Account Detected</div>
            <a href="/admin?id={uid}" class="btn-red animate-in delay-2">Open Admin Panel →</a>
        </div>
        </body></html>"""

    # ── Registration guard ──────────────────────────────────────────────────
    if user["registered"] == 0:
        conn.close()
        return f"""<!DOCTYPE html><html lang="en">
        <head>{base_head()}</head>
        <body>
        <div class="page"><div class="result-page">
            <div class="result-icon">🚀</div>
            <div class="result-title">Welcome!</div>
            <div class="result-sub">Complete your registration to start earning</div>
            <a href="/register?id={uid}" class="btn-primary" style="max-width:280px">Complete Registration →</a>
        </div></div>
        </body></html>"""

    # ── VIP upgrade check ───────────────────────────────────────────────────
    current_vip = get_vip_level(user["balance"])
    if current_vip > user["vip_level"]:
        bonus = get_vip_bonus(current_vip)
        now = datetime.now().isoformat()
        c.execute("UPDATE users SET vip_level=?,reward_balance=reward_balance+?,reward_timestamp=? WHERE id=?",
                  (current_vip, bonus, now, uid))
        c.execute("INSERT INTO messages VALUES(NULL,?,?)",
                  (uid, f"🎉 VIP {current_vip} Achieved! {bonus} USDT reward added!"))
        conn.commit()

    # ── Reward auto-credit ──────────────────────────────────────────────────
    if user["reward_timestamp"] and user["reward_balance"] > 0:
        if datetime.now() - datetime.fromisoformat(user["reward_timestamp"]) >= timedelta(hours=24):
            c.execute("UPDATE users SET balance=balance+?,reward_balance=0,reward_timestamp=NULL WHERE id=?",
                      (user["reward_balance"], uid))
            c.execute("INSERT INTO messages VALUES(NULL,?,?)",
                      (uid, f"💰 {user['reward_balance']} USDT reward added to main balance!"))
            conn.commit()

    c.execute("SELECT message FROM messages WHERE user_id=?", (uid,))
    msgs = c.fetchall()
    conn.close()

    badge        = f'<span class="badge">{len(msgs)}</span>' if msgs else ""
    daily_amount = round(user["balance"] * (user["daily_profit_percent"] / 100), 2)
    display_name = user["name"] or user["first_name"] or username or "User"
    vip_col      = VIP_COLORS.get(user["vip_level"], "#64748b")

    msgs_html = "".join(
        f'<div class="msg-bubble"><div class="msg-from">From Admin / Support</div>{m[0]}</div>'
        for m in msgs
    ) or '<div style="text-align:center;color:var(--muted);padding:32px 0">No messages yet</div>'

    mark_btn = '<button onclick="markAsRead()" class="btn-green" style="margin-top:8px">Mark All as Read</button>' if msgs else ""

    vip_cards = "".join(
        f'<div class="vip-card"><div class="vip-badge" style="background:linear-gradient(135deg,{c1},{c2});color:#fff">V{lvl}</div>'
        f'<div class="vip-info"><div class="vip-name">VIP {lvl}</div><div class="vip-req">Min. {req} USDT balance</div></div>'
        f'<div class="vip-reward">+{rew} USDT</div></div>'
        for lvl, (req, rew, c1, c2) in VIP_CONFIG.items()
    )

    content = f"""
    <div class="page">
        <div class="app-logo animate-in">
            <div class="logo-icon">💰</div>
            <div><div class="logo-text">SMART SAVINGS</div><div class="logo-tag">PREMIUM EARNINGS</div></div>
            <div style="margin-left:auto;text-align:right">
                <div style="font-size:0.78rem;color:var(--muted)">Welcome back</div>
                <div style="font-size:0.88rem;font-weight:700">{display_name}</div>
            </div>
        </div>

        {ticker_html()}

        <div class="balance-card animate-in delay-1">
            <div class="balance-label">Total Balance</div>
            <div class="balance-amount">{max(0, user['balance']):.2f} <span class="balance-unit">USD</span></div>
            <div style="margin-top:12px;display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.08);border-radius:999px;padding:5px 14px;font-size:0.75rem">
                <span style="width:8px;height:8px;background:{vip_col};border-radius:50%;display:inline-block"></span>
                <span style="color:{vip_col};font-weight:700">VIP {user['vip_level']}</span>
                <span style="color:var(--muted)">•</span>
                <span style="color:var(--muted)">{user['daily_profit_percent']}%/day</span>
            </div>
        </div>

        <div class="stat-grid animate-in delay-2">
            <div class="stat-box stat-green"><div class="stat-icon">📈</div><div class="stat-val">{daily_amount:.2f}</div><div class="stat-lbl">Daily Profit</div></div>
            <div class="stat-box stat-green"><div class="stat-icon">💰</div><div class="stat-val">{user['total_profit']:.2f}</div><div class="stat-lbl">Total Profit</div></div>
            <div class="stat-box stat-purple"><div class="stat-icon">🌟</div><div class="stat-val">{max(0,user['reward_balance']):.2f}</div><div class="stat-lbl">Reward Balance</div></div>
            <div class="stat-box" style="border-color:rgba(245,158,11,0.3)"><div class="stat-icon">🏆</div><div class="stat-val" style="color:#fbbf24">VIP {user['vip_level']}</div><div class="stat-lbl">VIP Level</div></div>
        </div>

        <div class="action-grid animate-in delay-2">
            <a href="/deposit?id={uid}" class="action-btn"><span class="icon">💳</span><span>Deposit</span></a>
            <a href="/withdraw?id={uid}" class="action-btn"><span class="icon">💸</span><span>Withdraw</span></a>
        </div>

        {market_section()}

        <div class="divider"></div>
        <div class="section-title animate-in delay-4">Menu</div>

        <a href="/profile?id={uid}" class="menu-row animate-in delay-4">
            <div class="row-icon">👤</div>
            <div class="row-text"><div class="row-title">My Profile</div><div class="row-sub">View account details & stats</div></div>
            <div class="row-arrow">›</div>
        </a>
        <a href="/support?id={uid}&username={username}" class="menu-row animate-in delay-4">
            <div class="row-icon">💬</div>
            <div class="row-text"><div class="row-title">Support</div><div class="row-sub">Contact our team</div></div>
            <div class="row-arrow">›</div>
        </a>
        <div onclick="openModal('messagesModal')" class="menu-row animate-in delay-4" style="cursor:pointer">
            <div class="row-icon">📩</div>
            <div class="row-text"><div class="row-title">Messages</div><div class="row-sub">Notifications from admin</div></div>
            {badge}<div class="row-arrow">›</div>
        </div>
        <div onclick="openModal('vipModal')" class="menu-row animate-in delay-4" style="cursor:pointer">
            <div class="row-icon">🌟</div>
            <div class="row-text"><div class="row-title">VIP Program</div><div class="row-sub">Levels, rewards & bonuses</div></div>
            <div class="row-arrow">›</div>
        </div>

        <div style="height:24px"></div>
    </div>

    <!-- Messages Modal -->
    <div id="messagesModal" class="modal-overlay">
        <div class="modal-box" onclick="event.stopPropagation()">
            <div class="modal-handle"></div>
            <div class="modal-title">📩 Messages</div>
            <div class="modal-body">{msgs_html}{mark_btn}</div>
        </div>
    </div>

    <!-- VIP Modal -->
    <div id="vipModal" class="modal-overlay">
        <div class="modal-box" onclick="event.stopPropagation()">
            <div class="modal-handle"></div>
            <div class="modal-title">🌟 VIP Rewards Program</div>
            <div class="modal-body">
                <div style="text-align:center;color:var(--muted);font-size:0.82rem;margin-bottom:16px">Higher balance = higher VIP = bigger rewards</div>
                {vip_cards}
            </div>
        </div>
    </div>
    """
    
    return page(content, scripts=f"""
    <script>
    function openModal(id)  {{ document.getElementById(id).classList.add('open'); }}
    function closeModal(id) {{ document.getElementById(id).classList.remove('open'); }}
    document.querySelectorAll('.modal-overlay').forEach(el => el.addEventListener('click', () => el.classList.remove('open')));
    function markAsRead() {{
        fetch('/clear_messages?id={uid}').then(() => location.reload());
    }}
    </script>
    """, uid=uid)


@home_bp.route("/clear_messages")
def clear_messages():
    uid = request.args.get("id")
    if uid:
        conn = get_db(); c = conn.cursor()
        c.execute("DELETE FROM messages WHERE user_id=?", (uid,))
        conn.commit(); conn.close()
    return "OK"


# ── Registration ──────────────────────────────────────────────────────────────

@home_bp.route("/register")
def register():
    uid = request.args.get("id")
    return f"""<!DOCTYPE html><html lang="en">
    <head>{base_head()}</head>
    <body>
    <div class="page">
        <div class="app-logo animate-in">
            <div class="logo-icon">💰</div>
            <div><div class="logo-text">SMART SAVINGS</div><div class="logo-tag">REGISTRATION</div></div>
        </div>
        <div class="card card-glow animate-in delay-1">
            <div style="text-align:center;margin-bottom:24px">
                <div style="font-size:2rem;margin-bottom:10px">👤</div>
                <div style="font-size:1.3rem;font-weight:800">Create Account</div>
                <div style="font-size:0.8rem;color:var(--muted);margin-top:4px">Complete your profile to get started</div>
            </div>
            <form action="/register_submit" method="GET">
                <input type="hidden" name="uid" value="{uid}">
                <label class="field-label">Full Name</label>
                <input type="text" name="name" placeholder="Your full name" required class="field">
                <label class="field-label">Email Address</label>
                <input type="email" name="email" placeholder="you@email.com" required class="field">
                <label class="field-label">Country Code</label>
                <input type="text" name="country_code" placeholder="+1, +44, +880 ..." required class="field">
                <label class="field-label">Phone Number</label>
                <input type="tel" name="phone" placeholder="Phone number" required class="field">
                <label class="field-label">Address</label>
                <textarea name="address" rows="2" placeholder="Your full address" required class="field"></textarea>
                <label class="field-label">Referral Code</label>
                <input type="text" name="referral_code" placeholder="Optional" class="field">
                <div class="check-row">
                    <input type="checkbox" id="agree" required>
                    <label for="agree">I agree to the Terms and Conditions</label>
                </div>
                <button type="submit" class="btn-primary">Create Account →</button>
            </form>
        </div>
    </div>
    </body></html>"""


@home_bp.route("/register_submit")
def register_submit():
    uid = request.args.get("uid")
    conn = get_db(); c = conn.cursor()
    c.execute(
        "UPDATE users SET name=?,email=?,country_code=?,phone=?,address=?,referral_code=?,registered=1 WHERE id=?",
        (
            request.args.get("name"),
            request.args.get("email"),
            request.args.get("country_code"),
            request.args.get("phone"),
            request.args.get("address"),
            request.args.get("referral_code") or "",
            uid,
        ),
    )
    conn.commit(); conn.close()
    return result_page("✅", "Registration Successful!", "Welcome to SMART SAVINGS Premium Earnings", f"/?id={uid}", "Go to Dashboard →")


# ── Profile ───────────────────────────────────────────────────────────────────

@home_bp.route("/profile")
def profile():
    uid = request.args.get("id")
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = c.fetchone(); conn.close()
    daily = round(user["balance"] * (user["daily_profit_percent"] / 100), 2)

    price_rows = "".join(
        f'<div class="price-row"><div class="price-coin"><span class="price-icon">{icon}</span>'
        f'<div><div class="price-name">{sym}</div><div class="price-ticker">{name}</div></div></div>'
        f'<div class="price-right"><div class="price-usd" data-coin-price="{cid}">Loading...</div>'
        f'<div class="price-chg pos" data-coin-chg="{cid}">--</div></div></div>'
        for cid, icon, sym, name in [
            ("bitcoin","₿","BTC","Bitcoin"), ("ethereum","Ξ","ETH","Ethereum"),
            ("tether","₮","USDT","Tether"), ("binancecoin","🔶","BNB","BNB Chain"),
            ("solana","◎","SOL","Solana"), ("ripple","✕","XRP","XRP Ledger"),
        ]
    )

    content = f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/?id={uid}" class="back-btn">←</a>
            <div><div class="header-title">My Profile</div><div class="header-sub">Account overview</div></div>
        </div>
        {ticker_html()}
        <div class="balance-card animate-in delay-1">
            <div class="balance-label">Main Balance</div>
            <div class="balance-amount">{max(0,user['balance']):.2f} <span class="balance-unit">USD</span></div>
        </div>
        <div class="stat-grid animate-in delay-2">
            <div class="stat-box stat-green"><div class="stat-icon">📈</div><div class="stat-val">{daily:.2f}</div><div class="stat-lbl">Daily Profit</div></div>
            <div class="stat-box stat-green"><div class="stat-icon">💰</div><div class="stat-val">{user['total_profit']:.2f}</div><div class="stat-lbl">Total Profit</div></div>
            <div class="stat-box stat-purple"><div class="stat-icon">🌟</div><div class="stat-val">{max(0,user['reward_balance']):.2f}</div><div class="stat-lbl">Reward Bal.</div></div>
            <div class="stat-box" style="border-color:rgba(245,158,11,0.3)"><div class="stat-icon">🏆</div><div class="stat-val" style="color:#fbbf24">VIP {user['vip_level']}</div><div class="stat-lbl">VIP Level</div></div>
        </div>
        <div class="card animate-in delay-2">
            <div class="section-title">Account Details</div>
            <div class="profile-info-row"><span class="profile-key">Name</span><span class="profile-val">{user['name'] or 'N/A'}</span></div>
            <div class="profile-info-row"><span class="profile-key">Email</span><span class="profile-val">{user['email'] or 'N/A'}</span></div>
            <div class="profile-info-row"><span class="profile-key">Phone</span><span class="profile-val">{(user['country_code'] or '') + ' ' + (user['phone'] or 'N/A')}</span></div>
            <div class="profile-info-row"><span class="profile-key">Daily Profit %</span><span class="profile-val">{user['daily_profit_percent']}%</span></div>
            <div class="profile-info-row"><span class="profile-key">User ID</span><span class="profile-val" style="font-size:0.75rem">{user['id']}</span></div>
        </div>
        <div class="section-title animate-in delay-3">Live Crypto Prices</div>
        <div class="card animate-in delay-3">{price_rows}</div>
    </div>"""
    
    return page(content, scripts=f"""
    <script>
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.nav-item')[1].classList.add('active');
    </script>
    """, uid=uid)


# ── Settings Page ──────────────────────────────────────────────────────────────

@home_bp.route("/settings")
def settings():
    uid = request.args.get("id")
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = c.fetchone(); conn.close()
    
    content = f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/?id={uid}" class="back-btn">←</a>
            <div><div class="header-title">Settings</div><div class="header-sub">Manage your preferences</div></div>
        </div>
        
        <div class="card animate-in delay-1">
            <div class="section-title">Account Settings</div>
            <div class="menu-row">
                <div class="row-icon">👤</div>
                <div class="row-text"><div class="row-title">Profile Information</div><div class="row-sub">View and edit your details</div></div>
                <div class="row-arrow">›</div>
            </div>
            <div class="menu-row">
                <div class="row-icon">🔐</div>
                <div class="row-text"><div class="row-title">Security</div><div class="row-sub">Manage security settings</div></div>
                <div class="row-arrow">›</div>
            </div>
        </div>
        
        <div class="card animate-in delay-2">
            <div class="section-title">Notifications</div>
            <div class="menu-row">
                <div class="row-icon">🔔</div>
                <div class="row-text"><div class="row-title">Push Notifications</div><div class="row-sub">Receive updates and alerts</div></div>
                <div class="row-arrow">›</div>
            </div>
            <div class="menu-row">
                <div class="row-icon">📧</div>
                <div class="row-text"><div class="row-title">Email Preferences</div><div class="row-sub">Manage email communications</div></div>
                <div class="row-arrow">›</div>
            </div>
        </div>
        
        <div class="card animate-in delay-3">
            <div class="section-title">About</div>
            <div class="menu-row">
                <div class="row-icon">ℹ️</div>
                <div class="row-text"><div class="row-title">About SMART SAVINGS</div><div class="row-sub">Version 1.0.0</div></div>
                <div class="row-arrow">›</div>
            </div>
            <div class="menu-row">
                <div class="row-icon">📋</div>
                <div class="row-text"><div class="row-title">Terms & Conditions</div><div class="row-sub">Read our terms</div></div>
                <div class="row-arrow">›</div>
            </div>
        </div>
        
        <a href="/?id={uid}" class="btn-ghost animate-in delay-4" style="margin-top:20px">Back to Home</a>
    </div>"""
    
    return page(content, scripts=f"""
    <script>
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.nav-item')[4].classList.add('active');
    </script>
    """, uid=uid)
