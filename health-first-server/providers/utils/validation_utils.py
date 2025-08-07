"""
Validation utility functions for provider registration.
"""

import re
import html
import phonenumbers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.text import slugify


def sanitize_input(value):
    """
    Sanitize input to prevent injection attacks.
    """
    if not isinstance(value, str):
        return value
    
    # Strip whitespace
    value = value.strip()
    
    # HTML escape
    value = html.escape(value)
    
    # Remove potential SQL injection characters
    dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
    for char in dangerous_chars:
        value = value.replace(char, '')
    
    return value


def validate_phone_number(phone_number):
    """
    Validate and format phone number to international format.
    
    Args:
        phone_number (str): Phone number to validate
    
    Returns:
        str: Formatted phone number in E164 format
    
    Raises:
        ValidationError: If phone number is invalid
    """
    if not phone_number:
        raise ValidationError("Phone number is required.")
    
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, None)
        
        # Check if the number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError("Invalid phone number format.")
        
        # Format to international format
        formatted_number = phonenumbers.format_number(
            parsed_number, 
            phonenumbers.PhoneNumberFormat.E164
        )
        
        return formatted_number
        
    except phonenumbers.phonenumberutil.NumberParseException as e:
        raise ValidationError("Invalid phone number format. Please use international format (e.g., +1234567890).")
    except Exception as e:
        raise ValidationError("Invalid phone number format.")


def validate_license_number(license_number):
    """
    Validate license number format (alphanumeric).
    """
    if not license_number:
        raise ValidationError("License number is required.")
    
    # Remove whitespace and convert to uppercase
    license_number = license_number.strip().upper()
    
    # Check if alphanumeric
    if not re.match(r'^[A-Z0-9]+$', license_number):
        raise ValidationError("License number must contain only letters and numbers.")
    
    # Check length (minimum 5, maximum 20)
    if len(license_number) < 5 or len(license_number) > 20:
        raise ValidationError("License number must be between 5 and 20 characters.")
    
    return license_number


def validate_zip_code(zip_code, country='US'):
    """
    Validate postal/ZIP code format.
    """
    if not zip_code:
        raise ValidationError("ZIP/Postal code is required.")
    
    zip_code = zip_code.strip()
    
    if country == 'US':
        # US ZIP code format: 12345 or 12345-6789
        if not re.match(r'^\d{5}(-\d{4})?$', zip_code):
            raise ValidationError("Invalid US ZIP code format. Use 12345 or 12345-6789.")
    else:
        # Generic postal code validation (3-10 alphanumeric characters)
        if not re.match(r'^[A-Z0-9\s-]{3,10}$', zip_code.upper()):
            raise ValidationError("Invalid postal code format.")
    
    return zip_code


def validate_name(name, field_name="Name"):
    """
    Validate name fields (first name, last name).
    """
    if not name:
        raise ValidationError(f"{field_name} is required.")
    
    name = name.strip()
    
    # Check length
    if len(name) < 2 or len(name) > 50:
        raise ValidationError(f"{field_name} must be between 2 and 50 characters.")
    
    # Check for valid characters (letters, spaces, hyphens, apostrophes)
    if not re.match(r"^[a-zA-Z\s'-]+$", name):
        raise ValidationError(f"{field_name} can only contain letters, spaces, hyphens, and apostrophes.")
    
    # Capitalize properly
    name = ' '.join([part.capitalize() for part in name.split()])
    
    return name


def validate_specialization(specialization, valid_choices):
    """
    Validate medical specialization.
    """
    if not specialization:
        raise ValidationError("Specialization is required.")
    
    specialization = specialization.strip().lower()
    
    # Check if it's in the valid choices
    valid_values = [choice[0] for choice in valid_choices]
    if specialization not in valid_values:
        raise ValidationError("Invalid specialization selected.")
    
    return specialization


def validate_years_of_experience(years):
    """
    Validate years of experience.
    """
    try:
        years = int(years)
    except (ValueError, TypeError):
        raise ValidationError("Years of experience must be a number.")
    
    if years < 0 or years > 50:
        raise ValidationError("Years of experience must be between 0 and 50.")
    
    return years


