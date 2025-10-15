from sqlalchemy.orm import Session
from payment_service.app.models import Transaction
from payment_service.app.services.paystack_service import PaystackService
from typing import Optional

class VerificationService:
    def __init__(self):
        self.paystack_service = PaystackService()

    async def verify_and_update_transaction(
        self, 
        db: Session, 
        reference: str
    ) -> Optional[Transaction]:
        """
        Verify transaction with Paystack and update database
        
        Args:
            db: Database session
            reference: Transaction reference to verify
            
        Returns:
            Updated Transaction object or None if not found
        """
        # Get transaction from database
        transaction = db.query(Transaction).filter(
            Transaction.reference == reference
        ).first()
        
        if not transaction:
            return None
            
        try:
            # Verify with Paystack
            verification_response = await self.paystack_service.verify_transaction(reference)
            
            if verification_response.get("status"):
                data = verification_response.get("data", {})
                
                # Update transaction status
                if data.get("status") == "success":
                    transaction.status = "success"
                elif data.get("status") == "failed":
                    transaction.status = "failed"
                else:
                    transaction.status = "pending"
                
                # Update additional fields
                transaction.paystack_reference = data.get("reference")
                transaction.gateway_response = str(verification_response)
                
                db.commit()
                db.refresh(transaction)
                
                return transaction
            else:
                # Verification failed
                transaction.status = "failed"
                transaction.gateway_response = str(verification_response)
                db.commit()
                db.refresh(transaction)
                
                return transaction
                
        except Exception as e:
            # Handle verification error
            transaction.status = "failed"
            transaction.gateway_response = f"Verification error: {str(e)}"
            db.commit()
            db.refresh(transaction)
            
            return transaction

    def update_transaction_status(
        self, 
        db: Session, 
        reference: str, 
        status: str,
        paystack_reference: str = None
    ) -> Optional[Transaction]:
        """
        Update transaction status in database
        
        Args:
            db: Database session
            reference: Transaction reference
            status: New status
            paystack_reference: Paystack reference (optional)
            
        Returns:
            Updated Transaction object or None if not found
        """
        transaction = db.query(Transaction).filter(
            Transaction.reference == reference
        ).first()
        
        if transaction:
            transaction.status = status
            if paystack_reference:
                transaction.paystack_reference = paystack_reference
            
            db.commit()
            db.refresh(transaction)
            
        return transaction
