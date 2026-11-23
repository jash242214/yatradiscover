# 🚀 Vercel Frontend Deployment Guide

Deploy your Next.js frontend to Vercel in 5 minutes!

---

## ✅ Prerequisites

- [ ] GitHub account with yatradiscover repository
- [ ] Vercel account (free tier available)
- [ ] Backend running on Railway (we did this already!)
- [ ] Railway API URL ready

---

## 🎯 Step 1: Connect GitHub to Vercel

### 1.1 Go to Vercel
https://vercel.com/

### 1.2 Sign Up / Log In
- Click "Sign Up" or "Log In"
- Select "Continue with GitHub"
- Authorize Vercel to access your GitHub account

### 1.3 Import Project
1. Click "Add New..." → "Project"
2. Click "Import Git Repository"
3. Find "jash242214/yatradiscover"
4. Click "Import"

---

## ⚙️ Step 2: Configure Project Settings

### 2.1 Framework Selection
- **Framework Preset:** Next.js ✅ (auto-detected)
- **Root Directory:** `frontend/web` ← **IMPORTANT!**

### 2.2 Build Settings (Auto-Filled)
```
Build Command:   npm run build
Install Command: npm install
Output Directory: .next
```

### 2.3 Environment Variables

Add these environment variables in Vercel dashboard:

| Key | Value | Notes |
|-----|-------|-------|
| `NEXT_PUBLIC_API_URL` | `https://[your-railway-url]` | Backend API URL |
| `NEXT_PUBLIC_APP_NAME` | `YatraDiscover AI` | App name |

**To get Railway URL:**
1. Go to https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965
2. Click yatradiscover service
3. Copy the URL (looks like: `https://yatradiscover-prod-xxx.railway.app`)

### 2.4 Git Configuration
- **Production Branch:** `master`
- **Deploy on Push:** Enable
- **Preview Deployments:** Enable

---

## 🚀 Step 3: Deploy

### 3.1 Click "Deploy"
- Vercel starts building automatically
- Watch the build logs
- Should take 2-3 minutes

### 3.2 Build Success Indicators
```
✓ Installed dependencies
✓ Next.js build succeeded
✓ Generated static pages
✓ Created optimized bundle
✓ Deployment complete
```

### 3.3 Get Your URL
After deployment:
- **Production URL:** `https://yatradiscover.vercel.app`
- Or your custom domain if configured

---

## 🧪 Step 4: Verify Deployment

### 4.1 Test Home Page
```
https://yatradiscover.vercel.app/
```

You should see:
- ✅ Hero section with "AI-Powered Travel Planning"
- ✅ Features grid
- ✅ API Status showing backend health

### 4.2 Check API Connection
On the homepage, the "API Status" section should show:
- Status: ✅ OK
- Service: YatraDiscover AI
- Version: 0.1.0
- Environment: production

If it shows error:
1. Check `NEXT_PUBLIC_API_URL` in Vercel settings
2. Verify Railway backend is running
3. Trigger redeploy in Vercel

---

## 🌐 Step 5: Custom Domain Setup (Optional)

### 5.1 Add Domain in Vercel
1. Go to Project Settings → Domains
2. Click "Add Domain"
3. Enter `www.yatradiscover.com`

### 5.2 Update DNS
Vercel provides nameserver records:
1. Copy the nameserver values
2. Go to your domain registrar (GoDaddy, Namecheap, etc.)
3. Update nameservers
4. Wait 24-48 hours for DNS propagation

### 5.3 Verify Domain
Once DNS propagates:
```
https://www.yatradiscover.com → Vercel
```

---

## 📋 Troubleshooting

### Build Fails
**Error:** "Cannot find module 'next'"

**Solution:**
1. Check `frontend/web/package.json` exists
2. Verify root directory is set to `frontend/web`
3. Clear build cache in Vercel: Settings → Advanced → Clear Build Cache

### API Connection Error
**Error:** "Failed to connect to API"

**Solution:**
1. Verify `NEXT_PUBLIC_API_URL` is set correctly
2. Test API manually: `curl https://[your-railway-url]/health`
3. Check CORS is enabled on backend
4. Trigger redeploy

### Environment Variables Not Working
**Error:** "undefined" for API_URL

**Solution:**
1. Environment variables must start with `NEXT_PUBLIC_` for client-side
2. Redeploy after adding variables
3. Clear browser cache (Ctrl+Shift+Delete)
4. Check `.env.example` file for reference

---

## 🔄 Redeploying

### Auto Redeploy (On Push)
```bash
git add .
git commit -m "Update frontend"
git push origin master
```
✅ Vercel automatically builds and deploys

### Manual Redeploy
1. Go to Vercel dashboard
2. Click project → Deployments
3. Click "..." on latest deployment
4. Select "Redeploy"

---

## 📊 Monitoring

### View Logs
1. Go to Vercel dashboard
2. Click project → Deployments
3. Click deployment → "View Logs"

### Common Logs
```
✓ Retrieved source code
✓ Installed 20 packages
✓ Building Next.js application
✓ Collecting page data
✓ Finalizing page optimization
✓ Created optimized images in 500ms
✓ Deployment successful
```

---

## 🔒 Security Checklist

- ✅ No secrets in code (use env vars)
- ✅ HTTPS enabled by default
- ✅ Security headers configured
- ✅ CORS properly set up
- ✅ API key stored securely

---

## 🎯 Next Steps

1. ✅ Deploy to Vercel (THIS STEP)
2. ⏳ Configure Cloudflare DNS
3. ⏳ Set up custom domains
4. ⏳ Deploy mobile apps
5. ⏳ Configure admin dashboard

---

## 📚 Resources

- [Vercel Docs](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Environment Variables](https://vercel.com/docs/projects/environment-variables)

---

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] Vercel account created
- [ ] Project imported to Vercel
- [ ] Root directory set to `frontend/web`
- [ ] `NEXT_PUBLIC_API_URL` environment variable set
- [ ] Build completed successfully
- [ ] Homepage loads at `https://yatradiscover.vercel.app`
- [ ] API status shows healthy
- [ ] All features display correctly

---

**Status:** Ready for Vercel Deployment ✅
**Last Updated:** 2026-11-23
**Version:** 1.0
