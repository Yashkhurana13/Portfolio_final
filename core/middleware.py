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

import time
import hashlib
from datetime import datetime
from urllib import request, response
from django.conf import settings
from .models import VisitorLog

class VisitorAnalyticsMiddleware:
    """
    Lightweight visitor analytics middleware.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.ignore_prefixes = ('/static/', '/media/', '/admin/', '/favicon.ico')
        self.bot_agents = ('googlebot','bingbot','slurp','duckduckbot','baiduspider','yandexbot','facebookexternalhit','facebot','linkedinbot','twitterbot','slackbot')

    def __call__(self, request):
        response = self.get_response(request)

        try:
            path = request.path
            
            # Skip static/admin routes
            if path.startswith(self.ignore_prefixes):
                return response
            
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ua_lower = user_agent.lower()
            # Skip analytics for social/media crawlers
            if request.method == 'HEAD':
                return response
            if any(bot in ua_lower for bot in self.bot_agents):
                return response

            # Session throttling
            if hasattr(request, 'session'):
                recent_visits = request.session.get('recent_analytics_visits', {})
                current_time = time.time()
                last_visit_time = recent_visits.get(path)
                
                # If visited within 5 minutes, skip logging
                if last_visit_time and (current_time - last_visit_time) < 300:
                    return response
                    
                recent_visits[path] = current_time
                request.session['recent_analytics_visits'] = recent_visits

            # Extract IP safely
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Privacy: Hash IP if raw logging is disabled
            raw_logging = getattr(settings, 'ENABLE_RAW_IP_LOGGING', False)
            if not raw_logging and ip:
                today_str = datetime.now().strftime('%Y-%m-%d')
                hash_input = f"{ip}-{today_str}".encode('utf-8')
                ip = hashlib.sha256(hash_input).hexdigest()
                
            referrer = request.META.get('HTTP_REFERER', '')
            
            # Async-safe approach: in a high traffic env, consider celery. 
            # For this scale, sync DB write is fast enough.
            VisitorLog.objects.create(
                ip_address=ip,
                path=path,
                method=request.method,
                user_agent=user_agent,
                referrer=referrer
            )
        except Exception:
            # Never block page rendering on analytics failure
            pass

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
