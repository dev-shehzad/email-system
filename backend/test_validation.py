#!/usr/bin/env python3
"""
Test the sender validation logic
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Import the validation function
from routes.campaigns import is_sender_verified, get_verified_identities

print("\n" + "="*70)
print("TESTING SENDER VALIDATION")
print("="*70)

# Get verified identities
identities = get_verified_identities()
print(f"\n📋 VERIFIED IDENTITIES IN AWS SES:")
print(f"   Verified Emails: {identities['emails']}")
print(f"   Verified Domains: {identities['domains']}")

# Test cases
test_senders = [
    "devshehzad@gmail.com",      # Should pass - directly verified
    "info@umar.agency",           # Should fail - domain verified but email not
    "support@umar.agency",        # Should fail - domain verified but email not
    "unknown@example.com",        # Should fail - neither domain nor email verified
]

print(f"\n🧪 TESTING DIFFERENT SENDERS:\n")

for sender in test_senders:
    is_verified, message = is_sender_verified(sender)
    status = "✅ PASS" if is_verified else "❌ FAIL"
    print(f"{status} - {sender}")
    print(f"     {message}\n")

print("="*70)
print("SUMMARY:")
print("="*70)
print("""
In AWS SES SANDBOX MODE:
- You can ONLY send from directly verified email addresses
- Having a verified domain is NOT enough in sandbox mode
- Each email address must be individually verified

To send from info@umar.agency:
1. Go to AWS SES Console
2. Go to "Verified identities" 
3. Click "Create identity"
4. Select "Email address"
5. Enter: info@umar.agency
6. Verify the email by clicking the link in the verification email

For now, use: devshehzad@gmail.com
""")
print("="*70 + "\n")
