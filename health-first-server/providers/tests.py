"""
Test suite for provider registration functionality.
"""

import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, Mock

from .models import Provider, ClinicAddress, ProviderRegistrationLog
from .utils.password_utils import validate_password_strength
from .utils.validation_utils import validate_phone_number, validate_license_number


class ProviderModelTest(TestCase):
    """Test Provider model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.clinic_address = ClinicAddress.objects.create(
            street="123 Test St",
            city="Test City",
            state="Test State",
            zip_code="12345"
        )
        
        self.provider_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@test.com',
            'phone_number': '+1234567890',
            'specialization': 'cardiology',
            'license_number': 'MD123456',
            'years_of_experience': 5,
            'clinic_address': self.clinic_address
        }
    
    def test_provider_creation(self):
        """Test provider model creation."""
        provider = Provider.objects.create(**self.provider_data)
        
        self.assertEqual(provider.first_name, 'John')
        self.assertEqual(provider.last_name, 'Doe')
        self.assertEqual(provider.email, 'john.doe@test.com')
        self.assertEqual(provider.verification_status, 'pending')
        self.assertFalse(provider.email_verified)
        self.assertTrue(provider.is_active)
    
    def test_provider_string_representation(self):
        """Test provider string representation."""
        provider = Provider.objects.create(**self.provider_data)
        expected_str = "Dr. John Doe (john.doe@test.com)"
        self.assertEqual(str(provider), expected_str)
    
    def test_password_hashing(self):
        """Test password hashing functionality."""
        provider = Provider.objects.create(**self.provider_data)
        provider.set_password('TestPassword123!')
        
        self.assertNotEqual(provider.password, 'TestPassword123!')
        self.assertTrue(provider.check_password('TestPassword123!'))
        self.assertFalse(provider.check_password('WrongPassword'))
    
    def test_get_full_name(self):
        """Test get_full_name method."""
        provider = Provider.objects.create(**self.provider_data)
        self.assertEqual(provider.get_full_name(), 'John Doe')


class ProviderRegistrationAPITest(APITestCase):
    """Test provider registration API endpoints."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.registration_url = reverse('providers:provider-register')
        
        self.valid_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@test.com',
            'phone_number': '+1987654321',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'specialization': 'dermatology',
            'license_number': 'MD987654',
            'years_of_experience': 8,
            'clinic_address': {
                'street': '456 Medical Ave',
                'city': 'Health City',
                'state': 'Medical State',
                'zip': '54321'
            }
        }
    
    @patch('providers.tasks.send_verification_email_task.delay')
    @patch('providers.tasks.send_admin_notification_task.delay')
    @patch('providers.tasks.log_registration_attempt.delay')
    def test_successful_registration(self, mock_log, mock_admin, mock_email):
        """Test successful provider registration."""
        response = self.client.post(
            self.registration_url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('provider_id', data['data'])
        self.assertEqual(data['data']['email'], 'jane.smith@test.com')
        
        # Check provider was created
        provider = Provider.objects.get(email='jane.smith@test.com')
        self.assertEqual(provider.first_name, 'Jane')
        self.assertEqual(provider.specialization, 'dermatology')
        
        # Check tasks were called
        mock_email.assert_called_once()
        mock_admin.assert_called_once()
        mock_log.assert_called_once()
    
    def test_duplicate_email_registration(self):
        """Test registration with duplicate email."""
        # Create first provider
        clinic_address = ClinicAddress.objects.create(
            street="123 Test St",
            city="Test City",
            state="Test State",
            zip_code="12345"
        )
        Provider.objects.create(
            first_name='Existing',
            last_name='Provider',
            email='jane.smith@test.com',
            phone_number='+1111111111',
            specialization='cardiology',
            license_number='MD111111',
            years_of_experience=5,
            clinic_address=clinic_address
        )
        
        # Try to register with same email
        response = self.client.post(
            self.registration_url,
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('email', data['errors'])
    
    def test_invalid_password_registration(self):
        """Test registration with invalid password."""
        invalid_data = self.valid_data.copy()
        invalid_data['password'] = 'weak'
        invalid_data['confirm_password'] = 'weak'
        
        response = self.client.post(
            self.registration_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('password', data['errors'])
    
    def test_password_mismatch_registration(self):
        """Test registration with password mismatch."""
        invalid_data = self.valid_data.copy()
        invalid_data['confirm_password'] = 'DifferentPass123!'
        
        response = self.client.post(
            self.registration_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('confirm_password', data['errors'])
    
    def test_invalid_phone_number_registration(self):
        """Test registration with invalid phone number."""
        invalid_data = self.valid_data.copy()
        invalid_data['phone_number'] = 'invalid-phone'
        
        response = self.client.post(
            self.registration_url,
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('phone_number', data['errors'])


class EmailVerificationAPITest(APITestCase):
    """Test email verification API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.verify_url = reverse('providers:email-verification')
        
        clinic_address = ClinicAddress.objects.create(
            street="123 Test St",
            city="Test City",
            state="Test State",
            zip_code="12345"
        )
        
        self.provider = Provider.objects.create(
            first_name='Test',
            last_name='Provider',
            email='test@example.com',
            phone_number='+1234567890',
            specialization='cardiology',
            license_number='MD123456',
            years_of_experience=5,
            clinic_address=clinic_address,
            email_verification_token='test-token-123'
        )
    
    @patch('providers.tasks.send_welcome_email_task.delay')
    def test_successful_email_verification(self, mock_welcome):
        """Test successful email verification."""
        data = {'token': 'test-token-123'}
        
        response = self.client.post(
            self.verify_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertTrue(response_data['data']['verified'])
        
        # Check provider was updated
        self.provider.refresh_from_db()
        self.assertTrue(self.provider.email_verified)
        self.assertIsNone(self.provider.email_verification_token)
        
        # Check welcome email task was called
        mock_welcome.assert_called_once()
    
    def test_invalid_token_verification(self):
        """Test email verification with invalid token."""
        data = {'token': 'invalid-token'}
        
        response = self.client.post(
            self.verify_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('token', response_data['errors'])


class PasswordUtilsTest(TestCase):
    """Test password utility functions."""
    
    def test_valid_password(self):
        """Test valid password validation."""
        valid_password = 'SecurePass123!'
        # Should not raise exception
        try:
            validate_password_strength(valid_password)
        except Exception:
            self.fail("validate_password_strength raised exception for valid password")
    
    def test_short_password(self):
        """Test password too short validation."""
        with self.assertRaises(Exception):
            validate_password_strength('Short1!')
    
    def test_password_without_uppercase(self):
        """Test password without uppercase validation."""
        with self.assertRaises(Exception):
            validate_password_strength('nouppercase123!')
    
    def test_password_without_lowercase(self):
        """Test password without lowercase validation."""
        with self.assertRaises(Exception):
            validate_password_strength('NOLOWERCASE123!')
    
    def test_password_without_number(self):
        """Test password without number validation."""
        with self.assertRaises(Exception):
            validate_password_strength('NoNumberHere!')
    
    def test_password_without_special_char(self):
        """Test password without special character validation."""
        with self.assertRaises(Exception):
            validate_password_strength('NoSpecialChar123')


class ValidationUtilsTest(TestCase):
    """Test validation utility functions."""
    
    def test_valid_phone_number(self):
        """Test valid phone number validation."""
        valid_phone = '+1234567890'
        formatted = validate_phone_number(valid_phone)
        self.assertEqual(formatted, '+1234567890')
    
    def test_invalid_phone_number(self):
        """Test invalid phone number validation."""
        with self.assertRaises(Exception):
            validate_phone_number('invalid-phone')
    
    def test_valid_license_number(self):
        """Test valid license number validation."""
        valid_license = 'MD123456'
        formatted = validate_license_number(valid_license)
        self.assertEqual(formatted, 'MD123456')
    
    def test_invalid_license_number(self):
        """Test invalid license number validation."""
        with self.assertRaises(Exception):
            validate_license_number('MD-123@456')


class RateLimitingTest(APITestCase):
    """Test rate limiting functionality."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.registration_url = reverse('providers:provider-register')
        
        self.valid_data = {
            'first_name': 'Rate',
            'last_name': 'Test',
            'email': 'rate.test@example.com',
            'phone_number': '+1555555555',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'specialization': 'cardiology',
            'license_number': 'RT123456',
            'years_of_experience': 5,
            'clinic_address': {
                'street': '123 Rate St',
                'city': 'Rate City',
                'state': 'Rate State',
                'zip': '12345'
            }
        }
    
    @patch('providers.tasks.send_verification_email_task.delay')
    @patch('providers.tasks.send_admin_notification_task.delay')
    @patch('providers.tasks.log_registration_attempt.delay')
    def test_rate_limiting_not_triggered(self, mock_log, mock_admin, mock_email):
        """Test that rate limiting doesn't trigger for normal use."""
        # Make one request - should succeed
        response = self.client.post(
            self.registration_url,
            data=json.dumps(self.valid_data),
            content_type='application/json',
            REMOTE_ADDR='127.0.0.1'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SpecializationsAPITest(APITestCase):
    """Test specializations API endpoint."""
    
    def test_get_specializations(self):
        """Test getting list of specializations."""
        url = reverse('providers:provider-specializations')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], list)
        self.assertGreater(len(data['data']), 0)
        
        # Check structure of specialization items
        specialization = data['data'][0]
        self.assertIn('value', specialization)
        self.assertIn('label', specialization)


class HealthCheckAPITest(APITestCase):
    """Test health check API endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        url = reverse('providers:health-check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('timestamp', data) 