# AI Class Scheduling System

An intelligent scheduling system that automatically generates optimized class schedules using generative AI algorithms. Built with Python and machine learning techniques to solve complex scheduling constraints.

## 🤖 AI-Powered Features

- **Intelligent Timetable Generation**: Uses genetic algorithms (evolutionary AI) to create optimal conflict-free schedules
- **Machine Learning Optimization**: Automatically learns from constraints to find the best scheduling solutions
- **Smart Resource Management**: AI-driven allocation of teachers, rooms, courses, departments, batches, and sections
- **Automated Conflict Resolution**: Intelligent detection and resolution of scheduling conflicts
- **PDF Export**: Generate and download optimized timetables
- **User Management**: Secure admin authentication and user profiles

## 🧠 AI Technology

This system employs **Genetic Algorithms**, a class of evolutionary algorithms inspired by natural selection:
- **Population-based search**: Maintains multiple schedule solutions simultaneously
- **Fitness evaluation**: Scores schedules based on constraint satisfaction
- **Selection**: Chooses best-performing schedules for reproduction
- **Crossover**: Combines features from successful schedules
- **Mutation**: Introduces variations to explore new solutions
- **Evolution**: Iteratively improves schedules until optimal solution is found

## Tech Stack

- **Backend**: Django 4.0.6
- **Database**: SQLite (development), PostgreSQL-ready (production)
- **PDF Generation**: xhtml2pdf, ReportLab
- **Frontend**: Bootstrap 4, HTML/CSS/JavaScript

## Project Structure

```
AI-Class-Scheduling-System/
├── apps/
│   ├── account/          # User authentication and profiles
│   │   ├── migrations/
│   │   ├── templates/account/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   └── schedule/         # Timetable scheduling
│       ├── migrations/
│       ├── services/     # Business logic
│       │   ├── genetic_algorithm.py
│       │   └── timetable_generator.py
│       ├── templates/schedule/
│       ├── models.py
│       ├── views.py
│       ├── forms.py
│       └── urls.py
├── config/               # Project configuration
│   ├── settings/
│   │   ├── base.py      # Base settings
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded files
├── templates/           # Global templates
├── .env.example         # Environment variables template
├── .gitignore
├── manage.py
├── requirements.txt
└── requirements-dev.txt
```

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AMUCSS
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and set:
   - `SECRET_KEY`: Generate using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: Set to `False` in production
   - `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`: Your email credentials

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### 1. Add Basic Data

Before generating timetables, add the following data through the admin dashboard:

1. **Departments**: CS, IT, SE
2. **Teachers/Instructors**: Add faculty members
3. **Rooms**: Add classrooms with seating capacity
4. **Meeting Times**: Define time slots and days
5. **Courses**: Add courses and assign instructors
6. **Batches**: Create batches and assign courses
7. **Sections**: Define sections with weekly class frequency

### 2. Generate Timetable

1. Navigate to "Generate Timetable"
2. Click "Generate"
3. The genetic algorithm will create an optimized schedule
4. View and export the generated timetable

### 3. Manage Users

- Register new users through `/account/register/`
- Manage users through the admin panel
- Reset passwords via email

## Genetic Algorithm

The system uses a genetic algorithm with the following parameters:

- **Population Size**: 9 schedules per generation
- **Elite Schedules**: 1 (best schedule preserved)
- **Tournament Size**: 3
- **Mutation Rate**: 5%

### Fitness Function

Fitness is calculated based on:
- Room capacity constraints
- Instructor availability
- Time slot conflicts
- Room double-booking

The algorithm evolves until a conflict-free schedule (fitness = 1.0) is found.

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
python manage.py test

# With coverage
pytest --cov=apps
```

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8
pylint apps/
```

### Environment-Specific Settings

- **Development**: `DJANGO_ENV=development` (default)
- **Staging**: `DJANGO_ENV=staging`
- **Production**: `DJANGO_ENV=production`

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up proper `ALLOWED_HOSTS`
- [ ] Configure email backend
- [ ] Set up HTTPS
- [ ] Configure static file serving (WhiteNoise or CDN)
- [ ] Set up logging
- [ ] Configure backup strategy
- [ ] Enable security middleware

### Deployment Options

- **Heroku**: Use `Procfile` and `runtime.txt`
- **AWS**: Use Elastic Beanstalk or EC2
- **DigitalOcean**: Use App Platform or Droplets
- **Docker**: Create `Dockerfile` and `docker-compose.yml`

## API Documentation

Currently, the system uses Django views. To add REST API:

```bash
pip install djangorestframework
```

Add to `INSTALLED_APPS` and create serializers and viewsets.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8
- Write docstrings for all functions/classes
- Add type hints where applicable
- Write tests for new features
- Update documentation

## Troubleshooting

### Common Issues

**Import Errors**
- Ensure virtual environment is activated
- Check `PYTHONPATH` includes project root

**Database Errors**
- Run migrations: `python manage.py migrate`
- Check database connection settings

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check `STATIC_ROOT` and `STATIC_URL` settings

**Timetable Generation Fails**
- Ensure all required data is added (rooms, instructors, courses, etc.)
- Check for sufficient resources (rooms, time slots)
- Review genetic algorithm parameters

## License

[Add your license here]

## Contact

- **Project Maintainer**: [Your Name]
- **Email**: [Your Email]
- **University**: Arbaminch University, FCSE

## Acknowledgments

- Arbaminch University Faculty of Computer Science and Engineering
- Django Software Foundation
- Contributors and testers
