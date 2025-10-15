from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from payment_service.app.db import get_db
from payment_service.app.models import Transaction
from payment_service.app.services.paystack_service import PaystackService
from payment_service.app.services.verification import VerificationService
from payment_service.app.config import settings
import logging

router = APIRouter(prefix="/payments", tags=["payments"])
templates = Jinja2Templates(directory="app/templates")

# Initialize services
paystack_service = PaystackService()
verification_service = VerificationService()

@router.post("/initiate")
async def initiate_payment(
    request: Request,
    email: str = Form(...),
    amount: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Initiate payment with Paystack
    """
    try:
        # Validate input
        if not email or not amount:
            raise HTTPException(status_code=400, detail="Email and amount are required")
        
        if amount < 100:  # Minimum amount in kobo (1 NGN)
            raise HTTPException(status_code=400, detail="Amount must be at least 1 NGN")
        
        # Generate unique reference
        reference = paystack_service.generate_reference()
        
        # Create transaction record
        transaction = Transaction(
            email=email,
            amount=amount,
            reference=reference,
            status="pending"
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        # Prepare callback URL
        base_url = str(request.base_url).rstrip('/')
        callback_url = f"{base_url}/payments/success"
        
        # Initialize payment with Paystack
        paystack_response = await paystack_service.initialize_transaction(
            email=email,
            amount=amount,
            reference=reference,
            callback_url=callback_url
        )
        
        if paystack_response.get("status"):
            # Redirect to Paystack checkout
            authorization_url = paystack_response["data"]["authorization_url"]
            return RedirectResponse(url=authorization_url, status_code=302)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Payment initialization failed: {paystack_response.get('message', 'Unknown error')}"
            )
            
    except Exception as e:
        logging.error(f"Payment initiation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Payment initiation failed: {str(e)}")

@router.get("/success")
async def payment_success(
    request: Request,
    reference: str = None,
    trxref: str = None,
    db: Session = Depends(get_db)
):
    """
    Handle successful payment redirect from Paystack
    """
    try:
        # Use trxref if reference is not provided (Paystack standard)
        transaction_ref = reference or trxref
        
        if not transaction_ref:
            return templates.TemplateResponse(
                "failed.html", 
                {"request": request, "error": "Transaction reference not provided"}
            )
        
        # Verify transaction with Paystack
        transaction = await verification_service.verify_and_update_transaction(
            db=db,
            reference=transaction_ref
        )
        
        if not transaction:
            return templates.TemplateResponse(
                "failed.html", 
                {"request": request, "error": "Transaction not found"}
            )
        
        if transaction.status == "success":
            return templates.TemplateResponse(
                "success.html", 
                {
                    "request": request, 
                    "transaction": transaction,
                    "amount_ngn": transaction.amount / 100  # Convert from kobo to NGN
                }
            )
        else:
            return templates.TemplateResponse(
                "failed.html", 
                {
                    "request": request, 
                    "error": f"Payment {transaction.status}",
                    "transaction": transaction
                }
            )
            
    except Exception as e:
        logging.error(f"Payment success handling error: {str(e)}")
        return templates.TemplateResponse(
            "failed.html", 
            {"request": request, "error": f"Error processing payment: {str(e)}"}
        )

@router.get("/failed")
async def payment_failed(
    request: Request,
    reference: str = None,
    trxref: str = None,
    db: Session = Depends(get_db)
):
    """
    Handle failed payment
    """
    transaction_ref = reference or trxref
    transaction = None
    
    if transaction_ref:
        transaction = db.query(Transaction).filter(
            Transaction.reference == transaction_ref
        ).first()
    
    return templates.TemplateResponse(
        "failed.html", 
        {
            "request": request, 
            "error": "Payment was not successful",
            "transaction": transaction
        }
    )
