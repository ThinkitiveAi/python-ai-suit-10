"""
Password utility functions for provider registration.
"""

import re
import secrets
import bcrypt
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password_strength(password):
    """
    Validate password strength according to requirements:
    - At least 8 characters
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains number
    - Contains special character
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number.")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character.")
    
    if errors:
        raise ValidationError(errors)
    
    return True


def hash_password(password):
    """
    Hash password using bcrypt with configured salt rounds.
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    validate_password_strength(password)
    
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_SALT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """
    Verify a password against its hash.
    """
    if not password or not hashed_password:
        return False
    
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except (ValueError, TypeError):
        return False


def generate_secure_token(length=32):
    """
    Generate a cryptographically secure random token.
    """
    return secrets.token_urlsafe(length)


def generate_verification_token():
    """
    Generate a secure token for email verification.
    """
    return generate_secure_token(64)


class PasswordValidator:
    """
    Custom password validator class for Django forms.
    """
    
    def validate(self, password, user=None):
        """Validate password strength."""
        validate_password_strength(password)
    
    def get_help_text(self):
        """Return help text for password requirements."""
        return (
            "Your password must contain at least 8 characters, including "
            "uppercase and lowercase letters, numbers, and special characters."
        ) 