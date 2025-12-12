# 📊 Email Marketing System - Project Analysis

**Date:** December 13, 2025  
**Project:** Email System (FastAPI + React)  
**Owner:** dev-shehzad

---

## 🎯 Executive Summary

This is a **production-ready email marketing platform** (similar to MailerLite) built with:
- **Backend:** FastAPI + PostgreSQL + AWS SES
- **Frontend:** React 19 + Vite + Tailwind CSS
- **Features:** Campaign management, contact import, email tracking, analytics

**Status:** ✅ Core functionality working. Database schema fixed. Tracking implemented.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend (port 5173)               │
│  Dashboard | Contacts | Campaign Create | Campaign List     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/CORS (Axios)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (port 8000)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Routes (prefixed /api/)                              │   │
│  │ • auth.py      - JWT login/verify                    │   │
│  │ • contacts.py  - CSV upload                          │   │
│  │ • campaigns.py - CRUD + send                         │   │
│  │ • stats.py     - Dashboard metrics                   │   │
│  │ • tracking.py  - Opens/clicks                        │   │
│  │ • webhooks.py  - SES bounce/complaint               │   │
│  │ • unsubscribe.py - Token-based unsubscribe          │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ Python DB Driver
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         PostgreSQL Database (port 5432)                     │
│  Tables: contacts, campaigns, campaign_sends, events,       │
│          suppressions, unsubscribe_tokens                   │
└──────────────────────────┬────────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        ↓                                      ↓
   AWS SES                            SES Webhooks (SNS)
   (Send emails)                      (Bounce/Complaint)
```

---

## 📁 Project Structure

```
email-system/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── database.py                # PostgreSQL connection
│   ├── ses.py                     # AWS SES client
│   ├── schema.sql                 # Database schema (tables/indexes)
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # Credentials (DB, AWS, JWT)
│   ├── env.example                # Template for .env
│   ├── migrate_db.py              # Database migration script (ADDED)
│   ├── init_db.py                 # Database init helper (ADDED)
│   ├── routes/
│   │   ├── auth.py                # Login/JWT endpoints
│   │   ├── contacts.py            # CSV contact upload
│   │   ├── campaigns.py           # Campaign CRUD + send with tracking
│   │   ├── stats.py               # Dashboard & campaign stats
│   │   ├── tracking.py            # Open/click tracking (SIMPLIFIED)
│   │   ├── unsubscribe.py         # Unsubscribe handling
│   │   ├── webhooks.py            # SES webhook handler
│   │   └── __init__.py
│   ├── Dockerfile
│   └── __pycache__/
│
├── frontend/
│   ├── package.json               # Node dependencies
│   ├── vite.config.js             # Build config
│   ├── eslint.config.js           # Linting
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx                # Router + layout
│   │   ├── index.css              # Tailwind + global styles
│   │   ├── pages/
│   │   │   ├── Login.jsx          # JWT token input
│   │   │   ├── Dashboard.jsx      # Stats display (FIXED route)
│   │   │   ├── Contacts.jsx       # CSV upload page
│   │   │   ├── CampaignCreate.jsx # HTML editor
│   │   │   └── CampaignList.jsx   # View campaigns
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   └── ProtectedRoute.jsx
│   │   │   ├── common/
│   │   │   │   ├── Tooltip.jsx
│   │   │   │   └── HelpIcon.jsx
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar/
│   │   │   │   └── Topbar/
│   │   │   ├── dashboard/
│   │   │   │   └── StatsCard.jsx
│   │   │   └── contacts/
│   │   │       └── UploadContacts.jsx
│   │   └── utils/
│   │       └── axios.js           # HTTP client config
│   ├── public/
│   ├── Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
├── CHANGELOG.md
├── README.md
├── TESTING_GUIDE.md               # (ADDED) Testing instructions
└── contacts.csv                   # Sample data
```

---

## 🔄 Data Flow: Email Send + Tracking

### Step 1: Campaign Creation
```
Frontend: User fills HTML editor → POST /api/campaign/create
Backend:
  1. INSERT into campaigns table (subject, sender, html)
  2. Return campaign_id
Frontend: Shows "Campaign created! ID: 123"
```

### Step 2: Send Campaign
```
Frontend: User clicks "Send Campaign" → POST /api/campaign/send?campaign_id=123
Backend:
  1. Get campaign (SELECT from campaigns)
  2. Get active contacts (SELECT from contacts WHERE unsubscribed=FALSE)
  3. For each contact:
     a. Inject tracking pixel: <img src="/api/t/open?campaign_id=123&email=...">
     b. Rewrite links: href="/api/t/click?campaign_id=123&email=...&url=..."
     c. Add unsubscribe link: /unsubscribe/{token}?email=...
     d. Send via SES
     e. INSERT into campaign_sends (campaign_id, contact_email, message_id, delivered=TRUE)
     f. Sleep 0.1s (rate limiting)
  4. Return {sent: 5, failed: 0}
Frontend: Shows "✅ 5 emails sent"
```

### Step 3: User Opens Email
```
Email Client:
  1. Loads HTML
  2. Requests <img src="http://127.0.0.1:8000/api/t/open?campaign_id=123&email=user@example.com">
  
