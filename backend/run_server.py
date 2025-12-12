#!/usr/bin/env python3
"""
Simple server starter - runs without reload mode to keep server alive
"""
import uvicorn
from main import app

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Email System Backend - Starting")
    print("="*60)
    print("\n📊 Check SES Status: http://127.0.0.1:8000/api/health/ses")
    print("📧 Dashboard: http://localhost:5173")
    print("\n" + "="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Keep server running
        log_level="info"
    )
