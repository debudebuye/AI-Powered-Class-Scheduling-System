# Architecture Documentation

## Overview

The AI Class Scheduling System follows a modern Django architecture with clear separation of concerns, making it maintainable, testable, and scalable. The system leverages genetic algorithms (a form of evolutionary AI) to solve complex scheduling optimization problems.

## Design Principles

1. **Separation of Concerns**: Business logic separated from views
2. **DRY (Don't Repeat Yourself)**: Reusable components and services
3. **SOLID Principles**: Single responsibility, open/closed, etc.
4. **Security First**: Environment variables, proper authentication
5. **Scalability**: Modular design for easy feature additions

## Architecture Layers

### 1. Presentation Layer (Views & Templates)

**Location**: `apps/*/views.py`, `templates/`

**Responsibilities**:
- Handle HTTP requests/responses
- Validate user input
- Render templates
- Redirect users

**Best Practices**:
- Keep views thin
- Delegate business logic to services
- Use class-based views for complex logic
- Use function-based views for simple CRUD

### 2. AI Business Logic Layer (Services)

**Location**: `apps/*/services/`

**Responsibilities**:
- AI-powered scheduling algorithms
- Genetic algorithm implementation (evolutionary AI)
- Machine learning optimization
- Constraint satisfaction solving
- Fitness evaluation and scoring

**AI Services**:
```python
# apps/schedule/services/genetic_algorithm.py
class GeneticAlgorithm:
    """AI engine for schedule optimization"""
    def evolve(self, population):
        # Evolutionary algorithm logic
        pass

# apps/schedule/services/timetable_generator.py
class TimetableGeneratorService:
    """High-level AI scheduling service"""
    @staticmethod
    def generate():
        # Uses genetic algorithm to find optimal schedule
        data = Data()
        population = Population(POPULATION_SIZE, data)
        genetic_algorithm = GeneticAlgorithm(data)
        
        # Evolve until optimal solution found
        while population.get_schedules()[0].get_fitness() != 1.0:
            population = genetic_algorithm.evolve(population)
        
        return best_schedule
```

### 3. Data Access Layer (Models)

**Location**: `apps/*/models.py`

**Responsibilities**:
- Database schema definition
- Data validation
- Model methods for data manipulation
- Relationships between entities

**Best Practices**:
- Use model managers for complex queries
- Add custom methods for business logic
- Use properties for computed fields
- Implement `__str__` for readable representations

### 4. Configuration Layer

**Location**: `config/settings/`

**Structure**:
- `base.py`: Shared settings
- `development.py`: Dev-specific settings
- `staging.py`: Staging settings
- `production.py`: Production settings

**Benefits**:
- Environment-specific configurations
- Easy deployment
- Security through environment variables

## Application Structure

### Account App

**Purpose**: User authentication and profile management

**Components**:
- `models.py`: User profile model
- `views.py`: Registration, login, user management
- `forms.py`: User registration and login forms
- `urls.py`: Account-related URLs

**Key Features**:
- User registration
- Profile management
- Password reset
- User CRUD operations

### Schedule App

**Purpose**: Timetable generation and resource management

**Components**:
- `models.py`: Room, Instructor, Course, Department, Batch, Section, MeetingTime
- `views.py`: CRUD operations for resources, timetable generation
- `forms.py`: Forms for all models
- `services/`: Business logic for timetable generation
- `urls.py`: Schedule-related URLs

**Key Features**:
- Resource management (CRUD)
- Timetable generation using genetic algorithm
- PDF export
- Conflict detection and resolution

## Data Flow

### Timetable Generation Flow

```
User Request
    ↓
View (schedule/views.py::timetable)
    ↓
Service (TimetableGeneratorService.generate())
    ↓
Genetic Algorithm (Population → Evolution → Best Solution)
    ↓
Database (Save to TimeTableModel)
    ↓
Response (Render template with schedule)
```

### CRUD Operations Flow

```
User Request
    ↓
View (validate form)
    ↓
Form (clean and validate data)
    ↓
Model (save to database)
    ↓
Response (redirect or render)
```

## Database Schema

### Core Entities

1. **Room**
   - r_number (CharField)
   - seating_capacity (IntegerField)

2. **Instructor**
   - uid (CharField)
   - name (CharField)

3. **MeetingTime**
   - pid (CharField, PK)
   - time (CharField, choices)
   - day (CharField, choices)

4. **Course**
   - course_number (CharField, PK)
   - course_name (CharField)
   - max_numb_students (CharField)
   - instructors (ManyToMany → Instructor)

5. **Department**
   - dept_name (CharField)

6. **Batch**
   - batch_name (CharField)
   - department (ForeignKey → Department)
   - courses (ManyToMany → Course)

7. **Section**
   - section_id (CharField, PK)
   - batch (ForeignKey → Batch)
   - num_class_in_week (IntegerField)
   - course (ForeignKey → Course, nullable)
   - meeting_time (ForeignKey → MeetingTime, nullable)
   - room (ForeignKey → Room, nullable)
   - instructor (ForeignKey → Instructor, nullable)

8. **TimeTableModel**
   - section (CharField)
   - batch (CharField)
   - course (CharField)
   - venue (CharField)
   - instructor (CharField)
   - clstime (CharField)

### Relationships

```
Department ←─── Batch ←─── Section
                  ↓
                Course ←─── Instructor
                  ↓
            MeetingTime
                  ↓
                Room
```

## AI-Powered Genetic Algorithm Architecture

### 🤖 Evolutionary AI Components

The system uses **Genetic Algorithms**, a machine learning technique inspired by natural evolution:

1. **Data**: Container for all scheduling entities (rooms, instructors, courses, etc.)
2. **Class**: Represents a single scheduled class (gene)
3. **Schedule**: Complete timetable solution (chromosome)
4. **Population**: Collection of candidate schedules (gene pool)
5. **GeneticAlgorithm**: AI evolution engine that optimizes schedules

### 🧬 AI Evolution Process

The algorithm mimics natural selection to find optimal schedules:

```
1. Initialize Population
   └─> Generate random schedule candidates
       
2. Evaluate Fitness (AI Scoring)
   └─> Score each schedule based on constraints
       └─> Fewer conflicts = Higher fitness
       
3. Selection (Survival of the Fittest)
   └─> Tournament selection picks best schedules
       └─> Better schedules have higher chance of reproduction
       
4. Crossover (Genetic Recombination)
   └─> Combine features from successful schedules
       └─> Creates offspring with mixed traits
       
5. Mutation (Genetic Diversity)
   └─> Random changes to explore new solutions
       └─> Prevents local optima, encourages innovation
       
6. Evolution Loop
   └─> Repeat until optimal solution found (fitness = 1.0)
       └─> Typically converges in 10-100 generations
```

### 🎯 AI Optimization Parameters

- **Population Size**: 9 schedules per generation
- **Elite Preservation**: Top 1 schedule always survives
- **Tournament Size**: 3 schedules compete for selection
- **Mutation Rate**: 5% chance of random changes
- **Fitness Goal**: 100% constraint satisfaction (no conflicts)

### Fitness Calculation

```python
conflicts = 0

# Room capacity check
if room.capacity < course.max_students:
    conflicts += 1

# Time conflict check
if same_time and different_section:
    if same_room:
        conflicts += 1
    if same_instructor:
        conflicts += 1

fitness = 1 / (conflicts + 1)
```

## Security Architecture

### Authentication

- Django's built-in authentication system
- Password hashing (PBKDF2)
- Session-based authentication
- CSRF protection

### Authorization

- Login required decorators
- Permission-based access control
- Admin-only views

### Data Protection

- Environment variables for secrets
- SQL injection protection (ORM)
- XSS protection (template escaping)
- HTTPS in production

### Best Practices

1. Never commit `.env` file
2. Use strong SECRET_KEY
3. Set DEBUG=False in production
4. Configure ALLOWED_HOSTS properly
5. Use HTTPS
6. Regular security updates

## Performance Considerations

### Database Optimization

- Use `select_related()` for foreign keys
- Use `prefetch_related()` for many-to-many
- Add database indexes for frequently queried fields
- Use database connection pooling

### Caching Strategy

```python
# Cache timetable results
from django.core.cache import cache

def get_timetable(batch_id):
    key = f'timetable_{batch_id}'
    result = cache.get(key)
    if not result:
        result = generate_timetable(batch_id)
        cache.set(key, result, 3600)  # 1 hour
    return result
```

### Static Files

- Use CDN for static files in production
- Enable gzip compression
- Minify CSS/JS
- Use WhiteNoise for serving static files

## Testing Strategy

### Unit Tests

Test individual components in isolation:
- Model methods
- Form validation
- Service functions

### Integration Tests

Test component interactions:
- View responses
- Database operations
- Form submissions

### End-to-End Tests

Test complete user workflows:
- User registration
- Timetable generation
- PDF export

### Example Test

```python
from django.test import TestCase
from apps.schedule.services import TimetableGeneratorService

class TimetableGeneratorTest(TestCase):
    def setUp(self):
        # Create test data
        pass
    
    def test_generate_timetable(self):
        schedule = TimetableGeneratorService.generate()
        self.assertIsNotNone(schedule)
        self.assertTrue(len(schedule) > 0)
```

## Deployment Architecture

### Development

- SQLite database
- Django development server
- Debug toolbar enabled
- Console email backend

### Staging

- PostgreSQL database
- Gunicorn/uWSGI
- Nginx reverse proxy
- Similar to production

### Production

- PostgreSQL database
- Gunicorn with multiple workers
- Nginx reverse proxy
- Redis for caching
- Celery for background tasks
- Logging to files/services
- HTTPS with SSL certificate
- Static files on CDN

### Infrastructure Diagram

```
Internet
    ↓
Load Balancer
    ↓
Nginx (Reverse Proxy)
    ↓
Gunicorn (WSGI Server)
    ↓
Django Application
    ↓
PostgreSQL Database
    ↓
Redis Cache
```

## Monitoring and Logging

### Logging Levels

- DEBUG: Detailed information for debugging
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical issues

### Monitoring Tools

- Django Debug Toolbar (development)
- Sentry (error tracking)
- New Relic (performance monitoring)
- CloudWatch (AWS)

## Future Enhancements

1. **REST API**: Add Django REST Framework
2. **Real-time Updates**: WebSockets for live timetable updates
3. **Mobile App**: React Native or Flutter
4. **Advanced Analytics**: Dashboard with statistics
5. **Email Notifications**: Automated timetable distribution
6. **Multi-tenancy**: Support multiple universities
7. **Conflict Resolution UI**: Manual conflict resolution
8. **Calendar Integration**: Export to Google Calendar, iCal

## Conclusion

This architecture provides a solid foundation for a maintainable, scalable, and secure timetable generation system. Follow the established patterns when adding new features to maintain consistency and code quality.
