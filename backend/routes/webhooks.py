from fastapi import APIRouter, Request, HTTPException
from database import get_db
import json

router = APIRouter()


@router.post("/webhooks/ses")
async def ses_webhook(request: Request):
    """Handle SES bounce and complaint webhooks"""
    try:
        # SES sends notifications via SNS (Simple Notification Service)
        # The webhook payload structure depends on SES configuration
        body = await request.json()
        
        # Handle SNS notification format
        if "Type" in body:
            if body["Type"] == "Notification":
                message = json.loads(body["Message"])
                
                # Handle bounce
                if message.get("notificationType") == "Bounce":
                    bounce = message.get("bounce", {})
                    bounce_type = "hard" if bounce.get("bounceType") == "Permanent" else "soft"
                    
                    for recipient in bounce.get("bouncedRecipients", []):
                        email = recipient.get("emailAddress")
                        if email:
                            _handle_bounce(email, bounce_type)
                
                # Handle complaint
                elif message.get("notificationType") == "Complaint":
                    complaint = message.get("complaint", {})
                    
                    for recipient in complaint.get("complainedRecipients", []):
                        email = recipient.get("emailAddress")
                        if email:
                            _handle_complaint(email)
        
        # Handle direct SES notification format (if configured differently)
        elif "notificationType" in body:
            if body["notificationType"] == "Bounce":
                bounce = body.get("bounce", {})
                bounce_type = "hard" if bounce.get("bounceType") == "Permanent" else "soft"
                
                for recipient in bounce.get("bouncedRecipients", []):
                    email = recipient.get("emailAddress")
                    if email:
                        _handle_bounce(email, bounce_type)
            
            elif body["notificationType"] == "Complaint":
                complaint = body.get("complaint", {})
                
                for recipient in complaint.get("complainedRecipients", []):
                    email = recipient.get("emailAddress")
                    if email:
                        _handle_complaint(email)
        
        return {"status": "success"}
        
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        # Don't raise error to prevent SES from retrying
        return {"status": "error", "message": str(e)}


def _handle_bounce(email: str, bounce_type: str):
    """Handle bounce - add to suppressions and mark contact as unsubscribed"""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Add to suppressions table
        cur.execute(
            """
            INSERT INTO suppressions (email, reason, bounce_type)
            VALUES (%s, 'bounce', %s)
            ON CONFLICT (email) 
            DO UPDATE SET reason = 'bounce', bounce_type = %s, updated_at = CURRENT_TIMESTAMP
            """,
            (email, bounce_type, bounce_type)
        )
        
        # Mark contact as unsubscribed (hard bounces only)
        if bounce_type == "hard":
            cur.execute(
                "UPDATE contacts SET unsubscribed = TRUE WHERE email = %s",
                (email,)
            )
            
            # Record bounce event
            cur.execute(
                """
                INSERT INTO events (contact_email, event_type, metadata)
                VALUES (%s, 'bounce', %s::jsonb)
                """,
                (email, f'{{"bounce_type": "{bounce_type}"}}')
            )
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error handling bounce: {str(e)}")
    finally:
        cur.close()
        conn.close()


def _handle_complaint(email: str):
    """Handle complaint - add to suppressions and unsubscribe"""
    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Add to suppressions table
        cur.execute(
            """
            INSERT INTO suppressions (email, reason)
            VALUES (%s, 'complaint')
            ON CONFLICT (email) 
            DO UPDATE SET reason = 'complaint', updated_at = CURRENT_TIMESTAMP
            """,
            (email,)
        )
        
        # Mark contact as unsubscribed
        cur.execute(
            "UPDATE contacts SET unsubscribed = TRUE WHERE email = %s",
            (email,)
        )
        
        # Record complaint event
        cur.execute(
            """
            INSERT INTO events (contact_email, event_type)
            VALUES (%s, 'complaint')
            """,
            (email,)
        )
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error handling complaint: {str(e)}")
    finally:
        cur.close()
        conn.close()
