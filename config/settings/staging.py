"""
Staging-specific settings.
"""
from .base import *

DEBUG = True

# Staging uses similar security to production but with DEBUG enabled
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
