# 🚀 YatraDiscover AI - Complete Domain Deployment Guide

**Domain:** yatradiscover.com  
**Status:** Ready to Deploy  
**Last Updated:** 2024

---

## 📊 QUICK DECISION MATRIX

| Aspect | Recommended | Alternative | Why? |
|--------|-------------|-------------|------|
| **Frontend** | Vercel | Netlify, AWS S3 | Free, automatic deployments, included SSL |
| **Backend** | Railway/Render | DigitalOcean, AWS EC2 | Simple FastAPI hosting, free tier, pay-as-you-go |
| **Database** | Supabase | AWS RDS, PlanetScale | PostgreSQL hosting, free tier, easy backups |
| **DNS** | Cloudflare | AWS Route53, Namecheap | Free SSL, DDoS protection, CDN, easy setup |

---

## 🎯 PHASE 1: PREPARE YOUR CODE (TODAY - 30 mins)

### 1.1 Backend Preparation

Your FastAPI backend is ready! Just need:

```bash
# Check your backend structure
cd backend
ls -la

# Key files ready:
✅ app/main.py - FastAPI app
✅ app/api/ - 19 endpoints
✅ app/db/ - PostgreSQL models
✅ requirements.txt - All dependencies
✅ alembic/ - Database migrations
```

**What to do:**
1. Create `backend/.env.production` for production secrets
2. Create `backend/Procfile` for deployment (see template below)
3. Create `backend/runtime.txt` for Python version

**backend/Procfile:**
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**backend/runtime.txt:**
```
python-3.11.7
```

### 1.2 Frontend Preparation

Your Next.js frontend needs to be created. Currently you have placeholder structure.

**Commands to initialize:**
```bash
cd frontend
npm create next-app@latest web -- --typescript --tailwind --app
cd web
npm install
```

**Key files needed:**
- `frontend/web/.env.local` - Local environment variables
- `frontend/web/.env.production` - Production environment variables

**frontend/web/.env.production:**
```
NEXT_PUBLIC_API_URL=https://api.yatradiscover.com
NEXT_PUBLIC_APP_URL=https://www.yatradiscover.com
```

### 1.3 Version Control Setup

```bash
# From project root
cd D:\yatradiscover

# Ensure everything is committed
git add .
git commit -m "feat: Prepare application for deployment to yatradiscover.com"
git push origin master
```

---

## 🎯 PHASE 2: CHOOSE YOUR HOSTING STRATEGY

### OPTION A: VERCEL + RAILWAY + SUPABASE (RECOMMENDED) ⭐

**Cost:** $0-50/month  
**Setup Time:** 2 hours  
**Difficulty:** Easy  

#### Flow:
```
yatradiscover.com
├── www.yatradiscover.com → Vercel (Frontend)
├── api.yatradiscover.com → Railway (Backend)
└── Database → Supabase (PostgreSQL)
```

#### Step-by-Step:

**A1. Set Up Supabase Database (20 mins)**

1. Go to https://supabase.com
2. Click "Start your project" → Sign up with GitHub
3. Create new project:
   - Organization: Create "YatraDiscover"
   - Project name: "yatradiscover-prod"
   - Database password: `[Generate strong password, store in vault]`
   - Region: Closest to your users
4. Wait 2-3 minutes for database creation
5. Go to "Settings > Database":
   - Copy **Connection String** (looks like: `postgresql://[user]:[password]@[host]/postgres`)
   - Store safely: `D:\yatradiscover\backend\.env.production`

**Setup Supabase Schema:**
```bash
# From backend directory
cd D:\yatradiscover\backend

# Create .env.production with:
# DATABASE_URL=postgresql://[paste-from-supabase]

# Run migrations
alembic upgrade head

# Verify tables created:
# (via Supabase dashboard: Table Editor)
```

---

**A2. Deploy Backend to Railway (30 mins)**

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "Create a new project" → "Deploy from GitHub repo"
4. Connect to: `jash242214/yatradiscover`
5. Railway will auto-detect Procfile
6. Set environment variables:
   ```
   DATABASE_URL=postgresql://...  [from Supabase]
   SECRET_KEY=... [generate: python -c "import secrets; print(secrets.token_urlsafe(32))"]
   OPENAI_API_KEY=... [your OpenAI key]
   STRIPE_API_KEY=... [if needed]
   ENVIRONMENT=production
   ```
