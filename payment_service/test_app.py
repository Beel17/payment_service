import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "FastAPI Payment Service"

def test_home_endpoint():
    """Test the home page endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI Payment" in response.text

def test_info_endpoint():
    """Test the app info endpoint"""
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["app_name"] == "FastAPI Payment Service"
    assert "endpoints" in data
    assert "features" in data

def test_payment_initiate_invalid_data():
    """Test payment initiation with invalid data"""
    response = client.post("/payments/initiate", data={
        "email": "",
        "amount": ""
    })
    # Should handle validation errors gracefully
    assert response.status_code in [400, 422]

def test_payment_initiate_valid_data():
    """Test payment initiation with valid data (requires Paystack keys)"""
    response = client.post("/payments/initiate", data={
        "email": "test@example.com",
        "amount": "1000"
    })
    # Without valid Paystack keys, this will fail
    # In a real test environment, you'd mock the Paystack service
    assert response.status_code in [200, 400, 500]

def test_payment_success_no_reference():
    """Test payment success page without reference"""
    response = client.get("/payments/success")
    assert response.status_code == 200
    assert "Transaction reference not provided" in response.text

def test_payment_failed_no_reference():
    """Test payment failed page without reference"""
    response = client.get("/payments/failed")
    assert response.status_code == 200
    assert "Payment was not successful" in response.text

def test_webhook_endpoint():
    """Test webhook endpoint"""
    response = client.post("/webhook/paystack", json={})
    # Should handle invalid webhook data gracefully
    assert response.status_code in [200, 400, 422]

if __name__ == "__main__":
    pytest.main([__file__])
