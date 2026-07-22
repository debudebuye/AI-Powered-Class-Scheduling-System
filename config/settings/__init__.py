"""
Settings package initialization.
Import the appropriate settings module based on environment.
"""

from decouple import config

ENV = config("DJANGO_ENV", default="development")

if ENV == "production":
    from .production import *  # noqa: F401,F403
elif ENV == "staging":
    from .staging import *  # noqa: F401,F403
else:
    from .development import *  # noqa: F401,F403
