"""
Celery tasks for provider registration and email handling.
"""

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Provider, ProviderRegistrationLog
from .utils.email_utils import (
    send_verification_email,
    send_welcome_email,
    send_registration_notification_email
)

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_verification_email_task(self, provider_id):
    """
    Send verification email to provider asynchronously.
    """
    try:
        provider = Provider.objects.get(id=provider_id)
        success = send_verification_email(provider)
        
        if not success:
            logger.error(f"Failed to send verification email to provider {provider.email}")
            # Retry the task
            self.retry(countdown=60, max_retries=3)
        
        logger.info(f"Verification email sent successfully to {provider.email}")
        return {"success": True, "message": "Verification email sent"}
        
    except Provider.DoesNotExist:
        logger.error(f"Provider with ID {provider_id} not found")
        return {"success": False, "message": "Provider not found"}
    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")
        self.retry(countdown=60, max_retries=3)


@shared_task(bind=True, max_retries=3)
def send_welcome_email_task(self, provider_id):
    """
    Send welcome email to provider after verification.
    """
    try:
        provider = Provider.objects.get(id=provider_id)
        success = send_welcome_email(provider)
        
        if not success:
            logger.error(f"Failed to send welcome email to provider {provider.email}")
            self.retry(countdown=60, max_retries=3)
        
        logger.info(f"Welcome email sent successfully to {provider.email}")
        return {"success": True, "message": "Welcome email sent"}
        
    except Provider.DoesNotExist:
        logger.error(f"Provider with ID {provider_id} not found")
        return {"success": False, "message": "Provider not found"}
    except Exception as e:
        logger.error(f"Error sending welcome email: {str(e)}")
        self.retry(countdown=60, max_retries=3)


@shared_task(bind=True, max_retries=3)
def send_admin_notification_task(self, provider_id):
    """
    Send notification email to admin about new provider registration.
    """
    try:
        provider = Provider.objects.get(id=provider_id)
        success = send_registration_notification_email(provider)
        
        if not success:
            logger.error(f"Failed to send admin notification for provider {provider.email}")
            self.retry(countdown=60, max_retries=3)
        
        logger.info(f"Admin notification sent for provider {provider.email}")
        return {"success": True, "message": "Admin notification sent"}
        
    except Provider.DoesNotExist:
        logger.error(f"Provider with ID {provider_id} not found")
        return {"success": False, "message": "Provider not found"}
    except Exception as e:
        logger.error(f"Error sending admin notification: {str(e)}")
        self.retry(countdown=60, max_retries=3)


@shared_task
def log_registration_attempt(ip_address, email, success, error_message=None, user_agent=None):
    """
    Log provider registration attempt for audit purposes.
    """
    try:
        ProviderRegistrationLog.objects.create(
            ip_address=ip_address,
            email=email,
            success=success,
            error_message=error_message,
            user_agent=user_agent
        )
        logger.info(f"Registration attempt logged for {email} from {ip_address}")
        return {"success": True, "message": "Registration attempt logged"}
        
    except Exception as e:
        logger.error(f"Error logging registration attempt: {str(e)}")
        return {"success": False, "message": "Failed to log registration attempt"}


@shared_task
def cleanup_expired_verification_tokens():
    """
    Clean up expired email verification tokens.
    """
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        # Delete tokens expired more than 48 hours ago
        cutoff_date = timezone.now() - timedelta(hours=48)
        
        expired_providers = Provider.objects.filter(
            email_verification_expires__lt=cutoff_date,
            email_verified=False
        )
        
        count = 0
        for provider in expired_providers:
            provider.email_verification_token = None
            provider.email_verification_expires = None
            provider.save(update_fields=['email_verification_token', 'email_verification_expires'])
            count += 1
        
        logger.info(f"Cleaned up {count} expired verification tokens")
        return {"success": True, "message": f"Cleaned up {count} expired tokens"}
        
    except Exception as e:
        logger.error(f"Error cleaning up expired tokens: {str(e)}")
        return {"success": False, "message": "Failed to cleanup expired tokens"}


@shared_task
def send_bulk_notification_email(subject, message, recipient_emails, html_message=None):
    """
    Send bulk notification emails.
    """
    try:
        success_count = 0
        failed_count = 0
        
        for email in recipient_emails:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send email to {email}: {str(e)}")
                failed_count += 1
        
        logger.info(f"Bulk email sent: {success_count} successful, {failed_count} failed")
        return {
            "success": True,
            "message": f"Sent {success_count} emails, {failed_count} failed"
        }
        
    except Exception as e:
        logger.error(f"Error sending bulk emails: {str(e)}")
        return {"success": False, "message": "Failed to send bulk emails"} 