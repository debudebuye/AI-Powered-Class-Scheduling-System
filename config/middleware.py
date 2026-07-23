"""
Rate limiting and security middleware.
"""

import logging
import time
from functools import wraps

from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse, resolve

logger = logging.getLogger(__name__)

# Rate limit defaults
LOGIN_MAX_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 900  # 15 minutes
REGISTER_MAX_ATTEMPTS = 3
REGISTER_WINDOW_SECONDS = 3600  # 1 hour

CACHE_TTL = max(LOGIN_WINDOW_SECONDS, REGISTER_WINDOW_SECONDS) + 60


def _get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "0.0.0.0")


def _check_rate_limit(key, max_attempts, window_seconds):
    now = time.time()
    record = cache.get(key)
    if record is None:
        return True

    attempts, window_start = record
    if now - window_start > window_seconds:
        cache.delete(key)
        return True

    if attempts >= max_attempts:
        return False

    return True


def _record_attempt(key, window_seconds):
    now = time.time()
    record = cache.get(key)
    if record is not None:
        attempts, window_start = record
        if now - window_start > window_seconds:
            cache.set(key, (1, now), CACHE_TTL)
        else:
            cache.set(key, (attempts + 1, window_start), CACHE_TTL)
    else:
        cache.set(key, (1, now), CACHE_TTL)


def _get_login_paths():
    """Dynamically resolve login URL paths."""
    paths = ["/account/login/"]
    try:
        paths.append(reverse("schedule:adminlogin"))
    except Exception:
        pass
    return paths


def _get_register_paths():
    """Dynamically resolve registration URL paths."""
    paths = ["/account/register/"]
    try:
        paths.append(reverse("account:register"))
    except Exception:
        pass
    return paths


class SecurityHeadersMiddleware:
    """Add security headers to all responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


class LoginRateLimitMiddleware:
    """Rate limit login attempts per IP."""

    def __init__(self, get_response):
        self.get_response = get_response
        self._login_paths = None

    def __call__(self, request):
        if self._login_paths is None:
            self._login_paths = _get_login_paths()

        if request.method == "POST" and request.path in self._login_paths:
            ip = _get_client_ip(request)
            key = f"login:{ip}"

            if not _check_rate_limit(key, LOGIN_MAX_ATTEMPTS, LOGIN_WINDOW_SECONDS):
                logger.warning("Rate limit exceeded for login from IP %s", ip)
                return render(
                    request,
                    "login_modern.html",
                    {"error": "Too many login attempts. Please try again later."},
                    status=429,
                )

            _record_attempt(key, LOGIN_WINDOW_SECONDS)

        return self.get_response(request)


class RegistrationRateLimitMiddleware:
    """Rate limit registration attempts per IP."""

    def __init__(self, get_response):
        self.get_response = get_response
        self._register_paths = None

    def __call__(self, request):
        if self._register_paths is None:
            self._register_paths = _get_register_paths()

        if request.method == "POST" and request.path in self._register_paths:
            ip = _get_client_ip(request)
            key = f"register:{ip}"

            if not _check_rate_limit(
                key, REGISTER_MAX_ATTEMPTS, REGISTER_WINDOW_SECONDS
            ):
                logger.warning("Rate limit exceeded for registration from IP %s", ip)
                return render(
                    request,
                    "account/register.html",
                    {
                        "error": "Too many registration attempts. Please try again later."
                    },
                    status=429,
                )

            _record_attempt(key, REGISTER_WINDOW_SECONDS)

        return self.get_response(request)
