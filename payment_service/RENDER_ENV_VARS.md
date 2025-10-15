# 🔧 Render Environment Variables Configuration

## Required Environment Variables

Set these environment variables in your Render dashboard under "Environment":

### 1. Paystack Configuration (REQUIRED)
```bash
PAYSTACK_SECRET_KEY=sk_live_your_secret_key_here
PAYSTACK_PUBLIC_KEY=pk_live_your_public_key_here
```
**Format**: 
- Secret Key: `sk_live_` or `sk_test_` followed by your key
- Public Key: `pk_live_` or `pk_test_` followed by your key
- Get these from: [Paystack Dashboard](https://dashboard.paystack.com/#/settings/developers)

### 2. Application Security (REQUIRED)
```bash
SECRET_KEY=your-super-secret-key-here-generate-a-long-random-string
```
**Format**: Any long random string (minimum 32 characters)
**Example**: `my-super-secret-key-for-production-2024-xyz789`

### 3. Environment Configuration
```bash
DEBUG=false
ENVIRONMENT=production
RENDER=true
```
**Format**: 
- DEBUG: `true` or `false` (use `false` for production)
- ENVIRONMENT: `production` or `development`
- RENDER: `true` (indicates running on Render)

### 4. Database Configuration (Optional)
```bash
DATABASE_URL=sqlite:///./payment_service.db
```
**Format**: 
- For SQLite (default): `sqlite:///./payment_service.db`
- For PostgreSQL: `postgresql://user:password@host:port/database`
- Render provides this automatically if you add a PostgreSQL database

### 5. CORS Configuration (Optional)
```bash
ALLOWED_ORIGINS=https://your-app-name.onrender.com
```
**Format**: Comma-separated list of allowed origins
**Example**: `https://fastapi-payment-service.onrender.com,https://yourdomain.com`

## How to Set Environment Variables in Render

1. Go to your Render dashboard
2. Click on your service
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add each variable with the exact name and value

## Environment Variables Summary

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PAYSTACK_SECRET_KEY` | ✅ Yes | - | Paystack secret key |
| `PAYSTACK_PUBLIC_KEY` | ✅ Yes | - | Paystack public key |
| `SECRET_KEY` | ✅ Yes | - | App secret key |
| `DEBUG` | ❌ No | `false` | Debug mode |
| `ENVIRONMENT` | ❌ No | `production` | Environment type |
| `RENDER` | ❌ No | `true` | Running on Render |
| `DATABASE_URL` | ❌ No | SQLite | Database connection |
| `ALLOWED_ORIGINS` | ❌ No | Auto | CORS origins |

## Production Checklist

- [ ] Set `PAYSTACK_SECRET_KEY` (production key)
- [ ] Set `PAYSTACK_PUBLIC_KEY` (production key)
- [ ] Set strong `SECRET_KEY`
- [ ] Set `DEBUG=false`
- [ ] Set `ENVIRONMENT=production`
- [ ] Configure webhook URL in Paystack dashboard
- [ ] Test payment flow with real cards (small amounts)

## Paystack Webhook Configuration

After deployment, configure Paystack webhooks:

1. Go to [Paystack Dashboard](https://dashboard.paystack.com/#/settings/developers)
2. Click "Webhooks"
3. Add webhook URL: `https://your-app-name.onrender.com/webhook/paystack`
4. Select events: `charge.success`, `charge.failed`
5. Save configuration

## Testing Your Deployment

After setting environment variables:

1. **Health Check**: `https://your-app.onrender.com/health`
2. **API Docs**: `https://your-app.onrender.com/docs`
3. **Payment Form**: `https://your-app.onrender.com/`

## Troubleshooting

If deployment fails:
- Check all required environment variables are set
- Verify Paystack keys are correct
- Check build logs for dependency issues
- Ensure `runtime.txt` specifies `python-3.11.9`
