# 🚀 Complete Railway + Supabase Setup Guide

**Status:** Backend Deployment Ready  
**Timeline:** 15 minutes total  
**Result:** Production-ready backend with database

---

## Overview - 3 Parts

| Part | Task | Time | Status |
|------|------|------|--------|
| 1️⃣ | Create Supabase PostgreSQL Database | 5 min | ⏳ To Do |
| 2️⃣ | Configure Railway Environment Variables | 3 min | ⏳ To Do |
| 3️⃣ | Deploy and Verify Backend | 5 min | ⏳ To Do |

**Total Time to Production:** 15 minutes ⏱️

---

## Part 1️⃣ - Create Supabase Database (5 minutes)

### Step 1.1: Create Supabase Account

1. Go to: **https://supabase.com**
2. Click "Sign Up" (top right)
3. Sign up with one of:
   - GitHub (recommended - easiest)
   - Google
   - Email
4. Verify your email

### Step 1.2: Create New Project

After login:

1. Click **"New Project"**
2. Fill in:
   - **Name:** `yatradiscover-db`
   - **Database Password:** Create a STRONG password (save it!)
   - **Region:** Choose closest to you
     - Asia-South (India) if you're in India
     - Asia-Pacific if you're in Asia
   - **Organization:** Select or create
3. Click **"Create new project"**
4. ⏳ Wait 2-3 minutes for initialization

### Step 1.3: Get Connection String

After project is created:

1. Go to: **Project Settings** (bottom left sidebar)
2. Click: **"Database"**
3. Look for: **"Connection string"** section
4. Copy the FULL connection string (should look like):

```
postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

5. 🔐 **SAVE THIS STRING** - You'll need it immediately!

### ✅ Part 1 Complete When:
- ✓ Supabase account created
- ✓ Project "yatradiscover-db" exists
- ✓ Connection string copied and saved

---

## Part 2️⃣ - Configure Railway (3 minutes)

### Step 2.1: Open Railway Dashboard

1. Go to: **https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965**
2. You should see the "yatradiscover" project
3. You should see your backend service (currently RED/CRASHED)

### Step 2.2: Set Environment Variables

1. **Click** on the backend service (the red "CRASHED" box)
2. Go to **"Variables"** tab
3. Add each variable by clicking "Add Variable":

| Variable Name | Value | Notes |
|---------------|-------|-------|
| `DATABASE_URL` | `postgresql://postgres.[PROJECT_ID]:[PASSWORD]@...` | Paste from Supabase |
| `SECRET_KEY` | `your-super-secret-key-12345` | Any random string for JWT |
| `ENVIRONMENT` | `production` | Tells app it's production |
| `DEBUG` | `false` | Disables debug mode |
| `LOG_LEVEL` | `INFO` | Standard logging |

**⚠️ Important Notes:**
- **DATABASE_URL:** Paste the EXACT connection string from Supabase
- **SECRET_KEY:** Can be any random string (used for JWT token signing)
- **Don't use quotes** around values in Railway

### Step 2.3: Deploy Service

After adding all variables:

1. Look for the RED "CRASHED" deployment card
2. Click the **"..."** menu (three dots)
3. Click **"Redeploy"**
4. ⏳ Wait 2-3 minutes for build to complete

### Step 2.4: Monitor Build

While rebuilding, check the **Console** tab:

Look for these messages:
```
✓ Pulling Docker image
✓ Installing dependencies  
✓ Starting server process
✓ Application initialized: YatraDiscover AI
```

**Status changes:** RED → YELLOW → GREEN ✅

**⚠️ No red ERROR messages should appear**

### ✅ Part 2 Complete When:
- ✓ All 5 variables added to Railway
- ✓ "Redeploy" button clicked
- ✓ Build completed (status GREEN ✅)

---

## Part 3️⃣ - Verify & Get URL (5 minutes)

### Step 3.1: Wait for Green Status ✅

Watch the Railway Console. When you see:

```
INFO - Starting YatraDiscover AI v0.1.0
INFO - Waiting for application startup.
INFO - Application initialized: YatraDiscover AI
```

Status should be: 🟢 **GREEN**

### Step 3.2: Get Your Railway URL

In Railway dashboard:

1. Find the **"Public URL"** or **"Domain"** section
2. It will look like:

```
🔗 https://yatradiscover-prod-abc123.railway.app
```

**📌 COPY THIS URL** - You'll need it for Vercel deployment!

### Step 3.3: Test the Backend

In your browser, test the health endpoint:

**URL:**
```
https://[YOUR_RAILWAY_URL]/health
```

**Expected Response:**
```json
{
  "status": "ok",
  "message": "YatraDiscover AI Backend is running"
}
```

✅ If you see this, your backend is PERFECT!

### Step 3.4: Check API Documentation

Go to:
```
https://[YOUR_RAILWAY_URL]/docs
```

You should see an interactive **Swagger API documentation** page with all endpoints!

This is your API playground and reference.

### ✅ Part 3 Complete When:
- ✓ Status is GREEN ✅
- ✓ /health endpoint returns OK
- ✓ /docs page loads successfully
- ✓ You have your Railway URL copied

---

