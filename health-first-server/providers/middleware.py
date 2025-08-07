"""
Middleware for rate limiting and security.
"""

import time
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware for provider registration.
    Limits registration attempts to 5 per IP per hour.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_window = getattr(settings, 'RATE_LIMIT_WINDOW_MINUTES', 60) * 60
        self.max_requests = getattr(settings, 'RATE_LIMIT_MAX_REQUESTS', 5)
        super().__init__(get_response)
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def is_registration_endpoint(self, path):
        """Check if the request is for provider registration."""
        registration_paths = [
            '/api/v1/provider/register',
            '/api/v1/provider/register/',
        ]
        return path in registration_paths
    
    def process_request(self, request):
        """Process incoming request for rate limiting."""
        # Only apply rate limiting to registration endpoints
        if not self.is_registration_endpoint(request.path):
            return None
        
        # Only apply to POST requests
        if request.method != 'POST':
            return None
        
        ip = self.get_client_ip(request)
        if not ip:
            return None
        
        cache_key = f"rate_limit:registration:{ip}"
        request_data = cache.get(cache_key, [])
        current_time = time.time()
        
        # Filter out old requests
        cutoff_time = current_time - self.rate_limit_window
        recent_requests = [timestamp for timestamp in request_data if timestamp > cutoff_time]
        
        # Check if limit exceeded
        if len(recent_requests) >= self.max_requests:
            oldest_request = min(recent_requests)
            retry_after = int(oldest_request + self.rate_limit_window - current_time)
            
            response_data = {
                'success': False,
                'message': 'Rate limit exceeded. Too many registration attempts.',
                'errors': {
                    'rate_limit': [
                        f'You have exceeded the maximum number of registration attempts. '
                        f'Please try again in {retry_after} seconds.'
                    ]
                },
                'retry_after': retry_after
            }
            
            response = JsonResponse(response_data, status=429)
            response['Retry-After'] = str(retry_after)
            return response
        
        # Add current request
        recent_requests.append(current_time)
        cache.set(cache_key, recent_requests, self.rate_limit_window + 60)
        
        return None 