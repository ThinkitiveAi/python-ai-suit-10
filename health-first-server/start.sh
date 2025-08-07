#!/bin/bash

# HealthFirst Provider Registration Backend Startup Script

echo "🏥 HealthFirst Provider Registration Backend"
echo "============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to wait for service
wait_for_service() {
    local host=$1
    local port=$2
    local service=$3
    
    echo "⏳ Waiting for $service to be ready..."
    timeout=60
    count=0
    while ! nc -z $host $port && [ $count -lt $timeout ]; do
        sleep 1
        ((count++))
    done
    
    if [ $count -eq $timeout ]; then
        echo "❌ Timeout waiting for $service"
        return 1
    fi
    
    echo "✅ $service is ready!"
    return 0
}

# Check for Docker and Docker Compose
if command_exists docker && command_exists docker-compose; then
    echo "🐳 Using Docker setup..."
    
    # Create necessary directories
    mkdir -p logs media staticfiles
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "📋 Created .env file from .env.example"
        echo "⚠️  Please edit .env file with your configuration before continuing"
        read -p "Press Enter to continue after editing .env file..."
    fi
    
    # Clean up any existing containers
    echo "🧹 Cleaning up existing containers..."
    docker-compose down -v
    
    # Start services
    echo "🚀 Starting all services with Docker Compose..."
    docker-compose up --build -d
    
    # Wait for services with updated ports
    echo "⏳ Waiting for services to start..."
    sleep 10
    
    if wait_for_service localhost 5433 "PostgreSQL"; then
        echo "✅ PostgreSQL is ready"
    else
        echo "❌ PostgreSQL failed to start"
        docker-compose logs db
        exit 1
    fi
    
    if wait_for_service localhost 6380 "Redis"; then
        echo "✅ Redis is ready"
    else
        echo "❌ Redis failed to start"
        docker-compose logs redis
        exit 1
    fi
    
    # Wait a bit more for Django to start
    echo "⏳ Waiting for Django application to start..."
    sleep 15
    
    if wait_for_service localhost 8000 "Django App"; then
        echo "✅ Django application is ready"
    else
        echo "❌ Django application failed to start"
        docker-compose logs web
        exit 1
    fi
    
    # Create superuser if it doesn't exist
    echo "👤 Setting up admin user..."
    docker-compose exec -T web python manage.py shell << 'EOF'
from providers.models import Provider, ClinicAddress

# Create superuser if it doesn't exist
if not Provider.objects.filter(is_superuser=True).exists():
    print('Creating superuser...')
    try:
        clinic = ClinicAddress.objects.create(
            street='123 Admin St',
            city='Admin City',
            state='Admin State',
            zip_code='12345'
        )
        user = Provider.objects.create(
            first_name='Admin',
            last_name='User',
            email='admin@healthfirst.com',
            phone_number='+1234567890',
            specialization='family_medicine',
            license_number='ADMIN123',
            years_of_experience=10,
            clinic_address=clinic,
            is_staff=True,
            is_superuser=True,
            email_verified=True,
            verification_status='verified'
        )
        user.set_password('admin123')
        user.save()
        print('✅ Superuser created successfully!')
        print('Email: admin@healthfirst.com')
        print('Password: admin123')
    except Exception as e:
        print(f'Error creating superuser: {e}')
else:
    print('ℹ️ Superuser already exists')
EOF
    
    echo ""
    echo "🎉 HealthFirst Backend is now running!"
    echo ""
    echo "🌐 Services:"
    echo "   • API: http://localhost:8000/api/v1/"
    echo "   • Admin: http://localhost:8000/admin/"
    echo "   • Health Check: http://localhost:8000/api/v1/health"
    echo "   • Celery Monitor: http://localhost:5556"
    echo "   • PostgreSQL: localhost:5433"
    echo "   • Redis: localhost:6380"
    echo ""
    echo "👤 Admin Login:"
    echo "   • Email: admin@healthfirst.com"
    echo "   • Password: admin123"
    echo ""
    echo "📚 API Documentation:"
    echo "   • Registration: POST /api/v1/provider/register"
    echo "   • Verification: POST /api/v1/provider/verify-email"
    echo "   • Specializations: GET /api/v1/provider/specializations"
    echo ""
    echo "🧪 Test the API:"
    echo "   curl http://localhost:8000/api/v1/health"
    echo ""
    echo "🐳 Docker Commands:"
    echo "   • View logs: docker-compose logs -f"
    echo "   • Stop services: docker-compose down"
    echo "   • Restart: docker-compose restart"
    echo ""
    
elif command_exists python3; then
    echo "🐍 Using local Python setup..."
    
    # Check for virtual environment
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "📋 Created .env file from .env.example"
        echo "⚠️  Please configure your database and Redis URLs in .env"
    fi
    
    # Create directories
    mkdir -p logs media staticfiles
    
    # Run migrations
    echo "📊 Running database migrations..."
    python manage.py migrate
    
    # Collect static files
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
    
    # Create superuser
    echo "👤 Create a superuser account:"
    python manage.py createsuperuser
    
    echo ""
    echo "🚀 Starting development server..."
    echo "   Press Ctrl+C to stop"
    echo ""
    echo "🌐 Access the application at:"
    echo "   • API: http://localhost:8000/api/v1/"
    echo "   • Admin: http://localhost:8000/admin/"
    echo ""
    echo "⚠️  Don't forget to start Celery worker and Redis separately:"
    echo "   • Redis: redis-server"
    echo "   • Celery: celery -A healthfirst worker --loglevel=info"
    echo ""
    
    python manage.py runserver
    
else
    echo "❌ Neither Docker nor Python 3 found!"
    echo "Please install either:"
    echo "   • Docker and Docker Compose (recommended)"
    echo "   • Python 3.11+ with pip"
    exit 1
fi 