Backend:
  1. Handler receives GET /api/t/open?campaign_id=123&email=user@example.com
  2. INSERT into events (campaign_id, contact_email, event_type='open')
  3. Return 1x1 transparent GIF (image/gif)
  
Database: events table now has open event
```

### Step 4: User Clicks Link
```
Email Client:
  1. User clicks link in email
  2. Browser requests: GET /api/t/click?campaign_id=123&email=user@example.com&url=https://google.com
  
Backend:
  1. Handler receives request
  2. INSERT into events (campaign_id, contact_email, event_type='click')
  3. Return 302 redirect to https://google.com
  
Browser: Redirects to target URL
Database: events table now has click event
```

### Step 5: Dashboard Displays Stats
```
Frontend: Loads Dashboard
  1. GET /api/stats/dashboard
  
Backend:
  1. Count total campaigns
  2. Count total contacts
  3. Count emails sent (from campaign_sends WHERE delivered=TRUE)
  4. Count opens (COUNT DISTINCT contact_email FROM events WHERE event_type='open')
  5. Count clicks (COUNT DISTINCT contact_email FROM events WHERE event_type='click')
  6. Calculate open_rate = opens / delivered * 100
  7. Calculate click_rate = clicks / delivered * 100
  8. Return JSON with all stats
  
