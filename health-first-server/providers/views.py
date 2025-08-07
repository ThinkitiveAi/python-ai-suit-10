"""
Views for provider registration and management.
"""

import logging
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Provider, ProviderRegistrationLog
from .serializers import (
    ProviderRegistrationSerializer,
    ProviderResponseSerializer,
    EmailVerificationSerializer,
    ResendVerificationSerializer
)
from .utils.email_utils import (
    send_verification_email,
    send_welcome_email,
    send_registration_notification_email,
    is_verification_token_valid
)

logger = logging.getLogger(__name__)


class ProviderRegistrationView(APIView):
    """
    Provider registration endpoint.
    
    Register a new healthcare provider with comprehensive validation,
    secure password hashing, and automatic email verification.
    """
    
    @swagger_auto_schema(
        operation_description="Register a new healthcare provider",
        operation_summary="Provider Registration",
        request_body=ProviderRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Provider registered successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Provider registered successfully. Verification email sent.",
                        "data": {
                            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "john.doe@clinic.com",
                            "verification_status": "pending"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Validation errors",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Registration validation failed",
                        "errors": {
                            "email": ["This email is already registered"],
                            "password": ["Password too weak"]
                        }
                    }
                }
            ),
            409: openapi.Response(description="Duplicate email/phone/license"),
            500: openapi.Response(description="Internal server error")
        },
        tags=['Provider Registration']
    )
    def post(self, request):
        """Register a new provider."""
        try:
            # Get client information for logging
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Validate and serialize the data
            serializer = ProviderRegistrationSerializer(data=request.data)
            
            if not serializer.is_valid():
                # Log failed attempt
                email = request.data.get('email', 'unknown')
                ProviderRegistrationLog.objects.create(
                    ip_address=ip_address,
                    email=email,
                    success=False,
                    error_message=str(serializer.errors),
                    user_agent=user_agent
                )
                
                logger.warning(f"Registration validation failed for {email} from {ip_address}")
                
                return Response({
                    'success': False,
                    'message': 'Registration validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create the provider
            with transaction.atomic():
                provider = serializer.save()
                
                # Log successful registration
                ProviderRegistrationLog.objects.create(
                    ip_address=ip_address,
                    email=provider.email,
                    success=True,
                    user_agent=user_agent
                )
                
                # Send verification email directly
                try:
                    send_verification_email(provider)
                except Exception as e:
                    logger.error(f"Failed to send verification email to {provider.email}: {str(e)}")
                
                # Send admin notification directly
                try:
                    send_registration_notification_email(provider)
                except Exception as e:
                    logger.error(f"Failed to send admin notification for {provider.email}: {str(e)}")
                
                logger.info(f"Provider registered successfully: {provider.email} from {ip_address}")
                
                # Return success response
                response_data = {
                    'success': True,
                    'message': 'Provider registered successfully. Verification email sent.',
                    'data': {
                        'provider_id': str(provider.id),
                        'email': provider.email,
                        'verification_status': provider.verification_status
                    }
                }
                
                return Response(response_data, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            # Log error
            email = request.data.get('email', 'unknown')
            ProviderRegistrationLog.objects.create(
                ip_address=ip_address,
                email=email,
                success=False,
                error_message=str(e),
                user_agent=user_agent
            )
            
            logger.error(f"Registration error for {email} from {ip_address}: {str(e)}")
            
            return Response({
                'success': False,
                'message': 'An error occurred during registration',
                'errors': {'general': ['Please try again later']}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class EmailVerificationView(APIView):
    """
    Email verification endpoint.
    
    Verify provider email address using the token sent via email.
    """
    
    @swagger_auto_schema(
        operation_description="Verify provider email address using verification token",
        operation_summary="Email Verification",
        request_body=EmailVerificationSerializer,
        responses={
            200: openapi.Response(
                description="Email verified successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Email verified successfully",
                        "data": {
                            "provider_id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "john.doe@clinic.com",
                            "verified": True
                        }
                    }
                }
            ),
            400: openapi.Response(description="Invalid or expired token"),
            500: openapi.Response(description="Internal server error")
        },
        tags=['Email Verification']
    )
    def post(self, request):
        """Verify provider email address."""
        try:
            serializer = EmailVerificationSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Invalid verification data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = serializer.validated_data['token']
            
            # Find provider with this token
            try:
                provider = Provider.objects.get(email_verification_token=token)
            except Provider.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Invalid verification token',
                    'errors': {'token': ['Invalid or expired verification token']}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if token is valid and not expired
            if not is_verification_token_valid(token, provider):
                return Response({
                    'success': False,
                    'message': 'Verification token has expired',
                    'errors': {'token': ['Verification token has expired. Please request a new one.']}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if already verified
            if provider.email_verified:
                return Response({
                    'success': True,
                    'message': 'Email already verified',
                    'data': {
                        'provider_id': str(provider.id),
                        'email': provider.email,
                        'verified': True
                    }
                }, status=status.HTTP_200_OK)
            
            # Verify the email
            with transaction.atomic():
                provider.email_verified = True
                provider.email_verification_token = None
                provider.email_verification_expires = None
                provider.save(update_fields=[
                    'email_verified',
                    'email_verification_token',
                    'email_verification_expires'
                ])
                
                # Send welcome email directly
                try:
                    send_welcome_email(provider)
                except Exception as e:
                    logger.error(f"Failed to send welcome email to {provider.email}: {str(e)}")
                
                logger.info(f"Email verified successfully for provider {provider.email}")
                
                return Response({
                    'success': True,
                    'message': 'Email verified successfully',
                    'data': {
                        'provider_id': str(provider.id),
                        'email': provider.email,
                        'verified': True
                    }
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            
            return Response({
                'success': False,
                'message': 'An error occurred during email verification',
                'errors': {'general': ['Please try again later']}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResendVerificationView(APIView):
    """
    Resend verification email endpoint.
    
    Resend email verification link to provider's email address.
    """
    
    @swagger_auto_schema(
        operation_description="Resend verification email to provider",
        operation_summary="Resend Verification Email",
        request_body=ResendVerificationSerializer,
        responses={
            200: openapi.Response(description="Verification email sent successfully"),
            400: openapi.Response(description="Email already verified or invalid"),
            404: openapi.Response(description="Provider not found"),
            500: openapi.Response(description="Internal server error")
        },
        tags=['Email Verification']
    )
    def post(self, request):
        """Resend verification email to provider."""
        try:
            serializer = ResendVerificationSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Invalid email address',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            email = serializer.validated_data['email']
            
            # Find provider
            try:
                provider = Provider.objects.get(email=email)
            except Provider.DoesNotExist:
                return Response({
                    'success': False,
                    'message': 'Provider not found',
                    'errors': {'email': ['No provider found with this email address']}
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if already verified
            if provider.email_verified:
                return Response({
                    'success': False,
                    'message': 'Email already verified',
                    'errors': {'email': ['This email address is already verified']}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Resend verification email
            try:
                send_verification_email(provider)
            except Exception as e:
                logger.error(f"Failed to resend verification email to {provider.email}: {str(e)}")
            
            logger.info(f"Verification email resent to {provider.email}")
            
            return Response({
                'success': True,
                'message': 'Verification email sent successfully',
                'data': {
                    'email': provider.email,
                    'sent': True
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Resend verification error: {str(e)}")
            
            return Response({
                'success': False,
                'message': 'An error occurred while sending verification email',
                'errors': {'general': ['Please try again later']}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProviderDetailView(APIView):
    """
    Provider detail view.
    
    Get detailed information about a specific provider.
    """
    
    @swagger_auto_schema(
        operation_description="Get provider details by ID",
        operation_summary="Get Provider Details",
        manual_parameters=[
            openapi.Parameter(
                'provider_id',
                openapi.IN_PATH,
                description="Provider UUID",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_UUID
            )
        ],
        responses={
            200: ProviderResponseSerializer,
            404: openapi.Response(description="Provider not found"),
            500: openapi.Response(description="Internal server error")
        },
        tags=['Provider Management']
    )
    def get(self, request, provider_id):
        """Get provider details."""
        try:
            provider = get_object_or_404(Provider, id=provider_id)
            serializer = ProviderResponseSerializer(provider)
            
            return Response({
                'success': True,
                'message': 'Provider details retrieved successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving provider details: {str(e)}")
            
            return Response({
                'success': False,
                'message': 'An error occurred while retrieving provider details',
                'errors': {'general': ['Please try again later']}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Get list of available medical specializations",
    operation_summary="Get Specializations List",
    responses={
        200: openapi.Response(
            description="Specializations retrieved successfully",
            examples={
                "application/json": {
                    "success": True,
                    "message": "Specializations retrieved successfully",
                    "data": [
                        {"value": "cardiology", "label": "Cardiology"},
                        {"value": "dermatology", "label": "Dermatology"}
                    ]
                }
            }
        ),
        500: openapi.Response(description="Internal server error")
    },
    tags=['Provider Management']
)
@api_view(['GET'])
def provider_specializations(request):
    """
    Get list of available specializations.
    
    Returns all available medical specializations that providers can select from.
    """
    try:
        specializations = [
            {'value': choice[0], 'label': choice[1]}
            for choice in Provider.SPECIALIZATION_CHOICES
        ]
        
        return Response({
            'success': True,
            'message': 'Specializations retrieved successfully',
            'data': specializations
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error retrieving specializations: {str(e)}")
        
        return Response({
            'success': False,
            'message': 'An error occurred while retrieving specializations',
            'errors': {'general': ['Please try again later']}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@swagger_auto_schema(
    method='get',
    operation_description="Health check endpoint for monitoring API status",
    operation_summary="API Health Check",
    responses={
        200: openapi.Response(
            description="API is healthy",
            examples={
                "application/json": {
                    "success": True,
                    "message": "API is healthy",
                    "timestamp": "2024-01-01T12:00:00Z"
                }
            }
        )
    },
    tags=['System']
)
@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint.
    
    Returns the current status of the API for monitoring purposes.
    """
    return Response({
        'success': True,
        'message': 'API is healthy',
        'timestamp': timezone.now().isoformat()
    }, status=status.HTTP_200_OK) 