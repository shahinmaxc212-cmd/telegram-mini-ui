# SMART SAVINGS - Quick Start Guide

## 🎯 5-Minute Setup

### Step 1: Extract and Install
```bash
unzip smart_savings.zip
cd smart_savings
pip install -r requirements.txt
```

### Step 2: Configure
Edit `config.py` and update:
```python
ADMIN_ID = "YOUR_TELEGRAM_ID"
BOT_USERNAME = "your_bot_username"
TRC_WALLET = "your_trc20_address"
ERC_WALLET = "your_erc20_address"
```

### Step 3: Run Locally
```bash
python app.py
```
App runs on `http://localhost:8080`

### Step 4: Deploy to Railway (Recommended)
1. Push code to GitHub
2. Go to https://railway.app
3. Create new project → Deploy from GitHub
4. Select your repository
5. Railway auto-deploys! 🚀

### Step 5: Update Telegram Bot
In BotFather, set Mini App URL to:
```
https://your-railway-url.railway.app/?id={user_id}
```

## 📱 Features at a Glance

| Feature | Description |
|---------|-------------|
| 🏠 Home | Dashboard with balance & stats |
| 👤 Profile | Account details & crypto prices |
| 💳 Deposit | Fund account via TRC20/ERC20 |
| 💸 Withdraw | Withdraw to your wallet |
| ⚙️ Settings | Manage preferences |
| 📊 Live Market | Real-time crypto prices |
| 🌟 VIP Program | Earn rewards by balance |
| 💬 Support | Contact support team |

## 🔧 Key Files

```
smart_savings/
├── app.py                 # Main Flask app
├── config.py              # Configuration (EDIT THIS!)
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment config
├── routes/
│   ├── home.py           # Home, profile, settings
│   ├── deposit.py        # Deposit & withdraw
│   ├── support.py        # Support tickets
│   └── admin.py          # Admin panel
├── database/
│   └── db.py             # Database setup
├── static/
│   ├── css/main.css      # Styling (customize colors here)
│   └── js/crypto.js      # Live price updates
└── templates/
    └── base.html         # Base template
```

## 🎨 Customize Colors

Edit `static/css/main.css`:
```css
:root {
    --purple: #6366f1;  /* Primary color */
    --cyan: #06b6d4;    /* Accent color */
    --green: #10b981;   /* Success */
    --gold: #f59e0b;    /* Warning */
    --red: #ef4444;     /* Error */
}
```

## 🚀 Deployment Options

### Railway (Recommended - Free)
- Easiest setup
- Auto-deploys from GitHub
- Free tier available
- https://railway.app

### Render (Alternative - Free)
- Also free tier
- Good performance
- https://render.com

### Heroku (Legacy)
- Requires credit card
- Still works but not recommended

## 🔐 Important Security

1. Keep `ADMIN_ID` secret
2. Use dedicated wallets
3. Always use HTTPS in production
4. Backup database regularly
5. Never commit secrets to GitHub

## 📊 Admin Access

To access admin panel:
1. Set your Telegram ID as `ADMIN_ID` in `config.py`
2. Open the app
3. You'll see admin panel link
4. Manage users, deposits, withdrawals

## 🐛 Common Issues

**Port already in use:**
```bash
python app.py --port 8081
```

**Database error:**
```bash
rm smart_savings.db
python app.py
```

**Module not found:**
```bash
pip install -r requirements.txt --force-reinstall
```

## 📞 Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Review code comments
3. Check logs for errors
4. Verify `config.py` is correct

## ✨ What's Included

✅ Bottom navigation bar (Home, Profile, Deposit, Withdraw, Settings)
✅ SMART SAVINGS branding
✅ Premium animations & effects
✅ Glassmorphism UI design
✅ Live crypto prices
✅ VIP system
✅ Admin panel
✅ Mobile optimized
✅ Ready to deploy

---

**You're all set! Deploy to Railway and start earning! 🎉**
