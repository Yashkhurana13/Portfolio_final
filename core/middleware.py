"""
Custom Security Middleware
Adds additional security headers to all responses
"""

class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to HTTP responses
    Provides defense-in-depth against common web attacks
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Remove server header to hide technology stack
        if 'server' in response:
            del response['server']
        
        # Content Security Policy (CSP)
        response['Content-Security-Policy'] = (
    "default-src 'self'; "

    "script-src 'self' "
    "https://www.google.com "
    "https://www.gstatic.com "
    "https://www.googletagmanager.com "
    "https://www.google-analytics.com "
    "https://www.clarity.ms "
    "https://scripts.clarity.ms "
    "'unsafe-inline' "
    "'unsafe-eval'; "

    "connect-src 'self' "
    "https://www.google.com "
    "https://www.google-analytics.com "
    "https://region1.google-analytics.com "
    "https://www.clarity.ms "
    "https://scripts.clarity.ms "
    "https://x.clarity.ms "
    "https://o.clarity.ms "
    "https://*.clarity.ms "
    "wss://*.clarity.ms; "

    "worker-src 'self' blob:; "

    "style-src 'self' "
    "https://fonts.googleapis.com "
    "'unsafe-inline'; "

    "font-src 'self' "
    "https://fonts.gstatic.com "
    "data:; "

    "img-src 'self' data: https: blob:; "

    "media-src 'self' blob:; "

    "frame-src 'self' "
    "https://www.google.com "
    "https://recaptcha.google.com; "

    "frame-ancestors 'self'; "

    "base-uri 'self'; "

    "form-action 'self';"
)
        # Permissions Policy (formerly Feature Policy)
        response['Permissions-Policy'] = (
            "camera=(), "
            "microphone=(), "
            "geolocation=(), "
            "payment=(), "
            "usb=(), "
            "magnetometer=(), "
            "gyroscope=(), "
            "accelerometer=()"
        )
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response


from django.http import HttpResponse, JsonResponse
from django_ratelimit.exceptions import Ratelimited

class RateLimitMiddleware:
    """
    Middleware to gracefully handle django-ratelimit exceptions globally.
    Returns a 429 response when limits are exceeded.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, Ratelimited):
            msg = "Too many requests. Please try again later."
            # Check for JSON/AJAX requests
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept', '').startswith('application/json'):
                return JsonResponse({'error': msg}, status=429)
            # Default HTML response for standard form submissions
            return HttpResponse(
                f'<div style="text-align:center;font-family:sans-serif;margin-top:20vh;">'
                f'<h1>429 Too Many Requests</h1>'
                f'<p>{msg}</p>'
                f'</div>',
                status=429
            )
        return None
