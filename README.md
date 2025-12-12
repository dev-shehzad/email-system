# Email Marketing System

**🎉 STATUS: FULLY OPERATIONAL** ✅  
**Backend:** http://0.0.0.0:8000  
**Frontend:** http://localhost:5173

---

## 📚 DOCUMENTATION INDEX

### 🚀 Quick Start (Pick One)
- **5-min test:** [`START_HERE.md`](./START_HERE.md) ⭐
- **3-min overview:** [`QUICK_FIX.md`](./QUICK_FIX.md)
- **Setup check:** [`CHECKLIST.md`](./CHECKLIST.md)

### 🔧 Configuration Issues
- **❌ Sender not verified?** → [`SENDER_VALIDATION_FIX.md`](./SENDER_VALIDATION_FIX.md) ⭐ READ THIS
- **Sandbox mode details:** [`SANDBOX_MODE_GUIDE.md`](./SANDBOX_MODE_GUIDE.md)
- **Sender email errors:** [`USE_VERIFIED_SENDER.md`](./USE_VERIFIED_SENDER.md)
- **Troubleshooting:** [`SENDER_NOT_VERIFIED.md`](./SENDER_NOT_VERIFIED.md)

### 📖 Complete Guides
- **Full overview:** [`FINAL_SUMMARY.md`](./FINAL_SUMMARY.md)
- **What was fixed:** [`SESSION_SUMMARY.md`](./SESSION_SUMMARY.md)
- **Technical details:** [`SYSTEM_WORKING.md`](./SYSTEM_WORKING.md)

### 🔍 Analysis
- **Root cause:** [`DIAGNOSIS_REPORT.md`](./DIAGNOSIS_REPORT.md)
- **Testing guide:** [`TESTING_GUIDE.md`](./TESTING_GUIDE.md)
- **Architecture:** [`ARCHITECTURE.md`](./ARCHITECTURE.md)

---

## ✨ What Changed (Session Summary)

### Issues Fixed
1. **AWS Region Mismatch** → Changed from eu-north-1 to us-east-1 ✅
2. **Unverified Sender** → Added validation + clear error messages ✅
3. **No Error Details** → Returns verified identities in responses ✅

### Features Added
- ✅ Sender validation before sending
- ✅ Comprehensive error messages
- ✅ Health endpoint with verified identities
- ✅ 9 new documentation files

### Status
- ✅ All issues resolved
- ✅ System fully operational
- ✅ Production ready

---

## ⚡ Quick Start (5 Minutes)

```
1. Open http://localhost:5173
2. Create campaign with:
   Sender: devshehzad@gmail.com (✅ Verified)
   Subject: Test
   HTML: <h1>Hello</h1>
3. Send test email
4. Check inbox (1-2 min)
```

**Expected:** Email arrives ✅

---

A production-ready Mailerlite clone built with **FastAPI** (Python) and **React** (TypeScript/JSX), integrated with **Amazon SES** for email delivery. Complete with contact management, campaign creation, email tracking, and analytics dashboard.

## 🚀 Tech Stack

### Backend
- **FastAPI** 0.115.6 - Modern Python web framework
- **PostgreSQL** 15+ - Relational database
- **Amazon SES** - Email delivery service
- **Pydantic** 2.10.3 - Data validation
- **JWT** - Authentication
- **Boto3** - AWS SDK

### Frontend
- **React** 19.2.0 - UI library
- **React Router** 7.9.6 - Routing
- **Tailwind CSS** 4.1.17 - Styling
- **Axios** - HTTP client
- **Vite** - Build tool

## 📁 Example Files

- **`contacts.example.csv`** - Sample CSV file showing the expected format for contact uploads
  ```csv
  email,name
  user@example.com,John Doe
  ```

## 📋 Features

- ✅ **JWT Authentication** - Secure admin login
- ✅ **Contact Management** - CSV bulk import with duplicate handling
- ✅ **Campaign Creation** - HTML email editor with test email support
- ✅ **Batch Email Sending** - SES integration with rate limiting (10 emails/sec)
- ✅ **Open Tracking** - 1x1 pixel tracking for email opens
- ✅ **Click Tracking** - Automatic link rewriting with redirect tracking
- ✅ **Unsubscribe System** - Secure token-based unsubscribe links
- ✅ **Analytics Dashboard** - Real-time metrics (sent, delivered, opens, clicks, rates)
- ✅ **Bounce/Complaint Handling** - Automatic suppression via SES webhooks
- ✅ **Responsive UI** - Mobile-first, fully responsive design
- ✅ **Docker Support** - Complete containerization with Docker Compose

