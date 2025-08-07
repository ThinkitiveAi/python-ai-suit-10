"""
URL configuration for providers app.
"""

from django.urls import path
from .views import (
    ProviderRegistrationView,
    EmailVerificationView,
    ResendVerificationView,
    ProviderDetailView,
    provider_specializations,
    health_check
)

app_name = 'providers'

urlpatterns = [
    # Provider registration
    path('provider/register', ProviderRegistrationView.as_view(), name='provider-register'),
    path('provider/register/', ProviderRegistrationView.as_view(), name='provider-register-slash'),
    
    # Email verification
    path('provider/verify-email', EmailVerificationView.as_view(), name='email-verification'),
    path('provider/verify-email/', EmailVerificationView.as_view(), name='email-verification-slash'),
    
    # Resend verification email
    path('provider/resend-verification', ResendVerificationView.as_view(), name='resend-verification'),
    path('provider/resend-verification/', ResendVerificationView.as_view(), name='resend-verification-slash'),
    
    # Provider details
    path('provider/<uuid:provider_id>', ProviderDetailView.as_view(), name='provider-detail'),
    path('provider/<uuid:provider_id>/', ProviderDetailView.as_view(), name='provider-detail-slash'),
    
    # Utility endpoints
    path('provider/specializations', provider_specializations, name='provider-specializations'),
    path('provider/specializations/', provider_specializations, name='provider-specializations-slash'),
    
    # Health check
    path('health', health_check, name='health-check'),
    path('health/', health_check, name='health-check-slash'),
] 