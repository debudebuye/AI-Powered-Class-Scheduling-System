"""
Views for account app - user authentication and management.
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from decouple import config

from .models import Profile
from .forms import LoginForm, UserRegistrationForm


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def user_list(request):
    """Display list of all users."""
    users = User.objects.all()
    return render(request, 'account/user_list.html', {'users': users})


@login_required
def delete_user(request, user_id):
    """Delete a user."""
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect('account:user_list')


@login_required
def update_user(request, user_id):
    """Update user information."""
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        user.username = request.POST.get('username')
        user.save()
        return redirect('account:user_list')
    else:
        return redirect(reverse('account:update_user_page', kwargs={'user_id': user_id}))


@login_required
def update_user_page(request, user_id):
    """Display user update form."""
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'account/update_user.html', {'user': user})


def admin_login(request):
    """
    Admin login view.
    Note: This should be replaced with Django's built-in authentication in production.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Get credentials from environment variables
        admin_username = config('ADMIN_USERNAME', default='admin')
        admin_password = config('ADMIN_PASSWORD', default='password')
        
        if username == admin_username and password == admin_password:
            messages.success(request, "Login successful!")
            return redirect('schedule:index1')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'account/adminlogin.html')
