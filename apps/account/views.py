"""
Views for account app - user authentication and management.
"""

import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import UserRegistrationForm
from .models import Profile

logger = logging.getLogger(__name__)


def _is_staff(user):
    return user.is_active and user.is_staff


def register(request):
    """Handle user registration."""
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def user_list(request):
    """Display list of all users."""
    users = User.objects.all()
    return render(request, "account/user_list.html", {"users": users})


@require_POST
@login_required
@user_passes_test(_is_staff)
def delete_user(request, user_id):
    """Delete a user. Staff only."""
    user = get_object_or_404(User, pk=user_id)
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("account:user_list")
    user.delete()
    messages.success(request, f"User '{user.username}' deleted.")
    return redirect("account:user_list")


@login_required
@user_passes_test(_is_staff)
def update_user(request, user_id):
    """Update user information. Staff only."""
    if request.method == "POST":
        user = get_object_or_404(User, pk=user_id)
        username = request.POST.get("username", "").strip()
        if not username:
            messages.error(request, "Username cannot be empty.")
            return redirect("account:update_user_page", user_id=user_id)
        if User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, "Username already taken.")
            return redirect("account:update_user_page", user_id=user_id)
        user.username = username
        user.save()
        messages.success(request, f"User '{user.username}' updated.")
        return redirect("account:user_list")
    return redirect(reverse("account:update_user_page", kwargs={"user_id": user_id}))


@login_required
def update_user_page(request, user_id):
    """Display user update form."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, "account/update_user.html", {"user": user})


def admin_login(request):
    """Admin login view using Django's built-in authentication."""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Please enter both username and password.")
            return render(request, "account/adminlogin.html")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info("User '%s' logged in successfully.", username)
                messages.success(request, "Login successful!")
                return redirect("schedule:admindash")
            else:
                logger.warning("Disabled user '%s' attempted login.", username)
                messages.error(request, "This account has been disabled.")
        else:
            logger.warning("Failed login attempt for username '%s'.", username)
            messages.error(request, "Invalid username or password.")

    return render(request, "account/adminlogin.html")
