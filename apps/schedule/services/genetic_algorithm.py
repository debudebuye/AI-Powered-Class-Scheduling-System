"""
Genetic Algorithm implementation for timetable generation.
"""
import random as rnd
from typing import List

from apps.schedule.models import Room, MeetingTime, Instructor, Course, Section, Batch

# Algorithm parameters
POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05


class Data:
    """Data container for all entities needed in scheduling."""
    
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._instructors = Instructor.objects.all()
        self._courses = Course.objects.all()
        self._batches = Batch.objects.all()

    def get_rooms(self):
        return self._rooms

    def get_instructors(self):
        return self._instructors

    def get_courses(self):
        return self._courses

    def get_meetingTimes(self):
        return self._meetingTimes

    def get_batches(self):
        return self._batches


class Class:
    """Represents a single class in the schedule."""
    
    def __init__(self, id, dept, section, course, batch):
        self.section_id = id
        self.department = dept
        self.course = course
        self.instructor = None
        self.meeting_time = None
        self.room = None
        self.section = section
        self.batch = batch

    def get_id(self):
        return self.section_id

    def get_dept(self):
        return self.department

    def get_course(self):
        return self.course

    def get_instructor(self):
        return self.instructor

    def get_meetingTime(self):
        return self.meeting_time

    def get_room(self):
        return self.room

    def get_batch(self):
        return self.batch

    def set_instructor(self, instructor):
        self.instructor = instructor

    def set_meetingTime(self, meetingTime):
        self.meeting_time = meetingTime

    def set_room(self, room):
        self.room = room


class Schedule:
    """Represents a complete schedule solution."""
    
    def __init__(self, data: Data):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self):
        return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        """Initialize schedule with random assignments."""
        sections = Section.objects.all()
        for section in sections:
            batch = section.batch
            courses = batch.courses.all()
            for course in courses:
                for i in range(section.num_class_in_week // len(courses)):
                    newClass = Class(
                        self._classNumb,
                        batch.department,
                        section.section_id,
                        course,
                        batch
                    )
                    self._classNumb += 1
                    
                    # Random assignments
                    meeting_times = self._data.get_meetingTimes()
                    rooms = self._data.get_rooms()
                    instructors = course.instructors.all()
                    
                    newClass.set_meetingTime(meeting_times[rnd.randrange(0, len(meeting_times))])
                    newClass.set_room(rooms[rnd.randrange(0, len(rooms))])
                    newClass.set_instructor(instructors[rnd.randrange(0, len(instructors))])
                    
                    self._classes.append(newClass)
        return self

    def calculate_fitness(self):
        """Calculate fitness based on number of conflicts."""
        self._numberOfConflicts = 0
        classes = self.get_classes()
        
        for i in range(len(classes)):
            # Check room capacity
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            
            # Check for conflicts with other classes
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                            (classes[i].section_id != classes[j].section_id):
                        # Room conflict
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        # Instructor conflict
                        if classes[i].instructor == classes[j].instructor:
                            self._numberOfConflicts += 1
        
        return 1 / (1.0 * self._numberOfConflicts + 1)


class Population:
    """Population of schedules."""
    
    def __init__(self, size: int, data: Data):
        self._size = size
        self._data = data
        self._schedules = [Schedule(data).initialize() for _ in range(size)]

    def get_schedules(self) -> List[Schedule]:
        return self._schedules


class GeneticAlgorithm:
    """Genetic algorithm for evolving schedules."""
    
    def __init__(self, data: Data):
        self._data = data

    def evolve(self, population: Population) -> Population:
        """Evolve population to next generation."""
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop: Population) -> Population:
        """Create new population through crossover."""
        crossover_pop = Population(0, self._data)
        
        # Keep elite schedules
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        
        # Generate rest through crossover
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        
        return crossover_pop

    def _mutate_population(self, population: Population) -> Population:
        """Apply mutation to population."""
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1: Schedule, schedule2: Schedule) -> Schedule:
        """Crossover two schedules."""
        crossoverSchedule = Schedule(self._data).initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule: Schedule) -> Schedule:
        """Mutate a schedule."""
        schedule = Schedule(self._data).initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop: Population) -> Population:
        """Select best schedule from tournament."""
        tournament_pop = Population(0, self._data)
        for _ in range(TOURNAMENT_SELECTION_SIZE):
            tournament_pop.get_schedules().append(
                pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)]
            )
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop
