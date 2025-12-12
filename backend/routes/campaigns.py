from fastapi import APIRouter
from database import get_db
from routes.unsubscribe import generate_unsubscribe_token
import os
import time
import re
import base64
import hashlib
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TRACKING_SUBDOMAIN = os.getenv("TRACKING_SUBDOMAIN", "links.yourdomain.com")

# SES rate limits: 14 emails per second (for production tier)
# We'll be conservative: 10 emails per second = 0.1 seconds per email
EMAIL_SEND_DELAY = 0.1


# ---------------------------------------------------------
# HELPER FUNCTION: Get Verified Identities
# ---------------------------------------------------------
def get_verified_identities():
    """Get all verified email addresses and domains"""
    from ses import ses
    try:
        # Get verified emails
        verified_emails = ses.list_verified_email_addresses()
        email_list = verified_emails.get('VerifiedEmailAddresses', [])
        
        # Get verified domains
        verified_domains = ses.list_identities(IdentityType='Domain')
        domain_list = verified_domains.get('Identities', [])
        
        return {
            "emails": email_list,
            "domains": domain_list,
            "all": email_list + domain_list
        }
    except Exception as e:
        print(f"Error getting identities: {str(e)}")
        return {"emails": [], "domains": [], "all": []}


def is_sender_verified(sender_email: str) -> tuple[bool, str]:
    """Check if sender email is verified in AWS SES
    
    NOTE: In AWS SES Sandbox mode, only DIRECTLY VERIFIED emails can send.
    Domain verification alone is NOT sufficient.
    """
    identities = get_verified_identities()
    
    # Check if it's a directly verified email (this is what actually works)
    if sender_email in identities["emails"]:
        return True, f"✅ Email {sender_email} is verified and can send"
    
    # Even if domain is verified, specific emails within that domain still need verification
    # in SES Sandbox mode. Do NOT allow it just because domain is verified.
    domain = sender_email.split('@')[-1] if '@' in sender_email else None
    if domain and domain in identities["domains"]:
        # Domain is verified, but specific email is not
        return False, f"❌ Email {sender_email} is NOT verified. Domain {domain} is verified, but individual emails must also be verified in AWS SES. Verified emails that can send: {', '.join(identities['emails']) if identities['emails'] else 'None'}"
    
    # Not verified at all
    verified_list = ", ".join(identities["emails"]) if identities["emails"] else "None"
    return False, f"❌ Sender {sender_email} is not verified. Verified emails that can send: {verified_list}"


# ---------------------------------------------------------
# HEALTH CHECK / SES VERIFICATION
# ---------------------------------------------------------
@router.get("/health/ses")
def check_ses_status():
    """Check AWS SES configuration and account status"""
    from ses import ses
    
    try:
        # Get account sending limits
        account_info = ses.get_account_sending_enabled()
        
        # Get send quota
        quota = ses.get_send_quota()
        
        # Get verified identities
        identities = get_verified_identities()
        verified_emails = identities["emails"]
        verified_domains = identities["domains"]
        
        status = "ok" if (verified_emails or verified_domains) else "error"
        
        print(f"\n✅ SES ACCOUNT STATUS:")
        print(f"   Account Sending Enabled: {account_info.get('Enabled')}")
        print(f"   Verified Emails: {verified_emails}")
        print(f"   Verified Domains: {verified_domains}")
        print(f"   Max Send Rate: {quota.get('MaxSendRate')} emails/sec")
        print(f"   Region: {os.getenv('AWS_REGION')}\n")
        
        return {
            "status": status,
            "ses_enabled": account_info.get('Enabled'),
            "verified_emails": verified_emails,
            "verified_domains": verified_domains,
            "max_send_rate": quota.get('MaxSendRate'),
            "region": os.getenv('AWS_REGION'),
            "has_credentials": bool(os.getenv('AWS_ACCESS_KEY_ID')),
            "message": "✅ Ready to send emails" if (verified_emails or verified_domains) else "❌ No verified identities. Please verify at least one email or domain in AWS SES console."
        }
    except Exception as e:
        print(f"\n❌ SES CHECK FAILED:")
        print(f"   Error: {str(e)}\n")
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "region": os.getenv('AWS_REGION'),
            "has_credentials": bool(os.getenv('AWS_ACCESS_KEY_ID')),
            "message": "❌ Failed to connect to AWS SES. Check your credentials."
        }