7. Railway will deploy automatically
8. Get your backend URL: `https://yatradiscover-backend-prod.railway.app`
9. Add to custom domain:
   - Railway dashboard → Settings → Custom Domains
   - Add: `api.yatradiscover.com`
   - Railway provides DNS value (keep for later)

---

**A3. Deploy Frontend to Vercel (30 mins)**

1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Import Project"
4. Select: `jash242214/yatradiscover`
5. Framework preset: "Next.js"
6. Set environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://api.yatradiscover.com
   NEXT_PUBLIC_APP_URL=https://www.yatradiscover.com
   ```
7. Click "Deploy"
8. Vercel will deploy automatically
9. Get your frontend URL: `https://yatradiscover-prod.vercel.app`
10. Add custom domain:
    - Vercel dashboard → Settings → Domains
    - Add both:
      - `yatradiscover.com`
      - `www.yatradiscover.com`
    - Vercel provides DNS values (keep for later)

---

**A4. Configure Cloudflare DNS (30 mins)**

1. Go to https://cloudflare.com
2. Sign up or log in
3. Click "Add site"
4. Enter: `yatradiscover.com`
5. Select "Free" plan
6. Cloudflare will scan for existing DNS records
7. Add these records:

| Type | Name | Target | Proxy | TTL | Purpose |
|------|------|--------|-------|-----|---------|
| CNAME | @ (root) | yatradiscover-prod.vercel.app | ✅ Proxied | Auto | Main website |
| CNAME | www | yatradiscover-prod.vercel.app | ✅ Proxied | Auto | www subdomain |
| CNAME | api | yatradiscover-prod.railway.app | ✅ Proxied | Auto | Backend API |
| CNAME | staging | yatradiscover-staging.vercel.app | ✅ Proxied | Auto | Staging (optional) |

**Important:** Keep email records as DNS-only (not proxied)

8. Update nameservers at your domain registrar:
   - Cloudflare gives you 2 nameservers to add
   - Go to your domain registrar (GoDaddy, Namecheap, etc.)
   - Update nameservers there
   - Wait 24-48 hours for DNS propagation

9. Verify in Cloudflare:
   - Dashboard → Overview
   - Should show "Active" status

---

**A5. Set Up SSL/TLS**

1. Cloudflare dashboard → SSL/TLS → Overview
2. Select "Full (strict)"
3. Each hosting provider will generate certificate:
   - Vercel: Automatic
   - Railway: Automatic
   - Supabase: Automatic
4. Cloudflare automatically enforces HTTPS

---

### OPTION B: AWS (If you prefer AWS)

**Cost:** $50-200/month  
**Setup Time:** 4-6 hours  
**Difficulty:** Hard  

If you prefer AWS, we can set up:
- CloudFront + S3 (Frontend)
- EC2 or Elastic Beanstalk (Backend)
- RDS PostgreSQL (Database)
- Route53 (DNS)

Would you like detailed AWS guide? Say "YES" and I'll prepare it.

---

### OPTION C: DIGITALOCEAN (Balanced)

**Cost:** $24-40/month  
**Setup Time:** 2 hours  
**Difficulty:** Medium  

DigitalOcean App Platform can host:
- Next.js frontend
- FastAPI backend
- PostgreSQL database

All in one place. Need guide? Say "YES".

---

## 🎯 PHASE 3: DOMAIN DNS SETUP

### DNS Records Required

After choosing hosting (Phase 2), you'll have these values:

```
Vercel Frontend:  yatradiscover-prod.vercel.app
Railway Backend:  yatradiscover-prod.railway.app
Supabase DB:      (hosted, no DNS needed)
```

### Complete DNS Configuration

**Step 1: Create Cloudflare Account**
```
1. Go to https://cloudflare.com
2. Sign up
3. Click "Add site"
4. Enter: yatradiscover.com
5. Choose "Free" plan
6. Continue
```

**Step 2: Review DNS Records**
```
Cloudflare will show any existing records.
If your domain is new, it's empty. That's fine.
```

