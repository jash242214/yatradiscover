# DNS Records Configuration Plan

## Overview

This document defines all DNS records required for YatraDiscover AI. **All entries use placeholders** until actual hosting infrastructure is provisioned.

**Important:** Do not create DNS records with invented IP addresses. Update the "Target" column only when hosting provider supplies actual values.

## DNS Records Table

### Root Domain & WWW

| # | Type | Name | Target | Proxy Status | TTL | Purpose | Status |
|---|------|------|--------|--------------|-----|---------|--------|
| 1 | A | `yatradiscover.com` | `[ORIGIN_IP_ROOT]` | Proxied | 3600 | Root domain (marketing website) | Placeholder |
| 2 | CNAME | `www` | `[ORIGIN_FQDN_WWW]` | Proxied | 3600 | WWW redirect to customer website | Placeholder |

### Application Subdomains

| # | Type | Name | Target | Proxy Status | TTL | Purpose | Status |
|---|------|------|--------|--------------|-----|---------|--------|
| 3 | CNAME | `api` | `[ORIGIN_FQDN_API]` | Proxied | 3600 | FastAPI backend | Placeholder |
| 4 | CNAME | `admin` | `[ORIGIN_FQDN_ADMIN]` | Proxied | 3600 | Admin portal | Placeholder |
| 5 | CNAME | `partners` | `[ORIGIN_FQDN_PARTNERS]` | Proxied | 3600 | Partner portal | Placeholder |
| 6 | CNAME | `staging` | `[ORIGIN_FQDN_STAGING]` | DNS Only | 3600 | Staging environment | Placeholder |

### Email Records (Keep DNS-Only)

| # | Type | Name | Target | Proxy Status | TTL | Purpose | Status |
|---|------|------|--------|--------------|-----|---------|--------|
| 7 | MX | `yatradiscover.com` | `[EMAIL_MX_SERVER]` | DNS Only | 3600 | Email routing | To Be Configured |
| 8 | TXT | `yatradiscover.com` | `[SPF_RECORD]` | DNS Only | 3600 | SPF record for email auth | To Be Configured |
| 9 | TXT | `_dkim.yatradiscover.com` | `[DKIM_RECORD]` | DNS Only | 3600 | DKIM record for email signing | To Be Configured |
| 10 | TXT | `_dmarc.yatradiscover.com` | `[DMARC_POLICY]` | DNS Only | 3600 | DMARC policy for email validation | To Be Configured |

### CAA Records (Certificate Authority Authorization)

| # | Type | Name | Target | Proxy Status | TTL | Purpose | Status |
|---|------|------|--------|--------------|-----|---------|--------|
| 11 | CAA | `yatradiscover.com` | `0 issue "letsencrypt.org"` | DNS Only | 3600 | Allow Let's Encrypt certificates | Recommended |
| 12 | CAA | `yatradiscover.com` | `0 issuewild ";` | DNS Only | 3600 | Restrict wildcard certificates | Recommended |

## Placeholder Variables Reference

### Infrastructure Placeholders

| Placeholder | Description | Example | Source |
|------------|-------------|---------|--------|
| `[ORIGIN_IP_ROOT]` | IPv4 address of root domain origin | `203.0.113.45` | Hosting provider |
| `[ORIGIN_FQDN_WWW]` | FQDN of www origin server | `www.myhost.vercel.app` | Hosting provider |
| `[ORIGIN_FQDN_API]` | FQDN of API origin server | `api.myhost.render.com` | Hosting provider |
| `[ORIGIN_FQDN_ADMIN]` | FQDN of admin origin server | `admin.myhost.vercel.app` | Hosting provider |
| `[ORIGIN_FQDN_PARTNERS]` | FQDN of partners origin server | `partners.myhost.vercel.app` | Hosting provider |
| `[ORIGIN_FQDN_STAGING]` | FQDN of staging origin server | `staging-app.myhost.render.com` | Hosting provider |

### Email Configuration Placeholders

| Placeholder | Description | Example | Source |
|------------|-------------|---------|--------|
| `[EMAIL_MX_SERVER]` | Mail exchange server | `10 mail.google.com.` | Email provider (Google Workspace, SendGrid, etc.) |
| `[SPF_RECORD]` | Sender Policy Framework | `v=spf1 include:_spf.google.com ~all` | Email provider |
| `[DKIM_RECORD]` | DomainKeys Identified Mail | `v=DKIM1; k=rsa; p=MIGfMA0BgQC...` | Email provider |
| `[DMARC_POLICY]` | DMARC policy | `v=DMARC1; p=reject; rua=mailto:security@yatradiscover.com` | Security policy |

---

**Last Updated:** 2026-11-13  
**Status:** Ready for implementation when hosting infrastructure is ready
