# 🎨 FRONTEND DEPLOYMENT PREP (Vercel)

## PART B: Frontend Deploy (Vercel)

### Step B1: Update API Base URL

Jab backend Render par deploy ho jaye, frontend ko uska URL dena padega.

#### File: `frontend/.env.local`

Banao (agar nahi hai):
```
VITE_API_BASE_URL=https://email-system-backend.onrender.com
```

#### File: `frontend/src/utils/axios.js`

Check karo ki api base URL use kar raha hai:

```javascript
import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add auth token to requests
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default axiosInstance;
```

---

### Step B2: Check Vite Config

File: `frontend/vite.config.js`

Should look like:
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
  }
})
```

---

### Step B3: Vercel Setup

1. Go: https://vercel.com
2. Sign up / Login (GitHub se best)
3. Click **"Add New"** → **"Project"**
4. Select GitHub repository: `email-system`
5. Click **"Import"**

---

### Step B4: Configure Project

When prompted:

- **Framework Preset:** Select **Vite**
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`

---

### Step B5: Add Environment Variables

1. **Environment Variables** section
2. Add:
   ```
   VITE_API_BASE_URL = https://email-system-backend.onrender.com
   ```
3. Click **"Add"**

---

### Step B6: Deploy

1. Click **"Deploy"**
2. Wait 2-5 minutes
3. Green ✅ = Success!
4. Copy URL: `https://your-project.vercel.app`

---

## 🔗 Update CORS After Deploy

Once frontend is deployed:

1. Go to Render (backend service)
2. **Environment** tab
3. Find `CORS_ORIGINS`
4. Change to:
   ```
   CORS_ORIGINS=https://email-system.vercel.app
   ```
5. Save (automatic redeploy)

---

## 🧪 Test Everything

### Frontend loads:
```
https://email-system.vercel.app
```

### Can login:
- Email: `test@example.com`
- Password: `password123`

### Can create campaign:
- Subject: Test
- Sender: `devshehzad@gmail.com`
- HTML: Test content

### Can send email:
- Click "Send Test Email"
- Email should arrive in inbox

---

## ⚠️ Common Issues

### Issue: "API calls failing"
- Check VITE_API_BASE_URL correct?
- Backend CORS_ORIGINS updated?

### Issue: "Build fails"
- Check `npm run build` locally first
- Check package.json scripts section

### Issue: "env vars not loading"
- Redeploy after adding env vars
- Check variable names match exactly

---

## 📝 Files to Check/Update

```
frontend/
  ├── .env.local              ← Create this with API URL
  ├── vite.config.js          ← Check build config
  ├── package.json            ← Check build script
  ├── src/
  │   └── utils/
  │       └── axios.js        ← Check API base URL usage
  └── index.html              ← Check scripts load correctly
```

---

## ✅ Deployment Summary

| Component | Host | URL |
|-----------|------|-----|
| **Backend** | Render | `email-system-backend.onrender.com` |
| **Frontend** | Vercel | `email-system.vercel.app` |
| **Database** | Render PostgreSQL | Render-managed |
| **Email** | AWS SES | us-east-1 |

---

**Next:** After both deploy → Update CORS → Test fully

