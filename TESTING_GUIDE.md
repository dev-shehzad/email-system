# 📧 Email System - Testing Guide

## Quick Test Steps

### 1. Login to Dashboard
- URL: http://localhost:5173
- Email: `admin@example.com`
- Password: `changeme`

### 2. Create a Test Campaign with Tracking

Go to **Create Campaign** and paste this HTML with tracking links:

```html
<h1>Welcome to Our Newsletter!</h1>

<p>Hi there! Check out these links:</p>

<ul>
  <li><a href="https://google.com">Visit Google</a></li>
  <li><a href="https://github.com">Visit GitHub</a></li>
  <li><a href="https://nodejs.org">Visit Node.js</a></li>
</ul>

<p>Thanks for reading!</p>
```

**Campaign Details:**
- Subject: "Welcome Newsletter"
- Sender: "noreply@Muhammad-Shehzad.com" (or your verified domain)
- HTML: ☝️ (paste above)

Click **Create Campaign** → note the Campaign ID shown in green

### 3. Send Test Email

After campaign is created:
- Enter your test email address
- Click **Send Test**
- Check your email inbox

**What happens inside:**
- ✅ Open tracking pixel injected automatically
- ✅ All links rewritten for click tracking  
- ✅ Unsubscribe link added to footer
- ✅ Email recorded in `campaign_sends` table

### 4. Verify Tracking Works

**Open Tracking:**
- Open the test email in your email client
- A 1x1 pixel image loads from: `/api/t/open?campaign_id=1&email=test@example.com`
- Backend inserts row into `events` table with `event_type='open'`

**Click Tracking:**
- Click any link in the email
- Browser redirects through `/api/t/click?campaign_id=1&email=test@example.com&url=https://google.com`
- Backend inserts row into `events` table with `event_type='click'`
- Then redirects you to the original URL

### 5. Check Dashboard Stats

Go back to Dashboard:
- **"Opens"** should increase (when you open email)
- **"Clicks"** should increase (when you click links)
- **"Open Rate %" and "Click Rate %"** calculated automatically

---

## Database Inspection (Optional)

View tracking events:

```sql
-- See all open events
SELECT campaign_id, contact_email, event_type, created_at 
FROM events 
WHERE event_type = 'open' 
ORDER BY created_at DESC;

-- See all click events
SELECT campaign_id, contact_email, event_type, created_at 
FROM events 
WHERE event_type = 'click' 
ORDER BY created_at DESC;

-- See campaign send records
SELECT campaign_id, contact_email, delivered, message_id, sent_at 
FROM campaign_sends 
ORDER BY sent_at DESC;
```

---

## Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/login` | POST | Admin login |
| `/api/campaign/create` | POST | Create email campaign |
| `/api/campaign/test` | POST | Send test email |
| `/api/campaign/send` | POST | Send to all contacts |
| `/api/campaigns/all` | GET | List campaigns |
| `/api/stats/dashboard` | GET | Dashboard stats |
| `/api/stats/campaign/{id}` | GET | Campaign-specific stats |
| `/api/t/open` | GET | Track email opens |
| `/api/t/click` | GET | Track link clicks |
| `/api/contacts/upload` | POST | Upload CSV contacts |
| `/unsubscribe/{token}` | GET | Unsubscribe link |

---

## Example HTML for Testing

Simple version (just text):
```html
<h1>Hello!</h1>
<p>This is a test email with tracking enabled.</p>
<p><a href="https://example.com">Click here</a></p>
```

Fancy version (with styling):
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; }
    a { color: #0066cc; text-decoration: none; }
    .footer { border-top: 1px solid #ccc; padding-top: 20px; font-size: 12px; color: #666; }
  </style>
</head>
<body>
  <h1>🎉 Special Offer!</h1>
  <p>We have an exciting new product for you.</p>
  <p><a href="https://example.com/product">Learn More →</a></p>
  <div class="footer">
    <p>© 2025 Your Company. All rights reserved.</p>
  </div>
</body>
</html>
```

---

## Troubleshooting

**Stats show 0 opens/clicks?**
- Ensure campaign HTML includes tracking links
- Check `/api/t/open` and `/api/t/click` endpoints return 200 OK
- Verify email client loads external images (some block tracking pixels)

**Links not redirecting?**
- Make sure links start with `https://` or `http://`
- Check browser console for redirect logs
- Verify `/api/t/click` endpoint is accessible

**Campaign send fails?**
- Verify sender email matches verified SES domain
- Check AWS SES credentials in `.env`
- Look at backend logs for SES errors

---

## Next: Production Checklist

- [ ] Update default login credentials
- [ ] Configure real AWS SES domain
- [ ] Set `FRONTEND_URL` and `BASE_URL` correctly
- [ ] Review CORS allowlist in `main.py`
- [ ] Add rate limiting to API endpoints
- [ ] Implement proper user/auth system
- [ ] Set up SSL/HTTPS
- [ ] Configure SES webhooks for bounce handling
- [ ] Add database backups
- [ ] Set up monitoring/alerting

