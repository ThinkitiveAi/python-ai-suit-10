"""
Serializers for provider registration and management.
"""

from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Provider, ClinicAddress
from .utils.validation_utils import (
    validate_registration_data,
    validate_phone_number,
    validate_license_number,
    validate_name,
    validate_specialization,
    validate_years_of_experience
)
from .utils.password_utils import validate_password_strength


class ClinicAddressSerializer(serializers.ModelSerializer):
    """Serializer for clinic address."""
    
    class Meta:
        model = ClinicAddress
        fields = ['street', 'city', 'state', 'zip_code']
        extra_kwargs = {
            'street': {'required': True, 'allow_blank': False, 'max_length': 200},
            'city': {'required': True, 'allow_blank': False, 'max_length': 100},
            'state': {'required': True, 'allow_blank': False, 'max_length': 50},
            'zip_code': {'required': True, 'allow_blank': False, 'max_length': 20},
        }
    
    def validate_street(self, value):
        """Validate street address."""
        if not value or not value.strip():
            raise serializers.ValidationError("Street address is required.")
        return value.strip()
    
    def validate_city(self, value):
        """Validate city name."""
        if not value or not value.strip():
            raise serializers.ValidationError("City is required.")
        return value.strip().title()
    
    def validate_state(self, value):
        """Validate state name."""
        if not value or not value.strip():
            raise serializers.ValidationError("State is required.")
        return value.strip().title()
    
    def validate_zip_code(self, value):
        """Validate ZIP/postal code."""
        if not value or not value.strip():
            raise serializers.ValidationError("ZIP/postal code is required.")
        return value.strip()


class ProviderRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for provider registration."""
    
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text="Password must contain at least 8 characters with uppercase, lowercase, numbers, and special characters."
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Confirm your password."
    )
    clinic_address = ClinicAddressSerializer()
    
    class Meta:
        model = Provider
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'password', 'confirm_password', 'specialization',
            'license_number', 'years_of_experience', 'clinic_address'
        ]
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False, 'min_length': 2, 'max_length': 50},
            'last_name': {'required': True, 'allow_blank': False, 'min_length': 2, 'max_length': 50},
            'email': {'required': True, 'allow_blank': False},
            'phone_number': {'required': True, 'allow_blank': False},
            'specialization': {'required': True, 'allow_blank': False},
            'license_number': {'required': True, 'allow_blank': False},
            'years_of_experience': {'required': True, 'min_value': 0, 'max_value': 50},
        }
    
    def validate_first_name(self, value):
        """Validate first name."""
        return validate_name(value, "First name")
    
    def validate_last_name(self, value):
        """Validate last name."""
        return validate_name(value, "Last name")
    
    def validate_email(self, value):
        """Validate email address."""
        if not value or not value.strip():
            raise serializers.ValidationError("Email address is required.")
        
        email = value.strip().lower()
        
        # Check if email already exists
        if Provider.objects.filter(email=email).exists():
            raise serializers.ValidationError("A provider with this email address already exists.")
        
        return email
    
    def validate_phone_number(self, value):
        """Validate phone number."""
        if not value or not value.strip():
            raise serializers.ValidationError("Phone number is required.")
        
        try:
            formatted_phone = validate_phone_number(value)
        except ValidationError as e:
            # Handle both string and list error messages
            error_message = str(e) if isinstance(e, str) else str(e.args[0]) if e.args else "Invalid phone number format."
            raise serializers.ValidationError(error_message)
        except Exception as e:
            raise serializers.ValidationError("Invalid phone number format.")
        
        # Check if phone number already exists
        if Provider.objects.filter(phone_number=formatted_phone).exists():
            raise serializers.ValidationError("A provider with this phone number already exists.")
        
        return formatted_phone
    
    def validate_license_number(self, value):
        """Validate license number."""
        if not value or not value.strip():
            raise serializers.ValidationError("License number is required.")
        
        try:
            formatted_license = validate_license_number(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        
        # Check if license number already exists
        if Provider.objects.filter(license_number=formatted_license).exists():
            raise serializers.ValidationError("A provider with this license number already exists.")
        
        return formatted_license
    
    def validate_specialization(self, value):
        """Validate specialization."""
        if not value or not value.strip():
            raise serializers.ValidationError("Specialization is required.")
        
        try:
            return validate_specialization(value, Provider.SPECIALIZATION_CHOICES)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate_years_of_experience(self, value):
        """Validate years of experience."""
        try:
            return validate_years_of_experience(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
    
    def validate_password(self, value):
        """Validate password strength."""
        try:
            validate_password_strength(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate(self, attrs):
        """Validate the entire registration data."""
        # Check password confirmation
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': ['Password and confirm password do not match.']
            })
        
        # Remove confirm_password from validated data
        attrs.pop('confirm_password', None)
        
        return attrs
    
    @transaction.atomic
    def create(self, validated_data):
        """Create a new provider with associated clinic address."""
        # Extract clinic address data
        clinic_address_data = validated_data.pop('clinic_address')
        
        # Extract password
        password = validated_data.pop('password')
        
        # Create clinic address
        clinic_address = ClinicAddress.objects.create(**clinic_address_data)
        
        # Create provider
        provider = Provider.objects.create(
            clinic_address=clinic_address,
            **validated_data
        )
        
        # Set password (this will hash it)
        provider.set_password(password)
        provider.save(update_fields=['password'])
        
        return provider


class ProviderResponseSerializer(serializers.ModelSerializer):
    """Serializer for provider response data."""
    
    clinic_address = ClinicAddressSerializer(read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)
    verification_status_display = serializers.CharField(source='get_verification_status_display', read_only=True)
    
    class Meta:
        model = Provider
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'specialization', 'specialization_display', 'license_number',
            'years_of_experience', 'clinic_address', 'verification_status',
            'verification_status_display', 'email_verified', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'verification_status', 'email_verified', 'is_active',
            'created_at', 'updated_at'
        ]


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification."""
    
    token = serializers.CharField(
        required=True,
        help_text="Email verification token"
    )
    
    def validate_token(self, value):
        """Validate the verification token."""
        if not value or not value.strip():
            raise serializers.ValidationError("Verification token is required.")
        return value.strip()


class ResendVerificationSerializer(serializers.Serializer):
    """Serializer for resending verification email."""
    
    email = serializers.EmailField(
        required=True,
        help_text="Email address to resend verification to"
    )
    
    def validate_email(self, value):
        """Validate email and check if provider exists."""
        if not value or not value.strip():
            raise serializers.ValidationError("Email address is required.")
        
        email = value.strip().lower()
        
        try:
            provider = Provider.objects.get(email=email)
            if provider.email_verified:
                raise serializers.ValidationError("Email is already verified.")
        except Provider.DoesNotExist:
            raise serializers.ValidationError("No provider found with this email address.")
        
        return email 