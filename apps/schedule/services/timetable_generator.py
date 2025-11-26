"""
Service for generating timetables using genetic algorithm.
"""
from typing import List, Dict
from apps.schedule.models import TimeTableModel, Section, MeetingTime
from .genetic_algorithm import Data, Population, GeneticAlgorithm, POPULATION_SIZE


class TimetableGeneratorService:
    """Service to generate optimized timetables."""
    
    @staticmethod
    def generate() -> List[Dict]:
        """
        Generate an optimized timetable using genetic algorithm.
        
        Returns:
            List of class dictionaries with schedule information
        """
        data = Data()
        population = Population(POPULATION_SIZE, data)
        genetic_algorithm = GeneticAlgorithm(data)
        generation_num = 0
        
        # Sort initial population by fitness
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        
        # Clear existing timetable
        TimeTableModel.objects.all().delete()
        
        # Evolve until perfect solution found
        while population.get_schedules()[0].get_fitness() != 1.0:
            generation_num += 1
            print(f'\n> Generation #{generation_num}')
            population = genetic_algorithm.evolve(population)
            population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
            
            # Safety check to prevent infinite loop
            if generation_num > 1000:
                print("Warning: Max generations reached. Using best solution found.")
                break
        
        # Get best schedule
        best_schedule = population.get_schedules()[0]
        schedule = best_schedule.get_classes()
        
        # Sort by day and time
        schedule.sort(key=lambda cls: cls.meeting_time.get_day_sort_key())
        
        # Save to database
        TimetableGeneratorService._save_to_database(schedule)
        
        # Return formatted schedule
        return TimetableGeneratorService._format_schedule(schedule)
    
    @staticmethod
    def _save_to_database(schedule):
        """Save generated schedule to database."""
        for sec in Section.objects.all():
            for scd in schedule:
                if scd.section == sec.section_id:
                    TimeTableModel.objects.create(
                        section=str(sec.section_id),
                        batch=str(sec.batch.batch_name),
                        course=str(scd.course),
                        venue=str(scd.room),
                        instructor=str(scd.instructor.name),
                        clstime=str(scd.meeting_time)
                    )
    
    @staticmethod
    def _format_schedule(schedule) -> List[Dict]:
        """Format schedule for template rendering."""
        context = []
        for cls in schedule:
            context.append({
                "section": cls.section_id,
                "dept": cls.department.dept_name,
                "course": f'{cls.course.course_name} ({cls.course.course_number}, {cls.course.max_numb_students})',
                "room": f'{cls.room.r_number} ({cls.room.seating_capacity})',
                "instructor": f'{cls.instructor.name} ({cls.instructor.uid})',
                "meeting_time": [cls.meeting_time.pid, cls.meeting_time.day, cls.meeting_time.time],
                "batch": cls.batch.batch_name
            })
        return context
