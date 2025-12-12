# 🚀 QUICK DEPLOYMENT REFERENCE

## TL;DR - Deploy in 30 Minutes

### Part 1: Backend (Render)
1. Signup: https://render.com (GitHub)
2. Create PostgreSQL → Copy connection details
3. Create Web Service:
   - Repo: email-system
   - Root: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env vars (12 total - see below)
5. Wait for green ✅
6. Copy URL: `https://xxx.onrender.com`

### Part 2: Frontend (Vercel)
1. Signup: https://vercel.com (GitHub)
2. Import project: email-system
3. Set root: `frontend`
4. Add env var: `VITE_API_BASE_URL=https://xxx.onrender.com`
5. Deploy ✅
6. Copy URL: `https://xxx.vercel.app`

### Part 3: CORS Update
1. Go back to Render backend
2. Update `CORS_ORIGINS=https://xxx.vercel.app`
3. Save (auto-redeploys)

### Part 4: Test
1. Open frontend URL
2. Login
3. Create campaign, send email
4. Check inbox ✅

---

## Environment Variables Required

### Backend (12 vars)

```env
# Database (from Render PostgreSQL)
DB_HOST=xxx.onrender.com
DB_NAME=email_system
DB_USER=postgres
DB_PASSWORD=your-password
DB_PORT=5432

# AWS



# App
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Domain
DOMAIN=umar.agency
TRACKING_SUBDOMAIN=links.umar.agency
BASE_URL=https://xxx.onrender.com
CORS_ORIGINS=*
```

### Frontend (1 var)

```env
VITE_API_BASE_URL=https://xxx.onrender.com
```

---

## Files Changed (Ready to Deploy)

✅ `backend/requirements.txt` - Dependencies listed
✅ `backend/database.py` - Env-based config
✅ `backend/main.py` - CORS fixed
✅ `backend/Procfile` - Created
✅ `backend/env.example` - Template
✅ `frontend/src/utils/axios.js` - Env-based API
✅ `frontend/.env.example` - Template
✅ `.gitignore` - Has `.env`

---

## Commands to Test Locally First

```bash
# Backend test
cd backend
pip install -r requirements.txt
python main.py
# Check: http://localhost:8000/health

# Frontend test (new terminal)
cd frontend
npm install
npm run dev
# Check: http://localhost:5173
```

---

## URLs After Deploy

```
Backend:  https://email-system-backend.onrender.com
Frontend: https://email-system.vercel.app
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| API calls fail | Check VITE_API_BASE_URL correct |
| Database error | Check DB_HOST, password from Postgres connection |
| CORS errors | Update CORS_ORIGINS in Render backend |
| Build fails | Run `npm install` & `npm run build` locally |
| Env vars not working | Redeploy after adding vars |

---

## Verification Steps

After deployment, verify each:

```bash
# Backend working?
curl https://email-system-backend.onrender.com/health

# Database connected?
curl https://email-system-backend.onrender.com/api/health/ses

# Frontend loads?
Open https://email-system.vercel.app in browser

# Can send email?
Login → Create campaign → Send test email
```

---

**Ready? Start with Render backend!** 🚀

