# Render Deployment Guide

## Step-by-Step Instructions

### 1. Create a Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub (recommended)

### 2. Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `aithal007/Optimization-Optimal-Drone-Path-Planning`
3. Configure the service:

   **Name:** `path-optimization-api` (or any name you like)
   
   **Region:** Choose closest to you
   
   **Branch:** `main`
   
   **Root Directory:** (leave empty)
   
   **Runtime:** `Python 3`
   
   **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Start Command:**
   ```bash
   gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 backend.server:app
   ```
   
   **Instance Type:** `Free`

4. Click **"Create Web Service"**

### 3. Wait for Deployment
- Render will automatically build and deploy your app
- Wait 2-5 minutes for the first deployment
- You'll get a URL like: `https://path-optimization-api.onrender.com`

### 4. Update Frontend
Once deployed, update your frontend's API URL:
1. Open `frontend/app.js`
2. Change the API_BASE_URL to your Render URL:
   ```javascript
   const API_BASE_URL = 'https://your-app-name.onrender.com/api';
   ```
3. Commit and push the change

### 5. Deploy Frontend to Vercel
The frontend can still be on Vercel:
- Go to Vercel dashboard
- Your project will auto-deploy with the new API URL
- Or manually redeploy if needed

### 6. Test Your App
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-app.onrender.com/api/health`

## Notes
- Free tier on Render goes to sleep after 15 min of inactivity
- First request after sleep takes ~30 seconds to wake up
- This is normal for free tier!

## Troubleshooting
If deployment fails:
1. Check Render logs in the dashboard
2. Make sure all files are committed to GitHub
3. Check that requirements.txt has all dependencies
