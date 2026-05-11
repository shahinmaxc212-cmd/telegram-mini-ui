from flask import Blueprint, request
from database.db import get_db
from routes.home import page, result_page

support_bp = Blueprint("support", __name__)


@support_bp.route("/support")
def support():
    uid      = request.args.get("id")
    username = request.args.get("username") or "unknown"
    return page(f"""
    <div class="page">
        <div class="page-header animate-in">
            <a href="/?id={uid}" class="back-btn">←</a>
            <div><div class="header-title">Support</div><div class="header-sub">We reply within 24 hours</div></div>
        </div>
        <div class="card animate-in delay-1">
            <form action="/send_support" method="GET">
                <input type="hidden" name="uid" value="{uid}">
                <input type="hidden" name="username" value="{username}">
                <label class="field-label">Your Message</label>
                <textarea name="msg" rows="6" placeholder="Describe your issue or question..." class="field"></textarea>
                <button type="submit" class="btn-primary">Send Message →</button>
            </form>
        </div>
    </div>""", uid=uid)


@support_bp.route("/send_support")
def send_support():
    uid      = request.args.get("uid")
    username = request.args.get("username") or "unknown"
    msg      = request.args.get("msg")
    conn = get_db(); c = conn.cursor()
    c.execute("INSERT INTO support VALUES(NULL,?,?,?,?)", (uid, username, "user", msg))
    conn.commit(); conn.close()
    return result_page("✅", "Message Sent!", "We'll get back to you soon", f"/?id={uid}", "← Back to Home")
