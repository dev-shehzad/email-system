# AWS SES Sandbox Mode Guide

## ⚠️ Current Status: SANDBOX MODE

Your AWS SES account is in **Sandbox Mode**, which has important restrictions:

### Sandbox Mode Restrictions:
1. **Domain verification is NOT enough** to send emails
2. **Individual email addresses must be verified** before you can send from them
3. You can only send to verified recipient email addresses
4. **Limited to 1 email per second** (will be increased when you request production access)

---

## ✅ Currently Verified & Working

**Email Addresses (can send FROM these):**
- ✅ `devshehzad@gmail.com` - **USE THIS FOR NOW**

**Domains (verified but individual emails still need verification):**
- ✅ `umar.agency` - Domain is verified, but you cannot send from `info@umar.agency`, `support@umar.agency`, etc. unless each is individually verified

---

## ❌ Why `info@umar.agency` Fails

```
Error: "Email address is not verified. 
The following identities failed the check in region US-EAST-1: info@umar.agency"
```

**Reason:** 
- The domain `umar.agency` is verified ✅
- BUT the specific email `info@umar.agency` is **NOT** verified ❌
- AWS SES requires BOTH the domain AND the specific email to be verified in sandbox mode

---

## ✅ How to Fix: Verify info@umar.agency

### Step 1: Go to AWS SES Console
1. Open [AWS SES Console](https://console.aws.amazon.com/ses/home?region=us-east-1)
2. Make sure you're in region **us-east-1** (top right dropdown)

### Step 2: Create New Identity
1. Click **"Create identity"** (or "Verified identities" → "Create identity")
2. Select **"Email address"** (not Domain)

### Step 3: Enter Email
1. Enter: `info@umar.agency`
2. Click **"Create identity"**

### Step 4: Verify Email
1. AWS sends a verification email to `info@umar.agency`
2. Open that email and click the verification link
3. The status will change to "✅ Verified"

### Step 5: Update Frontend
1. Go back to email system frontend
2. In campaign creation, use `info@umar.agency` as sender
3. Test email should now work! 🎉

---

## 🎯 For Now: Use devshehzad@gmail.com

**Until you verify `info@umar.agency`, use this verified email:**

```
Sender: devshehzad@gmail.com
```

All campaigns created with this sender will work and emails will be delivered.

---

## 🚀 Production Mode (Remove Sandbox Restrictions)

Once your account needs higher volume, request production access:

1. Go to [AWS SES Console](https://console.aws.amazon.com/ses/home?region=us-east-1)
2. Click **"Account dashboard"**
3. Under "Sandbox Information", click **"Request production access"**
4. Fill out the form and submit
5. AWS reviews (usually 24 hours) and approves

Once in production mode:
- ✅ Send from any verified domain (no need to verify specific emails)
- ✅ Send up to **14 emails per second** (adjustable)
- ✅ Send to any recipient (not just verified ones)

---

## 📋 Verification Checklist

Use this to check what's verified:

```bash
# Check verified identities
curl http://localhost:8000/api/health/ses

# Response will show:
{
  "verified_emails": ["devshehzad@gmail.com"],
  "verified_domains": ["umar.agency"],
  ...
}
```

---

## 🔧 Technical Details

**Backend Validation Logic:**
- When you try to send from `info@umar.agency`, the backend checks:
  1. Is this email directly verified? ❌ No
  2. Is the domain verified? ✅ Yes, but...
  3. In sandbox mode, that's not enough ❌
  4. Error returned with list of verified emails

**Verified emails that CAN send:**
- devshehzad@gmail.com ✅

**Not verified (will fail):**
- info@umar.agency (domain verified, but email not)
- support@umar.agency (domain verified, but email not)
- any@example.com (neither domain nor email verified)

---

## 📞 AWS SES Documentation

- [AWS SES Sandbox Mode](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)
- [Verifying Email Addresses in SES](https://docs.aws.amazon.com/ses/latest/dg/verify-email-addresses.html)
- [Verifying Domains in SES](https://docs.aws.amazon.com/ses/latest/dg/verify-domain-procedure.html)

