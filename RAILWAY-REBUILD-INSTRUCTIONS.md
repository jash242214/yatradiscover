# 🔄 RAILWAY REBUILD - FORCE FRESH DEPLOYMENT

## ❌ What Went Wrong

Railway was using **cached Docker layers** from the previous build. This meant:

1. ✅ Docker used old layers (without the config fixes)
2. ❌ Did NOT rebuild the Python environment with updated code
3. ❌ App still tried to connect to `localhost:5432`
4. ❌ Failed with `psycopg2.OperationalError: connection refused`

---

## ✅ What We Fixed

**Commit 1:** Fixed schema import names
- `app/schemas/__init__.py` - `UserRegisterRequest` → `UserRegister`

**Commit 2:** Fixed database configuration
- `app/core/config.py` - Now reads `DATABASE_URL` from environment variables instead of hardcoded `localhost`
- Also fixed `JWT_SECRET_KEY` and `REDIS_URL` to use env vars

**Commit 3:** Added cache buster
- `Dockerfile` - Added `BUILD_DATE` ARG to force Docker layer cache miss
- This ensures Railway rebuilds everything fresh

---

## 🚀 NOW DO THIS: Force Full Rebuild in Railway

### Step 1: Clear Railway's Docker Cache

1. Go to: https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965
2. Click **yatradiscover** service
3. Click **⋯ menu** → **"Settings"**
4. Scroll to **"Build Logs"** section
5. Click **"Clear build cache"** (if available)
   - OR if not available, skip to Step 2

### Step 2: Trigger New Deploy

1. Still in the yatradiscover service
2. Click **⋯ menu** → **"Trigger Deploy"**
3. Wait for the **"Building..."** status to appear
4. Watch the build logs (should take 2-5 minutes)

---

## ✅ Expected Build Output

Watch for these in the build logs:

```
✓ Cloning repository...
✓ Pulling python:3.11-slim base image
✓ COPY backend/requirements.txt
✓ RUN pip install --no-cache-dir -r requirements.txt
  (Installing: fastapi, uvicorn, sqlalchemy, psycopg2, pydantic, etc.)
✓ COPY backend/ .
✓ Build date: (cache buster line)
✓ Exporting to image...
✓ Successfully built image sha256:...
✓ Pushing to Railway registry...
✓ Container starting...
✓ Starting server process [PID]
✓ Uvicorn running on 0.0.0.0:8000
✓ Deployment successful
```

**Key indicators of success:**
- ✅ Full rebuild (not "Using cached layer")
- ✅ All 41 dependencies installed
- ✅ No traceback or error messages
- ✅ "Deployment successful" at the end

---

## 🧪 Verify It's Working

After the deployment completes, check the **Logs**:

```
2026-11-23 09:XX:XX - CORS enabled for origins: [...]
2026-11-23 09:XX:XX - Application initialized: YatraDiscover AI
2026-11-23 09:XX:XX - Starting YatraDiscover AI v0.1.0
2026-11-23 09:XX:XX - Environment: production
✓ Database tables created/verified
✓ Started server process [PID]
✓ Uvicorn running
✓ Application startup complete
```

**NO errors about localhost connection!** ✅

---

## 🌐 Test the Backend URL

Once deployment shows "Running" (green status):

1. Copy your Railway backend URL (looks like: `https://yatradiscover-prod-xxx.railway.app`)
2. Test health endpoint:

```bash
# Replace YOUR_RAILWAY_URL with actual URL
curl https://YOUR_RAILWAY_URL/health
```

Should return:
```json
{
  "status": "ok",
  "service": "YatraDiscover AI",
  "version": "0.1.0",
  "environment": "production"
}
```

---

## 📋 Troubleshooting

### If Build Still Fails With Same Error

1. **Check Variables** (in Railway Settings → Variables):
   - ✅ `DATABASE_URL` = `postgresql://postgres:Itsmygame@143@db.zseviucrtfdwuvmiokzv.supabase.co:5432/postgres`
   - ✅ `SECRET_KEY` = (some secure string)
   - ✅ `ENVIRONMENT` = `production`

2. **If DATABASE_URL looks wrong:**
   - Delete it and re-add it from Supabase
   - Supabase → Settings → Database → URI

3. **Force complete rebuild:**
   - Delete the service and redeploy
   - Or ask Railway support to clear all build artifacts

### If Build Succeeds But App Still Crashes

1. Check **Logs** tab for error messages
2. Look for `ImportError` or connection errors
3. Copy the error message and we'll debug

---

## 📝 Recent Changes Summary

```
✅ e38eee7 - chore: Add cache buster to Dockerfile
✅ a24253a - fix: Use environment variables for DATABASE_URL and secrets
✅ 04775f6 - fix: Correct schema import names
```

All committed and pushed to GitHub. ✅

---

## 🎯 Next Steps After Deploy

1. **NOW:** Trigger rebuild in Railway
2. **After 2-5 min:** Verify "Deployment successful"
3. **Then:** Test health endpoint (see above)
4. **Record:** Railway backend URL for Phase 3
5. **Finally:** Deploy frontend to Vercel

---

## ⚠️ Important Notes

- **Do NOT** manually edit config files in Railway's container
- **Do NOT** delete DATABASE_URL from Railway variables
- **All changes** should be in GitHub, not in Railway
- **Environment variables** in Railway take precedence over code defaults

---

**Go trigger that rebuild now!** 🚀

The app should connect to Supabase successfully this time! ✅
