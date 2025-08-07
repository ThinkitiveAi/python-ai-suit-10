"""
Django signals for provider app.
"""

import logging
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Provider

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Provider)
def provider_post_save(sender, instance, created, **kwargs):
    """Handle provider post-save signal."""
    if created:
        logger.info(f"New provider created: {instance.email} (ID: {instance.id})")
    else:
        logger.info(f"Provider updated: {instance.email} (ID: {instance.id})")


@receiver(pre_save, sender=Provider)
def provider_pre_save(sender, instance, **kwargs):
    """Handle provider pre-save signal."""
    if instance.pk:
        try:
            old_instance = Provider.objects.get(pk=instance.pk)
            
            # Log verification status changes
            if old_instance.verification_status != instance.verification_status:
                logger.info(
                    f"Provider {instance.email} verification status changed: "
                    f"{old_instance.verification_status} -> {instance.verification_status}"
                )
            
            # Log email verification changes
            if old_instance.email_verified != instance.email_verified:
                logger.info(
                    f"Provider {instance.email} email verification changed: "
                    f"{old_instance.email_verified} -> {instance.email_verified}"
                )
                
        except Provider.DoesNotExist:
            pass 