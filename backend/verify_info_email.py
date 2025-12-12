#!/usr/bin/env python3
"""
Verify info@umar.agency in AWS SES
"""
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

ses = boto3.client(
    'ses',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

print("\n" + "="*70)
print("📧 VERIFYING info@umar.agency IN AWS SES")
print("="*70)

try:
    # Verify the email address
    response = ses.verify_email_identity(EmailAddress='info@umar.agency')
    
    print("\n✅ SUCCESS!")
    print(f"Email: info@umar.agency")
    print(f"Status: Verification email sent")
    print(f"\nResponse: {response}")
    
    print("\n" + "-"*70)
    print("📧 NEXT STEPS:")
    print("-"*70)
    print("""
1. Check your email inbox for: info@umar.agency
   (AWS sends a verification email to this address)

2. Open the verification email from AWS SES

3. Click the verification link in the email

4. Status will change to: ✅ Verified

5. Then you can send from: info@umar.agency
""")
    
    # Show current verified identities
    print("\n📋 CURRENT VERIFIED IDENTITIES:")
    print("-"*70)
    
    emails = ses.list_verified_email_addresses()
    print("Verified Emails:")
    for email in emails.get('VerifiedEmailAddresses', []):
        print(f"   ✅ {email}")
    
    domains = ses.list_identities(IdentityType='Domain')
    print("\nVerified Domains:")
    for domain in domains.get('Identities', []):
        print(f"   ✅ {domain}")
    
    print("\n" + "="*70)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print(f"Details: {repr(e)}")

print("\n")