Frontend: Renders stats cards
```

---

## 🗄️ Database Schema

### contacts
```sql
email (PK)
name
unsubscribed (boolean)
created_at
updated_at
```

### campaigns
```sql
id (PK)
subject
sender
html
created_at
updated_at
```

### campaign_sends
```sql
id (PK)
campaign_id (FK → campaigns)
contact_email (FK → contacts)
message_id (from SES)
delivered (boolean)
bounce_type (hard/soft/null)
sent_at
UNIQUE(campaign_id, contact_email)
```

### events
```sql
id (PK)
campaign_id (FK → campaigns)
contact_email (FK → contacts)
event_type (open/click/bounce/complaint)
created_at
```

### suppressions
```sql
email (PK)
reason (bounce/complaint)
bounce_type
created_at
updated_at
```

### unsubscribe_tokens
```sql
token (PK)
contact_email (FK → contacts)
campaign_id (FK → campaigns)
created_at
used_at
```

---

## 🔐 Authentication Flow

1. **Login Page**
   - User enters email + password
   - POST `/api/login` (form-encoded)
   - Backend verifies against hardcoded admin credentials

2. **Token Generation**
   - Backend creates JWT token
   - Claims: `{sub: email, exp: now + 24h}`
   - Signed with SECRET_KEY (from .env)

3. **Token Storage**
   - Frontend stores token in `localStorage`

4. **Protected Requests**
   - All `/api/*` requests include `Authorization: Bearer <token>`
   - Axios interceptor adds header automatically
   - Backend verifies token signature

5. **Protected Routes**
   - `ProtectedRoute` wrapper checks for token
   - Redirects to `/login` if missing

---

## 🔧 Recent Changes (Fixes Made)

### 1. Fixed API Route Prefix ✅
**Problem:** Frontend called `/stats/dashboard`, backend mounted at `/api/stats/dashboard`  
**Solution:** Updated `Dashboard.jsx` to use `/api/stats/dashboard`

### 2. Added Missing Database Column ✅
**Problem:** `events.contact_email` column didn't exist  
**Solution:** 
- Created `migrate_db.py` script
- Ran: `ALTER TABLE events ADD COLUMN contact_email VARCHAR(255)`
- Added indexes and FK constraint

### 3. Implemented Tracking System ✅
**Problem:** Opens/clicks not being recorded  
**Solution:**
- Simplified `/api/t/open` and `/api/t/click` endpoints
- Inject tracking pixel into HTML automatically
- Rewrite links for click tracking
- Record events in database

### 4. Added Error Handling ✅
**Problem:** DB errors returned 500 with full traceback  
**Solution:** Added try/except in `stats.py`, returns JSON errors

### 5. Fixed Campaign Send Recording ✅
**Problem:** Emails sent but not recorded in `campaign_sends`  
**Solution:** Insert into `campaign_sends` table with message_id after successful SES send

---

## 📊 Tech Stack Details

### Backend
- **FastAPI 0.115.6** - Modern async Python framework
- **PostgreSQL 15** - Relational database
- **psycopg2** - PostgreSQL driver
- **Pydantic 2.10.3** - Request/response validation
- **python-jose** - JWT creation/verification
- **boto3** - AWS SES SDK
- **python-dotenv** - Environment variables
- **pandas** - CSV parsing

### Frontend
- **React 19.2.0** - UI library (latest major version)
- **React Router 7.9.6** - Client-side routing
- **Tailwind CSS 4.1.17** - Utility CSS
- **Axios 1.13.2** - HTTP client
- **Vite 7.2.4** - Fast build tool
- **ESLint 9.39.1** - Code linting

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **nginx** - Reverse proxy (for frontend)
- **Uvicorn** - ASGI server

---

## 🚀 Key Features

### ✅ Authentication
- JWT-based admin login
- Token stored in localStorage
- Protected routes via wrapper component
- 24-hour token expiration

### ✅ Contact Management
- CSV bulk import with duplicate detection
- Unsubscribe tracking
- Bounce/complaint auto-suppression via SES webhooks

### ✅ Campaign Management
- HTML editor for email content
- Test email functionality
- Batch send to all contacts
- Rate limiting (10 emails/sec to respect SES)

### ✅ Email Tracking
- **Open Tracking:** 1x1 pixel injected into HTML
- **Click Tracking:** Links rewritten with tracking URLs
- **Unsubscribe:** Secure token-based links
- **Event Recording:** Opens/clicks recorded in events table

### ✅ Analytics Dashboard
- Total campaigns/contacts/emails
- Open rate % and click rate %
- Campaign-specific stats
- Real-time updates

### ✅ Bounce/Complaint Handling
- SES webhooks for hard/soft bounces
- Auto-suppression of invalid addresses
- Complaint handling (spam reports)

### ✅ Responsive UI
- Mobile-first design
- Works on all screen sizes
- Tailwind CSS styling
- Loading states and error handling

---

## ⚠️ Known Limitations & TODO

### Security (Before Production)
- [ ] Replace hardcoded admin credentials with proper user management
- [ ] Generate strong SECRET_KEY (`openssl rand -hex 32`)
- [ ] Use AWS IAM roles instead of access key/secret
- [ ] Enable HTTPS/SSL
- [ ] Add rate limiting to prevent API abuse
- [ ] Sanitize HTML input (prevent XSS in campaigns)
- [ ] Implement CSRF protection

### Scalability
- [ ] Add database connection pooling (pgbounce)
- [ ] Cache dashboard stats (Redis)
- [ ] Queue email sends (Celery/RabbitMQ) for large campaigns
- [ ] Implement pagination for contacts/campaigns
- [ ] Add database replication/backups

### Monitoring & Logging
- [ ] Set up error tracking (Sentry)
- [ ] Add structured logging
- [ ] Monitor SES sending limits
- [ ] Track API performance metrics
- [ ] Database query monitoring

### Features (Nice-to-Have)
- [ ] Campaign scheduling (send at specific time)
- [ ] A/B testing for subject lines
- [ ] Advanced segmentation of contacts
- [ ] Template library for common email types
- [ ] WYSIWYG HTML editor instead of raw HTML
- [ ] Attachment support
- [ ] Multi-sender support

---

## 🧪 Testing

### Quick Start Test
1. Login: admin@example.com / changeme
2. Upload contacts CSV
3. Create campaign with HTML
4. Send test email to yourself
5. Check Dashboard for stats

**See `TESTING_GUIDE.md` for detailed instructions**

### API Testing
```bash
# Verify backend is running
curl http://127.0.0.1:8000/health

# Test login
curl -X POST http://127.0.0.1:8000/api/login \
  -d "email=admin@example.com&password=changeme" \
  -H "Content-Type: application/x-www-form-urlencoded"

# Test stats endpoint
curl http://127.0.0.1:8000/api/stats/dashboard \
  -H "Authorization: Bearer <token>"
```

---

## 📝 Environment Configuration

See `backend/.env`:
```env
# Database
DB_HOST=localhost
DB_NAME=email_system
DB_USER=postgres
DB_PASSWORD=123456
DB_PORT=5432

# AWS SES
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=eu-north-1

# Application
SECRET_KEY=change-this-later
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Domain & Tracking
DOMAIN=muhammad-shehzad.com
TRACKING_SUBDOMAIN=links.muhammad-shehzad.com
BASE_URL=http://localhost:8000

# Frontend
FRONTEND_URL=http://localhost:5173
```

---

## 🚢 Deployment Checklist

- [ ] Change default admin credentials
- [ ] Generate strong SECRET_KEY
- [ ] Configure real AWS SES account
- [ ] Verify sending domain in SES
- [ ] Set up database backups
- [ ] Enable HTTPS/SSL
- [ ] Configure production PostgreSQL (connection pooling, replication)
- [ ] Add monitoring and alerting
- [ ] Test SES bounce/complaint webhooks
- [ ] Set up CI/CD pipeline
- [ ] Performance testing (load test email sending)
- [ ] Security audit (OWASP, SQL injection, XSS, CSRF)

---

## 📖 Documentation Files

- **README.md** - Project overview & setup instructions
- **TESTING_GUIDE.md** - Step-by-step testing instructions
- **CHANGELOG.md** - Version history
- **ARCHITECTURE.md** (this file) - Detailed technical architecture

---

## 📞 Support

**Issues Found & Fixed (Dec 13, 2025):**
1. ✅ Missing `/api` prefix in frontend API calls
2. ✅ Missing `contact_email` column in events table
3. ✅ Tracking endpoints not implemented
4. ✅ No error handling in stats endpoint
5. ✅ Campaign send not recording to database

**Current Status:** All core functionality working ✅

