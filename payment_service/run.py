#!/usr/bin/env python3
"""
FastAPI Payment Service - Startup Script
Run this script to start the payment service
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    print("🚀 Starting FastAPI Payment Service...")
    print(f"📱 App: {settings.APP_NAME}")
    print(f"🌐 URL: http://localhost:8000")
    print(f"📚 Docs: http://localhost:8000/docs")
    print(f"🔍 Health: http://localhost:8000/health")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.DEBUG,
        log_level="info"
    )
