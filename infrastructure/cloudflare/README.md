# YatraDiscover AI – Cloudflare Infrastructure Setup

## Overview

This documentation covers the complete Cloudflare infrastructure setup for YatraDiscover AI, a production-ready AI-powered travel planning platform.

**Domain:** `yatradiscover.com`

## What Cloudflare Provides

- **DNS Management** – Authoritative DNS for yatradiscover.com
- **HTTPS / SSL/TLS** – Automatic SSL certificate provisioning and renewal
- **Content Delivery Network (CDN)** – Global edge network for fast content delivery
- **DDoS Protection** – Automatic and manual DDoS mitigation
- **Web Application Firewall (WAF)** – Protection against common web exploits
- **Performance Optimization** – Caching, minification, and optimization
- **Analytics & Monitoring** – Traffic insights and threat detection

## Plan Overview

### Phase 1: Preparation (This Document)
- [ ] Verify existing DNS records at current registrar
- [ ] Document all email records (MX, SPF, DKIM, DMARC)
- [ ] Create DNS configuration plan with placeholders
- [ ] Design subdomain architecture

### Phase 2: Cloudflare Onboarding
- [ ] Add domain to Cloudflare Free plan
- [ ] Review imported DNS records
- [ ] Update nameservers at domain registrar
- [ ] Wait for DNS propagation (24-48 hours)
- [ ] Verify nameserver configuration

### Phase 3: Security & SSL
- [ ] Generate Cloudflare origin certificate
- [ ] Configure SSL/TLS settings (Full Strict mode)
- [ ] Enable HTTPS redirects
- [ ] Configure security headers
- [ ] Enable DDoS protection

### Phase 4: DNS Configuration
- [ ] Configure A/CNAME records for all subdomains
- [ ] Set proxy status for each record
- [ ] Verify DNS resolution
- [ ] Test routing to origin servers

### Phase 5: Application Integration
- [ ] Configure API rate limiting
- [ ] Set up WAF rules for API endpoints
- [ ] Configure CORS policies
- [ ] Disable caching for authenticated endpoints
- [ ] Test end-to-end routing

### Phase 6: Production Validation
- [ ] Run deployment readiness checks
- [ ] Verify SSL certificate chain
- [ ] Test DDoS protection
- [ ] Validate performance metrics
- [ ] Document rollback procedures

## Subdomain Architecture

| Subdomain | Purpose | Service | Proxy |
|-----------|---------|---------|-------|
| `yatradiscover.com` | Main marketing website | Frontend (React/Next.js) | ✓ Proxied |
| `www.yatradiscover.com` | Customer-facing website | Frontend (React/Next.js) | ✓ Proxied |
| `api.yatradiscover.com` | FastAPI backend | Python FastAPI | ✓ Proxied |
| `admin.yatradiscover.com` | Admin portal | React/Next.js | ✓ Proxied |
| `partners.yatradiscover.com` | Partner portal | React/Next.js | ✓ Proxied |
| `staging.yatradiscover.com` | Staging environment | Frontend/Backend | DNS Only |

## Technology Stack

```
┌─────────────────────────────────────────────────────┐
│            YatraDiscover AI Architecture            │
├─────────────────────────────────────────────────────┤
│                                                       │
│  Cloudflare (DNS, CDN, SSL/TLS, DDoS, WAF)        │
│            ↓                                         │
│  ┌──────────┬──────────┬──────────┬────────────┐    │
│  │          │          │          │            │    │
│  ▼          ▼          ▼          ▼            ▼    │
│  Front-   Front-    API       Admin       Partners  │
│  end      end      (FastAPI)  Portal      Portal    │
│  (Root)   (www)                                     │
│  │        │         │         │          │         │
│  └────┬───┴─────────┴─────────┴──────────┘         │
│       │                                              │
│       ▼                                              │
│  Vercel / AWS / DigitalOcean (Origin Servers)     │
│       │                                              │
│       ├─► Supabase PostgreSQL (Database)           │
│       │                                              │
│       └─► OpenAI API (AI Services)                 │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## Environments

### Development
- **Nameservers:** Original domain registrar
- **DNS Management:** Manual or Terraform
- **SSL:** Self-signed or Let's Encrypt
- **Secrets:** Local `.env` files (Git ignored)

### Staging
- **Nameservers:** Cloudflare nameservers
- **Subdomain:** `staging.yatradiscover.com`
- **SSL:** Cloudflare SSL/TLS
- **Secrets:** Staging AWS Secrets Manager

### Production
- **Nameservers:** Cloudflare nameservers
- **All subdomains:** Cloudflare-managed
- **SSL:** Cloudflare SSL/TLS Full Strict
- **Secrets:** Production AWS Secrets Manager / HashiCorp Vault

## Critical Security Rules

✓ **Must Do:**
- Keep Cloudflare API tokens secure (use GitHub Secrets)
- Enable TLS 1.2 or newer only
- Configure HTTPS redirects
- Disable caching for authenticated endpoints
- Implement rate limiting on API endpoints
- Use separate databases for each environment
- Rotate API keys regularly
- Enable 2FA on Cloudflare account

✗ **Must NOT Do:**
- Store API tokens in version control
- Expose OpenAI keys through CDN
- Cache user authentication tokens
- Use production database credentials in staging
- Enable Cloudflare proxy for email services
- Modify DNS records without documentation
- Deploy without runbook documentation

## File Structure

```
infrastructure/
├── cloudflare/
│   ├── README.md (this file)
│   ├── dns-records-plan.md
│   ├── nameserver-migration.md
│   ├── ssl-configuration.md
│   ├── security-policy.md
│   ├── production-checklist.md
│   └── rollback-plan.md
├── scripts/
│   ├── validate-dns.ps1
│   ├── check-nameservers.ps1
│   ├── test-https.ps1
│   ├── generate-readiness-report.ps1
│   └── test-dns-resolution.ps1
├── .github/workflows/
│   ├── dns-validation.yml
│   ├── deployment-readiness.yml
│   └── security-audit.yml
└── environments/
    ├── dev.env.example
    ├── staging.env.example
    └── production.env.example
```

## Next Steps

1. **Review DNS Records** → Read `dns-records-plan.md`
2. **Understand Nameserver Migration** → Read `nameserver-migration.md`
3. **Plan SSL/TLS Setup** → Read `ssl-configuration.md`
4. **Review Security Settings** → Read `security-policy.md`
5. **Prepare for Production** → Read `production-checklist.md`
6. **Create Rollback Plan** → Read `rollback-plan.md`

## Support & Resources

- **Cloudflare Documentation:** https://developers.cloudflare.com/
- **Cloudflare Free Plan:** https://www.cloudflare.com/plans/free/
- **DNS Propagation Checker:** https://www.whatsmydns.net/
- **SSL/TLS Checker:** https://www.ssllabs.com/ssltest/

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-11-13 | DevOps Team | Initial infrastructure setup |

---

**Last Updated:** 2026-11-13  
**Status:** Ready for Phase 1 (Preparation)
