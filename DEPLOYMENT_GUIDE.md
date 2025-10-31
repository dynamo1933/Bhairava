# 🚀 Free Hosting Deployment Guide

This guide will help you deploy your Flask application to free hosting platforms.

## 📋 Table of Contents

1. [Best Free Hosting Options](#best-free-hosting-options)
2. [Prerequisites](#prerequisites)
3. [Environment Variables Setup](#environment-variables-setup)
4. [Deploy to Render](#deploy-to-render)
5. [Deploy to Railway](#deploy-to-railway)
6. [Deploy to PythonAnywhere](#deploy-to-pythonanywhere)
7. [Deploy to Fly.io](#deploy-to-flyio)
8. [Post-Deployment Checklist](#post-deployment-checklist)
9. [Troubleshooting](#troubleshooting)

---

## Best Free Hosting Options

### 🏆 Recommended (Easiest & Most Reliable)

1. **Render.com** ⭐ (Best for beginners)
   - Free tier: Web service + PostgreSQL
   - Easy setup with GitHub integration
   - Automatic SSL certificates
   - 750 hours/month free

2. **Railway.app** ⭐ (Great for quick deployment)
   - Free tier: $5 credit/month
   - Simple deployment from GitHub
   - Built-in PostgreSQL
   - Excellent documentation

### 🔧 Alternative Options

3. **PythonAnywhere**
   - Free tier: Limited to 1 web app
   - Requires manual setup
   - Good for learning

4. **Fly.io**
   - Free tier: 3 shared VMs
   - More complex setup
   - Good for scaling

---

## Prerequisites

Before deploying, make sure you have:

1. ✅ A GitHub account
2. ✅ Your code pushed to a GitHub repository
3. ✅ Your Supabase PostgreSQL database ready
4. ✅ Google Sheets credentials (if using Google Sheets integration)

---

## Environment Variables Setup

Your application needs these environment variables. Set them in your hosting platform's dashboard:

### Required Variables

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=production
PORT=5000

# Database (Supabase PostgreSQL)
SQLALCHEMY_DATABASE_URI=postgresql://postgres.cuyilngsmocyhadlbrgv:_Bottlemepani%4035@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres

# Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Google Sheets (Optional)
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
```

### Generating a Secret Key

Run this in Python to generate a secure secret key:

```python
import secrets
print(secrets.token_hex(32))
```

---

## Deploy to Render

### Step 1: Prepare Your Repository

1. Push your code to GitHub
2. Make sure these files exist:
   - `Procfile`
   - `requirements.txt`
   - `runtime.txt`

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"

### Step 3: Connect Repository

1. Connect your GitHub repository
2. Render will auto-detect it's a Python app

### Step 4: Configure Settings

**Basic Settings:**
- **Name**: `daiva-anughara` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main` or `master`
- **Root Directory**: Leave empty (or `./` if needed)
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Environment Variables:**
Add all variables from the [Environment Variables Setup](#environment-variables-setup) section.

### Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

### Step 6: Free Tier Limitations

- ⚠️ Apps spin down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes ~30 seconds
- ⚠️ 750 hours/month free (enough for always-on small apps)

---

## Deploy to Railway

### Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. You'll get $5 free credit/month

### Step 2: Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

### Step 3: Configure Environment

1. Railway will auto-detect Python
2. Add environment variables:
   - Go to "Variables" tab
   - Add all variables from [Environment Variables Setup](#environment-variables-setup)

### Step 4: Deploy

1. Railway will automatically deploy
2. It will assign a URL like: `https://your-app.railway.app`
3. To use a custom domain, add it in "Settings"

### Step 5: Add PostgreSQL (Optional)

If you want Railway's PostgreSQL instead of Supabase:

1. Click "+ New" → "Database" → "Add PostgreSQL"
2. Railway will create a new PostgreSQL instance
3. Use the connection string from Railway as `SQLALCHEMY_DATABASE_URI`

---

## Deploy to PythonAnywhere

### Step 1: Create Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Log into your dashboard

### Step 2: Upload Your Code

**Option A: From GitHub**
1. Go to "Files" tab
2. Click "Bash console"
3. Clone your repo:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   ```

**Option B: Upload files**
1. Use the web interface to upload files
2. Or use their API

### Step 3: Create Virtual Environment

In the Bash console:
```bash
cd your-repo-name
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10

### Step 5: Update WSGI File

Edit the WSGI file (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import sys
import os

# Add your project directory to path
path = '/home/yourusername/your-repo-name'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
# ... add other variables

# Import your app
from app import app as application
```

### Step 6: Reload Web App

1. Go to "Web" tab
2. Click "Reload" button
3. Your app will be live at: `https://yourusername.pythonanywhere.com`

---

## Deploy to Fly.io

### Step 1: Install Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login

```bash
fly auth login
```

### Step 3: Create Fly App

```bash
fly launch
```

This will:
- Detect your app
- Ask for app name
- Create `fly.toml` config file

### Step 4: Configure fly.toml

Edit `fly.toml`:

```toml
app = "your-app-name"
primary_region = "sin"  # Singapore (closest to Supabase region)

[build]

[env]
  PORT = "8080"
  FLASK_ENV = "production"
  # Add other env vars or set in dashboard

[[services]]
  internal_port = 8080
  protocol = "tcp"
  
  [[services.ports]]
    handlers = ["http"]
    port = 80
    force_https = true
  
  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

### Step 5: Set Secrets

```bash
fly secrets set SECRET_KEY=your-secret-key
fly secrets set SQLALCHEMY_DATABASE_URI=your-database-uri
# ... set other secrets
```

### Step 6: Deploy

```bash
fly deploy
```

Your app will be live at: `https://your-app-name.fly.dev`

---

## Post-Deployment Checklist

After deploying, verify:

- [ ] App loads without errors
- [ ] Database connection works
- [ ] User registration/login works
- [ ] Admin panel accessible
- [ ] Static files load correctly
- [ ] Forms submit successfully
- [ ] Google Sheets integration (if used) works
- [ ] SSL certificate is active (HTTPS)
- [ ] Custom domain configured (if applicable)

---

## Troubleshooting

### App Crashes on Startup

**Check logs:**
- Render: Dashboard → Your service → Logs
- Railway: Deployments tab → View logs
- PythonAnywhere: Web tab → Error log

**Common issues:**
- Missing environment variables
- Database connection string incorrect
- Python version mismatch
- Missing dependencies

### Database Connection Errors

1. Verify your Supabase connection string
2. Check if Supabase allows connections from hosting IP
3. Ensure password is URL-encoded (especially `@` → `%40`)
4. Test connection locally first

### psycopg2 Python 3.13 Compatibility Error

**Error:** `ImportError: undefined symbol: _PyInterpreterState_Get`

This error occurs when `psycopg2-binary` is used with Python 3.13, which is incompatible.

**Solution 1: Use Python 3.12 (Recommended)**
- Ensure `runtime.txt` specifies: `python-3.12.8`
- Railway should respect this file

**Solution 2: Switch to psycopg (psycopg3)**

If Railway still uses Python 3.13, switch to the modern `psycopg` driver:

1. Update `requirements.txt`:
   - Replace `psycopg2-binary==2.9.9` with `psycopg[binary]==3.2.0`

2. Update `app.py` connection string:
   - Change `postgresql://` to `postgresql+psycopg://` in `SQLALCHEMY_DATABASE_URI`

Example:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'SQLALCHEMY_DATABASE_URI',
    'postgresql+psycopg://postgres.cuyilngsmocyhadlbrgv:_Bottlemepani%4035@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres'
)
```

**Solution 3: Force Python Version in Railway**

In Railway dashboard:
1. Go to your project → Settings
2. Add environment variable: `PYTHON_VERSION=3.12.8`
3. Redeploy

### Static Files Not Loading

1. Check `static` folder is included in deployment
2. Verify `STATIC_FOLDER` configuration
3. Check file permissions

### Timeout Errors

- Free tiers have limitations
- Render apps spin down after inactivity
- Consider upgrading or using keep-alive services

### Port Configuration

Different platforms use different ports:
- Render: Uses `PORT` environment variable (usually 10000)
- Railway: Uses `PORT` (usually 3000 or provided)
- Fly.io: Uses port from `fly.toml`
- PythonAnywhere: Configured in WSGI file

Update your app to use `os.getenv('PORT', 5000)` ✅ (Already done!)

---

## Keep Your App Alive (Render Free Tier)

Render free tier apps sleep after 15 minutes. To keep them awake:

### Option 1: Use a Cron Job

Create a free cron job on Render that pings your app every 14 minutes:

1. Go to "New +" → "Background Worker" or "Cron Job"
2. Use this command: `curl https://your-app.onrender.com`

### Option 2: External Ping Service

Use services like:
- [UptimeRobot](https://uptimerobot.com) (free)
- [Cron-Job.org](https://cron-job.org) (free)

Set them to ping your app every 10-15 minutes.

---

## Security Notes

⚠️ **Important Security Steps:**

1. ✅ Change `SECRET_KEY` in production
2. ✅ Never commit `.env` file
3. ✅ Use strong passwords for admin accounts
4. ✅ Enable HTTPS (most platforms do this automatically)
5. ✅ Regularly update dependencies

---

## Need Help?

If you encounter issues:

1. Check platform-specific documentation
2. Review error logs carefully
3. Test locally with same environment variables
4. Verify database connectivity
5. Check platform status pages

---

## 🎉 You're All Set!

Your app should now be live and accessible to the world!

**Next Steps:**
- Set up a custom domain
- Configure email notifications
- Set up monitoring
- Regularly backup your database
- Keep dependencies updated

---

*Happy Deploying! 🚀*
