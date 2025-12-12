from fastapi import APIRouter, HTTPException
from database import get_db
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")


def generate_unsubscribe_token(contact_email: str, campaign_id: int) -> str:
    """Generate a secure unsubscribe token"""
    message = f"{contact_email}:{campaign_id}"
    token = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return token


def verify_unsubscribe_token(token: str, contact_email: str, campaign_id: int) -> bool:
    """Verify unsubscribe token"""
    expected_token = generate_unsubscribe_token(contact_email, campaign_id)
    return hmac.compare_digest(token, expected_token)


@router.get("/unsubscribe/{token}")
def unsubscribe(token: str, email: str):
    """Unsubscribe a contact from emails"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Find contact and verify token with any campaign
        # Since we need campaign_id to verify, we'll check all campaigns
        cur.execute(
            "SELECT email FROM contacts WHERE email = %s",
            (email,)
        )
        contact = cur.fetchone()
        
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Verify token by checking campaigns
        cur.execute(
            "SELECT id FROM campaigns ORDER BY id DESC LIMIT 100"
        )
        campaigns = cur.fetchall()
        
        token_valid = False
        for (campaign_id,) in campaigns:
            if verify_unsubscribe_token(token, email, campaign_id):
                token_valid = True
                break
        
        if not token_valid:
            raise HTTPException(status_code=400, detail="Invalid unsubscribe token")
        
        # Mark as unsubscribed
        cur.execute(
            "UPDATE contacts SET unsubscribed = TRUE WHERE email = %s",
            (email,)
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Return HTML page
        html_response = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Unsubscribed</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                .container { max-width: 500px; margin: 0 auto; }
                h1 { color: #333; }
                p { color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✓ Successfully Unsubscribed</h1>
                <p>You have been unsubscribed from our mailing list.</p>
                <p>You will no longer receive emails from us.</p>
            </div>
        </body>
        </html>
        """
        
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=html_response)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
