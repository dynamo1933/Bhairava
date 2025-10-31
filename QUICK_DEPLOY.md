# ⚡ Quick Deploy Guide

Fastest way to get your app online for FREE.

## 🚀 Recommended: Render.com (5 minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub

### Step 3: Deploy
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Use these settings:
   - **Name**: `daiva-anughara`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: `Python 3`

### Step 4: Add Environment Variables
In the "Environment" section, add:

```
SECRET_KEY=<generate-with-python-secrets-token_hex-32>
SQLALCHEMY_DATABASE_URI=postgresql://postgres.cuyilngsmocyhadlbrgv:_Bottlemepani%4035@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
FLASK_ENV=production
PORT=10000
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Step 5: Deploy!
Click "Create Web Service" and wait 5-10 minutes.

✅ **Done!** Your app will be live at `https://your-app-name.onrender.com`

---

## 🔄 Alternative: Railway.app (3 minutes)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repo
5. Add environment variables (same as above)
6. Railway auto-deploys!

✅ **Done!** Your app will be live at `https://your-app.railway.app`

---

## 📝 Generate Secret Key

Run this in Python to get a secure secret key:

```python
import secrets
print(secrets.token_hex(32))
```

Copy the output and use it as your `SECRET_KEY`.

---

## ⚠️ Important Notes

1. **Never commit secrets** - Use environment variables only
2. **Change admin password** - Default is `admin123`
3. **Keep app alive** - Free tiers may sleep after inactivity
4. **Check logs** - If something breaks, check the deployment logs

---

## 🆘 Troubleshooting

**App won't start?**
- Check environment variables are set
- Verify database connection string
- Check logs for error messages

**Database connection fails?**
- Verify Supabase connection string
- Check password is URL-encoded (`@` → `%40`)
- Ensure Supabase allows external connections

**Static files not loading?**
- Check `static` folder is in repo
- Verify file paths in templates

---

For detailed instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

🎉 **Happy Deploying!**
