from flask import Blueprint, request
from database.db import get_db
from config import TRC_WALLET, ERC_WALLET
from routes.home import page, ticker_html, result_page

deposit_bp = Blueprint("deposit", __name__)


# ── Deposit ───────────────────────────────────────────────────────────────────

@deposit_bp.route("/deposit")
def deposit():
    uid = request.args.get("id")
    mini_rates = "".join(
        f'<div class="price-row"><div class="price-coin"><span class="price-icon">{icon}</span>'
        f'<div><div class="price-name">{sym}</div></div></div>'
        f'<div class="price-right"><div class="price-usd" data-coin-price="{cid}">--</div>'
        f'<div class="price-chg pos" data-coin-chg="{cid}">--</div></div></div>'
        for cid, icon, sym in [("tether","₮","USDT"), ("ethereum","Ξ","ETH"), ("bitcoin","₿","BTC")]
    )
    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/?id={uid}" class="back-btn">←</a>
            <div><div class="header-title">Deposit Funds</div><div class="header-sub">USDT via TRC20 or ERC20</div></div>
        </div>
        {ticker_html()}
        <div class="card animate-in delay-1">
            <form action="/dep2" method="GET">
                <input type="hidden" name="uid" value="{uid}">
                <label class="field-label">Amount (USD)</label>
                <input name="amount" type="number" min="1" placeholder="0.00" class="field">
                <label class="field-label">Network</label>
                <select name="network" class="field">
                    <option>TRC20 (USDT)</option>
                    <option>ERC20 (USDT)</option>
                </select>
                <button type="submit" class="btn-green">Continue →</button>
            </form>
        </div>
        <div class="card animate-in delay-2">
            <div class="section-title">Live Rates</div>
            {mini_rates}
        </div>
    </div>""", uid=uid)


@deposit_bp.route("/dep2")
def dep2():
    uid    = request.args.get("uid")
    net    = request.args.get("network")
    amount = request.args.get("amount")
    addr   = TRC_WALLET if "TRC20" in net else ERC_WALLET
    label  = "TRC20 (USDT)" if "TRC20" in net else "ERC20 (USDT/ETH)"

    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/deposit?id={uid}" class="back-btn">←</a>
            <div><div class="header-title">Send Payment</div><div class="header-sub">{label}</div></div>
        </div>
        <div class="card animate-in delay-1" style="text-align:center">
            <div style="font-size:2.5rem;margin-bottom:8px">💳</div>
            <div style="font-size:1.5rem;font-weight:800;color:#10b981">${amount} USD</div>
            <div style="font-size:0.8rem;color:var(--muted);margin-top:4px">Send exactly this amount</div>
        </div>
        <div class="card animate-in delay-1">
            <div class="wallet-label">SEND TO THIS ADDRESS ({net})</div>
            <div class="wallet-box">{addr}</div>
            <button onclick="copyAddr()" class="btn-ghost" id="copyBtn">📋 Copy Address</button>
        </div>
        <div class="card animate-in delay-2">
            <form action="/dep3" method="GET">
                <input type="hidden" name="uid" value="{uid}">
                <input type="hidden" name="amount" value="{amount}">
                <input type="hidden" name="network" value="{net}">
                <label class="field-label">Transaction ID (TXID)</label>
                <input name="txid" placeholder="Paste your transaction hash here" class="field">
                <button type="submit" class="btn-primary">Submit Deposit →</button>
            </form>
        </div>
    </div>""",
    scripts=f"""
    <script>
    function copyAddr() {{
        navigator.clipboard.writeText('{addr}');
        document.getElementById('copyBtn').textContent = '✅ Copied!';
        setTimeout(() => document.getElementById('copyBtn').textContent = '📋 Copy Address', 2000);
    }}
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.nav-item')[2].classList.add('active');
    </script>""", uid=uid)


@deposit_bp.route("/dep3")
def dep3():
    uid = request.args.get("uid")
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO deposits VALUES(NULL,?,?,?,?,?,?)",
              (uid, float(request.args.get("amount")), request.args.get("network"),
               request.args.get("txid"), "pending", ""))
    conn.commit(); conn.close()
    return result_page("⏳", "Deposit Submitted!", "Admin will verify within 24 hours. Check messages for updates.", f"/?id={uid}", "← Back to Home")


# ── Withdraw ──────────────────────────────────────────────────────────────────

@deposit_bp.route("/withdraw")
def withdraw():
    uid = request.args.get("id")
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE id=?", (uid,))
    user = c.fetchone(); conn.close()
    bal = max(0, user["balance"]) if user else 0

    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/?id={uid}" class="back-btn">←</a>
            <div><div class="header-title">Withdraw Funds</div><div class="header-sub">Available: ${bal:.2f} USD</div></div>
        </div>
        {ticker_html()}
        <div class="card animate-in delay-1">
            <form action="/w2" method="GET">
                <input type="hidden" name="uid" value="{uid}">
                <label class="field-label">Amount (USD)</label>
                <input name="amount" type="number" min="1" placeholder="0.00" class="field">
                <label class="field-label">Wallet Address</label>
                <input name="address" placeholder="Your wallet address" class="field">
                <label class="field-label">Network</label>
                <select name="network" class="field">
                    <option>TRC20 (USDT)</option>
                    <option>ERC20 (USDT/ETH)</option>
                </select>
                <button type="submit" class="btn-red">Submit Withdrawal →</button>
            </form>
        </div>
    </div>""", scripts=f"""
    <script>
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.nav-item')[3].classList.add('active');
    </script>""", uid=uid)


@deposit_bp.route("/w2")
def w2():
    uid = request.args.get("uid")
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO withdraws VALUES(NULL,?,?,?,?,?,?)",
              (uid, float(request.args.get("amount")), request.args.get("address"),
               request.args.get("network"), "pending", ""))
    conn.commit(); conn.close()
    return result_page("⏳", "Withdrawal Submitted!", "Processing within 24 hours. Check messages for updates.", f"/?id={uid}", "← Back to Home")
