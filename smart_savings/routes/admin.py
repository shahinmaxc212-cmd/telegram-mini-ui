from flask import Blueprint, request
from database.db import get_db
from config import ADMIN_ID
from routes.home import page, ticker_html, result_page

admin_bp = Blueprint("admin", __name__)


def _admin_guard(uid: str) -> bool:
    return uid == ADMIN_ID


# ── Admin Panel ───────────────────────────────────────────────────────────────

@admin_bp.route("/admin")
def admin():
    uid = request.args.get("id")
    if not _admin_guard(uid):
        return page("""<div class="page"><div class="result-page">
            <div class="result-icon">🚫</div>
            <div class="result-title">Access Denied</div>
            <div class="result-sub">Admins only</div>
        </div></div>""")

    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id, username, first_name, balance FROM users")
    users = c.fetchall()
    c.execute("SELECT * FROM support")
    sup = c.fetchall()
    c.execute("SELECT COUNT(*) FROM deposits WHERE status='pending'")
    pending_dep = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM withdraws WHERE status='pending'")
    pending_wd = c.fetchone()[0]
    conn.close()

    badge_dep = f'<span class="badge">{pending_dep}</span>' if pending_dep > 0 else ""
    badge_wd  = f'<span class="badge">{pending_wd}</span>'  if pending_wd  > 0 else ""
    badge_sup = f'<span class="badge">{len(sup)}</span>'    if sup         else ""

    user_list_html = "".join(f"""
        <div class="user-item">
            <div class="user-item-info">
                <div class="u-name">@{u['username'] or u['first_name'] or u['id']}</div>
                <div class="u-bal">${u['balance']:.2f} USD</div>
            </div>
            <a href='/manage?uid={u["id"]}'>Manage</a>
        </div>""" for u in users)

    support_html = "".join(f"""
        <div class="card" style="margin-bottom:12px">
            <div style="font-size:0.75rem;color:var(--cyan);margin-bottom:6px">@{s['username']} — ID: {s['user_id']}</div>
            <div style="font-size:0.88rem;margin-bottom:12px">{s['msg']}</div>
            <form action="/reply_support" method="GET">
                <input type="hidden" name="uid" value="{s['user_id']}">
                <input name="reply" placeholder="Reply..." class="field">
                <button type="submit" class="btn-primary">Send Reply</button>
            </form>
        </div>""" for s in sup)

    return page(f"""
    <div class="page">
        <div class="app-logo animate-in">
            <div class="logo-icon">🔐</div>
            <div><div class="logo-text">Admin Panel</div><div class="logo-tag">SMART SAVINGS ADMIN</div></div>
        </div>
        <div class="admin-banner animate-in delay-1">🔴 ADMIN — Restricted Access</div>
        {ticker_html()}

        <div class="stat-grid animate-in delay-1">
            <div class="stat-box"><div class="stat-icon">👥</div><div class="stat-val">{len(users)}</div><div class="stat-lbl">Total Users</div></div>
            <div class="stat-box stat-green"><div class="stat-icon">💰</div><div class="stat-val">${sum(u['balance'] for u in users):.0f}</div><div class="stat-lbl">Total Funds</div></div>
        </div>

        <div class="section-title animate-in delay-2">Actions</div>
        <a href='/all_user_info' class='menu-row animate-in delay-2'>
            <div class="row-icon">👥</div>
            <div class="row-text"><div class="row-title">All User Info</div><div class="row-sub">Registered users detail</div></div>
            <div class="row-arrow">›</div>
        </a>
        <a href='/deposits' class='menu-row animate-in delay-2'>
            <div class="row-icon">💳</div>
            <div class="row-text"><div class="row-title">Pending Deposits</div><div class="row-sub">Review & approve</div></div>
            {badge_dep}<div class="row-arrow">›</div>
        </a>
        <a href='/withdraws' class='menu-row animate-in delay-2'>
            <div class="row-icon">💸</div>
            <div class="row-text"><div class="row-title">Pending Withdrawals</div><div class="row-sub">Review & process</div></div>
            {badge_wd}<div class="row-arrow">›</div>
        </a>
        <div onclick="openModal('supportModal')" class='menu-row animate-in delay-3' style="cursor:pointer">
            <div class="row-icon">💬</div>
            <div class="row-text"><div class="row-title">Support Inbox</div><div class="row-sub">User messages</div></div>
            {badge_sup}<div class="row-arrow">›</div>
        </div>

        <div class="card animate-in delay-3">
            <div class="section-title">📢 Broadcast Message</div>
            <form action="/broadcast" method="GET">
                <textarea name="m" rows="3" placeholder="Message to all users..." class="field"></textarea>
                <button type="submit" class="btn-primary">Send to All Users</button>
            </form>
        </div>

        <div class="card animate-in delay-4">
            <div class="section-title">All Users ({len(users)})</div>
            {user_list_html}
        </div>
    </div>

    <!-- Support Modal -->
    <div id="supportModal" class="modal-overlay">
        <div class="modal-box" onclick="event.stopPropagation()">
            <div class="modal-handle"></div>
            <div class="modal-title">💬 Support Inbox</div>
            <div class="modal-body">{support_html or '<div style="text-align:center;color:var(--muted);padding:32px 0">No support messages</div>'}</div>
        </div>
    </div>
    """, scripts="""
    <script>
    function openModal(id)  { document.getElementById(id).classList.add('open'); }
    function closeModal(id) { document.getElementById(id).classList.remove('open'); }
    document.querySelectorAll('.modal-overlay').forEach(el => el.addEventListener('click', () => el.classList.remove('open')));
    </script>""")


