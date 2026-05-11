# PulseForge — Telegram Mini App

A **Flask-based Telegram Web App** for smart savings, crypto tracking, VIP rewards, deposits & withdrawals.

---

## 📁 Project Structure

```
pulseforge/
├── app.py                  # Flask entry point — run this
├── config.py               # All constants (Admin ID, wallets, VIP config)
├── helpers.py              # VIP logic, daily profit processing
├── requirements.txt        # Python dependencies
├── Procfile                # For Railway / Heroku
├── railway.json            # Railway deployment config
├── .gitignore
│
├── database/
│   ├── db.py               # DB connection + init_db()
│   └── users.db            # Auto-created on first run (not in git)
│
├── routes/
│   ├── home.py             # Home, registration, profile, messages
│   ├── deposit.py          # Deposit & withdraw flows
│   ├── support.py          # User support form
│   └── admin.py            # Admin panel + all admin actions
│
├── static/
│   ├── css/
│   │   └── main.css        # All styling
│   └── js/
│       └── crypto.js       # Live CoinGecko price fetcher
│
└── templates/
    └── base.html           # Shared HTML base (for future Jinja2 templates)
```

---

## ⚙️ Configuration (IMPORTANT — do this first!)

Open **`config.py`** and update these values:

```python
ADMIN_ID     = "YOUR_TELEGRAM_USER_ID"   # Get from @userinfobot on Telegram
BOT_USERNAME = "your_bot_username"        # Without the @

TRC_WALLET   = "Your TRC20 USDT wallet address"
ERC_WALLET   = "Your ERC20 USDT wallet address"
```

---

## 🚀 Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```
App starts at `http://localhost:8080`

> The SQLite database (`database/users.db`) is created automatically on first run.

---

## 🌐 Deploy on Railway (Recommended — Free)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pulseforge.git
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **"New Project" → "Deploy from GitHub repo"**
3. Select your `pulseforge` repo
4. Railway auto-detects `Procfile` and deploys ✅
5. Go to **Settings → Networking → Generate Domain** to get your public URL
6. Copy the URL (e.g. `https://pulseforge-xxxx.up.railway.app`)

### Step 3: Set your Telegram Bot Webhook URL
In your Telegram Bot settings (via [@BotFather](https://t.me/BotFather)):
- Go to the bot → **Menu Button → Set URL**
- Set it to your Railway URL: `https://pulseforge-xxxx.up.railway.app`

---

## 🌐 Deploy on Render (Alternative Free Hosting)

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Deploy → copy your `.onrender.com` URL

---

## 🌐 Deploy on VPS / Self-Hosted

```bash
# Install
git clone https://github.com/YOUR_USERNAME/pulseforge.git
cd pulseforge
pip install -r requirements.txt

# Run with gunicorn (production)
gunicorn app:app --bind 0.0.0.0:8080 --workers 2 --daemon

# Or use systemd / supervisor for auto-restart
```

Use **Nginx** as a reverse proxy in front of gunicorn for production.

---

## 🔐 Admin Panel

Access at: `https://your-domain.com/admin?id=YOUR_ADMIN_TELEGRAM_ID`

Features:
- View all users & balances
- Manage individual users (add/remove balance, set daily profit %)
- Approve / reject deposits & withdrawals
- Send messages & broadcast to all users
- Support inbox with reply

---

## 📊 Features

| Feature | Description |
|---------|-------------|
| 🔐 Registration | Users register via Telegram Mini App |
| 💰 Balance | Per-user USDT balance management |
| 📈 Daily Profit | Admin sets daily % profit per user |
| 🌟 VIP System | 7-tier VIP with automatic bonus rewards |
| 💳 Deposits | TRC20/ERC20 USDT with TXID verification |
| 💸 Withdrawals | User submits wallet + amount, admin processes |
| 📩 Messaging | Admin can message / broadcast to all users |
| 💬 Support | Users send support tickets, admin replies |
| 📊 Live Prices | Real-time CoinGecko crypto prices |

---

## ⚠️ Notes

- **Database:** SQLite is used. It's fine for Railway but resets on redeploy if you don't attach a persistent volume. For production, add a Railway PostgreSQL volume or use an external DB.
- **Security:** Admin routes check Telegram ID only — add a secret token check for production.
- **HTTPS required:** Telegram Mini Apps only work over HTTPS (Railway/Render provide this automatically).
