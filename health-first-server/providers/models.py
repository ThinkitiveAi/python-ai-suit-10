"""
Provider models for the healthfirst application.
"""

import uuid
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import bcrypt
from django.conf import settings


class ProviderManager(BaseUserManager):
    """Custom manager for Provider model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular provider."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        provider = self.model(email=email, **extra_fields)
        if password:
            provider.set_password(password)
        provider.save(using=self._db)
        return provider

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser provider."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class ClinicAddress(models.Model):
    """Model for clinic address information."""
    
    street = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(1)],
        help_text="Street address"
    )
    city = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1)],
        help_text="City name"
    )
    state = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(1)],
        help_text="State or province"
    )
    zip_code = models.CharField(
        max_length=20,
        validators=[MinLengthValidator(3)],
        help_text="Postal/ZIP code"
    )
    
    class Meta:
        verbose_name = "Clinic Address"
        verbose_name_plural = "Clinic Addresses"
    
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"


class Provider(AbstractBaseUser):
    """Provider model with comprehensive validation and security."""
    
    VERIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('endocrinology', 'Endocrinology'),
        ('gastroenterology', 'Gastroenterology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
        ('urology', 'Urology'),
        ('family_medicine', 'Family Medicine'),
        ('internal_medicine', 'Internal Medicine'),
        ('emergency_medicine', 'Emergency Medicine'),
        ('anesthesiology', 'Anesthesiology'),
        ('pathology', 'Pathology'),
        ('obstetrics_gynecology', 'Obstetrics & Gynecology'),
        ('ophthalmology', 'Ophthalmology'),
        ('otolaryngology', 'Otolaryngology'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    first_name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2), MaxLengthValidator(50)],
        help_text="First name (2-50 characters)"
    )
    
    last_name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2), MaxLengthValidator(50)],
        help_text="Last name (2-50 characters)"
    )
    
    email = models.EmailField(
        unique=True,
        help_text="Unique email address"
    )
    
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique phone number in international format"
    )
    
    password = models.CharField(
        max_length=128,
        help_text="Hashed password"
    )
    
    specialization = models.CharField(
        max_length=100,
        choices=SPECIALIZATION_CHOICES,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
        help_text="Medical specialization (3-100 characters)"
    )
    
    license_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique alphanumeric license number"
    )
    
    years_of_experience = models.PositiveIntegerField(
        help_text="Years of medical experience (0-50)"
    )
    
    clinic_address = models.OneToOneField(
        ClinicAddress,
        on_delete=models.CASCADE,
        related_name='provider',
        help_text="Clinic address information"
    )
    
    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default='pending',
        help_text="Account verification status"
    )
    
    license_document_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to uploaded license document"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Account active status"
    )
    
    email_verified = models.BooleanField(
        default=False,
        help_text="Email verification status"
    )
    
    email_verification_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Email verification token"
    )
    
    email_verification_expires = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Email verification token expiration"
    )
    
    # Django admin fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = ProviderManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    
    class Meta:
        verbose_name = "Provider"
        verbose_name_plural = "Providers"
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['license_number']),
            models.Index(fields=['verification_status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.email})"
    
    def set_password(self, raw_password):
        """Hash and set the password using bcrypt."""
        if raw_password:
            salt = bcrypt.gensalt(rounds=settings.BCRYPT_SALT_ROUNDS)
            hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
            self.password = hashed.decode('utf-8')
    
    def check_password(self, raw_password):
        """Check if the provided password matches the stored hash."""
        if not raw_password or not self.password:
            return False
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password.encode('utf-8')
        )
    
    def get_full_name(self):
        """Return the provider's full name."""
        return f"{self.first_name} {self.last_name}"
    
    def get_short_name(self):
        """Return the provider's first name."""
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        """Return True if the user has the specified permission."""
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        """Return True if the user has permissions to view the app."""
        return self.is_superuser


class ProviderRegistrationLog(models.Model):
    """Log model for tracking provider registration attempts."""
    
    ip_address = models.GenericIPAddressField(
        help_text="IP address of registration attempt"
    )
    email = models.EmailField(
        help_text="Email used in registration attempt"
    )
    success = models.BooleanField(
        default=False,
        help_text="Whether registration was successful"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Error message if registration failed"
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="User agent string"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Provider Registration Log"
        verbose_name_plural = "Provider Registration Logs"
        indexes = [
            models.Index(fields=['ip_address', 'created_at']),
            models.Index(fields=['email', 'created_at']),
        ]
    
    def __str__(self):
        return f"Registration attempt for {self.email} from {self.ip_address}" 