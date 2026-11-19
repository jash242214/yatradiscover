# YatraDiscover AI - Deployment Quick Start

This directory contains all documentation needed to deploy YatraDiscover to production.

## 📋 Quick Links

1. **[DEPLOYMENT-COMPLETE-GUIDE.md](../DEPLOYMENT-COMPLETE-GUIDE.md)** - Full step-by-step deployment guide
2. **[DOMAIN-DEPLOYMENT-SETUP.md](../DOMAIN-DEPLOYMENT-SETUP.md)** - Domain configuration guide
3. **[dns-records-plan.md](./cloudflare/dns-records-plan.md)** - DNS records for Cloudflare
4. **[production-checklist.md](./cloudflare/production-checklist.md)** - Pre-launch checklist

## 🚀 Quick Start (5 minutes)

**Choose your hosting strategy:**

### Option A: RECOMMENDED - Vercel + Railway + Supabase ⭐

```bash
# 1. Frontend: Deploy to Vercel
#    Go to https://vercel.com
#    Import: jash242214/yatradiscover
#    Add domains: yatradiscover.com, www.yatradiscover.com

# 2. Backend: Deploy to Railway
#    Go to https://railway.app
#    Import: jash242214/yatradiscover
#    Add domain: api.yatradiscover.com

# 3. Database: Create on Supabase
#    Go to https://supabase.com
#    Create project: yatradiscover-prod
#    Run migrations: alembic upgrade head

# 4. DNS: Configure on Cloudflare
#    Go to https://cloudflare.com
#    Add site: yatradiscover.com
#    Add nameservers to your domain registrar
```

**Cost:** $0-50/month (free tier available)
**Setup Time:** 2 hours
**Difficulty:** Easy

### Option B: AWS (Advanced)

See [DEPLOYMENT-COMPLETE-GUIDE.md](../DEPLOYMENT-COMPLETE-GUIDE.md) for detailed AWS setup.

### Option C: DigitalOcean (Balanced)

See [DEPLOYMENT-COMPLETE-GUIDE.md](../DEPLOYMENT-COMPLETE-GUIDE.md) for detailed DigitalOcean setup.

## 📝 Configuration Files

Before deployment, configure:

1. **Backend:** `backend/.env.production`
   - Copy from: `backend/.env.production.example`
   - Add database URL from Supabase
   - Add API keys (OpenAI, Stripe, etc.)

2. **Frontend:** `frontend/web/.env.production`
   - Copy from: `frontend/web/.env.production.example`
   - Set `NEXT_PUBLIC_API_URL=https://api.yatradiscover.com`

3. **Backend Deployment Config:**
   - `backend/Procfile` - Deployment command ✅ (already created)
   - `backend/runtime.txt` - Python version ✅ (already created)

## 🔐 Security Checklist

Before going live:

- [ ] Never commit `.env.production` files
- [ ] Store secrets in deployment platform (Vercel, Railway)
- [ ] Use environment variables for all sensitive data
- [ ] Enable HTTPS on all domains
- [ ] Configure CORS properly
- [ ] Set up API rate limiting
- [ ] Enable DDoS protection (Cloudflare)
- [ ] Configure database backups
- [ ] Set up monitoring and logging

## 📊 Architecture After Deployment

```
┌─────────────────────────────────────────────────────┐
│                   CloudFlare DNS                      │
│              (DDoS, WAF, SSL/TLS, CDN)                │
└──────────────────┬──────────────────────────────────┘
                   │
       ┌───────────┼───────────┐
       │           │           │
   www.yd.com   api.yd.com  admin.yd.com
       │           │           │
       ▼           ▼           ▼
    Vercel      Railway    Vercel/NextJS
   (Frontend)  (Backend)   (Admin Panel)
       │           │
       └─────┬─────┘
           │
           ▼
        Supabase
      (PostgreSQL)
```

## 🧪 Testing After Deployment

```bash
# Check DNS resolution
nslookup yatradiscover.com

# Check HTTPS
curl -I https://yatradiscover.com
curl -I https://api.yatradiscover.com

# Check API health
curl https://api.yatradiscover.com/health

# Check SSL certificate
curl -v https://yatradiscover.com 2>&1 | grep -i "certificate"
```

## 📞 Support & Next Steps

1. **Read:** [DEPLOYMENT-COMPLETE-GUIDE.md](../DEPLOYMENT-COMPLETE-GUIDE.md)
2. **Choose:** Option A, B, or C
3. **Follow:** Step-by-step guide for your choice
4. **Configure:** Environment variables
5. **Deploy:** Push to GitHub (auto-deploy on Vercel/Railway)
6. **Verify:** Run testing commands above
7. **Monitor:** Set up logging and alerts

## 🎯 Timeline

- **Day 1:** Database setup + Backend deploy
- **Day 2:** Frontend deploy + DNS configuration
- **Day 3-5:** DNS propagation + Testing
- **Day 5+:** Production live! 🚀

---

**Start with:** [DEPLOYMENT-COMPLETE-GUIDE.md](../DEPLOYMENT-COMPLETE-GUIDE.md)