def prepare_email_html(html: str, campaign_id: int, contact_email: str, base_url: str) -> str:
    """
    Prepare email HTML by:
    1. Injecting open tracking pixel
    2. Rewriting links for click tracking
    """
    # 1) Inject open tracking pixel
    tracking_pixel = (
        f'<img src="{base_url}/api/t/open?campaign_id={campaign_id}&email={contact_email}" '
        f'width="1" height="1" style="display:none;" />'
    )
    
    if '</body>' in html.lower():
        html = re.sub(r'</body>', f'{tracking_pixel}\n</body>', html, flags=re.IGNORECASE)
    else:
        html += f'\n{tracking_pixel}'
    
    # 2) Rewrite links for click tracking
    def replace_link(match):
        original_url = match.group(1)
        # Simple URL encoding
        tracking_url = (
            f"{base_url}/api/t/click?campaign_id={campaign_id}&email={contact_email}&url={original_url}"
        )
        return f'href="{tracking_url}"'
    
    html = re.sub(r'href="(https?://[^"]+)"', replace_link, html, flags=re.IGNORECASE)
    
    # 3) Inject unsubscribe link
    token = generate_unsubscribe_token(contact_email, campaign_id)
    unsubscribe_link = (
        f'<div style="text-align:center;margin-top:20px;padding:10px;color:#999;font-size:12px;">'
        f'<a href="{base_url}/unsubscribe/{token}?email={contact_email}" style="color:#999;">Unsubscribe</a>'
        f'</div>'
    )
    
    if '</body>' in html.lower():
        html = re.sub(r'</body>', f'{unsubscribe_link}\n</body>', html, flags=re.IGNORECASE)
    else:
        html += f'\n{unsubscribe_link}'
    
    return html





# ---------------------------------------------------------
# 1) CREATE CAMPAIGN
# ---------------------------------------------------------
@router.post("/campaign/create")
def create_campaign(subject: str, sender: str, html: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO campaigns (subject, sender, html)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (subject, sender, html)
    )

    camp_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {
        "id": camp_id,
        "status": "created"
    }


