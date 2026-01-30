# AI Class Scheduling System

An intelligent scheduling system that automatically generates optimized class schedules using generative AI algorithms. Built with Python and machine learning techniques to solve complex scheduling constraints.

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` and set your configuration:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-password
```

Generate SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Setup Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## ✨ AI-Powered Features

- **🤖 Intelligent Timetable Generation** - Uses genetic algorithms (evolutionary AI) to automatically create optimal conflict-free schedules
- **🧠 Machine Learning Optimization** - Evolutionary algorithms that learn and adapt to find the best scheduling solutions
- **📊 Smart Resource Management** - AI-driven allocation of instructors, rooms, courses, departments, batches, and sections
- **⚡ Automated Conflict Resolution** - Intelligent detection and resolution of scheduling conflicts
- **📄 PDF Export** - Generate and download optimized timetables
- **👥 User Management** - Secure admin authentication and user profiles

## 🧬 AI Technology

This system employs **Genetic Algorithms**, a class of evolutionary algorithms inspired by natural selection:

- **Population-based Search**: Maintains multiple schedule solutions simultaneously
- **Fitness Evaluation**: Intelligently scores schedules based on constraint satisfaction
- **Natural Selection**: Automatically selects best-performing schedules
- **Genetic Crossover**: Combines successful scheduling patterns
- **Mutation**: Introduces variations to explore new solutions
- **Evolution**: Iteratively improves schedules until optimal solution is found

**Result**: Automatically generates optimal schedules that would take hours or days to create manually!

## 🏗️ Project Structure

```
apps/
├── account/          # User authentication and profiles
└── schedule/         # Timetable scheduling
    └── services/     # AI algorithms (genetic algorithm engine)
        ├── genetic_algorithm.py      # Core AI engine
        └── timetable_generator.py    # AI service layer

config/
└── settings/         # Environment-specific configurations
    ├── base.py
    ├── development.py
    ├── staging.py
    └── production.py
```

## 🛠️ Tech Stack

- **Backend**: Django 4.2.16
- **Language**: Python 3.8+
- **AI/ML**: Genetic Algorithms (Evolutionary AI)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 4, HTML/CSS/JavaScript
- **Optimization**: Population-based search, constraint satisfaction

## 📚 Documentation

- **[Full Documentation](docs/README.md)** - Complete project documentation
- **[AI Features](docs/AI_FEATURES.md)** - Detailed AI capabilities and algorithms
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design and patterns
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Common commands and tips

## 🔧 Common Commands

```bash
# Activate virtual environment
.\venv\Scripts\activate              # Windows
source venv/bin/activate             # Linux/Mac

# Run development server
python manage.py runserver

# Create/apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

## 📖 Usage

1. **Add Resources**: Navigate to admin dashboard and add:
   - Departments (CS, IT, SE)
   - Instructors/Teachers
   - Rooms with seating capacity
   - Meeting times (days and time slots)
   - Courses with assigned instructors

2. **Create Batches**: Define batches and assign courses to them

3. **Define Sections**: Create sections with weekly class frequency

4. **Generate Timetable**: Click "Generate Timetable" and let the genetic algorithm create an optimized schedule

5. **Export**: View and export the generated timetable as PDF

## 🚀 Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL database
4. Set up static file serving
5. Enable HTTPS
6. Configure email backend

See [docs/README.md](docs/README.md) for detailed deployment instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 👥 About

An open-source AI-powered scheduling solution for educational institutions.

## 🙏 Acknowledgments

- Django Software Foundation
- Machine Learning and AI community
- Open-source contributors

---

For detailed documentation, see the [docs](docs/) folder.
