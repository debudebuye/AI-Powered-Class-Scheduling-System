# Quick Reference Guide

## 🚀 Quick Start Commands

### Windows
```bash
# Setup (first time)
quick_setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Linux/Mac
```bash
# Setup (first time)
chmod +x quick_setup.sh
./quick_setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 📁 Project Structure

```
apps/
├── account/          # User authentication
└── schedule/         # Timetable scheduling
    └── services/     # Business logic

config/
└── settings/         # Environment configs
    ├── base.py
    ├── development.py
    ├── staging.py
    └── production.py
```

## 🔧 Common Commands

### Development
```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Django shell
python manage.py shell
```

### Database
```bash
# Reset database
del db.sqlite3                 # Windows
rm db.sqlite3                  # Linux/Mac
python manage.py migrate

# Backup database
copy db.sqlite3 db.backup      # Windows
cp db.sqlite3 db.backup        # Linux/Mac

# Show migrations
python manage.py showmigrations

# SQL for migration
python manage.py sqlmigrate app_name migration_name
```

### Cleanup
```bash
# Remove old files after migration
python cleanup_old_files.py

# Remove Python cache
del /s /q __pycache__          # Windows
find . -type d -name __pycache__ -exec rm -r {} +  # Linux/Mac
```

## 🌐 URLs

### Development
- Homepage: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/login/
- Dashboard: http://127.0.0.1:8000/admin-dashboard/

### URL Namespaces
```python
# In views
redirect('schedule:index')
redirect('account:login')

# In templates
{% url 'schedule:index' %}
{% url 'account:login' %}
```

## 🔐 Environment Variables

Edit `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-password

EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 Dependencies

### Install
```bash
# Production
pip install -r requirements.txt

# Development (includes testing tools)
pip install -r requirements-dev.txt

# Update requirements
pip freeze > requirements.txt
```

### Key Packages
- Django 4.0.6
- python-decouple (environment variables)
- xhtml2pdf (PDF generation)
- Pillow (image processing)

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.schedule

# Run with coverage (dev dependencies)
pytest --cov=apps

# Run specific test
python manage.py test apps.schedule.tests.TestTimetableGeneration
```

## 🐛 Debugging

```bash
# Check for issues
python manage.py check

# Check specific app
python manage.py check apps.schedule

# Validate templates
python manage.py validate_templates

# Show URLs
python manage.py show_urls  # requires django-extensions
```

## 📝 Git Commands

```bash
# Status
git status

# Add all changes
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Create branch
git checkout -b feature/your-feature

# View changes
git diff
```

## 🔄 Migration Workflow

```bash
# 1. Make model changes in models.py
# 2. Create migrations
python manage.py makemigrations

# 3. Review migration file
# Check apps/*/migrations/

# 4. Apply migrations
python manage.py migrate

# 5. Test changes
python manage.py runserver
```

## 🎨 Static Files

```bash
# Collect static files
python manage.py collectstatic

# Find static files
python manage.py findstatic filename.css

# Clear collected static
del /s /q staticfiles           # Windows
rm -rf staticfiles              # Linux/Mac
```

## 👥 User Management

```bash
# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username

# Create user programmatically
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('username', 'email@example.com', 'password')
```

## 📊 Database Queries

```bash
# Django shell
python manage.py shell

# Example queries
>>> from apps.schedule.models import Course, Instructor
>>> Course.objects.all()
>>> Instructor.objects.filter(name__contains='John')
>>> Course.objects.create(course_number='CS101', course_name='Intro to CS')
```

## 🚨 Emergency Commands

```bash
# Reset everything
del db.sqlite3
del /s /q apps\*\migrations\*.py  # Keep __init__.py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Clear cache
python manage.py clear_cache  # if cache configured

# Rebuild search index
python manage.py rebuild_index  # if search configured
```

## 📚 Documentation Files

- `README_NEW.md` - Main documentation
- `ARCHITECTURE.md` - System design
- `MIGRATION_GUIDE.md` - Migration steps
- `FINAL_SETUP.md` - Setup instructions
- `MIGRATION_CHECKLIST.md` - Progress tracking
- `QUICK_REFERENCE.md` - This file

## 🎯 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Import Error | Activate venv, reinstall requirements |
| URL Reverse Error | Add namespace to URL calls |
| Template Not Found | Check TEMPLATES in settings |
| Static Files 404 | Run collectstatic |
| Database Error | Run migrations |
| Module Not Found | Check INSTALLED_APPS |

## 💡 Tips

1. **Always activate virtual environment** before running commands
2. **Use namespaces** in all URL references
3. **Keep .env secure** - never commit to git
4. **Run migrations** after model changes
5. **Collect static** before deployment
6. **Test thoroughly** after changes
7. **Backup database** before major changes
8. **Use git** for version control

## 🔗 Useful Links

- Django Docs: https://docs.djangoproject.com/
- Python Decouple: https://github.com/henriquebastos/python-decouple
- Django Best Practices: https://django-best-practices.readthedocs.io/

---

**Keep this file handy for quick reference!** 📌
