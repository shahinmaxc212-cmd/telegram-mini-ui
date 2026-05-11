# 💰 SMART SAVINGS - Premium Telegram Mini App

A modern, high-performance Telegram Mini App for cryptocurrency earnings and portfolio management. Built with Flask, featuring a premium UI with glassmorphism effects, bottom navigation, and real-time crypto prices.

## ✨ Features

### User Dashboard
- 📊 Real-time balance and profit tracking
- 📈 Daily profit calculations
- 🌟 VIP level system with rewards
- 💬 Admin notifications and messages
- 🎯 Quick action buttons (Deposit/Withdraw)

### Navigation
- 🏠 **Home** - Dashboard with balance and stats
- 👤 **Profile** - Account details and crypto prices
- 💳 **Deposit** - Fund account via TRC20/ERC20
- 💸 **Withdraw** - Withdraw to wallet
- ⚙️ **Settings** - Preferences and account management

### Crypto Integration
- 📊 Live market data (BTC, ETH, USDT, BNB, SOL, XRP)
- 💱 Real-time price updates every 30 seconds
- 📈 Price change indicators
- 🔄 Automatic ticker scrolling

### Admin Panel
- 👥 User management
- 💰 Balance control
- 📋 Deposit verification
- 💸 Withdrawal processing
- 📢 Broadcasting messages
- 💬 Support ticket management

### Design
- ✨ Premium glassmorphism UI
- 🎨 Smooth animations and transitions
- 📱 Mobile-first responsive design
- 🌙 Dark theme optimized for Telegram
- ⚡ Fast and lightweight

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Access at http://localhost:8080
```

### Deploy to Railway (Recommended)
1. Push to GitHub
2. Go to https://railway.app
3. Create new project from GitHub repo
4. Railway auto-deploys!

### Deploy to Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

## 🔧 Configuration

Edit `config.py`:
```python
ADMIN_ID = "YOUR_TELEGRAM_ID"           # Your admin ID
BOT_USERNAME = "your_bot_username"      # Bot username
TRC_WALLET = "your_trc20_address"       # USDT TRC20 wallet
ERC_WALLET = "your_erc20_address"       # USDT ERC20 wallet
```

## 📁 Project Structure

```
smart_savings/
├── app.py                      # Main Flask application
├── config.py                   # Configuration (edit this!)
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment config
├── smart_savings.db            # SQLite database (auto-created)
├── routes/
│   ├── home.py                # Home, profile, settings pages
│   ├── deposit.py             # Deposit and withdraw routes
│   ├── support.py             # Support ticket system
│   └── admin.py               # Admin panel
├── database/
│   ├── __init__.py
│   └── db.py                  # Database initialization
├── static/
│   ├── css/
│   │   └── main.css           # Main stylesheet (customize here!)
│   └── js/
│       └── crypto.js          # Live price updates
├── templates/
│   └── base.html              # Base HTML template
├── helpers.py                 # Utility functions
├── SETUP_GUIDE.md             # Detailed setup guide
├── QUICK_START.md             # Quick start guide
└── README_ENHANCED.md         # This file
```

## 🎨 Customization

### Change Colors
Edit `static/css/main.css`:
```css
:root {
    --purple: #6366f1;      /* Primary */
    --cyan: #06b6d4;        /* Accent */
    --green: #10b981;       /* Success */
    --gold: #f59e0b;        /* Warning */
    --red: #ef4444;         /* Error */
}
```

### Change Branding
Edit `routes/home.py`:
- App name: "SMART SAVINGS"
- App tagline: "PREMIUM EARNINGS"
- Logo emoji: 💰

### Change Fonts
Edit `static/css/main.css`:
```css
--font: 'Syne', sans-serif;           /* UI font */
--mono: 'JetBrains Mono', monospace;  /* Data font */
```

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    type TEXT,
    username TEXT,
    first_name TEXT,
    name TEXT,
    email TEXT,
    country_code TEXT,
    phone TEXT,
    address TEXT,
    referral_code TEXT,
    registered INTEGER,
    balance REAL,
    total_profit REAL,
    daily_profit_percent REAL,
    reward_balance REAL,
    reward_timestamp TEXT,
    vip_level INTEGER,
    last_daily_profit_timestamp TEXT
);
```

### Deposits Table
```sql
CREATE TABLE deposits (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    network TEXT,
    txid TEXT,
    status TEXT,
    notes TEXT
);
```

### Withdrawals Table
```sql
CREATE TABLE withdraws (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    address TEXT,
    network TEXT,
    status TEXT,
    notes TEXT
);
```

## 🔐 Security

- ✅ Telegram user verification
- ✅ Admin ID protection
- ✅ HTTPS required in production
- ✅ SQLite database with proper queries
- ✅ CSRF protection via Telegram SDK
- ⚠️ Always use environment variables for secrets

## 📱 Supported Platforms

- ✅ Telegram Web App (Desktop)
- ✅ Telegram iOS App
- ✅ Telegram Android App
- ✅ All modern browsers
- ✅ Mobile-optimized

## 🌐 Deployment Platforms

| Platform | Cost | Setup Time | Recommendation |
|----------|------|-----------|-----------------|
| Railway | Free | 5 min | ⭐ Recommended |
| Render | Free | 10 min | ⭐ Good |
| Heroku | Paid | 10 min | ⚠️ Legacy |
| VPS | Varies | 30 min | For experts |

## 📈 Performance

- ⚡ Fast page loads (<1s)
- 📊 Real-time price updates
- 🔄 Efficient database queries
- 💾 Minimal memory footprint
- 🚀 Scales to thousands of users

## 🐛 Troubleshooting

### App won't start
```bash
# Check Python version (3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
lsof -i :8080
```

### Database issues
```bash
# Reset database
rm smart_savings.db
python app.py
```

### Telegram Mini App not loading
- Verify HTTPS in production
- Check Mini App URL format
- Ensure bot is properly configured

## 📞 Support

For issues:
1. Check `SETUP_GUIDE.md`
2. Review code comments
3. Check application logs
4. Verify configuration

## 🎯 What's New

### Version 1.0.0
- ✨ Bottom navigation bar
- 🎨 SMART SAVINGS branding
- ✨ Premium animations
- 🌟 Glassmorphism UI
- 📱 Mobile optimized
- 🔄 Real-time updates
- 👥 Admin panel
- 💰 VIP system

## 📝 License

This project is provided as-is for educational and commercial use.

## 🙏 Credits

- Built with Flask
- Telegram Bot API
- CoinGecko API for crypto prices
- Modern CSS with animations

## 🚀 Next Steps

1. **Configure** - Update `config.py`
2. **Test** - Run locally
3. **Deploy** - Push to Railway/Render
4. **Monitor** - Watch logs and metrics
5. **Grow** - Add users and features

---

**Ready to launch? Deploy to Railway in 5 minutes! 🚀**

For detailed setup instructions, see `SETUP_GUIDE.md` or `QUICK_START.md`
