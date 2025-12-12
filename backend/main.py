import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv

from database import get_db
from routes import auth
from routes import contacts
from routes import campaigns
from routes import tracking
from routes import unsubscribe
from routes import webhooks
from routes import stats

load_dotenv()

app = FastAPI()

# CORS (frontend access allowed)
# For development: allow all origins
# For production: set CORS_ORIGINS env var with specific URL
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins != "*":
    cors_origins = cors_origins.split(",")
else:
    cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def check():
    return {"status": "ok"}

@app.get("/db-test")
def db_test():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        conn.close()
        return {"db": "connected", "result": result[0]}
    except Exception as e:
        return {"db": "error", "details": str(e)}

# Include Routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(contacts.router, prefix="/api", tags=["contacts"])
app.include_router(campaigns.router, prefix="/api", tags=["campaigns"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(webhooks.router, prefix="/api", tags=["webhooks"])
app.include_router(tracking.router, prefix="/api", tags=["tracking"])

# Public routes (no /api prefix) - needed for unsubscribe
app.include_router(unsubscribe.router, tags=["unsubscribe"])

# Run server if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    # When using reload=True, uvicorn requires the application to be passed
    # as an import string (not as an app object). Use the import string
    # to allow `python main.py` to run with reload in development.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
