from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database import get_db

router = APIRouter()


@router.get("/stats/dashboard")
def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db()
    cur = conn.cursor()

    try:
        # Total campaigns
        cur.execute("SELECT COUNT(*) FROM campaigns")
        total_campaigns = cur.fetchone()[0]

        # Total contacts
        cur.execute("SELECT COUNT(*) FROM contacts")
        total_contacts = cur.fetchone()[0]

        # Active contacts (not unsubscribed)
        cur.execute("SELECT COUNT(*) FROM contacts WHERE unsubscribed = FALSE")
        active_contacts = cur.fetchone()[0]

        # Total emails sent
        cur.execute("SELECT COUNT(*) FROM campaign_sends")
        total_sent = cur.fetchone()[0]

        # Total delivered (sent and not bounced)
        cur.execute("""
            SELECT COUNT(*) FROM campaign_sends 
            WHERE delivered = TRUE OR (delivered = FALSE AND bounce_type IS NULL)
        """)
        total_delivered = cur.fetchone()[0]

        # Total opens
        cur.execute("SELECT COUNT(DISTINCT contact_email) FROM events WHERE event_type = 'open'")
        total_opens = cur.fetchone()[0]

        # Total clicks
        cur.execute("SELECT COUNT(DISTINCT contact_email) FROM events WHERE event_type = 'click'")
        total_clicks = cur.fetchone()[0]

        # Calculate rates
        open_rate = (total_opens / total_delivered * 100) if total_delivered > 0 else 0
        click_rate = (total_clicks / total_delivered * 100) if total_delivered > 0 else 0

        return {
            "campaigns": total_campaigns,
            "contacts": total_contacts,
            "active_contacts": active_contacts,
            "sent": total_sent,
            "delivered": total_delivered,
            "opens": total_opens,
            "clicks": total_clicks,
            "open_rate": round(open_rate, 2),
            "click_rate": round(click_rate, 2)
        }

    except Exception as e:
        # Log error to server (print is simple and visible in dev logs)
        print(f"Error in get_dashboard_stats: {e}")
        # Return clear JSON error so client sees details and CORS middleware can add headers
        return JSONResponse(status_code=500, content={"error": "Failed to fetch dashboard stats", "details": str(e)})

    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass


@router.get("/stats/campaign/{campaign_id}")
def get_campaign_stats(campaign_id: int):
    """Get statistics for a specific campaign"""
    conn = get_db()
    cur = conn.cursor()

    try:
        # Check if campaign exists
        cur.execute("SELECT id FROM campaigns WHERE id = %s", (campaign_id,))
        if not cur.fetchone():
            return JSONResponse(status_code=404, content={"error": "Campaign not found"})

        # Total sent
        cur.execute(
            "SELECT COUNT(*) FROM campaign_sends WHERE campaign_id = %s",
            (campaign_id,)
        )
        sent = cur.fetchone()[0]

        # Total delivered
        cur.execute(
            """
            SELECT COUNT(*) FROM campaign_sends 
            WHERE campaign_id = %s 
            AND (delivered = TRUE OR (delivered = FALSE AND bounce_type IS NULL))
            """,
            (campaign_id,)
        )
        delivered = cur.fetchone()[0]

        # Total opens
        cur.execute(
            "SELECT COUNT(DISTINCT contact_email) FROM events WHERE campaign_id = %s AND event_type = 'open'",
            (campaign_id,)
        )
        opens = cur.fetchone()[0]

        # Total clicks
        cur.execute(
            "SELECT COUNT(DISTINCT contact_email) FROM events WHERE campaign_id = %s AND event_type = 'click'",
            (campaign_id,)
        )
        clicks = cur.fetchone()[0]

        # Bounces
        cur.execute(
            "SELECT COUNT(*) FROM campaign_sends WHERE campaign_id = %s AND bounce_type IS NOT NULL",
            (campaign_id,)
        )
        bounces = cur.fetchone()[0]

        open_rate = (opens / delivered * 100) if delivered > 0 else 0
        click_rate = (clicks / delivered * 100) if delivered > 0 else 0

        return {
            "campaign_id": campaign_id,
            "sent": sent,
            "delivered": delivered,
            "opens": opens,
            "clicks": clicks,
            "bounces": bounces,
            "open_rate": round(open_rate, 2),
            "click_rate": round(click_rate, 2)
        }

    except Exception as e:
        print(f"Error in get_campaign_stats({campaign_id}): {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to fetch campaign stats", "details": str(e)})

    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
