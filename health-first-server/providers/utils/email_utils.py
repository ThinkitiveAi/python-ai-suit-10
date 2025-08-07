"""
Email utility functions for provider registration.
"""

import logging
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.urls import reverse
from .password_utils import generate_verification_token

logger = logging.getLogger(__name__)


def generate_verification_email_data(provider):
    """
    Generate verification token and expiration for a provider.
    """
    token = generate_verification_token()
    expires = datetime.now() + timedelta(hours=24)
    
    provider.email_verification_token = token
    provider.email_verification_expires = expires
    provider.save(update_fields=['email_verification_token', 'email_verification_expires'])
    
    return token


def build_verification_url(token):
    """
    Build the email verification URL.
    """
    return f"{settings.FRONTEND_URL}/verify-email?token={token}"


def send_verification_email(provider):
    """
    Send email verification email to the provider.
    """
    try:
        # Generate verification token
        token = generate_verification_email_data(provider)
        verification_url = build_verification_url(token)
        
        # Email context
        context = {
            'provider_name': provider.get_full_name(),
            'verification_url': verification_url,
            'site_name': 'HealthFirst',
            'company_name': 'HealthFirst Medical Services',
        }
        
        # Render email templates
        html_message = render_to_string('emails/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        success = send_mail(
            subject='Verify Your HealthFirst Provider Account',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[provider.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        if success:
            logger.info(f"Verification email sent successfully to {provider.email}")
            return True
        else:
            logger.error(f"Failed to send verification email to {provider.email}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending verification email to {provider.email}: {str(e)}")
        return False


def send_welcome_email(provider):
    """
    Send welcome email after successful verification.
    """
    try:
        context = {
            'provider_name': provider.get_full_name(),
            'login_url': f"{settings.FRONTEND_URL}/login",
            'site_name': 'HealthFirst',
            'company_name': 'HealthFirst Medical Services',
        }
        
        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)
        
        success = send_mail(
            subject='Welcome to HealthFirst - Account Verified',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[provider.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        if success:
            logger.info(f"Welcome email sent successfully to {provider.email}")
        else:
            logger.error(f"Failed to send welcome email to {provider.email}")
            
        return success
        
    except Exception as e:
        logger.error(f"Error sending welcome email to {provider.email}: {str(e)}")
        return False


def send_registration_notification_email(provider):
    """
    Send notification email to admin about new provider registration.
    """
    try:
        context = {
            'provider_name': provider.get_full_name(),
            'provider_email': provider.email,
            'provider_specialization': provider.get_specialization_display(),
            'provider_license': provider.license_number,
            'registration_date': provider.created_at,
            'admin_url': f"{settings.FRONTEND_URL}/admin/providers",
        }
        
        html_message = render_to_string('emails/admin_notification.html', context)
        plain_message = strip_tags(html_message)
        
        # Send to configured admin emails
        admin_emails = getattr(settings, 'ADMIN_NOTIFICATION_EMAILS', [])
        if admin_emails:
            success = send_mail(
                subject='New Provider Registration - HealthFirst',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                html_message=html_message,
                fail_silently=False,
            )
            
            if success:
                logger.info(f"Admin notification sent for provider {provider.email}")
            else:
                logger.error(f"Failed to send admin notification for provider {provider.email}")
                
            return success
        
        return True  # No admin emails configured, consider it successful
        
    except Exception as e:
        logger.error(f"Error sending admin notification for provider {provider.email}: {str(e)}")
        return False


def is_verification_token_valid(token, provider):
    """
    Check if the verification token is valid and not expired.
    """
    if not token or not provider.email_verification_token:
        return False
    
    if token != provider.email_verification_token:
        return False
    
    if provider.email_verification_expires and datetime.now() > provider.email_verification_expires:
        return False
    
    return True


def resend_verification_email(provider):
    """
    Resend verification email with a new token.
    """
    if provider.email_verified:
        return False, "Email is already verified"
    
    success = send_verification_email(provider)
    if success:
        return True, "Verification email sent successfully"
    else:
        return False, "Failed to send verification email" 