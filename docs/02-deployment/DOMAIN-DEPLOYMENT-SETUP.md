# 🚀 YatraDiscover AI - Domain Deployment Setup Guide

**Domain:** yatradiscover.com  
**Status:** Ready for Deployment  
**Created:** 2026-11-19  
**Version:** 1.0

---

## 📋 TABLE OF CONTENTS

1. [Quick Start (5 mins)](#-quick-start-5-mins)
2. [Complete Deployment Path](#-complete-deployment-path)
3. [Architecture Overview](#-architecture-overview)
4. [Step-by-Step Setup](#-step-by-step-setup)
5. [Environment Configuration](#-environment-configuration)
6. [Deployment Checklist](#-deployment-checklist)

---

## ⚡ Quick Start (5 mins)

### YOUR SITUATION:
✅ Domain purchased: yatradiscover.com  
✅ Code ready: 19 API endpoints + documentation  
✅ Database ready: PostgreSQL with 15 models  
❌ Not yet deployed anywhere  

### YOUR GOAL:
Make yatradiscover.com point to your code

### WHAT YOU NEED:
1. **Hosting Provider** (Vercel, AWS, DigitalOcean, etc.)
2. **Database Host** (Supabase, AWS RDS, etc.)
3. **DNS Management** (Cloudflare - recommended)

---

## 🎯 Complete Deployment Path

### STEP 1: Choose Your Hosting (Decide)
**Duration:** 15 minutes  
**Effort:** Decision only

Choose ONE hosting provider:

**Option A: Vercel + Supabase (Easiest - RECOMMENDED) ⭐**
```
Frontend (Next.js) → Vercel (Free tier available)
Backend (FastAPI) → Vercel Functions OR separate server
Database (PostgreSQL) → Supabase (Free tier available)
```
- ✅ Easiest to deploy
- ✅ Free tier sufficient for MVP
- ✅ One-click deployments
- ✅ Built-in SSL/TLS

**Option B: DigitalOcean (Balanced)**
```
Everything → Single DigitalOcean App ($12/month)
Database → PostgreSQL managed DB ($15/month)
```
- ✅ All-in-one solution
- ✅ Good performance
- ✅ Affordable

**Option C: AWS (Scalable)**
```
Frontend → CloudFront + S3
Backend → EC2 OR API Gateway + Lambda
Database → RDS PostgreSQL
DNS → Route53
```
- ✅ Scales infinitely
- ✅ Expensive ($100+/month)
- ✅ Complex setup

**Option D: Self-Hosted (Custom Server)**
```
Everything → Your own VPS ($5-20/month)
Requires: Linux, Docker, Nginx, SSL
```
- ✅ Full control
- ✅ Cheapest
- ✅ Requires Linux knowledge

### STEP 2: Set Up Hosting (Do It)
**Duration:** 1-2 hours  
**Effort:** Follow provider's guide

**If choosing Vercel + Supabase:**

#### 2A. Create Supabase Database
```bash
1. Go to https://supabase.com
2. Click "Sign Up"
3. Create new project
4. Wait for database to be ready
5. Get connection string from "Settings > Database"
6. Store connection string safely
```

#### 2B. Deploy Backend to Vercel Functions
```bash
# In your repository
1. Go to https://vercel.com
2. Click "Import Project"
3. Select your GitHub repository
4. Configure environment variables:
   - DATABASE_URL=your_supabase_connection
   - API_KEY=your_secret_key
   - OPENAI_API_KEY=your_openai_key
5. Deploy
6. Get your backend URL: https://yatradiscover-api.vercel.app
```

#### 2C. Deploy Frontend to Vercel
```bash
1. Go to https://vercel.com
2. Import your GitHub repository (frontend)
3. Configure environment variables:
   - REACT_APP_API_URL=https://yatradiscover-api.vercel.app
4. Deploy
5. Get your frontend URL: https://yatradiscover.vercel.app
```

### STEP 3: Connect Domain to Hosting
**Duration:** 30 minutes  
**Effort:** DNS configuration

#### 3A. Get Your Hosting DNS Records
From your hosting provider, you'll receive:
- **For Vercel:** A CNAME record pointing to Vercel
- **For AWS:** CloudFront domain
- **For DigitalOcean:** Nameservers

#### 3B. Configure Domain DNS
**Option 1: Keep registrar, add DNS records (Easiest)**

1. Go to your domain registrar (GoDaddy, Namecheap, etc.)
2. Find "DNS Settings" or "Nameservers"
3. Add these records:

```
Root Domain (yatradiscover.com):
  Type: A
  Value: Your hosting IP or CNAME
  
www subdomain (www.yatradiscover.com):
  Type: CNAME
  Value: your-hosting-domain.com
  
api subdomain (api.yatradiscover.com):
  Type: CNAME
  Value: your-api-hosting-domain.com
```

**Option 2: Use Cloudflare (Recommended for security) ⭐**

1. Go to https://cloudflare.com
2. Click "Add Site"
3. Enter: yatradiscover.com
4. Select Free plan
5. Add these DNS records:

```
Name: @ (root)
Type: CNAME
Value: your-hosting-domain.com
Proxy: Proxied (orange cloud)

Name: www
Type: CNAME
Value: your-hosting-domain.com
Proxy: Proxied (orange cloud)

Name: api
Type: CNAME
Value: your-api-hosting-domain.com
Proxy: Proxied (orange cloud)
```

6. Update your domain nameservers to Cloudflare:
   - Go to domain registrar settings
   - Replace nameservers with Cloudflare's:
     - ns1.cloudflare.com
     - ns2.cloudflare.com
   - Wait 24-48 hours for DNS propagation

### STEP 4: Enable HTTPS (SSL/TLS)
**Duration:** 15 minutes  
**Effort:** 1-click setup

**If using Vercel:**
- ✅ Automatic! HTTPS enabled by default
- ✅ SSL certificate auto-renewed

**If using Cloudflare:**
1. Go to Cloudflare dashboard
2. Click "SSL/TLS"
3. Select "Full (strict)"
4. Wait for certificate generation
5. HTTPS enabled!

### STEP 5: Verify & Test
**Duration:** 15 minutes  
**Effort:** Testing

```bash
# Test DNS resolution
nslookup yatradiscover.com
# Should return your hosting IP

# Test HTTPS
curl -I https://yatradiscover.com
# Should return: HTTP/2 200

# Test subdomain
curl -I https://api.yatradiscover.com
# Should return: HTTP/2 200
```

---

## 🏗️ Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                    yatradiscover.com                           │
│                                                                │
│  Cloudflare / DNS Provider                                    │
│  ├─ Manages DNS records                                       │
│  ├─ Provides CDN (caching)                                    │
│  ├─ Handles SSL/TLS                                           │
│  └─ DDoS protection                                           │
│         ↓                                                       │
├────────┼────────┬────────────┬──────────────┬────────────────┤
│        │        │            │              │                │
▼        ▼        ▼            ▼              ▼                ▼
─────────────────────────────────────────────────────────────────
yatra   www.    api.         admin.        partners.        staging.
                                                               
Main    Docs   FastAPI       Admin        Partner           Staging
Site    Site   Backend       Portal       Portal            Env
│        │      │             │            │                 │
└────┬───┴──┬───┴──────┬──────┴────┬───────┘                 │
     │      │          │           │                          │
     ▼      ▼          ▼           ▼                          ▼
   Vercel (Frontend)  Vercel Functions  (Backend)       Vercel Preview
   
     ↓
   ┌─────────────────────────────────────────────────┐
   │      Supabase PostgreSQL Database               │
   │  ├─ Hotels (500+ records)                       │
   │  ├─ Restaurants (500+ records)                  │
   │  ├─ Attractions (500+ records)                  │
   │  ├─ Users                                        │
   │  ├─ Reviews & Ratings                           │
   │  └─ Bookings                                     │
   └─────────────────────────────────────────────────┘
```

---

## 📝 Step-by-Step Setup

### PHASE 1: Database Setup (1 hour)

#### Step 1.1: Create Supabase Project
```bash
1. Visit https://supabase.com
2. Sign up with email
3. Create new project (choose region closest to users)
4. Wait for initialization (5-10 minutes)
5. Copy connection string
```

#### Step 1.2: Run Database Migrations
```bash
# Clone your code
git clone https://github.com/jash242214/yatradiscover.git
cd yatradiscover/backend

# Set environment variable
export DATABASE_URL="postgresql://user:password@host:5432/database"

# Run migrations
python -m alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
```

#### Step 1.3: Seed Sample Data
```bash
# Create seed script
python scripts/seed_data.py

# Verify data loaded
psql $DATABASE_URL -c "SELECT COUNT(*) FROM hotels;"
```

### PHASE 2: Backend Deployment (1-2 hours)

#### Step 2.1: Prepare Backend for Production
```bash
# Update settings
backend/app/config.py:
  ENVIRONMENT = "production"
  DEBUG = False
  CORS_ORIGINS = ["https://yatradiscover.com"]

# Update secrets
Create .env.production with:
  DATABASE_URL=your_supabase_url
  OPENAI_API_KEY=your_key
  SECRET_KEY=generate_secure_key
  API_KEY=generate_secure_key
```

#### Step 2.2: Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy backend
cd backend
vercel --prod

# Get deployment URL
# Your backend is now at: https://yatradiscover-api.vercel.app
```

#### Step 2.3: Configure Environment
```bash
# In Vercel dashboard:
1. Go to your project settings
2. Environment Variables
3. Add:
   - DATABASE_URL=your_supabase_url
   - OPENAI_API_KEY=your_key
   - ENVIRONMENT=production
   - DEBUG=false
4. Redeploy
```

### PHASE 3: Frontend Deployment (1 hour)

#### Step 3.1: Prepare Frontend
```bash
# Update config
frontend/.env.production:
  REACT_APP_API_URL=https://yatradiscover-api.vercel.app
  REACT_APP_ENV=production

# Build test
npm run build
```

#### Step 3.2: Deploy Frontend
```bash
# Deploy to Vercel
cd frontend
vercel --prod

# Get deployment URL
# Your frontend is now at: https://yatradiscover.vercel.app
```

### PHASE 4: Domain Configuration (30 mins)

#### Step 4.1: Connect Domain to Vercel
```bash
# In Vercel dashboard:
1. Go to project settings
2. Domains
3. Add custom domain: yatradiscover.com
4. Add subdomain: www.yatradiscover.com
5. Add subdomain: api.yatradiscover.com
```

#### Step 4.2: Update DNS at Registrar
```bash
# Go to your registrar (GoDaddy, Namecheap, etc.)
1. Find DNS/Nameserver settings
2. Update nameservers to Vercel's (they'll provide):
   - cname.vercel-dns.com
3. Wait 24-48 hours for propagation
```

#### Step 4.3: Verify Domain
```bash
# After 24 hours:
1. Visit https://yatradiscover.com
2. Should load your frontend
3. Visit https://api.yatradiscover.com
4. Should return API endpoints
```

### PHASE 5: Security & HTTPS (30 mins)

#### Step 5.1: Enable Cloudflare (Optional but Recommended)
```bash
1. Visit https://cloudflare.com
2. Add site: yatradiscover.com
3. Update nameservers to Cloudflare
4. Configure SSL: Full (strict)
5. Enable DDoS protection
6. Wait for HTTPS cert
```

#### Step 5.2: Configure HTTPS Redirects
```bash
# In backend/app/main.py:
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
app.add_middleware(HTTPSRedirectMiddleware)

# In frontend build:
# Vercel handles this automatically
```

#### Step 5.3: Security Headers
```bash
# In backend:
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response
```

---

## 🔧 Environment Configuration

### Development Environment
```bash
# .env.development
DATABASE_URL=postgresql://localhost:5432/yatradiscover_dev
ENVIRONMENT=development
DEBUG=True
API_KEY=dev_key_12345
SECRET_KEY=dev_secret
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

### Staging Environment
```bash
# .env.staging
DATABASE_URL=postgresql://user@supabase:password@db.supabase.co:5432/database
ENVIRONMENT=staging
DEBUG=True
API_KEY=staging_key_xxxx
SECRET_KEY=staging_secret_xxxx
CORS_ORIGINS=["https://staging.yatradiscover.com"]
```

### Production Environment
```bash
# .env.production (NEVER commit this!)
DATABASE_URL=postgresql://user@supabase:password@db.supabase.co:5432/database
ENVIRONMENT=production
DEBUG=False
API_KEY=prod_key_xxxx (use Vercel Secrets)
SECRET_KEY=prod_secret_xxxx (use Vercel Secrets)
OPENAI_API_KEY=sk-xxxx
CORS_ORIGINS=["https://yatradiscover.com", "https://www.yatradiscover.com"]
```

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] All code committed to GitHub
- [ ] Environment variables configured
- [ ] Database migrations tested locally
- [ ] Frontend builds without errors
- [ ] API endpoints tested with sample data
- [ ] SSL certificates obtained
- [ ] Backups created

### DNS Configuration
- [ ] Domain registered ✅ (yatradiscover.com)
- [ ] Registrar updated with hosting nameservers
- [ ] DNS records created:
  - [ ] Root domain (yatradiscover.com)
  - [ ] www subdomain
  - [ ] api subdomain
  - [ ] staging subdomain (optional)
- [ ] DNS propagation verified (24-48 hours)
- [ ] DNS resolution tested with nslookup

### Frontend Deployment
- [ ] Frontend code deployed to Vercel
- [ ] Environment variables configured
- [ ] API endpoint URL correct in config
- [ ] Build succeeds
- [ ] Site loads at https://yatradiscover.com

### Backend Deployment
- [ ] Backend code deployed to Vercel
- [ ] Database migrations applied
- [ ] Sample data seeded
- [ ] Environment variables configured
- [ ] API endpoints accessible at https://api.yatradiscover.com
- [ ] /api/v2/hotels/best-value returns data

### Security
- [ ] HTTPS enabled on all subdomains
- [ ] SSL/TLS certificate valid
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] API keys stored in secrets (not in code)
- [ ] Database credentials not exposed
- [ ] Cloudflare DDoS protection enabled

### Testing
- [ ] Can access https://yatradiscover.com
- [ ] Can access https://www.yatradiscover.com
- [ ] Can access https://api.yatradiscover.com
- [ ] Hotel search endpoint returns data
- [ ] Restaurant search endpoint returns data
- [ ] Attraction search endpoint returns data
- [ ] Authentication working (if implemented)
- [ ] Error handling works (try invalid request)
- [ ] Rate limiting works (if implemented)

### Monitoring
- [ ] Error tracking set up (Sentry, etc.)
- [ ] Performance monitoring set up
- [ ] Database backups configured
- [ ] Log aggregation set up
- [ ] Alerts configured for failures

### Documentation
- [ ] Deployment guide created
- [ ] Runbook documented
- [ ] Environment variables documented
- [ ] Disaster recovery plan created
- [ ] Team notified of deployment

---

## 🚀 Quick Reference - Which Hosting?

### FOR MVP (Fastest):
**Vercel + Supabase**
```
Timeline: 3-4 hours
Cost: $0 (free tier)
Effort: Easy
Perfect for: Getting started quickly
```

### FOR SCALE:
**DigitalOcean App**
```
Timeline: 2-3 hours
Cost: $27/month
Effort: Medium
Perfect for: Growing app with good performance
```

### FOR ENTERPRISE:
**AWS**
```
Timeline: 1-2 days
Cost: $200+/month
Effort: Hard
Perfect for: Massive scale and control
```

---

## 🆘 Troubleshooting

### Domain not resolving?
```bash
# Check DNS propagation
nslookup yatradiscover.com
# Should show your hosting provider's IP

# If not, wait 24-48 hours for DNS propagation
# Check: https://www.whatsmydns.net/?domain=yatradiscover.com
```

### HTTPS certificate error?
```bash
# Wait 24-48 hours for certificate issuance
# Check certificate status at:
# https://www.ssllabs.com/ssltest/analyze.html?d=yatradiscover.com
```

### Backend not responding?
```bash
# Check environment variables in Vercel
# Check logs: vercel logs

# Test locally:
export DATABASE_URL=your_url
npm run dev  # or python -m uvicorn app.main:app
```

### Database not connecting?
```bash
# Verify connection string format:
# postgresql://user:password@host:5432/database

# Test connection:
psql your_connection_string -c "SELECT 1"

# If fails, check:
# 1. Username and password correct
# 2. Host is correct
# 3. Database exists
# 4. Network access allowed (IP whitelisted)
```

---

## 📚 Additional Resources

**Vercel Deployment:**
- https://vercel.com/docs/deployments/overview
- https://vercel.com/docs/environment-variables

**Supabase Setup:**
- https://supabase.com/docs/guides/getting-started
- https://supabase.com/docs/guides/database

**Cloudflare Setup:**
- https://developers.cloudflare.com/dns/
- https://developers.cloudflare.com/ssl/

**FastAPI Deployment:**
- https://fastapi.tiangolo.com/deployment/
- https://fastapi.tiangolo.com/advanced/security/

**Next.js Deployment:**
- https://nextjs.org/docs/deployment/vercel
- https://nextjs.org/docs/advanced-features/environment-variables

---

## 🎯 NEXT IMMEDIATE STEPS

1. **Choose Hosting** (15 mins)
   - Vercel + Supabase (RECOMMENDED for MVP)

2. **Set Up Database** (1 hour)
   - Create Supabase account
   - Run migrations
   - Seed data

3. **Deploy Backend** (1 hour)
   - Deploy to Vercel Functions
   - Configure environment variables

4. **Deploy Frontend** (1 hour)
   - Deploy to Vercel
   - Point to backend

5. **Connect Domain** (30 mins)
   - Add DNS records
   - Wait for propagation

6. **Enable HTTPS** (15 mins)
   - Set up Cloudflare (optional)
   - Verify HTTPS works

**Total Time: 4-5 hours**  
**Result: Live website at yatradiscover.com ✅**

---

## ❓ QUESTIONS?

**Q: Do I need to pay for hosting?**
A: No! Use free tiers (Vercel + Supabase free tier is sufficient for MVP)

**Q: How long for DNS to work?**
A: 24-48 hours typically. Use https://www.whatsmydns.net/ to check.

**Q: Can I change hosting later?**
A: Yes! Just update DNS records. All your data is portable.

**Q: What if something breaks?**
A: See rollback-plan.md in infrastructure/ folder

**Q: How much will it cost?**
A: MVP = $0/month (free tiers)
   Production = $27-100+/month depending on traffic

---

**Last Updated:** 2026-11-19  
**Status:** Ready to Deploy  
**Next Step:** Choose hosting and start deployment

🚀 **You're ready to go live!**
