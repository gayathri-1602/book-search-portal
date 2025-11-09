# Render Deployment Guide

## Current Configuration
- **Service Name:** book-search-portal
- **Python Version:** 3.9.0
- **Start Command:** `python seed_db.py && gunicorn --bind 0.0.0.0:$PORT "src.app:app"`

## How to Verify Deployment

### Step 1: Check Render Dashboard
1. Go to https://dashboard.render.com
2. Log in to your account
3. Look for service: **book-search-portal**
4. Check the status:
   - ✅ **Live** - Service is running
   - 🔄 **Building** - Currently deploying
   - ❌ **Failed** - Check logs for errors
   - ⏸️ **Suspended** - Service is paused

### Step 2: Get Your Service URL
- In the Render dashboard, click on your service
- Find the **Service URL** (format: `https://book-search-portal-xxxx.onrender.com`)
- Copy this URL

### Step 3: Test the Deployment
Open your service URL in a browser and verify:
- ✅ Homepage loads
- ✅ Search functionality works
- ✅ Book results display correctly
- ✅ New purple/teal theme is visible
- ✅ Additional book details are shown

## If Service is Not Deployed

### Option 1: Deploy via Render Dashboard
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Click **"Create Web Service"**

### Option 2: Manual Configuration
If auto-detection doesn't work, use these settings:

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python seed_db.py && gunicorn --bind 0.0.0.0:$PORT "src.app:app"`

**Environment Variables:**
- `PYTHON_VERSION` = `3.9.0`
- `PYTHONPATH` = `.`
- `FLASK_ENV` = `production`
- `FLASK_APP` = `src.app`

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is in the root directory
- Verify Python 3.9 is available
- Check build logs for specific errors

### Service Won't Start
- Verify `seed_db.py` runs successfully
- Check that gunicorn is installed in requirements.txt
- Review service logs for runtime errors

### Database Issues
- SQLite database is created automatically by `seed_db.py`
- Database file is stored in the `data/` directory
- If issues occur, the service will recreate the database on restart

## Current Deployment Status
- ✅ **Docker:** Live at http://localhost:5000
- ✅ **Docker Hub:** gayathrishree/book-search-portal:latest
- ⏳ **Render:** Check dashboard for status

## Support
If you encounter issues:
1. Check Render service logs
2. Verify all environment variables are set
3. Ensure the repository is properly connected
4. Review the `render.yaml` configuration

