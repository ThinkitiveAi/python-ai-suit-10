"""
Custom exception handler for Django REST Framework.
"""

import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides detailed error responses.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Log the exception
    request = context.get('request')
    if request:
        logger.error(
            f"Exception in {request.method} {request.path}: {str(exc)}",
            extra={'request': request}
        )
    
    # Handle Django ValidationError
    if isinstance(exc, ValidationError) and response is None:
        if hasattr(exc, 'error_dict'):
            # Field-specific errors
            error_data = {
                'success': False,
                'message': 'Validation failed',
                'errors': exc.error_dict
            }
        elif hasattr(exc, 'error_list'):
            # Non-field errors
            error_data = {
                'success': False,
                'message': 'Validation failed',
                'errors': {'non_field_errors': [str(error) for error in exc.error_list]}
            }
        else:
            # Single error message
            error_data = {
                'success': False,
                'message': str(exc),
                'errors': {'non_field_errors': [str(exc)]}
            }
        
        response = Response(error_data, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle database integrity errors (duplicates, etc.)
    elif isinstance(exc, IntegrityError) and response is None:
        error_message = str(exc).lower()
        
        if 'unique constraint' in error_message or 'duplicate key' in error_message:
            if 'email' in error_message:
                error_data = {
                    'success': False,
                    'message': 'Email address already exists',
                    'errors': {'email': ['A provider with this email already exists.']}
                }
            elif 'phone' in error_message:
                error_data = {
                    'success': False,
                    'message': 'Phone number already exists',
                    'errors': {'phone_number': ['A provider with this phone number already exists.']}
                }
            elif 'license' in error_message:
                error_data = {
                    'success': False,
                    'message': 'License number already exists',
                    'errors': {'license_number': ['A provider with this license number already exists.']}
                }
            else:
                error_data = {
                    'success': False,
                    'message': 'Duplicate entry detected',
                    'errors': {'non_field_errors': ['This information already exists in our system.']}
                }
        else:
            error_data = {
                'success': False,
                'message': 'Database error occurred',
                'errors': {'non_field_errors': ['An error occurred while saving your information.']}
            }
        
        response = Response(error_data, status=status.HTTP_409_CONFLICT)
    
    # Customize response format for existing responses
    if response is not None:
        custom_response_data = {
            'success': False,
            'message': 'Request failed',
            'errors': {}
        }
        
        if hasattr(response, 'data'):
            if isinstance(response.data, dict):
                # Handle DRF serializer errors
                if 'detail' in response.data:
                    custom_response_data['message'] = response.data['detail']
                    custom_response_data['errors'] = {'non_field_errors': [response.data['detail']]}
                else:
                    custom_response_data['errors'] = response.data
                    
                    # Extract a meaningful message from errors
                    if response.data:
                        first_error_key = list(response.data.keys())[0]
                        first_error_value = response.data[first_error_key]
                        if isinstance(first_error_value, list) and first_error_value:
                            custom_response_data['message'] = f"{first_error_key}: {first_error_value[0]}"
                        else:
                            custom_response_data['message'] = str(first_error_value)
            elif isinstance(response.data, list):
                custom_response_data['errors'] = {'non_field_errors': response.data}
                custom_response_data['message'] = response.data[0] if response.data else 'Request failed'
            else:
                custom_response_data['message'] = str(response.data)
                custom_response_data['errors'] = {'non_field_errors': [str(response.data)]}
        
        response.data = custom_response_data
    
    return response 