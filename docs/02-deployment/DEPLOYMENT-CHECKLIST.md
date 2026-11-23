# 📋 YatraDiscover AI - Complete Deployment Checklist

**Domain:** yatradiscover.com  
**Status:** Ready for Deployment  
**Last Updated:** 2024

---

## 🔄 PHASE 1: PRE-DEPLOYMENT SETUP

### Code Preparation

- [ ] All code committed to GitHub: `jash242214/yatradiscover`
- [ ] Backend FastAPI app working locally
- [ ] Frontend Next.js app initialized (or working locally)
- [ ] Database migrations created with Alembic
- [ ] All environment variables documented
- [ ] No hardcoded secrets in code
- [ ] `.gitignore` excludes `.env` files

**Verify:**
```bash
cd D:\yatradiscover
git status  # Should show clean working directory
```

### Documentation Created

- [ ] ✅ DEPLOYMENT-COMPLETE-GUIDE.md
- [ ] ✅ QUICK-DEPLOYMENT-SUMMARY.md
- [ ] ✅ infrastructure/README.md
- [ ] ✅ backend/Procfile
- [ ] ✅ backend/runtime.txt
- [ ] ✅ backend/.env.production.example
- [ ] ✅ frontend/web/.env.production.example

---

## 🎯 PHASE 2: CHOOSE & SETUP HOSTING

### Decision: Which Option?

- [ ] **Option A:** Vercel + Railway + Supabase (RECOMMENDED) ⭐
- [ ] **Option B:** AWS (CloudFront + EC2 + RDS)
- [ ] **Option C:** DigitalOcean App Platform

**Selected Option:** ___________

---

### IF OPTION A: Vercel + Railway + Supabase ⭐

#### Step 1: Create Supabase Database (20 mins)

- [ ] Go to https://supabase.com
- [ ] Sign up with GitHub
- [ ] Create new project:
  - [ ] Project name: `yatradiscover-prod`
  - [ ] Database password: `[strong password]`
  - [ ] Region: Choose closest to users
- [ ] Wait for database creation (2-3 minutes)
- [ ] Go to Settings > Database
- [ ] Copy connection string
- [ ] Store in secure location (password manager)

**Connection String Format:**
```
postgresql://postgres:[password]@[db].[region].supabase.co:5432/postgres
```

#### Step 2: Deploy Backend to Railway (30 mins)

- [ ] Go to https://railway.app
- [ ] Sign up with GitHub
- [ ] Create new project → "Deploy from GitHub repo"
- [ ] Select: `jash242214/yatradiscover`
- [ ] Railway auto-detects Python/FastAPI
- [ ] Set environment variables:
  - [ ] `DATABASE_URL` = [from Supabase]
  - [ ] `SECRET_KEY` = [generate new]
  - [ ] `OPENAI_API_KEY` = [your key]
  - [ ] `STRIPE_API_KEY` = [if needed]
  - [ ] `ENVIRONMENT` = `production`
- [ ] Deploy button → starts automatic deploy
- [ ] Wait for deployment to complete (3-5 minutes)
- [ ] Copy Railway-provided URL for backend
- [ ] Add custom domain: `api.yatradiscover.com`
  - [ ] Railway dashboard → Settings → Custom Domains
  - [ ] Copy DNS value provided by Railway

**Expected Backend URL:** `https://api.yatradiscover.com`

#### Step 3: Deploy Frontend to Vercel (30 mins)

- [ ] Go to https://vercel.com
- [ ] Sign up with GitHub
- [ ] Click "Import Project"
- [ ] Select: `jash242214/yatradiscover`
- [ ] Framework preset: Next.js
- [ ] Set environment variables:
  - [ ] `NEXT_PUBLIC_API_URL` = `https://api.yatradiscover.com`
  - [ ] `NEXT_PUBLIC_APP_URL` = `https://www.yatradiscover.com`
- [ ] Deploy button → starts automatic deploy
- [ ] Wait for deployment to complete (3-5 minutes)
- [ ] Copy Vercel-provided URL
- [ ] Add custom domains:
  - [ ] `yatradiscover.com`
  - [ ] `www.yatradiscover.com`
- [ ] Save DNS values provided by Vercel

**Expected Frontend URL:** `https://www.yatradiscover.com`