# ── Manage User ───────────────────────────────────────────────────────────────

@admin_bp.route("/manage")
def manage():
    uid = request.args.get("uid")
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = c.fetchone(); conn.close()
    name = (user["name"] or user["username"] or uid) if user else uid

    def _form(action, btn_class, label, field_name, field_type="number"):
        return f"""
        <form action="{action}" method="GET">
            <input type="hidden" name="uid" value="{uid}">
            <input name="{field_name}" type="{field_type}" placeholder="{label}" class="field"
                   {'step="0.01"' if field_type == "number" else ''}>
            <button type="submit" class="{btn_class}">{label}</button>
        </form>"""

    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/admin?id={ADMIN_ID}" class="back-btn">←</a>
            <div><div class="header-title">Manage User</div><div class="header-sub">{name}</div></div>
        </div>

        <div class="manage-section animate-in delay-1">
            <h4>💰 Main Balance</h4>
            {_form('/add', 'btn-green', '+ Add Balance', 'amount')}
            {_form('/remove', 'btn-red', '− Remove Balance', 'amount')}
        </div>

        <div class="manage-section animate-in delay-2">
            <h4>🌟 Reward Balance</h4>
            {_form('/add_reward', 'btn-primary', '+ Add Reward', 'amount')}
            {_form('/remove_reward', 'btn-red', '− Remove Reward', 'amount')}
        </div>

        <div class="manage-section animate-in delay-2">
            <h4>📈 Daily Profit Settings</h4>
            {_form('/set_daily_profit', 'btn-gold', 'Set Daily Profit %', 'percent')}
            {_form('/profit', 'btn-primary', 'Add One-Time Profit %', 'p')}
        </div>

        <div class="manage-section animate-in delay-3">
            <h4>📩 Send Message</h4>
            <form action="/msg" method="GET">
                <input type="hidden" name="uid" value="{uid}">
                <textarea name="m" rows="3" placeholder="Message to this user..." class="field"></textarea>
                <button type="submit" class="btn-primary">Send Message</button>
            </form>
        </div>
    </div>""")


# ── Admin Actions ─────────────────────────────────────────────────────────────

def _back_manage(uid, label):
    return result_page("✅", label, "", f"/manage?uid={uid}", "← Back to Manage")


@admin_bp.route("/set_daily_profit")
def set_daily_profit():
    uid     = request.args.get("uid")
    percent = float(request.args.get("percent", 0))
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET daily_profit_percent=? WHERE id=?", (percent, uid))
    conn.commit(); conn.close()
    return _back_manage(uid, f"Daily Profit {percent}% Set")


@admin_bp.route("/add")
def add():
    uid    = request.args.get("uid")
    amount = float(request.args.get("amount", 0))
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET balance=balance+? WHERE id=?", (amount, uid))
    conn.commit(); conn.close()
    return _back_manage(uid, f"${amount:.2f} Added")


@admin_bp.route("/remove")
def remove():
    uid    = request.args.get("uid")
    amount = float(request.args.get("amount", 0))
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET balance=balance-? WHERE id=?", (amount, uid))
    conn.commit(); conn.close()
    return _back_manage(uid, f"${amount:.2f} Removed")


@admin_bp.route("/add_reward")
def add_reward():
    uid    = request.args.get("uid")
    amount = float(request.args.get("amount", 0))
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET reward_balance=reward_balance+? WHERE id=?", (amount, uid))
    conn.commit(); conn.close()
    return _back_manage(uid, f"${amount:.2f} Reward Added")


@admin_bp.route("/remove_reward")
def remove_reward():
    uid    = request.args.get("uid")
    amount = float(request.args.get("amount", 0))
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET reward_balance=reward_balance-? WHERE id=?", (amount, uid))
    conn.commit(); conn.close()
    return _back_manage(uid, f"${amount:.2f} Reward Removed")


@admin_bp.route("/profit")
def profit():
    uid     = request.args.get("uid")
    percent = float(request.args.get("p", 0))
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET total_profit=total_profit+(balance*?/100) WHERE id=?", (percent, uid))
    conn.commit(); conn.close()
    return _back_manage(uid, f"{percent}% Profit Added")


@admin_bp.route("/msg")
def msg():
    uid     = request.args.get("uid")
    message = request.args.get("m", "")
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO messages VALUES(NULL,?,?)", (uid, message))
    conn.commit(); conn.close()
    return _back_manage(uid, "Message Sent")


@admin_bp.route("/broadcast")
def broadcast():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id FROM users")
    for u in c.fetchall():
        c.execute("INSERT INTO messages VALUES(NULL,?,?)", (u["id"], request.args.get("m")))
    conn.commit(); conn.close()
    return result_page("📢", "Broadcast Sent!", "", f"/admin?id={ADMIN_ID}", "← Back to Admin")


@admin_bp.route("/reply_support")
def reply_support():
    uid   = request.args.get("uid")
    reply = request.args.get("reply")
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO messages VALUES(NULL,?,?)", (uid, f"💬 Admin: {reply}"))
    conn.commit(); conn.close()
    return result_page("✅", "Reply Sent", "", f"/admin?id={ADMIN_ID}", "← Back to Admin")


# ── All User Info ─────────────────────────────────────────────────────────────

@admin_bp.route("/all_user_info")
def all_user_info():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id,name,email,phone,country_code,address,referral_code,balance FROM users WHERE registered=1")
    users = c.fetchall(); conn.close()
    cards = "".join(f"""
        <div class="card">
            <div class="section-title">User Info</div>
            <div class="profile-info-row"><span class="profile-key">ID</span><span class="profile-val" style="font-size:0.75rem">{u['id']}</span></div>
            <div class="profile-info-row"><span class="profile-key">Name</span><span class="profile-val">{u['name'] or 'N/A'}</span></div>
            <div class="profile-info-row"><span class="profile-key">Email</span><span class="profile-val">{u['email'] or 'N/A'}</span></div>
            <div class="profile-info-row"><span class="profile-key">Phone</span><span class="profile-val">{(u['country_code'] or '')+' '+(u['phone'] or 'N/A')}</span></div>
            <div class="profile-info-row"><span class="profile-key">Address</span><span class="profile-val" style="font-size:0.78rem">{u['address'] or 'N/A'}</span></div>
            <div class="profile-info-row"><span class="profile-key">Balance</span><span class="profile-val" style="color:var(--green)">${u['balance']:.2f}</span></div>
            <a href="/manage?uid={u['id']}" class="btn-ghost" style="margin-top:10px;font-size:0.82rem">Manage This User</a>
        </div>""" for u in users)
    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/admin?id={ADMIN_ID}" class="back-btn">←</a>
            <div><div class="header-title">All Users</div><div class="header-sub">{len(users)} registered</div></div>
        </div>
        {cards or '<div class="card" style="text-align:center;color:var(--muted);padding:32px">No registered users yet</div>'}
    </div>""")


