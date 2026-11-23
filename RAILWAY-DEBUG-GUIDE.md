# 🚀 Railway Deployment Debug Guide

## ❌ Build Failed Error - Solutions

Your build is failing because Railway can't properly start the FastAPI app. Here's how to fix it:

---

## 🔧 **IMMEDIATE ACTION: Check Build Logs**

1. Go to: https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965
2. Click on **yatradiscover** service card
3. Click **"Build"** tab
4. Look for error messages (scroll down)
5. **Share the error message** with us

---

## 🔍 **Common Railway Build Failures & Fixes**

### **Issue 1: "No module named 'app'"**
**Fix:** Add this to Railway environment variables:
```
PYTHONPATH=backend
```

### **Issue 2: "Cannot find Procfile"**
**Solution:** Railway looks in root directory. Create: `/Procfile` (not `backend/Procfile`)

**Content:**
```
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### **Issue 3: "Cannot find runtime.txt"**
**Solution:** Create: `/runtime.txt` (not `backend/runtime.txt`)

**Content:**
```
python-3.11.7
```

### **Issue 4: Missing dependencies**
**Solution:** Create: `/requirements.txt` (not `backend/requirements.txt`)

**OR** create symlink in root that points to `backend/requirements.txt`

### **Issue 5: Port binding issues**
**Problem:** App trying to use hardcoded port instead of `$PORT`

**Fix:** Procfile must use: `--port $PORT`

✅ Current Procfile looks correct!

---

## ✅ **Railway Environment Variables Required**

Your Shared Variables should have:

```
✅ DATABASE_URL = postgresql://postgres:Itsmygame@143@db.zseviucrtfdwuvmiokzv.supabase.co:5432/postgres
✅ ENVIRONMENT = production
✅ SECRET_KEY = (some-secret-value)
✅ JWT_SECRET_KEY = (should be a 32+ char string)
✅ DEBUG = False
```

---

## 🛠️ **Step-by-Step Fix Process**

### **Step 1: Make Root-Level Files (if needed)**

If your Procfile is in `backend/`, Railway might not find it.

**Solution:** Copy/symlink to root:

```bash
# Windows PowerShell - Run from project root
cp backend\Procfile Procfile
cp backend\runtime.txt runtime.txt
cp backend\requirements.txt requirements.txt
```

### **Step 2: Add PYTHONPATH Variable**

Go to Railway → Shared Variables → Add:
```
Name: PYTHONPATH
Value: backend
```

### **Step 3: Redeploy**

1. Go to Railway project
2. Click **"yatradiscover"** service
3. Click three-dot menu (⋯)
4. Select **"Trigger Deploy"**
5. Wait 2-5 minutes

### **Step 4: Check Logs**

If still failing, go to **"Logs"** tab and copy the error message.

---

## 📋 **Deployment Verification Checklist**

Before triggering deploy, verify:

- [ ] `Procfile` exists in project **root** (not just backend/)
- [ ] `runtime.txt` exists in project **root**
- [ ] `requirements.txt` exists in project **root** (or symlink)
- [ ] `DATABASE_URL` is set in Railway Shared Variables
- [ ] `SECRET_KEY` is set (at least 32 characters)
- [ ] `JWT_SECRET_KEY` is set
- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`
- [ ] `PYTHONPATH=backend` is set (if app is in backend folder)

---

## 🆘 **If Still Failing**

Please provide:

1. **Full error message from Build logs**
2. Screenshot of Railway → Logs tab
3. Output of this command:
   ```bash
   cd d:\yatradiscover
   git log --oneline -1
   ```

---

## ✨ **Next: After Backend Deploys Successfully**

1. ✅ Note the Railway URL (should be like `https://yatradiscover-backend-prod.railway.app`)
2. ✅ Test health endpoint: `https://yatradiscover-backend-prod.railway.app/health`
3. ✅ Proceed to Phase 3: Deploy Frontend to Vercel

---

## 🚀 **Quick Deploy After Fix**

```bash
# From project root
git add .
git commit -m "Fix: Railway deployment configuration"
git push
# Railway auto-deploys on push (should trigger in ~30 seconds)
```

---

**Need help?** Share the build error message and I'll provide specific fix! 🎯
