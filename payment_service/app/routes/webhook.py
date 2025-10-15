from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from payment_service.app.db import get_db
from payment_service.app.models import Transaction
from payment_service.app.config import settings
import json
import logging

router = APIRouter(prefix="/webhook", tags=["webhooks"])

@router.post("/paystack")
async def paystack_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Handle Paystack webhook events
    """
    try:
        # Get the raw body
        body = await request.body()
        
        # Parse JSON payload
        payload = json.loads(body.decode('utf-8'))
        
        # Verify webhook signature (in production, you should verify the signature)
        # For now, we'll process the webhook directly
        
        event_type = payload.get("event")
        data = payload.get("data", {})
        
        logging.info(f"Received Paystack webhook: {event_type}")
        
        if event_type == "charge.success":
            # Handle successful payment
            reference = data.get("reference")
            
            if reference:
                transaction = db.query(Transaction).filter(
                    Transaction.reference == reference
                ).first()
                
                if transaction:
                    transaction.status = "success"
                    transaction.paystack_reference = data.get("paystack_reference")
                    transaction.gateway_response = json.dumps(data)
                    
                    db.commit()
                    db.refresh(transaction)
                    
                    logging.info(f"Updated transaction {reference} to success")
        
        elif event_type == "charge.failed":
            # Handle failed payment
            reference = data.get("reference")
            
            if reference:
                transaction = db.query(Transaction).filter(
                    Transaction.reference == reference
                ).first()
                
                if transaction:
                    transaction.status = "failed"
                    transaction.paystack_reference = data.get("paystack_reference")
                    transaction.gateway_response = json.dumps(data)
                    
                    db.commit()
                    db.refresh(transaction)
                    
                    logging.info(f"Updated transaction {reference} to failed")
        
        return {"status": "success", "message": "Webhook processed"}
        
    except json.JSONDecodeError:
        logging.error("Invalid JSON in webhook payload")
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
        
    except Exception as e:
        logging.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
