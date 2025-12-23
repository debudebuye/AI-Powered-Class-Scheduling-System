#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create a new user
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
    user = User.objects.get(username=username)
else:
    # Create new user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    print(f"User '{username}' created successfully!")

print(f"Login credentials:")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Email: {email}")