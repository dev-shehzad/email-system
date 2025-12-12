#!/usr/bin/env python3
"""Test sending an email using verified domain"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

print("=" * 70)
print("📧 SES EMAIL SEND TEST")
print("=" * 70)

try:
    from ses import ses
    
    # Test parameters
    sender_email = "devshehzad@gmail.com"  # ✅ VERIFIED email
    recipient_email = "devshehzad@gmail.com"
    subject = "✅ Email System Test - Verified!"
    
    print(f"\n📤 SENDING TEST EMAIL:")
    print(f"   From: {sender_email}")
    print(f"   To: {recipient_email}")
    print(f"   Subject: {subject}")
    print(f"   Region: {os.getenv('AWS_REGION')}")
    
    # Send the email
    response = ses.send_email(
        Source=sender_email,
        Destination={"ToAddresses": [recipient_email]},
        Message={
            "Subject": {"Data": subject},
            "Body": {
                "Html": {
                    "Data": """
                    <html>
                        <head></head>
                        <body>
                            <h2>✅ Email System is Working!</h2>
                            <p>This email was sent from <strong>umar.agency</strong> domain.</p>
                            <p>Your email tracking system is now fully functional.</p>
                            <hr />
                            <p style="color: #666; font-size: 12px;">
                                Test email from Email System
                            </p>
                        </body>
                    </html>
                    """
                }
            }
        }
    )
    
    message_id = response.get("MessageId")
    
    print(f"\n✅ EMAIL SENT SUCCESSFULLY!")
    print(f"   Message ID: {message_id}")
    print(f"\n⏳ Check your inbox (devshehzad@gmail.com)")
    print(f"   Email should arrive within 1-2 minutes")
    print(f"\n📊 Response: {response}")
    print("\n" + "=" * 70)
    
except Exception as e:
    print(f"\n❌ FAILED TO SEND EMAIL")
    print(f"   Error Type: {type(e).__name__}")
    print(f"   Error Message: {str(e)}")
    
    print("\n🔍 TROUBLESHOOTING:")
    print("   1. Check domain verification status in AWS SES console")
    print("   2. Make sure sender email is from verified domain")
    print("   3. Check AWS region (eu-north-1)")
    print("   4. Verify AWS credentials are valid")
    
    print("\n" + "=" * 70)
    import traceback
    traceback.print_exc()
    sys.exit(1)
