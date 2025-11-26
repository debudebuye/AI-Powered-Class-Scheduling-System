# Setup Guide

Complete setup instructions for AMUCSS.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for version control)

## Installation Steps

### 1. Clone or Download Project

```bash
git clone <repository-url>
cd Class-scheduling-system
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter errors, try upgrading pip first:
```bash
python -m pip install --upgrade pip
```

### 4. Configure Environment Variables

Create `.env` file:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file with your settings:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default, no configuration needed)
# For PostgreSQL, uncomment and configure:
# DATABASE_URL=postgresql://user:password@localhost/dbname

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change-this-password
```

**Generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Setup Database

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Verification

Test these URLs:
- Homepage: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/login/

## Initial Data Setup

1. Login to admin panel
2. Add Departments (CS, IT, SE)
3. Add Instructors
4. Add Rooms with capacity
5. Add Meeting Times (days and time slots)
6. Add Courses and assign instructors
7. Create Batches and assign courses
8. Define Sections with weekly class frequency
9. Generate timetable

## Troubleshooting

### Virtual Environment Not Activating

**Windows PowerShell:**
If you get an execution policy error:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:
```bash
.\venv\Scripts\activate
```

**Windows CMD:**
```bash
venv\Scripts\activate.bat
```

### Import Errors

Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Errors

Delete database and recreate:
```bash
# Windows
del db.sqlite3

# Linux/Mac
rm db.sqlite3

# Then recreate
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Port Already in Use

Run on different port:
```bash
python manage.py runserver 8080
```

## Development Workflow

```bash
# 1. Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Make changes to code

# 3. If models changed, create migrations
python manage.py makemigrations
python manage.py migrate

# 4. Run tests
python manage.py test

# 5. Run server
python manage.py runserver
```

## Production Deployment

See [README.md](README.md) deployment section for production setup instructions.

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system design
- Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for common commands
- Start adding your data and generating timetables!
