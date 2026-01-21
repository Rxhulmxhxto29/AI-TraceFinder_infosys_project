# 🚀 Quick Deploy to Render.com

## One-Click Deployment (Easiest Way)

1. **Click this button:**

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/AI-TraceFinder/Rahul_Mahato-TraceFinder)

2. **Sign in with GitHub** (it's free, no credit card needed)

3. **Click "Deploy"** - That's it!

Your TraceFinder app will be live in 3-5 minutes at a URL like:
```
https://tracefinder-abc123.onrender.com
```

## Manual Deployment (If button doesn't work)

1. **Go to [Render.com](https://render.com)** and sign up with GitHub

2. **Click "New +"** → Select **"Web Service"**

3. **Connect your repository:**
   - Search for: `AI-TraceFinder/Rahul_Mahato-TraceFinder`
   - Click "Connect"

4. **Configure the service:**
   - **Name:** `tracefinder` (or anything you like)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Plan:** Select **Free**

5. **Click "Create Web Service"**

6. **Wait 3-5 minutes** for deployment to complete

7. **Your app is live!** Click the URL at the top to access it

## Why Render.com?

✅ **100% Free** - No credit card required
✅ **No Sleep** - Your app stays awake (unlike Heroku free tier)
✅ **Auto Deploy** - Pushes to GitHub automatically redeploy
✅ **HTTPS** - Free SSL certificate included
✅ **Easy Updates** - Just push to GitHub to update

## Troubleshooting

**If deployment fails:**
1. Check the logs in Render dashboard
2. Make sure Python version is 3.13 or compatible
3. Verify all dependencies in requirements.txt

**If app doesn't load:**
- Wait 5 minutes for initial build
- Check Render dashboard for service status
- Refresh your browser

## Update Your App

After deployment, any changes you push to GitHub will automatically redeploy!

```bash
git add .
git commit -m "Update app"
git push origin main
```

Render will detect the push and automatically redeploy within 2-3 minutes.

---

**Need help?** Open an issue on GitHub!
