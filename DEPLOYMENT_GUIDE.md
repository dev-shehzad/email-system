# 🚀 DEPLOYMENT GUIDE: Backend (Render) + Frontend (Vercel)

## PART A: Backend Deploy (Render)

### ✅ A1: Backend Code Ready

Ye cheezen verify ho gayin:

- ✅ `requirements.txt` - Sab dependencies listed hain
- ✅ `database.py` - Environment variables se read karta hai
- ✅ `main.py` - CORS fix ho gaya (allow_origins = "*")
- ✅ `Procfile` - Created for Render

---

## 📋 A2: Render pe Account Banao

1. Ja: https://render.com
2. **"Sign up"** karo (GitHub account se best hai)
3. Email verify karo

---

## 🔧 A3: Database Setup (PostgreSQL on Render)

### Step 1: Create PostgreSQL Database

1. Render dashboard me ja
2. **"New +"** → **"PostgreSQL"**
3. Fill karein:
   - **Name:** `email-system-db`
   - **Database:** `email_system`
   - **User:** `postgres`
   - **Region:** Closest to you
   - **Plan:** Free (for now)

4. Click **"Create Database"**

5. **Wait 2-3 minutes** for database to be ready

### Step 2: Get Database Connection Details

Database create hone ke baad:

1. **"Connections"** tab khol
2. Ye details copy karo:
   ```
   Host: [COPY THIS]
   Port: 5432
   Database: email_system
   User: postgres
   Password: [COPY THIS - LONG STRING]
   ```

3. Ye save karo - deploy ke time chahiye hoga

---

## 🚀 A4: Deploy Backend Service

### Step 1: Create Web Service

1. Render dashboard me ja
2. **"New +"** → **"Web Service"**
3. Connect GitHub repo (if not connected, connect now)
4. Select: **email-system** repository
5. Fill karein:
   - **Name:** `email-system-backend`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free (for now)

6. Click **"Create Web Service"**

### Step 2: Add Environment Variables

Service create hone ke baad:

1. **"Environment"** tab khol
2. Click **"Add Environment Variable"**
3. Add ye variables (PostgreSQL se copied values):

```
DB_HOST=your-database-host-from-postgres-connection
DB_NAME=email_system
DB_USER=postgres
DB_PASSWORD=your-postgres-password-from-connection
DB_PORT=5432

AWS_REGION=us-east-1


DOMAIN=umar.agency
TRACKING_SUBDOMAIN=links.umar.agency
BASE_URL=https://email-system-backend.onrender.com

CORS_ORIGINS=*
```

4. Click **"Save"**

### Step 3: Wait for Deploy

- Green checkmark ✅ = Deploy successful
- URL milega like: `https://email-system-backend.onrender.com`
- **Save this URL** - frontend me chahiye hoga

---

## 🧪 A5: Test Backend

### Check if running:
```
https://email-system-backend.onrender.com/health
```

Should return:
```json
{
  "status": "ok"
}
```

### Check SES status:
```
https://email-system-backend.onrender.com/api/health/ses
```

Should return verified identities.

---

## ⚠️ Common Issues & Fixes

### Issue: "Database connection failed"
- Check DB_HOST, DB_USER, DB_PASSWORD correct hain
- Render PostgreSQL me database ready hai?

### Issue: "ModuleNotFoundError"
- `requirements.txt` me sab packages hain?
- Build command: `pip install -r requirements.txt` set hai?

### Issue: "Connection refused on port 5432"
- Port 5432 network se open hai?
- PostgreSQL service running hai?

---

## 📝 Next Step

👉 **PART B: Frontend Deploy (Vercel)** ka intezar karo

---

## ✅ Checklist Before Moving Forward

- [ ] Render account created
- [ ] PostgreSQL database created + connection details saved
- [ ] Backend service deployed + green ✅
- [ ] `/health` endpoint responds
- [ ] `/api/health/ses` shows verified identities
- [ ] Backend URL saved (e.g., `email-system-backend.onrender.com`)

