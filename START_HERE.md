# ⚡ START HERE - 5 MINUTE TEST

**Goal:** Send your first email successfully ✅

---

## ✅ Prerequisites Check

- [ ] Backend server running at http://127.0.0.1:8000
- [ ] Frontend available at http://localhost:5173
- [ ] Database connected
- [ ] AWS credentials configured

---

## 🚀 Step-by-Step (5 minutes)

### Step 1: Open Frontend (30 seconds)
```
http://localhost:5173
```
- Login with credentials
- You should see Dashboard

### Step 2: Create a Campaign (1 minute)
```
Subject: Test Email
Sender: devshehzad@gmail.com  ← IMPORTANT: Use this email
HTML: <h1>Hello!</h1><p>This is a test.</p>
```
- Click Create
- You'll see: Campaign created successfully

### Step 3: Send Test Email (30 seconds)
```
Campaign ID: (from previous step)
Test Email: devshehzad@gmail.com
```
- Click Send Test Email
- Check console for success message

### Step 4: Check Your Inbox (2 minutes)
```
Open: Gmail/Outlook
Look for: Test Email
From: devshehzad@gmail.com
```
- Should arrive within 1-2 minutes
- Check spam folder if not found

### Step 5: Verify It Works (1 minute)
```
If email arrived: ✅ SUCCESS!
If not: Check troubleshooting below
```

---

## ✅ Success Indicators

You'll see:
```
✅ Campaign created with ID
✅ "Email sent successfully" message
✅ Email arrives in inbox within 2 minutes
✅ Dashboard stats update
```

---

## ❌ If Email Doesn't Arrive

### Check 1: Wrong Sender Email
**Problem:** Using info@umar.agency or other unverified email
**Solution:** Use `devshehzad@gmail.com` as sender
**Fix:** Create new campaign with correct sender

### Check 2: Spam Folder
**Problem:** Email in spam, not inbox
**Solution:** Check spam/junk folder
**Result:** Mark as "Not Spam" to whitelist

### Check 3: Backend Error
**Problem:** See error message in logs
**Solution:** Check backend console for error details
**Example:** 
```
❌ FAILED TO SEND TEST EMAIL:
   Error Type: MessageRejected
   Message: Email address is not verified
```

**Fix:** Use verified sender email!

### Check 4: Check Verified Identities
```
http://127.0.0.1:8000/api/health/ses
```

Look for:
```json
"verified_emails": ["devshehzad@gmail.com"],
"verified_domains": ["umar.agency"]
```

If empty or missing → Problem with AWS credentials

---

## 📱 Full Example

### Frontend Form:
```
Subject: Welcome to Umar Agency
Sender: devshehzad@gmail.com
HTML: 
<h1>Welcome!</h1>
<p>Thanks for testing our email system.</p>
<a href="https://umar.agency">Visit our website</a>
```

### Expected Result:
```
✅ Campaign created
✅ Test email sent
✅ Email in inbox with subject "Welcome to Umar Agency"
✅ Links tracked for clicks
✅ Opens tracked via pixel
✅ Dashboard shows 1 email sent, 1 open (when you open it)
```

---

## 💡 Important Points

✅ **Always use:** `devshehzad@gmail.com` as sender
✅ **Email to:** Any address (will arrive within 1-2 min)
✅ **HTML:** Any valid HTML (tracking auto-injected)
✅ **Subject:** Any text
✅ **Region:** us-east-1 (must match AWS)

---

## 🎯 Troubleshooting Quick Links

| Issue | Solution | Page |
|-------|----------|------|
| Wrong sender | Use devshehzad@gmail.com | USE_VERIFIED_SENDER.md |
| Not in inbox | Check spam folder | SENDER_NOT_VERIFIED.md |
| API error | Check backend logs | FINAL_SUMMARY.md |
| Need details | See full guide | SYSTEM_WORKING.md |

---

## ✨ After Success

Once first email works:
1. Try sending to multiple emails
2. Test campaign features
3. Check dashboard stats
4. Verify open/click tracking
5. Read TESTING_GUIDE.md for more features

---

## 🎉 Expected Timeline

| Action | Time | Result |
|--------|------|--------|
| Create campaign | 30 sec | ✅ Created |
| Send test email | 30 sec | ✅ Sent |
| Email arrives | 1-2 min | ✅ Inbox |
| Total | ~2 minutes | ✅ Working |

---

**Start now! Open http://localhost:5173 and send your first email!** 🚀

---

*Still having issues? Check the other documentation files or the backend logs for detailed error messages.*
