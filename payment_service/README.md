# FastAPI Payment Service 💳

A modern, production-ready payment microservice built with FastAPI and integrated with Paystack for secure payment processing.

## 🌟 Features

- **FastAPI Backend**: High-performance async API framework
- **Paystack Integration**: Secure payment processing with Nigeria's leading payment gateway
- **Transaction Verification**: Real-time payment status verification
- **Webhook Handling**: Automated transaction status updates
- **SQLite Database**: Lightweight database for transaction storage
- **Modern UI**: Responsive, beautiful web interface
- **Async Endpoints**: Non-blocking API operations
- **Health Checks**: Built-in monitoring endpoints
- **Comprehensive Logging**: Detailed transaction and error logging

## 🏗️ Project Structure

```
payment_service/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLAlchemy database models
│   ├── db.py                   # Database configuration
│   ├── config.py               # Application settings
│   ├── services/
│   │   ├── paystack_service.py # Paystack API integration
│   │   └── verification.py     # Transaction verification logic
│   ├── routes/
│   │   ├── payments.py         # Payment-related endpoints
│   │   └── webhook.py          # Webhook handling
│   ├── templates/
│   │   ├── index.html          # Payment form
│   │   ├── success.html        # Success page
│   │   └── failed.html         # Failed payment page
│   └── static/
│       └── styles.css          # Modern CSS styling
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Paystack account and API keys

### Installation

1. **Clone or download the project**
   ```bash
   cd payment_service
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   PAYSTACK_SECRET_KEY=sk_test_your_secret_key_here
   PAYSTACK_PUBLIC_KEY=pk_test_your_public_key_here
   SECRET_KEY=your-secret-key-for-jwt-etc
   DEBUG=True
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the application**
   - **Home Page**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health

## 📱 How It Works

### Payment Flow

1. **User visits home page** (`/`) - Beautiful payment form
2. **Fills in email and amount** - Form validation included
3. **Submits payment** - POST to `/payments/initiate`
4. **Redirected to Paystack** - Secure payment processing
5. **Payment completion** - Redirected back to `/payments/success`
6. **Transaction verification** - Backend verifies with Paystack
7. **Success/failure display** - User sees result with transaction details

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with payment form |
| `/health` | GET | Health check endpoint |
| `/info` | GET | Application information |
| `/payments/initiate` | POST | Initiate payment with Paystack |
| `/payments/success` | GET | Handle successful payment |
| `/payments/failed` | GET | Handle failed payment |
| `/webhook/paystack` | POST | Paystack webhook endpoint |
| `/docs` | GET | Interactive API documentation |

### Database Schema

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    amount INTEGER NOT NULL,        -- Amount in kobo
    reference VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    paystack_reference VARCHAR(255),
    gateway_response TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PAYSTACK_SECRET_KEY` | Paystack secret key (required) | - |
| `PAYSTACK_PUBLIC_KEY` | Paystack public key (required) | - |
| `SECRET_KEY` | Application secret key | auto-generated |
| `DEBUG` | Enable debug mode | False |
| `DATABASE_URL` | Database connection string | sqlite:///./payment_service.db |

### Paystack Setup

1. **Create Paystack Account**: Sign up at [paystack.com](https://paystack.com)
2. **Get API Keys**: 
   - Secret Key: `sk_test_...` (for server-side)
   - Public Key: `pk_test_...` (for client-side)
3. **Configure Webhooks**: Set webhook URL to `https://yourdomain.com/webhook/paystack`

## 🧪 Testing

### Manual Testing

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Test health endpoint**:
   ```bash
   curl http://localhost:8000/health
   ```

3. **Test payment flow**:
   - Visit http://localhost:8000
   - Enter test email and amount
   - Use Paystack test cards for payment

### Automated Testing

```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Deployment

1. **Set production environment variables**
2. **Use a production ASGI server**:
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Use a production database** (PostgreSQL recommended)
4. **Set up SSL/HTTPS**
5. **Configure reverse proxy** (Nginx)

## 🔒 Security Features

- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Configurable cross-origin policies
- **Error Handling**: Secure error messages
- **Logging**: Detailed audit trail
- **Environment Variables**: Secure configuration management

## 🛠️ Development

### Adding New Features

1. **Database Changes**: Update `models.py`
2. **New Endpoints**: Add to `routes/`
3. **Business Logic**: Add to `services/`
4. **Frontend**: Update `templates/` and `static/`

### Code Style

- Follow PEP 8
- Use type hints
- Async/await for I/O operations
- Comprehensive error handling

## 📊 Monitoring

### Health Checks
- `/health` - Basic health status
- `/info` - Application information

### Logging
- Transaction logs
- Error tracking
- Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation at `/docs`
- Review the logs for debugging

## 🎯 Next Steps

This payment service is ready for production use and can be extended with:

- User authentication (JWT)
- Admin dashboard
- Transaction analytics
- Multiple payment methods
- Email notifications
- API rate limiting
- Database migrations
- Docker containerization

---

**Built with ❤️ using FastAPI and Paystack**
