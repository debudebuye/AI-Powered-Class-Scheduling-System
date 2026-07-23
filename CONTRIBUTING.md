# Contributing to AI-Powered Class Scheduling System

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Messages](#commit-messages)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Requesting Features](#requesting-features)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check [existing issues](../../issues) to avoid duplicates. When creating a bug report, include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, browser)
- Any relevant logs or screenshots

### Suggesting Features

Feature requests are welcome. Please open an issue with:

- A clear description of the feature
- The motivation/use case
- Any implementation ideas you have

### Contributing Code

1. **Fork** the repository
2. **Clone** your fork locally
3. Create a **feature branch** from `main`
4. Make your changes
5. Add or update **tests**
6. Ensure all **tests pass**
7. Submit a **pull request**

## Development Setup

### Prerequisites

- Python 3.8+
- PostgreSQL (production) or SQLite (development)
- Git

### Setup

```bash
# Fork and clone the repo
git clone https://github.com/debudebuye/AI-Powered-Class-Scheduling-System.git
cd AI-Powered-Class-Scheduling-System

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create admin user
python manage.py create_initial_admin

# Start development server
python manage.py runserver
```

## Branching Strategy

- `main` — Stable, production-ready code
- `develop` — Integration branch for features
- `feature/<name>` — New features or enhancements
- `fix/<name>` — Bug fixes
- `hotfix/<name>` — Urgent production fixes

```bash
# Create a feature branch
git checkout -b feature/my-new-feature main

# Create a fix branch
git checkout -b fix/my-bugfix main
```

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type       | Description                                      |
|------------|--------------------------------------------------|
| `feat`     | New feature                                      |
| `fix`      | Bug fix                                          |
| `docs`     | Documentation changes                            |
| `style`    | Formatting, no code change                       |
| `refactor` | Code restructuring, no feature/fix               |
| `test`     | Adding or updating tests                         |
| `chore`    | Build process, dependencies, tooling             |
| `perf`     | Performance improvement                          |

### Examples

```
feat(schedule): add room capacity validation in GA
fix(auth): prevent session fixation on login
docs: update README with Docker instructions
test(schedule): add genetic algorithm unit tests
```

## Code Style

This project uses **Black** for formatting and **Flake8** for linting.

### Before committing, run:

```bash
# Auto-format code
black .

# Sort imports
isort .

# Check for linting issues
flake8 apps/ config/
```

### Style Rules

- Use **4 spaces** for indentation (no tabs)
- Maximum line length: **88 characters** (Black default)
- Use **double quotes** for strings
- Write **docstrings** for all public functions and classes
- Use **type hints** where practical
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions

### Django-Specific

- Use `snake_case` for Python files, variables, functions
- Use `PascalCase` for classes
- Use `UPPER_SNAKE_CASE` for constants
- Prefer `get_object_or_404()` over manual lookups
- Use `{% load static %}` in templates for static files
- Always use `{% csrf_token %}` in POST forms

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps -v

# Run specific test file
pytest apps/schedule/tests.py -v

# Run specific test
pytest apps/schedule/tests.py::ScheduleTestCase::test_method -v
```

### Writing Tests

- Place tests in `tests.py` within each app, or in a `tests/` directory for complex apps
- Use `TestCase` for database tests (transactions are rolled back)
- Use `Client` for testing views
- Test both success and error paths
- Aim for meaningful coverage of critical paths (GA, views, forms)

```python
from django.test import TestCase
from apps.schedule.models import Room


class RoomTest(TestCase):
    def setUp(self):
        Room.objects.create(r_number="R101", seating_capacity=30)

    def test_room_creation(self):
        room = Room.objects.get(r_number="R101")
        self.assertEqual(room.seating_capacity, 30)

    def test_room_str(self):
        room = Room.objects.get(r_number="R101")
        self.assertIn("R101", str(room))
```

## Pull Request Process

### Before Submitting

- [ ] Code follows project style (Black, Flake8)
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated if needed
- [ ] No `print()` statements left in code
- [ ] No secrets or credentials committed
- [ ] Migrations are clean (no conflicting migrations)

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran and how to reproduce.

## Checklist
- [ ] My code follows the project style
- [ ] I have added tests that prove my fix/feature works
- [ ] All new and existing tests pass
- [ ] I have updated documentation accordingly
```

### Review Process

1. A maintainer will review your PR within a reasonable timeframe
2. Address any requested changes
3. Once approved, a maintainer will merge your PR

## Project Structure

```
apps/
  account/       # Authentication, user management
  schedule/      # Core scheduling (models, views, GA engine)
config/          # Django settings, URLs, WSGI
templates/       # HTML templates
static/          # CSS, JS, images
```

### Key Files

| File | Purpose |
|------|---------|
| `apps/schedule/services/genetic_algorithm.py` | GA engine (Population, Schedule, Crossover, Mutation) |
| `apps/schedule/services/timetable_generator.py` | Service layer orchestrating the GA |
| `apps/schedule/models.py` | All data models |
| `apps/schedule/views.py` | CRUD views, timetable generation, PDF export |
| `apps/schedule/forms.py` | Django ModelForms with validation |

## Questions?

If you have questions about contributing, feel free to open a [discussion](../../discussions) or reach out to the maintainers.

Thank you for contributing!
