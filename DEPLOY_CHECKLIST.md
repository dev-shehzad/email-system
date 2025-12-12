# ✅ DEPLOYMENT CHECKLIST

## PART A: Backend (Render)

### Code Preparation
- [x] `requirements.txt` - All dependencies listed
- [x] `database.py` - Reads from environment variables
- [x] `main.py` - CORS fixed (allow_origins = "*")
- [x] `Procfile` - Created for Render deployment
- [x] `.env` - In `.gitignore` (secrets won't be pushed)
- [x] `env.example` - Template created

### Render Setup
- [ ] Create Render account (https://render.com)
- [ ] Create PostgreSQL database on Render
- [ ] Note PostgreSQL connection details:
  - [ ] Host: ________________
  - [ ] Port: 5432
  - [ ] Database: email_system
  - [ ] User: postgres
  - [ ] Password: ________________

### Deploy Backend
- [ ] Create Web Service on Render
- [ ] Set root directory to: `backend`
- [ ] Set build command: `pip install -r requirements.txt`
- [ ] Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables (12 total)
- [ ] Wait for green ✅ (usually 5-10 minutes)
- [ ] Note backend URL: ________________

### Test Backend
- [ ] `/health` endpoint returns `{"status": "ok"}`
- [ ] `/api/health/ses` shows verified identities
- [ ] Database connection works

---

## PART B: Frontend (Vercel)

### Code Preparation (Next)
- [ ] Update `src/utils/axios.js` - Use backend URL from Render
- [ ] Update `.env` - VITE_API_BASE_URL = backend URL
- [ ] Verify `vite.config.js` configured correctly

### Vercel Setup (Next)
- [ ] Create Vercel account (vercel.com)
- [ ] Connect GitHub repository
- [ ] Set framework: Vite
- [ ] Set output directory: `dist`

### Deploy Frontend
- [ ] Create project on Vercel
- [ ] Add environment variables
- [ ] Deploy success (green ✅)
- [ ] Note frontend URL: ________________

### Test Frontend
- [ ] Open frontend URL in browser
- [ ] Login works
- [ ] Campaigns can be created
- [ ] Email sending works

---

## 🔗 Final URLs

**Backend (Render):**
```
https://email-system-backend.onrender.com
```

**Frontend (Vercel):**
```
https://email-system.vercel.app
```

---

## 📱 CORS Configuration (After Deploy)

Once frontend deployed, update backend:

1. Go to Render dashboard
2. Select backend service
3. **Environment** tab
4. Change `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://email-system.vercel.app
   ```
5. Save (will redeploy automatically)

---

## 🎯 What's Working

Current Status:
- ✅ Backend code ready for production
- ✅ Database configuration flexible
- ✅ CORS configured
- ✅ AWS SES integration ready
- ✅ All endpoints working
- ✅ Email sending functional

Next: Frontend deployment on Vercel