#### Step 4: Create Cloudflare Account (10 mins)

- [ ] Go to https://cloudflare.com
- [ ] Sign up (use GitHub or email)
- [ ] Click "Add site"
- [ ] Enter: `yatradiscover.com`
- [ ] Click "Free" plan
- [ ] Continue through setup
- [ ] Keep browser tab open (you'll need DNS values)

---

### IF OPTION B: AWS

[See DEPLOYMENT-COMPLETE-GUIDE.md for AWS steps]

---

### IF OPTION C: DigitalOcean

[See DEPLOYMENT-COMPLETE-GUIDE.md for DigitalOcean steps]

---

## 🌐 PHASE 3: DNS CONFIGURATION

### Critical: Get DNS Values First

Before this step, ensure you have:

- [ ] Supabase connection string ✅
- [ ] Railway backend URL ✅
- [ ] Vercel frontend URLs ✅
- [ ] Cloudflare account created ✅

### In Cloudflare Dashboard

Navigate to: **DNS > Records**

#### Add DNS Records

**Record 1: Root Domain to Frontend**
```
Type:   CNAME
Name:   @ (root)
Target: yatradiscover-prod.vercel.app
TTL:    Auto
Proxy:  Proxied (orange cloud)
```
- [ ] Record created
- [ ] Verifying...

**Record 2: www to Frontend**
```
Type:   CNAME
Name:   www
Target: yatradiscover-prod.vercel.app
TTL:    Auto
Proxy:  Proxied (orange cloud)
```
- [ ] Record created
- [ ] Verifying...

**Record 3: api to Backend**
```
Type:   CNAME
Name:   api
Target: yatradiscover-prod.railway.app
TTL:    Auto
Proxy:  Proxied (orange cloud)
```
- [ ] Record created
- [ ] Verifying...

**Record 4: admin to Admin Dashboard (optional)**
```
Type:   CNAME
Name:   admin
Target: yatradiscover-admin.vercel.app
TTL:    Auto
Proxy:  Proxied (orange cloud)
```
- [ ] Record created (if deploying admin panel)

**Record 5: partners to Partners Portal (optional)**
```
Type:   CNAME
Name:   partners
Target: yatradiscover-partners.vercel.app
TTL:    Auto
Proxy:  Proxied (orange cloud)
```
- [ ] Record created (if deploying partners portal)

**Record 6: staging to Staging Site (optional)**
```
Type:   CNAME
Name:   staging
Target: yatradiscover-staging.vercel.app
TTL:    Auto
Proxy:  Proxied (orange cloud)
```
- [ ] Record created (if deploying staging site)

### Update Nameservers at Registrar

Cloudflare provides 2 nameservers. Example:
```
ns1.cloudflare.com
ns2.cloudflare.com
```

Go to your domain registrar (GoDaddy, Namecheap, Domain.com, etc.):

- [ ] Log in to domain registrar
- [ ] Find "Nameservers" or "DNS Settings"
- [ ] Delete old nameservers
- [ ] Add Cloudflare nameservers:
  - [ ] `ns1.cloudflare.com`
  - [ ] `ns2.cloudflare.com`
- [ ] Save changes
- [ ] ⏰ Wait 24-48 hours for DNS propagation

**Note:** This is critical. Everything depends on this step!

---

## 🔐 PHASE 4: SSL/TLS CONFIGURATION

### Configure HTTPS in Cloudflare

Navigate to: **SSL/TLS > Overview**

- [ ] Select: "Full (strict)"
- [ ] This enables HTTPS for all domains
- [ ] Cloudflare handles certificate automatically

### Enable HTTPS Redirect

Navigate to: **Rules > Page Rules**

- [ ] Click "Create Page Rule"
- [ ] URL: `http://*yatradiscover.com/*`
- [ ] Setting: "Always Use HTTPS"
- [ ] Save and Deploy

Repeat for:
- [ ] `http://*api.yatradiscover.com/*`
- [ ] Any other subdomains

### Verify SSL Certificate

Each hosting provider will generate certificates:

- [ ] Vercel: Automatic ✅
- [ ] Railway: Automatic ✅
- [ ] Supabase: Automatic ✅
- [ ] Cloudflare: Manages centrally ✅

No action needed - all automatic!

---

## 🛡️ PHASE 5: SECURITY CONFIGURATION

### Configure Security in Cloudflare

Navigate to: **Security > Settings**

- [ ] Security Level: "High"
- [ ] Challenge Passage: "30 minutes"
- [ ] Browser Integrity Check: "On"

### Enable Bot Management

Navigate to: **Security > Bots**

- [ ] Enable: "Bot Fight Mode"
- [ ] This protects against automated attacks

### Configure WAF (Web Application Firewall)

Navigate to: **Security > WAF**

- [ ] Enable: "OWASP ModSecurity Core Rule Set"
- [ ] This blocks common web attacks

### Configure DDoS Protection

Navigate to: **Security > DDoS Protection**

- [ ] Status: Enabled (automatic)
- [ ] Sensitivity: "High"

### Configure Rate Limiting

Navigate to: **Security > Rate Limiting**

- [ ] Create rule for login endpoint:
  - [ ] Threshold: 10 requests per 10 seconds
  - [ ] Action: Challenge
- [ ] Create rule for API endpoints:
  - [ ] Threshold: 100 requests per minute
  - [ ] Action: Challenge

---

## 📊 PHASE 6: VERIFY DEPLOYMENT

### Wait for DNS Propagation

⏰ **WAIT 24-48 HOURS** after updating nameservers

You can check status:

```powershell
# From your Windows machine
nslookup yatradiscover.com

# Should show Cloudflare nameservers:
# ns1.cloudflare.com
# ns2.cloudflare.com
```

### Test DNS Resolution

Once DNS propagates:

```powershell
# Test each domain
nslookup yatradiscover.com
nslookup www.yatradiscover.com
nslookup api.yatradiscover.com
nslookup admin.yatradiscover.com (if deployed)
```

Expected output: IP address or Cloudflare IP

- [ ] yatradiscover.com resolves
- [ ] www.yatradiscover.com resolves
- [ ] api.yatradiscover.com resolves

### Test HTTPS Connectivity

```powershell
# Check HTTPS works
curl -I https://yatradiscover.com
curl -I https://www.yatradiscover.com
curl -I https://api.yatradiscover.com

# Should show: HTTP/2 200 OK
```

- [ ] https://yatradiscover.com responds
- [ ] https://www.yatradiscover.com responds
- [ ] https://api.yatradiscover.com responds

### Test API Health

```powershell
# Check backend health
curl https://api.yatradiscover.com/health

# Should respond with: {"status": "ok"}
```

- [ ] API health check responds
- [ ] Database connection works

### Test Frontend Load

Open in browser:

- [ ] https://yatradiscover.com loads
- [ ] https://www.yatradiscover.com loads
- [ ] No SSL certificate warnings
- [ ] Page content displays correctly
- [ ] API calls work from browser

### Test SSL Certificate

```powershell
# Check certificate details
curl -v https://yatradiscover.com 2>&1 | Select-String "certificate"

# Should show:
# subject: CN=yatradiscover.com
# issuer: CN=...
```

- [ ] SSL certificate valid
- [ ] Certificate issued by Cloudflare/Hosting provider
- [ ] Certificate covers all subdomains

---

## 🎉 PHASE 7: POST-DEPLOYMENT

### Monitor First 24 Hours

After going live, monitor:

- [ ] Check Cloudflare dashboard for attacks/issues
- [ ] Monitor Railway backend logs
- [ ] Monitor Vercel frontend logs
- [ ] Check database performance in Supabase

### Set Up Monitoring & Alerts

- [ ] Configure Cloudflare notifications
- [ ] Set up Railway alerts
- [ ] Set up Vercel notifications
- [ ] Enable Sentry error tracking (optional)

### Database Backup

- [ ] Supabase: Automatic backups enabled ✅
- [ ] Verify backup schedule in Supabase settings
- [ ] Test restore process

### Logging & Analytics

- [ ] Configure Google Analytics (optional)
- [ ] Set up API logging
- [ ] Configure error tracking
- [ ] Set up performance monitoring

---

## 📝 PHASE 8: DOCUMENTATION & HANDOFF

### Documentation Complete

- [ ] Deployment guide created: DEPLOYMENT-COMPLETE-GUIDE.md
- [ ] Architecture documented
- [ ] Environment variables documented
- [ ] Disaster recovery plan created
- [ ] Team trained on deployment process

### Team Knowledge Transfer

- [ ] Show team Cloudflare dashboard
- [ ] Show team Railway dashboard
- [ ] Show team Vercel dashboard
- [ ] Show team Supabase dashboard
- [ ] Walk through emergency procedures

---

## ✅ PRODUCTION READINESS CHECKLIST

Before declaring "LIVE":

**Code Quality**
- [ ] No console.log() statements in production code
- [ ] No hardcoded secrets anywhere
- [ ] All dependencies up-to-date
- [ ] No security vulnerabilities (run: `npm audit`)

**Performance**
- [ ] Frontend loads in < 3 seconds
- [ ] API responds in < 500ms
- [ ] Database queries optimized
- [ ] CDN caching configured

**Security**
- [ ] HTTPS enforced on all domains
- [ ] SSL/TLS: Full (strict)
- [ ] DDoS protection enabled
- [ ] Rate limiting configured
- [ ] Bot protection enabled
- [ ] CORS properly configured
- [ ] Database backups automated
- [ ] Secrets not in code

**Reliability**
- [ ] Health check endpoint working
- [ ] Database monitored
- [ ] Error tracking enabled
- [ ] Logging centralized
- [ ] Alerts configured
- [ ] Runbook created for common issues

**Documentation**
- [ ] README updated
- [ ] API documentation complete
- [ ] Deployment guide written
- [ ] Troubleshooting guide created

---

## 🚨 TROUBLESHOOTING QUICK REFERENCE

### DNS Not Resolving

**Problem:** `nslookup yatradiscover.com` fails

**Solution:**
1. Verify nameservers updated at registrar
2. Wait 24-48 hours for DNS propagation
3. Check in Cloudflare that domain shows "Active"
4. Clear DNS cache: `ipconfig /flushdns`

### HTTPS Certificate Error

**Problem:** "SSL certificate problem" error

**Solution:**
1. Wait 5-10 minutes (certificate is being created)
2. Clear browser cache
3. Verify Cloudflare SSL is "Full (strict)"
4. Check each provider generated certificates

### API Not Responding

**Problem:** `curl https://api.yatradiscover.com` fails

**Solution:**
1. Check Railway dashboard - is app running?
2. Check environment variables in Railway
3. Check database URL is correct
4. Check Railway logs for errors
5. Try local test: `python -m uvicorn app.main:app`

### Frontend Can't Reach Backend

**Problem:** Browser console shows CORS error

**Solution:**
1. Update backend .env.production:
   ```
   ALLOWED_ORIGINS=["https://yatradiscover.com","https://www.yatradiscover.com"]
   ```
2. Update frontend .env.production:
   ```
   NEXT_PUBLIC_API_URL=https://api.yatradiscover.com
   ```
3. Restart both applications
4. Clear browser cache (Ctrl+Shift+Delete)

---

## 📞 SUPPORT RESOURCES

**Official Documentation:**
- [Cloudflare Docs](https://developers.cloudflare.com)
- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://railway.app/docs)
- [Supabase Docs](https://supabase.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Next.js Docs](https://nextjs.org/docs)

**Community Help:**
- Cloudflare Community: https://community.cloudflare.com
- Stack Overflow: Tag with `cloudflare`, `vercel`, `railway`
- GitHub Issues: Post in jash242214/yatradiscover

---

## 🎓 Timeline

| Day | Phase | Duration | Status |
|-----|-------|----------|--------|
| 1 | Database Setup | 20 min | ⏳ Pending |
| 1 | Backend Deploy | 30 min | ⏳ Pending |
| 1 | Frontend Deploy | 30 min | ⏳ Pending |
| 1 | DNS & Cloudflare | 30 min | ⏳ Pending |
| 2-3 | DNS Propagation | 24-48 hrs | ⏳ Pending |
| 3+ | Verification | 1-2 hrs | ⏳ Pending |
| 3+ | 🎉 PRODUCTION LIVE | ✅ Ready | ⏳ Pending |

---

**Status:** Ready to Deploy  
**Next Step:** Choose Option A/B/C and start Phase 2  
**Questions?** Check DEPLOYMENT-COMPLETE-GUIDE.md or reply with HELP: [question]

