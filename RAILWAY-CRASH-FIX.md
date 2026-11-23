# 🚨 RAILWAY BACKEND CRASH FIX

**Status:** 🔴 Backend is CRASHED  
**Issue:** Service crashed after latest deployment  
**Solution:** Fix environment variables and redeploy

---

## 🎯 IMMEDIATE FIX (3 minutes)

### Step 1: Check Railway Environment Variables
1. Go to: https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965
2. Click on your backend service
3. Go to **"Variables"** tab
4. Verify these variables are set:

```
DATABASE_URL=postgresql://user:password@host:5432/database
SECRET_KEY=your-jwt-secret-key
ENVIRONMENT=production
DEBUG=false
```

### Step 2: Verify Database URL
- Get your Supabase connection string from: https://supabase.com
- It should look like: `postgresql://postgres.[PROJECT_ID]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`
- Set this as `DATABASE_URL` in Railway variables

### Step 3: Restart the Service
1. In Railway, click the **"Restart"** button on the crashed deployment
2. Wait 30-60 seconds for it to restart
3. Check the **Console** tab for logs

### Step 4: Verify It's Running
Test the health endpoint:
```bash
curl https://yatradiscover-prod-xxx.railway.app/health
```

Should return:
```json
{"status":"ok","message":"YatraDiscover AI Backend is running"}
```

---

## 🔍 IF RESTART DOESN'T WORK

### Option A: Redeploy from GitHub

1. Go to Railway project
2. Click on backend service
3. Go to **"Settings"** tab
4. Click **"Redeploy"** button (not "Restart")
5. Wait 2-3 minutes for full rebuild
6. Check console for build logs

### Option B: Check Logs for Error

1. Click on the **"Console"** tab
2. Look for error messages (they'll be in red)
3. Common issues:
   - **"psycopg2.OperationalError"** → Database connection failed
   - **"ImportError"** → Python dependency missing
   - **"ModuleNotFoundError"** → Backend code path incorrect
   - **"Connection refused"** → Database not accessible

### Option C: Force Clean Rebuild

1. Go to Railway Settings
2. Find "Build & Deploy"
3. Click "Build"
4. It will rebuild Docker image from scratch
5. Wait 3-5 minutes

---

## ✅ WHAT TO DO NEXT

Once the backend is running:

1. **Test the backend:**
   ```bash
   curl https://[YOUR_RAILWAY_URL]/health
   ```
   Should show ✅ OK

2. **Copy your Railway URL:**
   - Format: `https://yatradiscover-prod-xxx.railway.app`
   - Use this for Vercel deployment

3. **Deploy to Vercel:**
   - Set environment variable: `NEXT_PUBLIC_API_URL=[YOUR_RAILWAY_URL]`
   - Deploy frontend

4. **Verify Everything Works:**
   - Open https://yatradiscover.vercel.app
   - Check API Status shows ✅ OK

---

## 🐛 COMMON CRASH REASONS

| Error | Cause | Fix |
|-------|-------|-----|
| Database connection refused | DATABASE_URL not set or invalid | Set correct PostgreSQL URL in Variables |
| ModuleNotFoundError | requirements.txt not updated | Redeploy from GitHub |
| Port already in use | 8000 occupied (unlikely) | Restart service |
| Memory limit exceeded | App too heavy for free tier | Upgrade Railway plan |
| Deployment timeout | Build taking too long | Increase timeout in Railway settings |

---

## 📞 IF STILL CRASHED

Check these documentation files:
- 👉 docs/02-deployment/RAILWAY-DEBUG-GUIDE.md
- 👉 docs/02-deployment/RAILWAY-REBUILD-INSTRUCTIONS.md
- 👉 docs/02-deployment/DATABASE-CONFIG-FIXED.md

---

## ✨ QUICK CHECKLIST

- [ ] Environment variables set in Railway
- [ ] DATABASE_URL is correct Supabase connection string
- [ ] Clicked "Restart" or "Redeploy" button
- [ ] Waited 30-60 seconds
- [ ] Checked Console tab for errors
- [ ] Tested /health endpoint
- [ ] Got Railway public URL
- [ ] Ready to deploy to Vercel

---

**Next Step:** Reply with your Railway URL once it's running! 🚀
