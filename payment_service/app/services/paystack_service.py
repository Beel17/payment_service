import httpx
from typing import Dict, Optional
from app.config import settings

class PaystackService:
    def __init__(self):
        self.base_url = settings.PAYSTACK_BASE_URL
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    async def initialize_transaction(
        self, 
        email: str, 
        amount: int, 
        reference: str,
        callback_url: str
    ) -> Dict:
        """
        Initialize a transaction with Paystack
        
        Args:
            email: Customer email
            amount: Amount in kobo (smallest currency unit)
            reference: Unique transaction reference
            callback_url: URL to redirect after payment
            
        Returns:
            Dict containing transaction initialization response
        """
        url = f"{self.base_url}/transaction/initialize"
        
        payload = {
            "email": email,
            "amount": amount,
            "reference": reference,
            "callback_url": callback_url,
            "currency": "NGN"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, 
                    json=payload, 
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise Exception(f"Paystack API error: {str(e)}")

    async def verify_transaction(self, reference: str) -> Dict:
        """
        Verify a transaction with Paystack
        
        Args:
            reference: Transaction reference to verify
            
        Returns:
            Dict containing transaction verification response
        """
        url = f"{self.base_url}/transaction/verify/{reference}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url, 
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise Exception(f"Paystack verification error: {str(e)}")

    def generate_reference(self) -> str:
        """
        Generate a unique transaction reference
        """
        import uuid
        import time
        timestamp = str(int(time.time()))
        unique_id = str(uuid.uuid4())[:8]
        return f"PAY_{timestamp}_{unique_id}"
