#!/usr/bin/env python3
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

print(f"\n🔍 Checking AWS SES Configuration...")
print(f"Region: {AWS_REGION}")
print(f"Access Key: {AWS_ACCESS_KEY_ID[:10]}...")

try:
    ses = boto3.client(
        'ses',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    
    # List verified emails
    print("\n📧 VERIFIED EMAILS:")
    try:
        response = ses.list_verified_email_addresses()
        emails = response.get('VerifiedEmailAddresses', [])
        if emails:
            for email in emails:
                print(f"   ✅ {email}")
        else:
            print(f"   ❌ NO VERIFIED EMAILS")
    except Exception as e:
        print(f"   Error: {e}")
    
    # List verified domains
    print("\n🌐 VERIFIED DOMAINS:")
    try:
        response = ses.list_identities(IdentityType='Domain')
        domains = response.get('Identities', [])
        if domains:
            for domain in domains:
                print(f"   ✅ {domain}")
        else:
            print(f"   ❌ NO VERIFIED DOMAINS")
    except Exception as e:
        print(f"   Error: {e}")
        
    # Check account status
    print("\n📊 ACCOUNT STATUS:")
    try:
        response = ses.get_account_sending_enabled()
        print(f"   Sending Enabled: {response.get('Enabled')}")
    except Exception as e:
        print(f"   Error: {e}")
        
except Exception as e:
    print(f"\n❌ ERROR: Could not connect to AWS SES")
    print(f"Details: {str(e)}")
    print(f"\n⚠️  Check your AWS credentials:")
    print(f"   - AWS_ACCESS_KEY_ID correct?")
    print(f"   - AWS_SECRET_ACCESS_KEY correct?")
    print(f"   - AWS_REGION set to us-east-1?")

print("\n")
