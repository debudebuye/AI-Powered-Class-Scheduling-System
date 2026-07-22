"""
Management command to create the initial admin/superuser.

Usage:
    python manage.py create_initial_admin
    python manage.py create_initial_admin --username admin --email admin@example.com
"""

import getpass
import logging

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create an initial admin superuser interactively"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Admin username")
        parser.add_argument("--email", type=str, help="Admin email")

    def handle(self, *args, **options):
        username = options["username"] or input("Username: ").strip()
        email = options["email"] or input("Email: ").strip()

        if not username or not email:
            self.stderr.write(self.style.ERROR("Username and email are required."))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"User '{username}' already exists. Skipping.")
            )
            return

        password = getpass.getpass("Password: ")
        password_confirm = getpass.getpass("Confirm password: ")

        if password != password_confirm:
            self.stderr.write(self.style.ERROR("Passwords do not match."))
            return

        if len(password) < 8:
            self.stderr.write(
                self.style.ERROR("Password must be at least 8 characters.")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        logger.info("Superuser '%s' created successfully.", username)
        self.stdout.write(
            self.style.SUCCESS(f"Superuser '{username}' created successfully.")
        )
