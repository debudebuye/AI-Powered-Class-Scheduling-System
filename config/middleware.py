"""
Rate limiting middleware for login and registration endpoints.
"""
import time
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages

logger = logging.getLogger(__name__)

# In-memory rate limit store. In production, use Redis via django.core.cache.
_rate_limit_store = {}

# Default limits
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 900  # 15 minutes
REGISTER_MAX_ATTEMPTS = 3
REGISTER_WINDOW_SECONDS = 3600  # 1 hour


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


def _check_rate_limit(key, max_attempts, window_seconds):
    now = time.time()
    if key not in _rate_limit_store:
        return True

    attempts, window_start = _rate_limit_store[key]
    if now - window_start > window_seconds:
        del _rate_limit_store[key]
        return True

    if attempts >= max_attempts:
        return False

    return True


def _record_attempt(key, window_seconds):
    now = time.time()
    if key in _rate_limit_store:
        attempts, window_start = _rate_limit_store[key]
        if now - window_start > window_seconds:
            _rate_limit_store[key] = (1, now)
        else:
            _rate_limit_store[key] = (attempts + 1, window_start)
    else:
        _rate_limit_store[key] = (1, now)


class SecurityHeadersMiddleware:
    """Add security headers to all responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        return response


class LoginRateLimitMiddleware:
    """Rate limit login attempts per IP."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path in ('/manage/', '/account/login/'):
            ip = _get_client_ip(request)
            key = f'login:{ip}'

            if not _check_rate_limit(key, LOGIN_MAX_ATTEMPTS, LOGIN_WINDOW_SECONDS):
                logger.warning("Rate limit exceeded for login from IP %s", ip)
                messages.error(request, "Too many login attempts. Please try again later.")
                return render(request, 'login_modern.html', status=429)

            _record_attempt(key, LOGIN_WINDOW_SECONDS)

        return self.get_response(request)


class RegistrationRateLimitMiddleware:
    """Rate limit registration attempts per IP."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/account/register/':
            ip = _get_client_ip(request)
            key = f'register:{ip}'

            if not _check_rate_limit(key, REGISTER_MAX_ATTEMPTS, REGISTER_WINDOW_SECONDS):
                logger.warning("Rate limit exceeded for registration from IP %s", ip)
                messages.error(request, "Too many registration attempts. Please try again later.")
                return render(request, 'account/register.html', status=429)

            _record_attempt(key, REGISTER_WINDOW_SECONDS)

        return self.get_response(request)