# ── Deposits Admin ────────────────────────────────────────────────────────────

@admin_bp.route("/deposits")
def deposits():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id,user_id,amount,network,txid FROM deposits WHERE status='pending'")
    data = c.fetchall(); conn.close()
    items = "".join(f"""
        <div class="card">
            <div class="profile-info-row"><span class="profile-key">User ID</span><span class="profile-val" style="font-size:0.75rem">{d['user_id']}</span></div>
            <div class="profile-info-row"><span class="profile-key">Amount</span><span class="profile-val" style="color:var(--green)">${d['amount']:.2f}</span></div>
            <div class="profile-info-row"><span class="profile-key">Network</span><span class="profile-val">{d['network']}</span></div>
            <div class="profile-info-row"><span class="profile-key">TXID</span><span class="profile-val" style="font-size:0.7rem;word-break:break-all">{d['txid']}</span></div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px">
                <a href="/approve_dep?id={d['id']}" class="btn-green" style="margin:0">✅ Approve</a>
                <form action="/reject_dep" method="GET" style="margin:0">
                    <input type="hidden" name="id" value="{d['id']}">
                    <input name="reason" placeholder="Reason..." class="field" style="margin-bottom:6px;font-size:0.82rem">
                    <button type="submit" class="btn-red" style="margin:0">❌ Reject</button>
                </form>
            </div>
        </div>""" for d in data)
    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/admin?id={ADMIN_ID}" class="back-btn">←</a>
            <div><div class="header-title">Pending Deposits</div><div class="header-sub">{len(data)} requests</div></div>
        </div>
        {items or '<div class="card" style="text-align:center;color:var(--muted);padding:32px">No pending deposits</div>'}
    </div>""")


@admin_bp.route("/approve_dep")
def approve_dep():
    id_ = request.args.get("id")
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id, amount FROM deposits WHERE id=?", (id_,))
    d = c.fetchone()
    c.execute("UPDATE users SET balance=balance+? WHERE id=?", (d["amount"], d["user_id"]))
    c.execute("UPDATE deposits SET status='approved' WHERE id=?", (id_,))
    c.execute("INSERT INTO messages VALUES(NULL,?,?)", (d["user_id"], f"✅ Deposit of ${d['amount']:.2f} Approved!"))
    conn.commit(); conn.close()
    return result_page("✅", "Deposit Approved", "", f"/admin?id={ADMIN_ID}", "← Back to Admin")


@admin_bp.route("/reject_dep")
def reject_dep():
    id_    = request.args.get("id")
    reason = request.args.get("reason") or "No reason given"
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id FROM deposits WHERE id=?", (id_,))
    uid = c.fetchone()["user_id"]
    c.execute("UPDATE deposits SET status='rejected',reason=? WHERE id=?", (reason, id_))
    c.execute("INSERT INTO messages VALUES(NULL,?,?)", (uid, f"❌ Deposit Rejected: {reason}"))
    conn.commit(); conn.close()
    return result_page("❌", "Deposit Rejected", "", f"/admin?id={ADMIN_ID}", "← Back to Admin")


# ── Withdrawals Admin ─────────────────────────────────────────────────────────

@admin_bp.route("/withdraws")
def withdraws():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id,user_id,amount,address,network FROM withdraws WHERE status='pending'")
    data = c.fetchall(); conn.close()
    items = "".join(f"""
        <div class="card">
            <div class="profile-info-row"><span class="profile-key">User ID</span><span class="profile-val" style="font-size:0.75rem">{d['user_id']}</span></div>
            <div class="profile-info-row"><span class="profile-key">Amount</span><span class="profile-val" style="color:var(--red)">${d['amount']:.2f}</span></div>
            <div class="profile-info-row"><span class="profile-key">Network</span><span class="profile-val">{d['network']}</span></div>
            <div class="profile-info-row"><span class="profile-key">Address</span><span class="profile-val" style="font-size:0.7rem;word-break:break-all">{d['address']}</span></div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px">
                <a href="/approve_w?id={d['id']}" class="btn-green" style="margin:0">✅ Approve</a>
                <form action="/reject_w" method="GET" style="margin:0">
                    <input type="hidden" name="id" value="{d['id']}">
                    <input name="reason" placeholder="Reason..." class="field" style="margin-bottom:6px;font-size:0.82rem">
                    <button type="submit" class="btn-red" style="margin:0">❌ Reject</button>
                </form>
            </div>
        </div>""" for d in data)
    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/admin?id={ADMIN_ID}" class="back-btn">←</a>
            <div><div class="header-title">Pending Withdrawals</div><div class="header-sub">{len(data)} requests</div></div>
        </div>
        {items or '<div class="card" style="text-align:center;color:var(--muted);padding:32px">No pending withdrawals</div>'}
    </div>""")


