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
            "script-src 'self' https://www.google.com https://www.gstatic.com 'unsafe-inline' 'unsafe-eval'; "
            "worker-src 'self'; "
            "style-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com 'unsafe-inline'; "
            "font-src 'self' https://fonts.gstatic.com https://fonts.googleapis.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://www.google.com; "
            "media-src 'self'; "
            "frame-src 'self' https://www.google.com https://recaptcha.google.com; "
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
        
        # Prevent clickjacking within reason (Allow SAMEORIGIN for the sandbox)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