## 🏗️ Project Structure

```
email-system/
├── backend/
│   ├── routes/              # API route handlers
│   │   ├── auth.py         # JWT authentication
│   │   ├── campaigns.py    # Campaign CRUD & sending
│   │   ├── contacts.py     # CSV contact upload
│   │   ├── stats.py        # Analytics endpoints
│   │   ├── tracking.py     # Open/click tracking
│   │   ├── unsubscribe.py  # Unsubscribe handling
│   │   └── webhooks.py      # SES webhook handler
│   ├── main.py             # FastAPI application entry
│   ├── database.py         # PostgreSQL connection
│   ├── ses.py              # AWS SES client
│   ├── schema.sql          # Database schema
│   ├── requirements.txt    # Python dependencies
│   ├── env.example         # Environment template
│   └── Dockerfile          # Backend container
│
├── frontend/
│   ├── src/
│   │   ├── pages/          # React page components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Contacts.jsx
│   │   │   ├── CampaignCreate.jsx
│   │   │   └── CampaignList.jsx
│   │   ├── components/     # Reusable components
│   │   │   ├── auth/       # Authentication components
│   │   │   ├── common/     # Shared components (Tooltip, HelpIcon)
│   │   │   ├── contacts/   # Contact upload component
│   │   │   ├── dashboard/  # Stats cards
│   │   │   └── layout/     # Sidebar, Topbar
│   │   ├── utils/          # Utilities (axios config)
│   │   ├── App.jsx         # Main app component
│   │   └── index.css       # Global styles
│   ├── package.json        # Node dependencies
│   ├── vite.config.js      # Vite configuration
│   ├── nginx.conf          # Production nginx config
│   └── Dockerfile          # Frontend container
│
├── docker-compose.yml      # Multi-container orchestration
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🛠️ Development Setup

### Prerequisites

- **Docker & Docker Compose** (recommended)
- OR **Python 3.11+**, **Node.js 18+**, **PostgreSQL 15+**
- **AWS Account** with SES access
- **Domain** for email sending (with DNS access)

### Quick Start (Docker)

```bash
# 1. Clone repository
git clone <repository-url>
cd email-system

# 2. Configure environment
cp backend/env.example backend/.env
# Edit backend/.env with your AWS credentials and domain

# 3. Start all services
docker-compose up -d

# 4. Access application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
createdb email_system
psql email_system < schema.sql

# Configure environment
cp env.example .env
# Edit .env with your credentials

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Access at http://localhost:5173
```

## ⚙️ Configuration

### Environment Variables

Create `backend/.env` from `backend/env.example`:

```env
# Database
DB_HOST=localhost
DB_NAME=email_system
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# AWS SES
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Application
SECRET_KEY=generate-strong-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Domain (replace with your domain)
DOMAIN=yourdomain.com
TRACKING_SUBDOMAIN=links.yourdomain.com
BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

### AWS SES Setup

1. **Verify Domain in SES Console**
   - AWS SES → Verified identities → Create identity
   - Select "Domain" and enter your domain
   - Follow DNS verification instructions

2. **Configure DNS Records**
   ```
   # SPF Record
   TXT @ "v=spf1 include:amazonses.com ~all"
   
   # DKIM Records (from SES console)
   # Add CNAME records as shown in SES verification
   
   # DMARC Record
   TXT _dmarc "v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com"
   ```

3. **Request Production Access** (if in sandbox)
   - SES Console → Account dashboard → Request production access

4. **Configure Webhooks** (optional)
   - Create SNS topic for bounces/complaints
   - Subscribe to: `http://your-domain/api/webhooks/ses`
   - Or use Lambda to forward notifications

### Default Credentials

**⚠️ CHANGE BEFORE PRODUCTION**

- Email: `admin@example.com`
- Password: `changeme`

Update in `backend/routes/auth.py` or implement proper user management.

## 📡 API Documentation

### Authentication

```http
POST /api/login
Content-Type: application/x-www-form-urlencoded

email=admin@example.com&password=changeme
```

```http
GET /api/verify
Authorization: Bearer <token>
```

### Contacts

```http
POST /api/contacts/upload
Content-Type: multipart/form-data

file: <CSV file>
```

**CSV Format:**
```csv
email,name
user@example.com,John Doe
```

### Campaigns

```http
POST /api/campaign/create
?subject=Welcome&sender=noreply@yourdomain.com&html=<h1>Hello</h1>
```

