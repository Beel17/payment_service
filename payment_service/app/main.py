from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from app.db import Base, engine
from app.config import settings
from app.routes import payments, webhook
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI-based payment microservice with Paystack integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(payments.router)
app.include_router(webhook.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page with payment form
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "database": "connected"
    }

@app.get("/info")
async def app_info():
    """
    Application information endpoint
    """
    return {
        "app_name": settings.APP_NAME,
        "version": "1.0.0",
        "description": "FastAPI Payment Service with Paystack integration",
        "endpoints": {
            "home": "/",
            "health": "/health",
            "docs": "/docs",
            "payment_form": "/",
            "initiate_payment": "/payments/initiate",
            "payment_success": "/payments/success",
            "payment_failed": "/payments/failed",
            "webhook": "/webhook/paystack"
        },
        "features": [
            "Paystack payment integration",
            "Transaction verification",
            "Webhook handling",
            "SQLite database storage",
            "Modern responsive UI",
            "Async endpoints"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
