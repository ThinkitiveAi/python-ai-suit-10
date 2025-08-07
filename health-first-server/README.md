# HealthFirst Provider Registration Backend

A comprehensive Django REST Framework backend for healthcare provider registration with secure authentication, validation, and email verification.

## 🚀 Features

### Core Functionality
- **Provider Registration**: Secure registration with comprehensive validation
- **Email Verification**: Automated email verification with secure tokens
- **Rate Limiting**: 5 registration attempts per IP per hour
- **Audit Logging**: Complete logging of registration attempts
- **Admin Interface**: Django admin for provider management

### Security Features
- **Password Security**: bcrypt hashing with 12+ salt rounds
- **Input Sanitization**: Protection against injection attacks
- **Rate Limiting**: IP-based rate limiting with Redis
- **Secure Headers**: XSS, clickjacking, and MIME-type protection
- **Field Validation**: Comprehensive validation for all input fields

### API Features
- **RESTful API**: Clean, documented REST endpoints
- **Error Handling**: Detailed error responses with proper HTTP codes
- **Email Integration**: Automated email notifications
- **Background Tasks**: Celery for asynchronous processing

## 🏗️ Architecture

### Tech Stack
- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache/Queue**: Redis 7
- **Task Queue**: Celery
- **Web Server**: Gunicorn + Nginx
- **Deployment**: Docker + Docker Compose

### Project Structure
```
health-first-server/
├── healthfirst/              # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── celery.py            # Celery configuration
├── providers/               # Provider app
│   ├── models.py            # Provider, ClinicAddress models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # Provider URLs
│   ├── admin.py             # Django admin
│   ├── tasks.py             # Celery tasks
│   ├── middleware.py        # Rate limiting middleware
│   ├── signals.py           # Django signals
│   └── utils/               # Utility functions
│       ├── password_utils.py    # Password validation
│       ├── email_utils.py       # Email utilities
│       ├── validation_utils.py  # Input validation
│       └── exception_handler.py # Custom exception handler
├── templates/               # Email templates
│   └── emails/
│       ├── verification_email.html
│       ├── welcome_email.html
│       └── admin_notification.html
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── nginx.conf              # Nginx configuration
├── .env                    # Environment variables
└── manage.py               # Django management script
```

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)
- Redis 7+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**:
```bash
git clone <repository-url>
cd health-first-server
```

2. **Start all services**:
```bash
docker-compose up --build
```

3. **Create superuser** (in a new terminal):
```bash
docker-compose exec web python manage.py createsuperuser
```

4. **Access the application**:
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- API Health Check: http://localhost:8000/api/v1/health
- Celery Monitoring: http://localhost:5555

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run migrations**:
```bash
python manage.py migrate
```

4. **Create superuser**:
```bash
python manage.py createsuperuser
```

5. **Start development server**:
```bash
python manage.py runserver
```

6. **Start Celery worker** (in another terminal):
```bash
celery -A healthfirst worker --loglevel=info
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1/
```

### Endpoints

#### Provider Registration
**POST** `/api/v1/provider/register`

Register a new healthcare provider.

**Request Body**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@clinic.com",
  "phone_number": "+1234567890",
  "password": "SecurePassword123!",
  "confirm_password": "SecurePassword123!",
  "specialization": "cardiology",
  "license_number": "MD123456789",
  "years_of_experience": 10,
  "clinic_address": {
    "street": "123 Medical Center Dr",
    "city": "New York",
    "state": "NY",
    "zip": "10001"
  }
}
```

**Success Response (201)**:
```json
{
  "success": true,
  "message": "Provider registered successfully. Verification email sent.",
  "data": {
    "provider_id": "uuid-here",
    "email": "john.doe@clinic.com",
    "verification_status": "pending"
  }
}
```

**Error Response (400)**:
```json
{
  "success": false,
  "message": "Registration validation failed",
  "errors": {
    "email": ["A provider with this email already exists."],
    "password": ["Password must contain at least one uppercase letter."]
  }
}
```

#### Email Verification
**POST** `/api/v1/provider/verify-email`

Verify provider email address.

**Request Body**:
```json
{
  "token": "verification-token-here"
}
```

**Success Response (200)**:
```json
{
  "success": true,
  "message": "Email verified successfully",
  "data": {
    "provider_id": "uuid-here",
    "email": "john.doe@clinic.com",
    "verified": true
  }
}
```

#### Resend Verification
**POST** `/api/v1/provider/resend-verification`

Resend verification email.

**Request Body**:
```json
{
  "email": "john.doe@clinic.com"
}
```

#### Get Provider Details
**GET** `/api/v1/provider/{provider_id}`

Get provider information.

#### Get Specializations
**GET** `/api/v1/provider/specializations`

Get list of available medical specializations.

#### Health Check
**GET** `/api/v1/health`

API health check endpoint.

## 🔒 Security Features

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Rate Limiting
- 5 registration attempts per IP address per hour
- Configurable time window and limits
- Redis-based rate limiting

### Input Validation
- Email format validation
- Phone number validation (international format)
- License number validation (alphanumeric)
- Address validation
- Input sanitization

### Security Headers
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

## 📧 Email Configuration

### Development
Emails are printed to console by default.

### Production
Configure SMTP settings in environment variables:
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@healthfirst.com
```

## 🐘 Database Schema

### Provider Model
- `id`: UUID primary key
- `first_name`: CharField (2-50 chars)
- `last_name`: CharField (2-50 chars)
- `email`: EmailField (unique)
- `phone_number`: CharField (unique, international format)
- `password`: CharField (bcrypt hashed)
- `specialization`: CharField (from predefined choices)
- `license_number`: CharField (unique, alphanumeric)
- `years_of_experience`: PositiveIntegerField (0-50)
- `verification_status`: CharField (pending/verified/rejected)
- `email_verified`: BooleanField
- `is_active`: BooleanField
- `created_at`: DateTimeField
- `updated_at`: DateTimeField

### ClinicAddress Model
- `street`: CharField (max 200 chars)
- `city`: CharField (max 100 chars)
- `state`: CharField (max 50 chars)
- `zip_code`: CharField (max 20 chars)

## 🔧 Environment Variables

Key environment variables:

```bash
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# Security
BCRYPT_SALT_ROUNDS=12
RATE_LIMIT_MAX_REQUESTS=5
RATE_LIMIT_WINDOW_MINUTES=60

# Frontend
FRONTEND_URL=http://localhost:3001
```

## 🧪 Testing

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test providers

# With coverage
pytest --cov=providers
```

### Test Categories
- Unit tests for models
- API endpoint tests
- Validation tests
- Email functionality tests
- Rate limiting tests

## 📊 Monitoring

### Logs
Application logs are stored in `/app/logs/django.log` with structured logging.

### Celery Monitoring
Access Flower at http://localhost:5555 to monitor Celery tasks.

### Health Checks
- API health: `/api/v1/health`
- Database health: Built into Docker Compose
- Redis health: Built into Docker Compose

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL/TLS certificates
- [ ] Configure email SMTP settings
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up load balancing (if needed)

### Docker Production
```bash
# Build and run
docker-compose -f docker-compose.yml up --build -d

# View logs
docker-compose logs -f web

# Scale services
docker-compose up --scale celery=3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for healthcare providers** 