## 🔧 Troubleshooting

### If Status Stays RED ❌

**Check 1: Variables are set**
1. Go to "Variables" tab
2. Confirm DATABASE_URL is there
3. Confirm SECRET_KEY is there

**Check 2: Database connection is valid**
1. Click "Console" tab
2. Look for red ERROR messages
3. If error mentions "psycopg2" or "connection refused":
   - Double-check Supabase connection string
   - Verify password is correct
   - Verify region matches where you created project

**Check 3: Redeploy again**
1. Click "..." menu
2. Click "Redeploy"
3. Wait full 3-5 minutes

### If /health Endpoint Fails ❌

**Check 1: URL is correct**
- Make sure it starts with `https://` (not `http`)
- Make sure path is exactly `/health`
- Example: `https://yatradiscover-prod-abc123.railway.app/health`

**Check 2: Backend is fully started**
1. Check Railway Console
2. Wait for all startup messages
3. Try again in 10 seconds

**Check 3: Check for errors**
1. Look in Railway Console for red ERROR text
2. See "Database Connection" section below

### If Database Connection Fails ❌

**Solution:**
1. Get fresh connection string from Supabase
2. Go to Railway Variables
3. Delete old DATABASE_URL
4. Add new one
5. Click "Redeploy"

---

## ✅ What's Next (After Backend is GREEN ✅)

Once your Railway backend is running:

1. ✅ You have your Railway URL
2. ✅ Backend is production-ready
3. ➡️ **Next Step:** Deploy frontend to Vercel
4. ➡️ **Final Step:** Website goes LIVE! 🚀

---

## 📋 Quick Checklist

### Part 1 - Supabase
- ☐ Created Supabase account at https://supabase.com
- ☐ Created project named "yatradiscover-db"
- ☐ Got connection string from Project Settings → Database
- ☐ Saved connection string safely

### Part 2 - Railway Configuration
- ☐ Opened Railway project dashboard
- ☐ Added DATABASE_URL variable
- ☐ Added SECRET_KEY variable
- ☐ Added ENVIRONMENT variable
- ☐ Added DEBUG variable
- ☐ Added LOG_LEVEL variable
- ☐ Clicked "Redeploy" button
- ☐ Watched build in Console tab

### Part 3 - Verification
- ☐ Status changed to GREEN ✅
- ☐ Tested /health endpoint in browser
- ☐ Saw successful JSON response
- ☐ Opened /docs endpoint (API documentation)
- ☐ Copied Railway URL for Vercel deployment

---

## 🎯 Key URLs to Save

```
Supabase Project:
https://supabase.com/dashboard

Railway Project:
https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965

Backend Health Check:
https://[YOUR_RAILWAY_URL]/health

API Documentation:
https://[YOUR_RAILWAY_URL]/docs
```

---

## 📌 Important Notes

### Environment Variables Explanation

| Variable | Purpose | Example |
|----------|---------|---------|
| DATABASE_URL | PostgreSQL connection string | `postgresql://postgres...` |
| SECRET_KEY | JWT token signing key | Any random string |
| ENVIRONMENT | App environment | `production` |
| DEBUG | Debug mode (security) | `false` |
| LOG_LEVEL | Logging verbosity | `INFO`, `DEBUG` |

### Security Reminders

✅ **DO:**
- Save DATABASE_URL securely
- Use strong passwords for Supabase
- Keep SECRET_KEY confidential
- Use HTTPS URLs only

❌ **DON'T:**
- Share your connection strings publicly
- Commit passwords to GitHub
- Use `DEBUG=true` in production
- Share your SECRET_KEY

---

## 🚀 Timeline

| Time | Task | Status |
|------|------|--------|
| Now | Start Part 1 | 🔴 Start Here |
| +5 min | Supabase ready | ⏳ Next |
| +8 min | Railway variables set | ⏳ Next |
| +11 min | Build completing | ⏳ Next |
| +15 min | Backend is LIVE! | 🟢 Done! |

---

## 📞 Need Help?

If something goes wrong, check these files:
- 👉 [RAILWAY-CRASH-FIX.md](./RAILWAY-CRASH-FIX.md) - Crash troubleshooting
- 👉 [docs/02-deployment/RAILWAY-DEBUG-GUIDE.md](./docs/02-deployment/RAILWAY-DEBUG-GUIDE.md) - Debug guide
- 👉 [docs/02-deployment/DATABASE-CONFIG-FIXED.md](./docs/02-deployment/DATABASE-CONFIG-FIXED.md) - Database config

---

## 🎉 Success Looks Like

After completing all 3 parts, you should have:

✅ Supabase PostgreSQL database running  
✅ Railway backend deployed and GREEN  
✅ /health endpoint responding with OK  
✅ /docs endpoint showing API documentation  
✅ Railway URL ready for Vercel deployment  

**Next:** Follow [VERCEL-FRONTEND-DEPLOYMENT.md](./docs/02-deployment/VERCEL-FRONTEND-DEPLOYMENT.md) to deploy frontend!

---

**Created:** November 23, 2026  
**Status:** Ready for deployment  
**Last Updated:** Today

**Let's make your backend LIVE! 🚀**