@admin_bp.route("/approve_w")
def approve_w():
    id_ = request.args.get("id")
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id, amount FROM withdraws WHERE id=?", (id_,))
    w = c.fetchone()
    c.execute("UPDATE users SET balance=balance-? WHERE id=?", (w["amount"], w["user_id"]))
    c.execute("UPDATE withdraws SET status='approved' WHERE id=?", (id_,))
    c.execute("INSERT INTO messages VALUES(NULL,?,?)", (w["user_id"], f"✅ Withdrawal of ${w['amount']:.2f} Approved!"))
    conn.commit(); conn.close()
    return result_page("✅", "Withdrawal Approved", "", f"/admin?id={ADMIN_ID}", "← Back to Admin")


@admin_bp.route("/reject_w")
def reject_w():
    id_    = request.args.get("id")
    reason = request.args.get("reason") or "No reason given"
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT user_id FROM withdraws WHERE id=?", (id_,))
    uid = c.fetchone()["user_id"]
    c.execute("UPDATE withdraws SET status='rejected',reason=? WHERE id=?", (reason, id_))
    c.execute("INSERT INTO messages VALUES(NULL,?,?)", (uid, f"❌ Withdrawal Rejected: {reason}"))
    conn.commit(); conn.close()
    return result_page("❌", "Withdrawal Rejected", "", f"/admin?id={ADMIN_ID}", "← Back to Admin")
