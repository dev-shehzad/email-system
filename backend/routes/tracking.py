from fastapi import APIRouter
from fastapi.responses import Response, RedirectResponse
from database import get_db

router = APIRouter()

# 1x1 transparent GIF (for open tracking pixel)
GIF_1x1 = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!"
    b"\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01"
    b"\x00\x00\x02\x02D\x01\x00;"
)


@router.get("/t/open")
def track_open(campaign_id: int, email: str):
    """Track email open by returning a 1x1 pixel"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Record open event
        cur.execute(
            "INSERT INTO events (campaign_id, contact_email, event_type) VALUES (%s, %s, 'open')",
            (campaign_id, email)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error tracking open: {e}")
    
    # Always return the pixel (even if DB insert fails)
    return Response(content=GIF_1x1, media_type="image/gif")


@router.get("/t/click")
def track_click(campaign_id: int, email: str, url: str):
    """Track link click and redirect to original URL"""
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Record click event
        cur.execute(
            "INSERT INTO events (campaign_id, contact_email, event_type) VALUES (%s, %s, 'click')",
            (campaign_id, email)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error tracking click: {e}")
    
    # Redirect to original URL
    return RedirectResponse(url=url, status_code=302)
