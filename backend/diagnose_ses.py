#!/usr/bin/env python3
"""Comprehensive AWS SES diagnostic"""
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("🔍 AWS SES COMPREHENSIVE DIAGNOSTIC")
print("=" * 70)

# 1. Check credentials
print("\n📋 CREDENTIALS CHECK:")
access_key = os.getenv('AWS_ACCESS_KEY_ID', '')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY', '')
region = os.getenv('AWS_REGION', '')

print(f"   Access Key: {access_key[:15]}...{access_key[-4:] if len(access_key) > 19 else ''}")
print(f"   Secret Key: {'***' + secret_key[-4:] if secret_key else 'NOT SET'}")
print(f"   Region: {region}")

# 2. Try different regions
print("\n🌍 CHECKING ALL REGIONS:")
regions_to_check = ['eu-north-1', 'us-east-1', 'eu-west-1', 'us-west-2']

for check_region in regions_to_check:
    try:
        ses_client = boto3.client(
            'ses',
            region_name=check_region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        # Try to list identities
        response = ses_client.list_identities()
        identities = response.get('Identities', [])
        
        if identities:
            print(f"\n   ✅ {check_region}:")
            for identity in identities:
                print(f"      - {identity}")
        else:
            print(f"   ⚠️  {check_region}: No identities found")
            
    except Exception as e:
        print(f"   ❌ {check_region}: {str(e)[:50]}...")

# 3. Detailed check for configured region
print(f"\n📊 DETAILED CHECK FOR {region}:")
try:
    ses = boto3.client(
        'ses',
        region_name=region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    
    # Get account attributes
    attrs = ses.get_account_sending_enabled()
    print(f"   Sending Enabled: {attrs.get('Enabled')}")
    
    # List all identities
    print(f"\n   All Identities:")
    response = ses.list_identities()
    identities = response.get('Identities', [])
    
    if identities:
        for identity in identities:
            print(f"      ✅ {identity}")
    else:
        print(f"      ⚠️  NO IDENTITIES FOUND")
    
    # Get send quota
    quota = ses.get_send_quota()
    print(f"\n   Send Quota:")
    print(f"      Max 24h: {quota.get('Max24HourSend')}")
    print(f"      Max Rate: {quota.get('MaxSendRate')} emails/sec")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
