# Railway Environment Variables - Quick Reference

**Link to Railway:** https://railway.app/project/7e7e42a2-1d4f-4c8c-b3fa-feb7786a6965

---

## 5 Variables to Add

Copy and paste each variable exactly as shown below.

### Variable 1
```
Name:  DATABASE_URL
Value: postgresql://postgres:Itsmygame@143@db.zseviucrtfdwuvmiokzv.supabase.co:5432/postgres
```

### Variable 2
```
Name:  SECRET_KEY
Value: your-super-secret-jwt-key-change-in-production
```

### Variable 3
```
Name:  ENVIRONMENT
Value: production
```

### Variable 4
```
Name:  DEBUG
Value: false
```

### Variable 5
```
Name:  LOG_LEVEL
Value: INFO
```

---

## Steps

1. ✅ Click backend service (RED box)
2. ✅ Click "Variables" tab
3. ✅ Add each 5 variables above
4. ✅ Click "Deployments" tab
5. ✅ Click "..." on RED deployment
6. ✅ Click "Redeploy"
7. ✅ Wait for GREEN status (2-3 min)
8. ✅ Tell me "Backend is running!"

---

**When Status is GREEN ✅**

Test: https://[YOUR_RAILWAY_URL]/health

Should return: `{"status":"ok","message":"YatraDiscover AI Backend is running"}`

---

**Save this file for easy copy-paste!**