# ---------------------------------------------------------
# 2) SEND TEST EMAIL
# ---------------------------------------------------------
@router.post("/campaign/test")
def send_test_email(campaign_id: int, test_email: str):
    """Send a test email to specified address"""
    from ses import ses
    
    conn = get_db()
    cur = conn.cursor()

    # Get campaign info
    cur.execute(
        "SELECT subject, sender, html FROM campaigns WHERE id = %s",
        (campaign_id,)
    )
    camp = cur.fetchone()

    if not camp:
        return {"error": "Campaign not found"}

    subject, sender, html = camp

    # ✅ VALIDATE SENDER BEFORE SENDING
    is_verified, verification_message = is_sender_verified(sender)
    
    if not is_verified:
        print(f"\n⚠️ SENDER VERIFICATION FAILED:")
        print(f"   {verification_message}")
        return {
            "error": "Sender email not verified",
            "message": verification_message,
            "verified_identities": get_verified_identities(),
            "suggestion": "Use one of the verified identities as the sender, or verify the sender email in AWS SES console"
        }
    
    # Prepare HTML with tracking
    prepared_html = prepare_email_html(html, campaign_id, test_email, BASE_URL)

    try:
        print(f"\n🔍 SENDING TEST EMAIL:")
        print(f"   From: {sender} {verification_message}")
        print(f"   To: {test_email}")
        print(f"   Subject: {subject}")
        print(f"   Region: {os.getenv('AWS_REGION')}")
        
        # Send test email
        response = ses.send_email(
            Source=sender,
            Destination={"ToAddresses": [test_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {
                    "Html": {"Data": prepared_html}
                }
            }
        )
        
        message_id = response.get("MessageId")
        print(f"✅ Email sent successfully!")
        print(f"   MessageId: {message_id}")
        print(f"   Response: {response}\n")
        
        return {
            "status": "sent",
            "message": f"Test email sent to {test_email}",
            "message_id": message_id
        }
    except Exception as e:
        print(f"\n❌ FAILED TO SEND TEST EMAIL:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {str(e)}")
        print(f"   Full Error: {repr(e)}\n")
        import traceback
        traceback.print_exc()
        return {"error": str(e), "error_type": type(e).__name__}
    finally:
        cur.close()
        conn.close()


# ---------------------------------------------------------
# 3) SEND CAMPAIGN (SES batch send with rate limiting)
# ---------------------------------------------------------
@router.post("/campaign/send")
def send_campaign(campaign_id: int):
    from ses import ses
    
    conn = get_db()
    cur = conn.cursor()

    # Get campaign info
    cur.execute(
        "SELECT subject, sender, html FROM campaigns WHERE id = %s",
        (campaign_id,)
    )
    camp = cur.fetchone()

    if not camp:
        cur.close()
        conn.close()
        return {"error": "Campaign not found"}

    subject, sender, html = camp

    # ✅ VALIDATE SENDER BEFORE SENDING
    is_verified, verification_message = is_sender_verified(sender)
    
    if not is_verified:
        print(f"\n⚠️ SENDER VERIFICATION FAILED:")
        print(f"   {verification_message}")
        cur.close()
        conn.close()
        return {
            "error": "Sender email not verified",
            "message": verification_message,
            "verified_identities": get_verified_identities(),
            "suggestion": "Use one of the verified identities as the sender, or verify the sender email in AWS SES console"
        }

    # Get active contacts (not unsubscribed, not in suppressions)
    cur.execute(
        """
        SELECT c.email FROM contacts c
        WHERE c.unsubscribed = FALSE
        AND NOT EXISTS (
            SELECT 1 FROM suppressions s WHERE s.email = c.email
        )
        """
    )
    contacts = cur.fetchall()

    sent = 0
    failed = 0
    total = len(contacts)
    
    print(f"\n📧 STARTING CAMPAIGN SEND:")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Subject: {subject}")
    print(f"   From: {sender}")
    print(f"   Total Contacts: {total}")
    print(f"   AWS Region: {os.getenv('AWS_REGION')}\n")

    # Process in batches with rate limiting
    for (email,) in contacts:
        try:
            # Check if already sent (avoid duplicates)
            cur.execute(
                """
                SELECT id FROM campaign_sends 
                WHERE campaign_id = %s AND contact_email = %s
                """,
                (campaign_id, email)
            )
            if cur.fetchone():
                continue  # Skip if already sent
            
            # Prepare HTML with tracking
            prepared_html = prepare_email_html(html, campaign_id, email, BASE_URL)

            # Send email via SES
            response = ses.send_email(
                Source=sender,
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {
                        "Html": {"Data": prepared_html}
                    }
                }
            )
            
            # Get message ID from response
            message_id = response.get("MessageId")
            print(f"✅ Sent to {email} (MessageId: {message_id})")
            
            # Record send into campaign_sends table
            cur.execute(
                """
                INSERT INTO campaign_sends (campaign_id, contact_email, message_id, delivered)
                VALUES (%s, %s, %s, TRUE)
                """,
                (campaign_id, email, message_id)
            )
            conn.commit()
            sent += 1
            
            # Rate limiting: wait between sends
            if sent < total:  # Don't wait after last email
                time.sleep(EMAIL_SEND_DELAY)
                
        except Exception as e:
            print(f"❌ Failed to send to {email}: {str(e)} ({type(e).__name__})")
            failed += 1
            
            # Record failed send into campaign_sends table
            cur.execute(
                """
                INSERT INTO campaign_sends (campaign_id, contact_email, delivered, bounce_type)
                VALUES (%s, %s, FALSE, %s)
                ON CONFLICT (campaign_id, contact_email) DO NOTHING
                """,
                (campaign_id, email, "soft" if "bounce" in str(e).lower() else None)
            )
            conn.commit()
            
            # Still rate limit even on failure
            if (sent + failed) < total:
                time.sleep(EMAIL_SEND_DELAY)
            
            continue

    cur.close()
    conn.close()
    
    print(f"\n📊 CAMPAIGN SEND COMPLETE:")
    print(f"   Sent: {sent}/{total}")
    print(f"   Failed: {failed}/{total}\n")

    return {
        "status": "completed",
        "total_sent": sent,
        "total_failed": failed,
        "total_contacts": total
    }


# ---------------------------------------------------------
# 4) LIST ALL CAMPAIGNS
# ---------------------------------------------------------
@router.get("/campaigns/all")
def get_all():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, subject, sender, created_at FROM campaigns ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = [
        {
            "id": r[0],
            "subject": r[1],
            "sender": r[2],
            "created_at": r[3].isoformat() if r[3] else None
        }
        for r in rows
    ]

    return data