**Step 3: Add DNS Records**

Navigate to: **DNS > Records**

Add these records:

```
1. Root Domain to Frontend:
   Type: CNAME
   Name: @ (or yatradiscover.com)
   Target: yatradiscover-prod.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)
   
2. www to Frontend:
   Type: CNAME
   Name: www
   Target: yatradiscover-prod.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)

3. API to Backend:
   Type: CNAME
   Name: api
   Target: yatradiscover-prod.railway.app
   TTL: Auto
   Proxy: Proxied (orange cloud)

4. Admin Portal (optional):
   Type: CNAME
   Name: admin
   Target: yatradiscover-admin.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)

5. Partners Portal (optional):
   Type: CNAME
   Name: partners
   Target: yatradiscover-partners.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)

6. Staging (optional):
   Type: CNAME
   Name: staging
   Target: yatradiscover-staging.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)
```

**Step 4: Update Nameservers at Registrar**

Cloudflare gives you 2 nameservers. Example:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

Go to your domain registrar:
- GoDaddy
- Namecheap
- Domain.com
- etc.

Update nameservers there. This takes 24-48 hours.

**Step 5: Configure SSL/TLS**

In Cloudflare dashboard:
```
1. Go to: SSL/TLS > Overview
2. Select: Full (strict)
3. Cloudflare handles the rest automatically
```

**Step 6: Configure Security**

In Cloudflare dashboard:
```
1. Security > Bot Management (Enable)
2. Security > DDoS (Enable)
3. Rules > WAF (Basic protection available)
4. Performance > Cache (Already optimal)
```

**Step 7: Verify Everything Works**

```powershell
# From your Windows machine:

# Check DNS resolution
nslookup yatradiscover.com
nslookup api.yatradiscover.com

# Check HTTPS
curl -I https://yatradiscover.com
curl -I https://api.yatradiscover.com

# Should see: HTTP/2 200
```

---

## 🎯 PHASE 4: ENVIRONMENT CONFIGURATION

### Backend Environment Variables

**File: `backend/.env.production`**

```bash
# Database
DATABASE_URL=postgresql://user:password@db.host:5432/yatradiscover

# Security
SECRET_KEY=your-secret-key-here-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# External APIs
OPENAI_API_KEY=sk-...
STRIPE_API_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

# CORS
ALLOWED_ORIGINS=["https://yatradiscover.com","https://www.yatradiscover.com"]

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
SENTRY_DSN=https://...

# Environment
ENVIRONMENT=production
DEBUG=False
```

### Frontend Environment Variables

**File: `frontend/web/.env.production`**

```bash
# API
NEXT_PUBLIC_API_URL=https://api.yatradiscover.com
NEXT_PUBLIC_APP_URL=https://www.yatradiscover.com

# Analytics (optional)
NEXT_PUBLIC_GA_ID=G-...

# Stripe (if using)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Environment
NEXT_PUBLIC_ENVIRONMENT=production
```

### Mobile Environment Variables

**File: `mobile/.env.production`**

```bash
# API
REACT_APP_API_URL=https://api.yatradiscover.com

# Google Maps (if using)
REACT_APP_GOOGLE_MAPS_API_KEY=...

# Stripe (if using)
REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Environment
REACT_APP_ENVIRONMENT=production
```

---

## 🎯 PHASE 5: DEPLOYMENT CHECKLIST

### Pre-Deployment (Before going live)

- [ ] Database migrations tested locally
- [ ] Backend API tested with Postman/curl
- [ ] Frontend builds locally: `npm run build`
- [ ] Mobile app builds locally
- [ ] Environment variables configured
- [ ] Secrets stored securely (not in code)
- [ ] CI/CD pipelines configured
- [ ] Git repository updated
- [ ] GitHub Actions workflows created

### Deployment Steps

1. **Deploy Database**
   - [ ] Supabase project created
   - [ ] Database migrations run: `alembic upgrade head`
   - [ ] Tables verified in Supabase dashboard

2. **Deploy Backend**
   - [ ] Railway project created
   - [ ] Environment variables set
   - [ ] Git push triggers automatic deploy
   - [ ] API endpoint responds: `curl https://api.yatradiscover.com/health`