def validate_email_format(email):
    """
    Validate email format and normalize.
    """
    if not email:
        raise ValidationError("Email is required.")
    
    email = email.strip().lower()
    
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError("Invalid email format.")
    
    return email


def validate_clinic_address(address_data):
    """
    Validate clinic address data.
    """
    errors = {}
    
    # Validate street
    street = address_data.get('street', '').strip()
    if not street:
        errors['street'] = "Street address is required."
    elif len(street) > 200:
        errors['street'] = "Street address must be 200 characters or less."
    
    # Validate city
    city = address_data.get('city', '').strip()
    if not city:
        errors['city'] = "City is required."
    elif len(city) > 100:
        errors['city'] = "City must be 100 characters or less."
    elif not re.match(r"^[a-zA-Z\s'-]+$", city):
        errors['city'] = "City can only contain letters, spaces, hyphens, and apostrophes."
    
    # Validate state
    state = address_data.get('state', '').strip()
    if not state:
        errors['state'] = "State is required."
    elif len(state) > 50:
        errors['state'] = "State must be 50 characters or less."
    elif not re.match(r"^[a-zA-Z\s'-]+$", state):
        errors['state'] = "State can only contain letters, spaces, hyphens, and apostrophes."
    
    # Validate ZIP code
    zip_code = address_data.get('zip', '').strip()
    if not zip_code:
        errors['zip'] = "ZIP/Postal code is required."
    else:
        try:
            validate_zip_code(zip_code)
        except ValidationError as e:
            errors['zip'] = str(e)
    
    if errors:
        raise ValidationError(errors)
    
    return {
        'street': street,
        'city': city.title(),
        'state': state.title(),
        'zip': zip_code,
    }


def normalize_data(data):
    """
    Normalize and sanitize all input data.
    """
    normalized = {}
    
    for key, value in data.items():
        if isinstance(value, str):
            normalized[key] = sanitize_input(value)
        elif isinstance(value, dict):
            normalized[key] = normalize_data(value)
        else:
            normalized[key] = value
    
    return normalized


def validate_registration_data(data):
    """
    Comprehensive validation for provider registration data.
    """
    errors = {}
    
    try:
        # Normalize data first
        data = normalize_data(data)
        
        # Validate first name
        if 'first_name' in data:
            try:
                data['first_name'] = validate_name(data['first_name'], "First name")
            except ValidationError as e:
                errors['first_name'] = str(e)
        
        # Validate last name
        if 'last_name' in data:
            try:
                data['last_name'] = validate_name(data['last_name'], "Last name")
            except ValidationError as e:
                errors['last_name'] = str(e)
        
        # Validate email
        if 'email' in data:
            try:
                data['email'] = validate_email_format(data['email'])
            except ValidationError as e:
                errors['email'] = str(e)
        
        # Validate phone number
        if 'phone_number' in data:
            try:
                data['phone_number'] = validate_phone_number(data['phone_number'])
            except ValidationError as e:
                errors['phone_number'] = str(e)
        
        # Validate license number
        if 'license_number' in data:
            try:
                data['license_number'] = validate_license_number(data['license_number'])
            except ValidationError as e:
                errors['license_number'] = str(e)
        
        # Validate years of experience
        if 'years_of_experience' in data:
            try:
                data['years_of_experience'] = validate_years_of_experience(data['years_of_experience'])
            except ValidationError as e:
                errors['years_of_experience'] = str(e)
        
        # Validate clinic address
        if 'clinic_address' in data:
            try:
                data['clinic_address'] = validate_clinic_address(data['clinic_address'])
            except ValidationError as e:
                if hasattr(e, 'error_dict'):
                    for field, field_errors in e.error_dict.items():
                        errors[f'clinic_address.{field}'] = field_errors[0] if field_errors else str(field_errors)
                else:
                    errors['clinic_address'] = str(e)
        
        if errors:
            raise ValidationError(errors)
        
        return data
        
    except Exception as e:
        if not isinstance(e, ValidationError):
            errors['general'] = "An error occurred during validation."
            raise ValidationError(errors)
        raise 