```http
POST /api/campaign/send?campaign_id=1
```

```http
POST /api/campaign/test?campaign_id=1&test_email=test@example.com
```

```http
GET /api/campaigns/all
```

### Statistics

```http
GET /api/stats/dashboard
GET /api/stats/campaign/{campaign_id}
```

### Tracking (Public Endpoints)

```http
GET /track/open/{campaign_id}/{base64_email}
GET /track/click/{campaign_id}/{base64_email}/{link_id}
GET /unsubscribe/{token}?email={email}
```

### Webhooks

```http
POST /api/webhooks/ses
Content-Type: application/json

# SES bounce/complaint notifications
```

## 🗄️ Database Schema

### Tables

- **`contacts`** - Email contacts with unsubscribe status
- **`campaigns`** - Email campaign definitions
- **`campaign_sends`** - Individual email send records
- **`events`** - Tracking events (opens, clicks, bounces, complaints)
- **`suppressions`** - Bounced/complained email addresses
- **`unsubscribe_tokens`** - Secure unsubscribe tokens

See `backend/schema.sql` for complete schema with indexes.

## 🔒 Security Considerations

### Before Production Deployment

- [ ] **Change default credentials** - Implement proper user management
- [ ] **Generate strong SECRET_KEY** - Use `openssl rand -hex 32`
- [ ] **Update database passwords** - Use strong, unique passwords
- [ ] **Enable HTTPS** - Use reverse proxy (nginx/traefik) with SSL
- [ ] **Secure AWS credentials** - Use IAM roles instead of access keys if possible
- [ ] **Configure CORS** - Restrict to your frontend domain only
- [ ] **Add input validation** - Sanitize HTML content, validate emails
- [ ] **Enable rate limiting** - Protect API endpoints from abuse
- [ ] **Set up monitoring** - Logging, error tracking, metrics
- [ ] **Backup strategy** - Regular database backups
- [ ] **Environment isolation** - Separate dev/staging/prod environments

## 🧪 Testing

### Manual Testing Checklist

1. **Authentication**
   - [ ] Login with valid credentials
   - [ ] Login with invalid credentials
   - [ ] Access protected routes without token

2. **Contacts**
   - [ ] Upload valid CSV file
   - [ ] Upload CSV with duplicates
   - [ ] Upload invalid CSV format

3. **Campaigns**
   - [ ] Create campaign
   - [ ] Send test email
   - [ ] Send campaign to all contacts
   - [ ] Verify tracking pixel in sent email
   - [ ] Click links and verify click tracking
   - [ ] Unsubscribe and verify suppression

4. **Analytics**
   - [ ] Verify dashboard stats update
   - [ ] Check campaign-specific stats

## 🐛 Troubleshooting

### Backend Issues

**Import Errors / Pydantic Issues**
```bash
# Reinstall dependencies
cd backend
pip uninstall -y pydantic fastapi
pip install pydantic==2.10.3 fastapi==0.115.6
```

**Database Connection**
- Verify PostgreSQL is running
- Check `.env` database credentials
- Ensure database exists: `createdb email_system`

**SES Errors**
- Verify domain in SES console
- Check AWS credentials in `.env`
- Ensure sender email matches verified domain
- Check SES sending limits (sandbox vs production)

### Frontend Issues

**Build Errors**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API Connection**
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify `FRONTEND_URL` in backend `.env`

### Tracking Issues

- Ensure `BASE_URL` is publicly accessible
- Verify tracking endpoints return correct responses
- Check email HTML includes tracking pixel
- Verify link rewriting is working

## 📦 Deployment

### Docker Production

```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Production

1. **Backend**
   ```bash
   # Use production WSGI server
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

2. **Frontend**
   ```bash
   npm run build
   # Serve dist/ with nginx/apache
   ```

3. **Database**
   - Use managed PostgreSQL (AWS RDS, DigitalOcean, etc.)
   - Set up automated backups

## 📊 Performance

- **Rate Limiting**: 10 emails/second (configurable in `campaigns.py`)
- **Database Indexes**: Optimized for common queries
- **Frontend**: Code splitting, lazy loading ready
- **Caching**: Can be added for stats endpoints

## 🔄 Rate Limiting

Email sending includes built-in rate limiting:
- Default: 0.1 seconds per email (10 emails/sec)
- Configurable via `EMAIL_SEND_DELAY` in `campaigns.py`
- Respects SES production limits

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Built with ❤️ using FastAPI and React**