3. **Deploy Frontend**
   - [ ] Vercel project created
   - [ ] Environment variables set
   - [ ] Git push triggers automatic deploy
   - [ ] Website loads: `https://www.yatradiscover.com`

4. **Configure DNS**
   - [ ] Cloudflare account created
   - [ ] Domain added to Cloudflare
   - [ ] DNS records created
   - [ ] Nameservers updated at registrar
   - [ ] Wait 24-48 hours for propagation
   - [ ] Verify: `nslookup yatradiscover.com`

5. **Configure SSL/TLS**
   - [ ] Cloudflare SSL set to "Full (strict)"
   - [ ] HTTPS redirect enabled
   - [ ] Certificate valid for all subdomains

6. **Post-Deployment Testing**
   - [ ] `https://yatradiscover.com` loads
   - [ ] `https://www.yatradiscover.com` loads
   - [ ] `https://api.yatradiscover.com/health` responds
   - [ ] Redirect: http → https works
   - [ ] Mobile app connects to API
   - [ ] Admin panel works (if applicable)

---

## 🛠️ TROUBLESHOOTING

### DNS Not Resolving

```powershell
# Check nameservers
nslookup -type=NS yatradiscover.com

# Should show:
# ns1.cloudflare.com
# ns2.cloudflare.com

# If not, update at domain registrar and wait 24-48 hours
```

### HTTPS Certificate Issues

```
Error: "SSL certificate problem"

Fix:
1. Wait 5-10 minutes (certificate is being created)
2. Cloudflare > SSL/TLS > ensure "Full (strict)"
3. Each hosting provider (Vercel, Railway) must generate cert
4. Wait 24 hours if problem persists
```

### API Not Responding

```
Error: "api.yatradiscover.com connection refused"

Fix:
1. Check Railway dashboard - is app running?
2. Check environment variables are set
3. Check database connection string is correct
4. Test locally: `python -m uvicorn app.main:app`
5. Check Railway logs for errors
```

### Frontend Can't Reach Backend

```
Error: "CORS error" in browser console

Fix:
1. Backend .env.production:
   ALLOWED_ORIGINS=["https://yatradiscover.com","https://www.yatradiscover.com"]
2. Frontend .env.production:
   NEXT_PUBLIC_API_URL=https://api.yatradiscover.com
3. Restart both applications
4. Clear browser cache (Ctrl+Shift+Delete)
```

---

## 📈 NEXT STEPS

### Immediate (Today)
- [ ] Choose hosting strategy: Vercel + Railway + Supabase
- [ ] Create Supabase account and database
- [ ] Deploy backend to Railway
- [ ] Deploy frontend to Vercel
- [ ] Add nameservers to Cloudflare

### Short-term (This Week)
- [ ] Update nameservers at domain registrar
- [ ] Verify DNS propagation
- [ ] Test all endpoints
- [ ] Set up monitoring/logging

### Medium-term (This Month)
- [ ] Set up CI/CD pipelines
- [ ] Configure automated backups
- [ ] Set up email notifications
- [ ] Deploy mobile app to App Store/Play Store

### Long-term (Ongoing)
- [ ] Monitor performance metrics
- [ ] Optimize database queries
- [ ] Scale as needed
- [ ] Regular security audits

---

## 📞 SUPPORT

### Hosting Provider Docs

- [Vercel Deployment Guide](https://vercel.com/docs)
- [Railway Deployment Guide](https://railway.app/docs)
- [Supabase Setup Guide](https://supabase.com/docs)
- [Cloudflare Setup Guide](https://developers.cloudflare.com/dns/)

### Quick Help Commands

```bash
# Test backend health
curl https://api.yatradiscover.com/health

# Check DNS
nslookup yatradiscover.com

# Check SSL certificate
curl -v https://yatradiscover.com 2>&1 | grep -i certificate

# Tail logs (from deployment platform)
# Railway: railway logs
# Vercel: vercel logs
```

---

**Ready to proceed?** Reply with:
- **"A"** for Vercel + Railway + Supabase (RECOMMENDED)
- **"B"** for AWS setup guide
- **"C"** for DigitalOcean setup guide
- **"HELP"** for specific step help

