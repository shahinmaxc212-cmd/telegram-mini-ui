# SMART SAVINGS - Premium Telegram Mini App Setup Guide

Welcome to **SMART SAVINGS**, a premium earnings platform built on Telegram. This guide will help you set up and run the application.

## 📋 What's New in This Version

✅ **Bottom Navigation Bar** - Easy access to Home, Profile, Deposit, Withdraw, and Settings  
✅ **SMART SAVINGS Branding** - Complete rebrand from PulseForge to SMART SAVINGS  
✅ **Premium Animations** - Smooth transitions, hover effects, and micro-interactions  
✅ **Enhanced UI** - High-level design with glassmorphism effects and gradient buttons  
✅ **Mobile Optimized** - Perfect display on Android, iOS, and all Telegram clients  

## 🚀 Quick Start

### Option 1: Local Development (Recommended for Testing)

#### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git (optional)

#### Installation Steps

1. **Extract the project**
   ```bash
   unzip smart_savings.zip
   cd smart_savings
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

   The app will start on `http://localhost:8080`

5. **Access via Telegram**
   - Open your Telegram bot
   - The app will open in a mini app window
   - Telegram will automatically detect the local URL

### Option 2: Deploy to Railway (Recommended for Production)

Railway is a modern platform for deploying Python applications. It's free to start and very easy to use.

#### Steps

1. **Create a Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub or email

2. **Connect Your Repository**
   - Create a new project
   - Select "Deploy from GitHub"
   - Connect your repository containing this code

3. **Configure Environment**
   - Railway will automatically detect the Python project
   - It will use the `Procfile` and `requirements.txt` files
   - No additional configuration needed

4. **Deploy**
   - Click "Deploy"
   - Railway will build and start your app automatically
   - You'll get a public URL like `https://smart-savings-prod.railway.app`

5. **Update Your Telegram Bot**
   - Go to your bot settings in BotFather
   - Set the Mini App URL to your Railway URL
   - Example: `https://smart-savings-prod.railway.app/?id={user_id}`

### Option 3: Deploy to Render (Alternative)

Render is another excellent free hosting option.

#### Steps

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create a New Web Service**
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository

3. **Configure**
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Deploy**
   - Click "Create Web Service"
   - Render will deploy your app
   - Get your public URL

5. **Update Telegram Bot Settings**
   - Set Mini App URL to your Render URL

### Option 4: Deploy to Heroku (Legacy)

Heroku still works but requires a credit card. Use Railway or Render instead.

## 🔧 Configuration

### Important Files to Customize

**`config.py`** - Main configuration file
```python
ADMIN_ID = "YOUR_TELEGRAM_ID"  # Your Telegram user ID (admin)
BOT_USERNAME = "your_bot_username"  # Your bot's username
TRC_WALLET = "your_trc20_wallet_address"  # USDT TRC20 wallet
ERC_WALLET = "your_erc20_wallet_address"  # USDT ERC20 wallet
```

**`requirements.txt`** - Python dependencies (already configured)

**`Procfile`** - Deployment configuration (already configured)

## 📱 Features

### User Features
- **Dashboard** - View balance, daily profit, and VIP level
- **Live Market** - Real-time crypto prices (BTC, ETH, USDT, BNB, SOL, XRP)
- **Deposit** - Deposit via TRC20 or ERC20 networks
- **Withdraw** - Withdraw to your wallet
- **Profile** - View account details and crypto prices
- **VIP Program** - Earn rewards based on balance
- **Messages** - Receive notifications from admin
- **Support** - Contact support team
- **Settings** - Manage preferences

### Admin Features
- **User Management** - View and manage all users
- **Balance Control** - Add/remove balance and rewards
- **Deposit Verification** - Approve or reject deposits
- **Withdrawal Processing** - Process user withdrawals
- **Broadcasting** - Send messages to all users
- **Support Inbox** - Reply to user support messages

## 🗄️ Database

The app uses SQLite for data storage. The database file is automatically created on first run.

**Database file:** `smart_savings.db`

Tables:
- `users` - User accounts and balances
- `messages` - Admin messages to users
- `support` - Support tickets
- `deposits` - Deposit transactions
- `withdraws` - Withdrawal transactions

## 🔐 Security Notes

⚠️ **Important Security Considerations:**

1. **HTTPS Required** - Always use HTTPS in production (Railway/Render handle this automatically)
2. **Admin ID** - Keep your admin ID secret in `config.py`
3. **Wallet Addresses** - Use dedicated wallets for this app
4. **Database Backup** - Regularly backup your SQLite database
5. **Environment Variables** - In production, use environment variables instead of hardcoding secrets

## 🎨 Customization

### Colors and Styling

Edit `static/css/main.css` to customize:
- Primary color: `--purple: #6366f1`
- Accent color: `--cyan: #06b6d4`
- Success color: `--green: #10b981`
- Warning color: `--gold: #f59e0b`
- Error color: `--red: #ef4444`

### Branding

Edit `routes/home.py` to change:
- App name: "SMART SAVINGS"
- App tagline: "PREMIUM EARNINGS"
- Logo emoji: 💰

## 🐛 Troubleshooting

### App won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run with debug mode
python app.py --debug
```

### Database errors
```bash
# Reset database
rm smart_savings.db
python app.py
```

### Port already in use
```bash
# Use a different port
python app.py --port 8081
```

### Telegram Mini App not loading
- Ensure the URL is HTTPS (for production)
- Check that the bot's Mini App URL is correctly set
- Verify the URL format: `https://your-domain.com/?id={user_id}`

## 📊 Monitoring

### Check Logs
```bash
# View application logs
tail -f app.log

# Check for errors
grep ERROR app.log
```

### Database Queries
```bash
# Access SQLite database
sqlite3 smart_savings.db

# View users
SELECT * FROM users;

# View pending deposits
SELECT * FROM deposits WHERE status='pending';
```

## 🚀 Performance Tips

1. **Use Production Server** - Don't use Flask's development server in production
2. **Enable Caching** - Add caching headers for static files
3. **Database Optimization** - Add indexes for frequently queried columns
4. **Monitor Resources** - Watch CPU and memory usage

## 📞 Support

For issues or questions:
1. Check this guide
2. Review the code comments
3. Check the logs for error messages
4. Verify all configuration is correct

## 📝 License

This project is provided as-is for educational and commercial use.

## 🎯 Next Steps

1. **Customize Configuration** - Update `config.py` with your details
2. **Test Locally** - Run the app locally first
3. **Deploy to Production** - Use Railway or Render
4. **Update Telegram Bot** - Set the Mini App URL
5. **Monitor** - Keep an eye on logs and user feedback

---

**Happy Earning! 🎉**

For more information, visit the Telegram Bot API documentation: https://core.telegram.org/bots/webapps
