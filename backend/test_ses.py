#!/usr/bin/env python3
"""Test script to verify SES configuration"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("AWS SES CONFIGURATION TEST")
print("=" * 60)

# Check environment variables
print("\n📋 ENVIRONMENT VARIABLES:")
print(f"   AWS_REGION: {os.getenv('AWS_REGION', 'NOT SET')}")
print(f"   AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID', 'NOT SET')}")
print(f"   AWS_SECRET_ACCESS_KEY: {os.getenv('AWS_SECRET_ACCESS_KEY', 'NOT SET')[:10]}***" if os.getenv('AWS_SECRET_ACCESS_KEY') else "   AWS_SECRET_ACCESS_KEY: NOT SET")

# Try to import and test SES
try:
    print("\n🔗 CONNECTING TO AWS SES...")
    from ses import ses
    print("✅ SES client imported successfully")
    
    print("\n📊 CHECKING ACCOUNT STATUS...")
    account_info = ses.get_account_sending_enabled()
    print(f"   Account Sending Enabled: {account_info.get('Enabled')}")
    
    print("\n📧 LISTING VERIFIED EMAILS...")
    verified_emails = ses.list_verified_email_addresses()
    email_list = verified_emails.get('VerifiedEmailAddresses', [])
    if email_list:
        for email in email_list:
            print(f"   ✅ {email}")
    else:
        print("   ⚠️  NO VERIFIED EMAILS FOUND")
    
    print("\n🌐 LISTING VERIFIED DOMAINS...")
    try:
        verified_domains = ses.list_identities(IdentityType='Domain')
        domain_list = verified_domains.get('Identities', [])
        if domain_list:
            for domain in domain_list:
                print(f"   ✅ {domain}")
        else:
            print("   ⚠️  NO VERIFIED DOMAINS FOUND")
    except Exception as e:
        print(f"   Error getting domains: {str(e)}")
    
    print("\n📈 GETTING SEND QUOTA...")
    quota = ses.get_send_quota()
    print(f"   Max 24-hour Send: {quota.get('Max24HourSend')}")
    print(f"   Max Send Rate: {quota.get('MaxSendRate')} emails/sec")
    print(f"   Sent (24h): {quota.get('Sent')}")
    
    print("\n✅ SES CONFIGURATION IS VALID")
    
    # Determine status
    if email_list or domain_list:
        print("🎉 YOU CAN SEND EMAILS NOW!")
    else:
        print("⚠️  Verify at least one email or domain to send emails")
    
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    print("\n🔍 POSSIBLE ISSUES:")
    print("   1. Invalid AWS credentials (check .env file)")
    print("   2. AWS region not available or incorrect")
    print("   3. AWS account not authorized for SES")
    print("   4. Network connectivity issue")
    print("\n" + "=" * 60)
    import traceback
    traceback.print_exc()
    sys.exit(1)

